from tools.proveedores import normalize_provider_name


def test_normalize_provider_name():
    assert normalize_provider_name("PagosRed") == "pagosred"

    assert normalize_provider_name("Empaques del Bajío") == "empaques del bajio"

    assert normalize_provider_name("Bajío S.A.") == "bajio sa"

    assert normalize_provider_name("GLOBAl66") == "global66"
