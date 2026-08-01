from src.supplier_validator import load_suppliers, validate_supplier


def test_approved_supplier_and_material():
    suppliers = load_suppliers()
    result = validate_supplier(
        "SUP-NANO-001",
        "photoresist precursor",
        suppliers,
    )
    assert result.approved is True
    assert result.supplier_active is True
    assert result.material_approved is True


def test_unknown_supplier_is_rejected():
    suppliers = load_suppliers()
    result = validate_supplier(
        "SUP-UNKNOWN-999",
        "dual-use nanomaterial precursor",
        suppliers,
    )
    assert result.approved is False
    assert result.supplier_found is False


def test_suspended_supplier_is_rejected():
    suppliers = load_suppliers()
    result = validate_supplier(
        "SUP-SUSPENDED-003",
        "nanomaterial precursor",
        suppliers,
    )
    assert result.approved is False
    assert result.supplier_active is False


def test_material_outside_supplier_scope_is_rejected():
    suppliers = load_suppliers()
    result = validate_supplier(
        "SUP-NANO-001",
        "etching gas",
        suppliers,
    )
    assert result.approved is False
    assert result.material_approved is False
