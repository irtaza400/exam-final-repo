"""Standalone verifier for the Topic 127 supply-chain ledger."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.supply_chain_ledger import load_ledger, verify_chain


DEFAULT_LEDGER = Path("reports/supply_chain_ledger.json")
DEFAULT_REPORT = Path("reports/ledger_verification_report.json")


def verify_ledger_file(path: Path) -> dict[str, Any]:
    chain = load_ledger(path)
    valid, errors = verify_chain(chain)

    return {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "ledger_path": str(path),
        "ledger_valid": valid,
        "record_count": len(chain),
        "errors": errors,
    }


def save_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the Topic 127 tamper-evident supply-chain ledger."
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=DEFAULT_LEDGER,
        help="Ledger JSON file to verify.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="Verification report output path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.ledger.exists():
        print(f"ERROR: Ledger file not found: {args.ledger}")
        return 1

    report = verify_ledger_file(args.ledger)
    save_report(args.report, report)

    print("Ledger path   :", report["ledger_path"])
    print("Record count  :", report["record_count"])
    print("Ledger valid  :", report["ledger_valid"])

    if report["errors"]:
        print("Verification errors:")
        for error in report["errors"]:
            print("  -", error)

    print("Report written:", args.report)

    return 0 if report["ledger_valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
