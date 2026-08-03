"""Generate examiner-facing status evidence for the simulated ledger.

The project uses an educational tamper-evident SHA-256 hash chain.
It is intentionally described as a simulated blockchain ledger rather
than a distributed production blockchain network.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.supply_chain_ledger import (
    GENESIS_HASH,
    LEDGER_PATH,
    calculate_hash,
    load_ledger,
    verify_chain,
)


DEFAULT_JSON_REPORT = Path(
    "reports/simulated_ledger_status.json"
)

DEFAULT_TEXT_REPORT = Path(
    "reports/simulated_ledger_status.txt"
)


def short_hash(value: str, length: int = 16) -> str:
    """Return a readable shortened hash without changing evidence."""

    if not value:
        return "N/A"

    if len(value) <= length:
        return value

    return f"{value[:length]}..."


def decision_counts(
    chain: list[dict[str, Any]],
) -> dict[str, int]:
    """Count final QMS decisions represented in the ledger."""

    return {
        "approved": sum(
            1
            for block in chain
            if block.get("decision") == "APPROVE_FOR_USE"
        ),
        "quarantined": sum(
            1
            for block in chain
            if block.get("decision")
            == "QUARANTINE_AND_QMS_REVIEW"
        ),
        "rejected_or_legal_review": sum(
            1
            for block in chain
            if block.get("decision")
            == "REJECT_OR_LEGAL_REVIEW"
        ),
    }


def certificate_counts(
    chain: list[dict[str, Any]],
) -> dict[str, int]:
    """Summarize certificate status values in the ledger."""

    counts: dict[str, int] = {}

    for block in chain:
        status = str(
            block.get(
                "certificate_status",
                "UNKNOWN",
            )
        )

        counts[status] = counts.get(status, 0) + 1

    return counts


def supplier_counts(
    chain: list[dict[str, Any]],
) -> dict[str, int]:
    """Summarize approved and non-approved supplier records."""

    return {
        "approved_supplier_records": sum(
            1
            for block in chain
            if bool(block.get("supplier_approved"))
        ),
        "non_approved_supplier_records": sum(
            1
            for block in chain
            if not bool(block.get("supplier_approved"))
        ),
    }


def build_status_report(
    ledger_path: Path,
) -> dict[str, Any]:
    """Build the complete simulated-ledger status report."""

    chain = load_ledger(ledger_path)
    valid, errors = verify_chain(chain)

    latest_block = chain[-1] if chain else {}
    latest_hash = str(
        latest_block.get(
            "current_hash",
            "",
        )
    )

    latest_hash_recalculated = (
        calculate_hash(latest_block)
        if latest_block
        else ""
    )

    previous_hash = str(
        latest_block.get(
            "previous_hash",
            GENESIS_HASH,
        )
    )

    counts = decision_counts(chain)

    first_error = errors[0] if errors else None
    first_failing_record = None

    if first_error and first_error.startswith("Record "):
        try:
            first_failing_record = int(
                first_error.split(":", 1)[0].split()[1]
            )
        except (IndexError, ValueError):
            first_failing_record = None

    report: dict[str, Any] = {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "component": "Simulated Blockchain Ledger",
        "implementation_type": (
            "Educational tamper-evident hash chain"
        ),
        "deployment_model": (
            "Single-node simulated blockchain ledger"
        ),
        "production_blockchain": False,
        "distributed_consensus": False,
        "hash_algorithm": "SHA-256",
        "canonical_serialization": (
            "Sorted compact JSON"
        ),
        "genesis_anchor": GENESIS_HASH,
        "ledger_path": ledger_path.as_posix(),
        "chain_status": (
            "VALID"
            if valid
            else "TAMPER_DETECTED"
        ),
        "ledger_valid": valid,
        "block_count": len(chain),
        "chain_errors": errors,
        "integrity_failure": {
            "detected": not valid,
            "first_failing_record": first_failing_record,
            "first_error": first_error,
        },
        "latest_block": {
            "index": latest_block.get("index"),
            "record_id": latest_block.get("record_id"),
            "batch_id": latest_block.get("batch_id"),
            "timestamp": latest_block.get("timestamp"),
            "previous_hash": previous_hash,
            "previous_hash_short": short_hash(
                previous_hash
            ),
            "current_hash": latest_hash,
            "current_hash_short": short_hash(
                latest_hash
            ),
            "recalculated_hash": (
                latest_hash_recalculated
            ),
            "stored_hash_matches_recalculated": (
                latest_hash == latest_hash_recalculated
                if latest_block
                else True
            ),
        },
        "decision_counts": counts,
        "certificate_counts": certificate_counts(
            chain
        ),
        "supplier_counts": supplier_counts(chain),
        "provenance_fields": [
            "batch_id",
            "supplier_id",
            "supplier_name",
            "approval_reference",
            "material",
            "lot_number",
            "manufactured_at",
            "expires_at",
            "certificate",
            "certificate_status",
            "quality_status",
            "risk_score",
            "decision",
            "previous_hash",
            "current_hash",
        ],
        "security_capabilities": [
            "SHA-256 block hashing",
            "Previous-hash chain linkage",
            "Genesis-anchor verification",
            "Sequential block-index verification",
            "Material-batch duplicate prevention",
            "Supplier-approval traceability",
            "Certificate and QMS decision evidence",
            "Controlled tamper detection",
        ],
        "limitations": [
            (
                "This is a simulated educational ledger, "
                "not a distributed blockchain network."
            ),
            (
                "It does not implement peer-to-peer consensus, "
                "mining, staking or smart contracts."
            ),
            (
                "Integrity is demonstrated through deterministic "
                "hash chaining and independent verification."
            ),
        ],
    }

    return report


def save_json_report(
    path: Path,
    report: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def save_text_report(
    path: Path,
    report: dict[str, Any],
) -> None:
    latest = report["latest_block"]
    decisions = report["decision_counts"]
    suppliers = report["supplier_counts"]

    lines = [
        "============================================================",
        "Simulated Blockchain Ledger — Status Evidence",
        "============================================================",
        f"Generated at          : {report['generated_at']}",
        f"Component             : {report['component']}",
        f"Implementation        : {report['implementation_type']}",
        f"Deployment model      : {report['deployment_model']}",
        f"Hash algorithm        : {report['hash_algorithm']}",
        f"Genesis anchor        : {report['genesis_anchor']}",
        f"Ledger path           : {report['ledger_path']}",
        "",
        "Chain Health",
        "------------------------------------------------------------",
        f"Chain status          : {report['chain_status']}",
        f"Ledger valid          : {report['ledger_valid']}",
        (
            "Integrity failure    : "
            f"{report['integrity_failure']['detected']}"
        ),
        (
            "First failing record: "
            f"{report['integrity_failure']['first_failing_record']}"
        ),
        f"Block count           : {report['block_count']}",
        f"Latest block index    : {latest['index']}",
        f"Latest record ID      : {latest['record_id']}",
        f"Latest batch ID       : {latest['batch_id']}",
        f"Previous hash         : {latest['previous_hash_short']}",
        f"Current hash          : {latest['current_hash_short']}",
        (
            "Stored hash verified  : "
            f"{latest['stored_hash_matches_recalculated']}"
        ),
        "",
        "QMS Decisions",
        "------------------------------------------------------------",
        f"Approved              : {decisions['approved']}",
        f"Quarantined           : {decisions['quarantined']}",
        (
            "Rejected/legal review : "
            f"{decisions['rejected_or_legal_review']}"
        ),
        (
            "Approved suppliers    : "
            f"{suppliers['approved_supplier_records']}"
        ),
        (
            "Non-approved records  : "
            f"{suppliers['non_approved_supplier_records']}"
        ),
        "",
        "Implementation Scope",
        "------------------------------------------------------------",
        "Educational simulated blockchain: YES",
        "Tamper-evident SHA-256 hash chain: YES",
        "Distributed consensus network: NO",
        "Smart contracts: NO",
        "",
        "Verification Errors",
        "------------------------------------------------------------",
    ]

    errors = report["chain_errors"]

    if errors:
        lines.extend(
            f"- {error}"
            for error in errors
        )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "Simulated blockchain ledger status: "
            + report["chain_status"],
        ]
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate status evidence for the "
            "simulated blockchain ledger."
        )
    )

    parser.add_argument(
        "--ledger",
        type=Path,
        default=LEDGER_PATH,
        help="Ledger JSON file to inspect.",
    )

    parser.add_argument(
        "--json-report",
        type=Path,
        default=DEFAULT_JSON_REPORT,
        help="JSON status report output path.",
    )

    parser.add_argument(
        "--text-report",
        type=Path,
        default=DEFAULT_TEXT_REPORT,
        help="Text status report output path.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.ledger.exists():
        print(
            "ERROR: Ledger file was not found:",
            args.ledger,
        )
        print(
            "Run first: python -m src.supply_chain_ledger"
        )
        return 1

    report = build_status_report(
        args.ledger
    )

    save_json_report(
        args.json_report,
        report,
    )

    save_text_report(
        args.text_report,
        report,
    )

    print(
        "Component      :",
        report["component"],
    )
    print(
        "Implementation :",
        report["implementation_type"],
    )
    print(
        "Chain status   :",
        report["chain_status"],
    )
    print(
        "Block count    :",
        report["block_count"],
    )
    print(
        "Latest hash    :",
        report["latest_block"][
            "current_hash_short"
        ],
    )
    print(
        "JSON report    :",
        args.json_report,
    )
    print(
        "Text report    :",
        args.text_report,
    )

    print()
    print(
        "Simulated blockchain ledger status generation:",
        report["chain_status"],
    )

    return 0 if report["ledger_valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
