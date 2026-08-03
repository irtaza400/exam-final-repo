"""Publish simulated-ledger health evidence to InfluxDB.

The module reads the examiner-facing simulated ledger status report
and writes a single ledger_health measurement for Grafana.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_STATUS_PATH = Path(
    "reports/simulated_ledger_status.json"
)

DEFAULT_INFLUX_URL = "http://localhost:8086"
DEFAULT_INFLUX_TOKEN = "topic127-token"
DEFAULT_INFLUX_ORG = "topic127"
DEFAULT_INFLUX_BUCKET = "cleanroom"

MEASUREMENT = "ledger_health"


def load_status(path: Path) -> dict[str, Any]:
    """Load and minimally validate the simulated-ledger status report."""

    if not path.is_file():
        raise FileNotFoundError(
            f"Ledger status report was not found: {path}"
        )

    report = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not isinstance(report, dict):
        raise ValueError(
            "Ledger status report must contain a JSON object."
        )

    required = [
        "chain_status",
        "ledger_valid",
        "block_count",
        "decision_counts",
        "integrity_failure",
    ]

    missing = [
        key
        for key in required
        if key not in report
    ]

    if missing:
        raise ValueError(
            "Ledger status report is missing required fields: "
            + ", ".join(missing)
        )

    return report


def metric_values(
    report: dict[str, Any],
) -> dict[str, int]:
    """Convert status evidence into numeric InfluxDB fields."""

    decisions = report.get(
        "decision_counts",
        {},
    )

    integrity = report.get(
        "integrity_failure",
        {},
    )

    return {
        "ledger_valid": (
            1
            if bool(report.get("ledger_valid"))
            else 0
        ),
        "block_count": int(
            report.get("block_count", 0)
        ),
        "approved_records": int(
            decisions.get("approved", 0)
        ),
        "quarantined_records": int(
            decisions.get("quarantined", 0)
        ),
        "rejected_records": int(
            decisions.get(
                "rejected_or_legal_review",
                0,
            )
        ),
        "integrity_failure_detected": (
            1
            if bool(integrity.get("detected"))
            else 0
        ),
    }


def build_point(
    report: dict[str, Any],
) -> Any:
    """Build the ledger_health InfluxDB point."""

    from influxdb_client import Point, WritePrecision

    values = metric_values(report)

    latest = report.get(
        "latest_block",
        {},
    )

    point = (
        Point(MEASUREMENT)
        .tag(
            "component",
            "simulated-ledger",
        )
        .tag(
            "project",
            "topic127",
        )
        .tag(
            "chain_status",
            str(
                report.get(
                    "chain_status",
                    "UNKNOWN",
                )
            ),
        )
        .tag(
            "hash_algorithm",
            str(
                report.get(
                    "hash_algorithm",
                    "SHA-256",
                )
            ),
        )
        .field(
            "ledger_valid",
            values["ledger_valid"],
        )
        .field(
            "block_count",
            values["block_count"],
        )
        .field(
            "approved_records",
            values["approved_records"],
        )
        .field(
            "quarantined_records",
            values["quarantined_records"],
        )
        .field(
            "rejected_records",
            values["rejected_records"],
        )
        .field(
            "integrity_failure_detected",
            values[
                "integrity_failure_detected"
            ],
        )
        .field(
            "latest_block_index",
            int(
                latest.get(
                    "index",
                    0,
                )
                or 0
            ),
        )
        .field(
            "latest_hash_short",
            str(
                latest.get(
                    "current_hash_short",
                    "N/A",
                )
            ),
        )
        .time(
            datetime.now(timezone.utc),
            WritePrecision.NS,
        )
    )

    return point


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Publish simulated-ledger health metrics "
            "to InfluxDB."
        )
    )

    parser.add_argument(
        "--status-report",
        type=Path,
        default=DEFAULT_STATUS_PATH,
    )

    parser.add_argument(
        "--influx-url",
        default=os.getenv(
            "INFLUX_URL",
            DEFAULT_INFLUX_URL,
        ),
    )

    parser.add_argument(
        "--token",
        default=os.getenv(
            "INFLUX_TOKEN",
            DEFAULT_INFLUX_TOKEN,
        ),
    )

    parser.add_argument(
        "--org",
        default=os.getenv(
            "INFLUX_ORG",
            DEFAULT_INFLUX_ORG,
        ),
    )

    parser.add_argument(
        "--bucket",
        default=os.getenv(
            "INFLUX_BUCKET",
            DEFAULT_INFLUX_BUCKET,
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        report = load_status(
            args.status_report
        )

        values = metric_values(report)

        point = build_point(report)

        from influxdb_client import InfluxDBClient

        with InfluxDBClient(
            url=args.influx_url,
            token=args.token,
            org=args.org,
        ) as client:
            write_api = client.write_api()

            write_api.write(
                bucket=args.bucket,
                org=args.org,
                record=point,
            )

            write_api.close()

    except (
        FileNotFoundError,
        ValueError,
        OSError,
    ) as exc:
        print("ERROR:", exc)
        return 1

    except Exception as exc:
        print(
            "ERROR: Unable to publish ledger metrics:",
            exc,
        )
        return 1

    print("Measurement  :", MEASUREMENT)
    print("Influx URL   :", args.influx_url)
    print("Org/Bucket   :", f"{args.org}/{args.bucket}")
    print(
        "Chain status :",
        report.get("chain_status"),
    )
    print(
        "Ledger valid :",
        values["ledger_valid"],
    )
    print(
        "Block count  :",
        values["block_count"],
    )
    print(
        "Approved     :",
        values["approved_records"],
    )
    print(
        "Quarantined  :",
        values["quarantined_records"],
    )
    print(
        "Rejected     :",
        values["rejected_records"],
    )
    print(
        "Failure      :",
        values["integrity_failure_detected"],
    )
    print()
    print(
        "Simulated ledger metrics publication: PASS"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
