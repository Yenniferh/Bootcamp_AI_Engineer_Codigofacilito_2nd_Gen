from contracts.tool_schemas import ConsultarProveedorArgs
from tools import proveedores

normalize_provider_name = proveedores.normalize_provider_name


def test_normalize_provider_case_insensitive():
    assert normalize_provider_name("PagosRed") == "pagosred"

    assert normalize_provider_name("GLOBAl66") == "global66"


def test_normalize_provider_accents_and_punctuation():
    assert normalize_provider_name("Empaques del Bajío") == "empaques del bajio"

    assert normalize_provider_name("Bajío S.A.") == "bajio s a"

    assert normalize_provider_name("Ajíllo-S.A.") == "ajillo s a"

    assert normalize_provider_name("Ajíllo-sa") == "ajillo sa"


def test_normalize_provider_white_space():
    assert normalize_provider_name("route      66") == "route 66"

    assert normalize_provider_name("route\n66") == "route 66"


def test_consultar_proveedor_case_insensitive(monkeypatch):
    fake_providers = {
        "pagosred": {
            "nombre": "PagosRed",
            "sla_horas": 4,
            "estado": "activo",
            "contacto": "test@example.com",
            "contratos_vigentes": 1,
        }
    }

    monkeypatch.setattr(
        proveedores,
        "_proveedores",
        lambda: fake_providers,
    )

    args = ConsultarProveedorArgs(provider_name="PAGOSRED")
    result = proveedores.consultar_proveedor(args)

    assert result["nombre"] == "PagosRed"


def test_consultar_proveedor_not_found(monkeypatch):
    fake_providers = {
        "pagosred": {
            "nombre": "PagosRed",
            "sla_horas": 4,
            "estado": "activo",
            "contacto": "test@example.com",
            "contratos_vigentes": 1,
        }
    }

    monkeypatch.setattr(
        proveedores,
        "_proveedores",
        lambda: fake_providers,
    )

    args = ConsultarProveedorArgs(provider_name="RED de Pagos")
    result = proveedores.consultar_proveedor(args)

    assert result["error"] == "proveedor RED de Pagos no existe"
