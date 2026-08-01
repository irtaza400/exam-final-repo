import json
from pathlib import Path

from src.ledger_verifier import verify_ledger_file
from src.supply_chain_ledger import (
    GENESIS_HASH,
    build_block,
    save_json,
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


def sample_batch():
    return {
        "batch_id": "BATCH-VERIFY-001",
        "supplier_id": "SUP-VERIFY-001",
        "material": "test material",
        "lot_number": "LOT-VERIFY-001",
        "manufactured_at": "2026-01-01",
        "expires_at": "2027-01-01",
        "certificate": {
            "certificate_id": "COA-VERIFY-001",
            "status": "VALID",
            "issued_at": "2026-01-01",
            "expires_at": "2027-01-01",
        },
    }


def test_valid_ledger_file(tmp_path: Path):
    ledger_path = tmp_path / "ledger.json"

    block = build_block(
        index=1,
        batch=sample_batch(),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=GENESIS_HASH,
    )

    save_json(ledger_path, [block])

    report = verify_ledger_file(ledger_path)

    assert report["ledger_valid"] is True
    assert report["record_count"] == 1
    assert report["errors"] == []


def test_tampered_ledger_file(tmp_path: Path):
    ledger_path = tmp_path / "ledger.json"

    block = build_block(
        index=1,
        batch=sample_batch(),
        supplier_result=DummySupplier(),
        risk_result=DummyRisk(),
        previous_hash=GENESIS_HASH,
    )

    block["material"] = "tampered material"
    save_json(ledger_path, [block])

    report = verify_ledger_file(ledger_path)

    assert report["ledger_valid"] is False
    assert any(
        "current_hash mismatch" in error
        for error in report["errors"]
    )
