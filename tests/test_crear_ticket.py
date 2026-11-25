from __future__ import annotations

import json

import pytest

from contracts.tool_schemas import (
    BuscarTicketArgs,
    CrearTicketArgs,
)
from tools import tickets


@pytest.fixture
def tickets_path(tmp_path, monkeypatch):
    path = tmp_path / "tickets_nuevos.json"
    monkeypatch.setattr(tickets, "NUEVOS_TICKETS_DB", path)
    monkeypatch.setattr(tickets, "ESTADOS_PATH", tmp_path / "tickets_estado.json")
    return path


def make_args(key: str | None = None) -> CrearTicketArgs:
    args = CrearTicketArgs(
        asunto="Portal de pagos caído",
        descripcion="Error al procesar pagos",
        prioridad="alta",
    )
    args._idempotency_key = key
    return args


def read_tickets(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_creates_and_persists_ticket(tickets_path):
    args = make_args("operation-001")

    result = tickets.crear_ticket(args)

    assert "error" not in result
    assert result["id"].startswith("T-")
    assert result["asunto"] == args.asunto
    assert result["prioridad"] == args.prioridad
    assert result["estado"] == "abierto"

    [stored] = read_tickets(tickets_path)

    assert stored["id"] == result["id"]
    assert stored["descripcion"] == args.descripcion
    assert stored["_idempotency_key"] == "operation-001"


def test_same_key_returns_existing_ticket(tickets_path):
    first = tickets.crear_ticket(make_args("operation-001"))
    second = tickets.crear_ticket(make_args("operation-001"))

    assert "error" not in first
    assert first == second
    assert len(read_tickets(tickets_path)) == 1


def test_different_keys_create_different_tickets(tickets_path):
    first = tickets.crear_ticket(make_args("operation-001"))
    second = tickets.crear_ticket(make_args("operation-002"))

    assert "error" not in first
    assert "error" not in second
    assert first["id"] != second["id"]
    assert len(read_tickets(tickets_path)) == 2


def test_missing_key_prevents_creation(tickets_path):
    result = tickets.crear_ticket(make_args())

    assert result["error"]["tipo"] == "permanente"
    assert not tickets_path.exists()


def test_created_ticket_can_be_retrieved(tickets_path):
    created = tickets.crear_ticket(make_args("operation-001"))

    result = tickets.buscar_ticket(BuscarTicketArgs(ticket_id=created["id"]))

    assert result == created


def test_existing_ticket_can_be_read_without_overlay(tickets_path):
    assert not tickets_path.exists()

    result = tickets.buscar_ticket(BuscarTicketArgs(ticket_id="T-1042"))

    assert result["id"] == "T-1042"
