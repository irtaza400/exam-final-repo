import json
from datetime import date
from pathlib import Path

from src.material_risk_engine import (
    evaluate_material_batch,
    load_rules,
)
from src.supplier_validator import load_suppliers, validate_supplier


BATCHES_PATH = Path("data/material_batches.json")


def load_batches():
    with BATCHES_PATH.open("r", encoding="utf-8") as handle:
        return {
            batch["batch_id"]: batch
            for batch in json.load(handle)
        }


def evaluate(batch_id):
    batches = load_batches()
    suppliers = load_suppliers()
    rules = load_rules()
    batch = batches[batch_id]

    supplier_result = validate_supplier(
        batch["supplier_id"],
        batch["material"],
        suppliers,
    )

    return evaluate_material_batch(
        batch,
        supplier_result,
        rules,
        evaluation_date=date(2026, 8, 1),
    )


def test_valid_low_risk_batch_is_approved():
    result = evaluate("BATCH-PR-001")
    assert result.decision == "APPROVE_FOR_USE"
    assert result.certificate_status == "VALID"
    assert result.risk_score == 0


def test_medium_risk_batch_is_approved_with_monitoring():
    result = evaluate("BATCH-GAS-002")
    assert result.decision == "APPROVE_FOR_USE"
    assert result.risk_score == 25
    assert "MEDIUM" in " ".join(result.reasons)


def test_unknown_supplier_and_missing_certificate_is_rejected():
    result = evaluate("BATCH-DU-003")
    assert result.decision == "REJECT_OR_LEGAL_REVIEW"
    assert result.certificate_status == "MISSING"
    assert result.risk_score == 100


def test_expired_certificate_causes_quarantine():
    result = evaluate("BATCH-EXP-004")
    assert result.decision == "QUARANTINE_AND_QMS_REVIEW"
    assert result.certificate_status == "EXPIRED"


def test_revoked_certificate_and_failed_quality_is_rejected():
    result = evaluate("BATCH-REV-005")
    assert result.decision == "REJECT_OR_LEGAL_REVIEW"
    assert result.certificate_status == "REVOKED"
    assert result.quality_status == "FAILED"


def test_suspended_supplier_is_rejected():
    result = evaluate("BATCH-SUSP-006")
    assert result.decision == "REJECT_OR_LEGAL_REVIEW"
