"""Herramienta `consultar_proveedor` sobre data/proveedores.json."""

from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contracts.tool_schemas import ConsultarProveedorArgs

# Ruta fija: nunca se construye a partir de los argumentos del modelo.
PROVEEDORES_DB = Path(__file__).resolve().parents[1] / "data" / "proveedores.json"
HISTORY_LIMIT = 3


def normalize_provider_name(name: str) -> str:
    lowercased = name.casefold()
    unicode_normalized = unicodedata.normalize("NFKD", lowercased)
    without_accents = "".join(
        char for char in unicode_normalized if unicodedata.category(char) != "Mn"
    )

    replace_punctuation_with_space = re.sub(r"[^a-z0-9\s]", " ", without_accents)
    normalized_spacing = " ".join(replace_punctuation_with_space.split())

    return normalized_spacing


@lru_cache(maxsize=1)
def _proveedores() -> dict[str, dict]:
    proveedores = json.loads(PROVEEDORES_DB.read_text(encoding="utf-8"))
    return {normalize_provider_name(proveedor["nombre"]): proveedor for proveedor in proveedores}


def consultar_proveedor(args: ConsultarProveedorArgs) -> dict:
    """Estado, SLA (horas) y contacto de un proveedor."""
    proveedor = _proveedores().get(normalize_provider_name(args.provider_name))
    if proveedor is None:
        return {"error": f"proveedor {args.provider_name} no existe"}
    return {
        "nombre": proveedor["nombre"],
        "sla_horas": proveedor["sla_horas"],
        "estado": proveedor["estado"],
        "contacto": proveedor["contacto"],
        "contratos_vigentes": proveedor["contratos_vigentes"],
    }
