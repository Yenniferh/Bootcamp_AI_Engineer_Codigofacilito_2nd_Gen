"""Herramientas `buscar_ticket` y `actualizar_estado` sobre data/tickets_db.json.

`data/tickets_db.json` es de solo lectura. Los cambios de estado van a un overlay,
`var/tickets_estado.json` (`{ticket_id: estado}`), que `buscar_ticket` aplica al leer.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contracts.tool_schemas import (
        ActualizarEstadoArgs,
        BuscarTicketArgs,
        CrearTicketArgs,
        ListarTicketsPorProveedorArgs,
    )

# Rutas fijas: nunca se construyen a partir de los argumentos del modelo.
TICKETS_DB = Path(__file__).resolve().parents[1] / "data" / "tickets_db.json"
ESTADOS_PATH = Path(__file__).resolve().parents[1] / "var" / "tickets_estado.json"
NUEVOS_TICKETS_DB = Path(__file__).resolve().parents[1] / "var" / "tickets_nuevos.json"
HISTORY_LIMIT = 3


@lru_cache(maxsize=1)
def _tickets() -> dict[str, dict]:
    tickets = json.loads(TICKETS_DB.read_text(encoding="utf-8"))
    return {ticket["id"]: ticket for ticket in tickets}


def _tickets_guardados(check_idempotency: bool = False) -> dict[str, dict]:
    if not NUEVOS_TICKETS_DB.exists():
        return {}

    tickets = json.loads(NUEVOS_TICKETS_DB.read_text(encoding="utf-8"))
    key = "_idempotency_key" if check_idempotency else "id"
    return {ticket[key]: ticket for ticket in tickets}


def _tickets_from_all_sources():
    return _tickets() | _tickets_guardados()


def buscar_ticket(args: BuscarTicketArgs) -> dict:
    """Estado, equipo, proveedor y últimas entradas del historial de un ticket."""
    ticket = _tickets_from_all_sources().get(args.ticket_id)
    if ticket is None:
        return {"error": f"ticket {args.ticket_id} no existe"}
    return {
        "id": ticket["id"],
        "asunto": ticket["asunto"],
        "estado": _estados().get(ticket["id"], ticket["estado"]),
        "equipo": ticket["equipo"],
        "prioridad": ticket["prioridad"],
        "proveedor": ticket["proveedor"],
        "historial": ticket["historial"][-HISTORY_LIMIT:],
    }


def _estados() -> dict[str, str]:
    """Overlay de estados. Se lee en cada llamada: otro proceso (el server MCP) lo escribe."""
    if not ESTADOS_PATH.exists():
        return {}
    return json.loads(ESTADOS_PATH.read_text(encoding="utf-8"))


def _guardar_estados(estados: dict[str, str]) -> None:
    """Escritura atómica: un archivo temporal y `os.replace`, nunca un JSON a medias."""
    ESTADOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = ESTADOS_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(estados, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, ESTADOS_PATH)


def actualizar_estado(args: ActualizarEstadoArgs) -> dict:
    """Fija el estado de un ticket. Idempotente: repetirla con el mismo estado no cambia nada."""
    from contracts.tool_schemas import tool_error  # Import local: tool_schemas importa este módulo.

    ticket = _tickets_from_all_sources().get(args.ticket_id)
    if ticket is None:
        return tool_error(
            "negocio",
            f"ticket {args.ticket_id} no existe",
            sugerencia="Confirma el ID con el usuario antes de reintentar.",
        )
    estados = _estados()
    anterior = estados.get(args.ticket_id, ticket["estado"])
    cambio = anterior != args.estado
    if cambio:
        estados[args.ticket_id] = args.estado
        _guardar_estados(estados)
    return {"id": args.ticket_id, "estado": args.estado, "cambio": cambio}


def listar_tickets_por_proveedor(args: ListarTicketsPorProveedorArgs) -> dict:
    """Lista los tickets de un proveedor. Devuelve entre 1 y 20 tickets según el valor de tope."""
    from contracts.tool_schemas import tool_error  # Import local: tool_schemas importa este módulo.
    from tools.proveedores import (
        normalize_provider_name,
    )  # Import local: proveedores tool define este helper

    nombre = normalize_provider_name(args.nombre)
    tickets_db = json.loads(TICKETS_DB.read_text(encoding="utf-8"))
    tickets = [
        ticket
        for ticket in tickets_db
        if ticket["proveedor"] and normalize_provider_name(ticket["proveedor"]) == nombre
    ]

    if not tickets:
        return tool_error(
            "negocio",
            f"no existen tickets para el proveedor {args.nombre}",
            sugerencia="Confirma el nombre del proveedor con el usuario antes de reintentar.",
        )

    DEFAULT_TOPE = 10
    tope = args.tope or DEFAULT_TOPE
    return {"proveedor": nombre, "tickets": tickets[:tope]}


def _get_last_ticket_id_used() -> int:
    return max(
        (int(ticket_id.split("-")[1]) for ticket_id in _tickets_from_all_sources()),
        default=1000,
    )


def _guardar_tickets(tickets: list[dict[str, str]]) -> None:
    """Escritura atómica: un archivo temporal y `os.replace`, nunca un JSON a medias."""
    NUEVOS_TICKETS_DB.parent.mkdir(parents=True, exist_ok=True)
    tmp = NUEVOS_TICKETS_DB.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(tickets, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, NUEVOS_TICKETS_DB)


def _from_args_to_ticket_schema(id: str, args: CrearTicketArgs) -> dict:
    return {
        "id": f"T-{id}",
        "_idempotency_key": args._idempotency_key,
        "asunto": args.asunto,
        "descripcion": args.descripcion,
        "estado": "abierto",
        "equipo": None,  # TODO: Include as arg or resolve it via RAG or a classifier
        "prioridad": args.prioridad,
        "proveedor": None,  # TODO: Resolve it via RAG or a classifier
        "historial": [],
    }


def crear_ticket(args: CrearTicketArgs) -> dict:
    """Crea un ticket si aun no existe. Idempotente"""
    if not args._idempotency_key:
        from contracts.tool_schemas import (
            tool_error,
        )  # Import local: tool_schemas importa este módulo.

        return tool_error(
            "permanente",
            "algo ha fallado. No se pudo crear el ticket",
        )

    ticket_exist = _tickets_guardados(check_idempotency=True).get(args._idempotency_key)
    if ticket_exist:
        return {
            "id": ticket_exist["id"],
            "asunto": ticket_exist["asunto"],
            "estado": _estados().get(ticket_exist["id"], ticket_exist["estado"]),
            "equipo": ticket_exist["equipo"],
            "prioridad": ticket_exist["prioridad"],
            "proveedor": ticket_exist["proveedor"],
            "historial": ticket_exist["historial"][-HISTORY_LIMIT:],
        }

    ticket_id = _get_last_ticket_id_used() + 1
    ticket = _from_args_to_ticket_schema(id=ticket_id, args=args)
    deflat_stored_tickets = [value for value in _tickets_guardados().values()]
    deflat_stored_tickets.append(ticket)
    _guardar_tickets(deflat_stored_tickets)
    return {
        "id": ticket["id"],
        "asunto": ticket["asunto"],
        "estado": _estados().get(ticket["id"], ticket["estado"]),
        "equipo": ticket["equipo"],
        "prioridad": ticket["prioridad"],
        "proveedor": ticket["proveedor"],
        "historial": ticket["historial"][-HISTORY_LIMIT:],
    }
