from src.supply_chain_ledger import (
    GENESIS_HASH,
    build_block,
    calculate_hash,
    existing_batch_ids,
    verify_chain,
)


class DummySupplier:
    supplier_name = "Test Supplier"
    supplier_status = "ACTIVE"
    approved = True
    approval_reference = "QMS-TEST-001"


class DummyRisk:
    certificate_status = "VALID"
    quality_status = "PASSED"
    export_risk = "LOW"
    country_risk = "LOW"
    risk_score = 0
    decision = "APPROVE_FOR_USE"
    reasons = ("No exceptions.",)
    control_actions = ("Release batch.",)


def sample_batch(batch_id="BATCH-TEST-001"):
    return {
        "batch_id": batch_id,
        "supplier_id": "SUP-TEST-001",
        "material": "test material",
        "lot_number": "LOT-TEST-001",
        "manufactured_at": "2026-01-01",
        "expires_at": "2027-01-01",
        "certificate": {
            "certificate_id": "COA-TEST-001",
            "status": "VALID",
            "issued_at": "2026-01-01",
            "expires_at": "2027-01-01",
        },
    }


def test_single_block_verifies():
    block = build_block(
        index=1,
        batch=sample_batch(),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=GENESIS_HASH,
    )

    valid, errors = verify_chain([block])

    assert valid is True
    assert errors == []


def test_two_block_chain_verifies():
    first = build_block(
        index=1,
        batch=sample_batch("BATCH-TEST-001"),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=GENESIS_HASH,
    )

    second = build_block(
        index=2,
        batch=sample_batch("BATCH-TEST-002"),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=first["current_hash"],
    )

    valid, errors = verify_chain([first, second])

    assert valid is True
    assert errors == []


def test_modified_historical_record_is_detected():
    block = build_block(
        index=1,
        batch=sample_batch(),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=GENESIS_HASH,
    )

    block["material"] = "tampered material"

    valid, errors = verify_chain([block])

    assert valid is False
    assert any(
        "current_hash mismatch" in error
        for error in errors
    )


def test_broken_previous_hash_is_detected():
    block = build_block(
        index=1,
        batch=sample_batch(),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash="WRONG",
    )

    valid, errors = verify_chain([block])

    assert valid is False
    assert any(
        "previous_hash mismatch" in error
        for error in errors
    )


def test_calculate_hash_is_deterministic():
    block = build_block(
        index=1,
        batch=sample_batch(),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=GENESIS_HASH,
    )

    assert calculate_hash(block) == block["current_hash"]


def test_existing_batch_ids():
    chain = [
        {"batch_id": "BATCH-001"},
        {"batch_id": "BATCH-002"},
    ]

    assert existing_batch_ids(chain) == {
        "BATCH-001",
        "BATCH-002",
    }
