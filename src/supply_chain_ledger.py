"""Tamper-evident supply-chain and QMS ledger for Topic 127."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from src.material_risk_engine import evaluate_material_batch, load_rules
from src.supplier_validator import load_suppliers, validate_supplier


BATCHES_PATH = Path("data/material_batches.json")
LEDGER_PATH = Path("reports/supply_chain_ledger.json")
RISK_REPORT_PATH = Path("reports/supply_chain_risk_report.csv")
VALIDATION_REPORT_PATH = Path("reports/supply_chain_validation_report.json")

GENESIS_HASH = "GENESIS"


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def calculate_hash(block: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in block.items()
        if key != "current_hash"
    }
    return hashlib.sha256(
        canonical_json(payload).encode("utf-8")
    ).hexdigest()


def load_json_list(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list.")

    return data


def load_ledger(path: Path = LEDGER_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    return load_json_list(path)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def existing_batch_ids(
    chain: list[dict[str, Any]],
) -> set[str]:
    return {
        str(block.get("batch_id"))
        for block in chain
        if block.get("batch_id")
    }


def build_block(
    *,
    index: int,
    batch: dict[str, Any],
    supplier_result: Any,
    risk_result: Any,
    previous_hash: str,
) -> dict[str, Any]:
    record_id = f"SC-{index:06d}-{batch['batch_id']}"

    block: dict[str, Any] = {
        "index": index,
        "record_id": record_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "batch_id": batch["batch_id"],
        "supplier_id": batch["supplier_id"],
        "supplier_name": supplier_result.supplier_name,
        "supplier_status": supplier_result.supplier_status,
        "supplier_approved": supplier_result.approved,
        "approval_reference": supplier_result.approval_reference,
        "material": batch["material"],
        "lot_number": batch["lot_number"],
        "manufactured_at": batch["manufactured_at"],
        "expires_at": batch["expires_at"],
        "certificate": batch["certificate"],
        "certificate_status": risk_result.certificate_status,
        "quality_status": risk_result.quality_status,
        "export_risk": risk_result.export_risk,
        "country_risk": risk_result.country_risk,
        "risk_score": risk_result.risk_score,
        "decision": risk_result.decision,
        "reasons": list(risk_result.reasons),
        "control_actions": list(risk_result.control_actions),
        "previous_hash": previous_hash,
    }

    block["current_hash"] = calculate_hash(block)
    return block


def verify_chain(
    chain: list[dict[str, Any]],
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    expected_previous_hash = GENESIS_HASH

    for expected_index, block in enumerate(chain, start=1):
        actual_index = block.get("index")

        if actual_index != expected_index:
            errors.append(
                f"Record {expected_index}: expected index "
                f"{expected_index}, found {actual_index}."
            )

        if block.get("previous_hash") != expected_previous_hash:
            errors.append(
                f"Record {expected_index}: previous_hash mismatch."
            )

        stored_hash = block.get("current_hash")
        calculated_hash = calculate_hash(block)

        if stored_hash != calculated_hash:
            errors.append(
                f"Record {expected_index}: current_hash mismatch."
            )

        expected_previous_hash = str(stored_hash)

    return not errors, errors


def write_risk_report(
    processed_blocks: list[dict[str, Any]],
) -> None:
    lines = [
        "timestamp,record_id,batch_id,supplier_id,material,"
        "risk_score,decision,certificate_status,quality_status"
    ]

    for block in processed_blocks:
        values = [
            block["timestamp"],
            block["record_id"],
            block["batch_id"],
            block["supplier_id"],
            block["material"],
            str(block["risk_score"]),
            block["decision"],
            block["certificate_status"],
            block["quality_status"],
        ]
        lines.append(",".join(values))

    RISK_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RISK_REPORT_PATH.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def run_supply_chain(
    evaluation_date: date | None = None,
) -> dict[str, Any]:
    if evaluation_date is None:
        evaluation_date = date.today()

    batches = load_json_list(BATCHES_PATH)
    suppliers = load_suppliers()
    rules = load_rules()
    chain = load_ledger()

    initial_valid, initial_errors = verify_chain(chain)

    if not initial_valid:
        raise ValueError(
            "Existing ledger verification failed: "
            + "; ".join(initial_errors)
        )

    known_batches = existing_batch_ids(chain)
    appended_blocks: list[dict[str, Any]] = []
    skipped_batches: list[str] = []

    previous_hash = (
        chain[-1]["current_hash"]
        if chain
        else GENESIS_HASH
    )

    for batch in batches:
        batch_id = str(batch["batch_id"])

        if batch_id in known_batches:
            skipped_batches.append(batch_id)
            print(f"SUPPLY CHAIN: {batch_id} duplicate skipped")
            continue

        supplier_result = validate_supplier(
            batch["supplier_id"],
            batch["material"],
            suppliers,
        )

        risk_result = evaluate_material_batch(
            batch,
            supplier_result,
            rules,
            evaluation_date=evaluation_date,
        )

        block = build_block(
            index=len(chain) + 1,
            batch=batch,
            supplier_result=supplier_result,
            risk_result=risk_result,
            previous_hash=previous_hash,
        )

        chain.append(block)
        appended_blocks.append(block)
        known_batches.add(batch_id)
        previous_hash = block["current_hash"]

        print(
            "SUPPLY CHAIN:",
            batch_id,
            "score=",
            risk_result.risk_score,
            "decision=",
            risk_result.decision,
        )

    save_json(LEDGER_PATH, chain)
    write_risk_report(appended_blocks)

    final_valid, final_errors = verify_chain(chain)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ledger_path": str(LEDGER_PATH),
        "ledger_valid": final_valid,
        "ledger_errors": final_errors,
        "total_records": len(chain),
        "records_appended": len(appended_blocks),
        "duplicate_batches_skipped": skipped_batches,
        "decisions": {
            "approved": sum(
                1
                for block in chain
                if block["decision"] == "APPROVE_FOR_USE"
            ),
            "quarantined": sum(
                1
                for block in chain
                if block["decision"]
                == "QUARANTINE_AND_QMS_REVIEW"
            ),
            "rejected_or_legal_review": sum(
                1
                for block in chain
                if block["decision"]
                == "REJECT_OR_LEGAL_REVIEW"
            ),
        },
    }

    save_json(VALIDATION_REPORT_PATH, report)
    return report


def main() -> int:
    report = run_supply_chain()

    print("Ledger written to", LEDGER_PATH)
    print("Risk report written to", RISK_REPORT_PATH)
    print("Validation report written to", VALIDATION_REPORT_PATH)
    print("Ledger valid:", report["ledger_valid"])
    print("Total records:", report["total_records"])
    print("Records appended:", report["records_appended"])
    print(
        "Duplicate batches skipped:",
        len(report["duplicate_batches_skipped"]),
    )

    return 0 if report["ledger_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
