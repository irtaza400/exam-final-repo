"""Validate simulated-ledger health metrics stored in InfluxDB."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from influxdb_client import InfluxDBClient


DEFAULT_INFLUX_URL = "http://localhost:8086"
DEFAULT_INFLUX_TOKEN = "topic127-token"
DEFAULT_INFLUX_ORG = "topic127"
DEFAULT_INFLUX_BUCKET = "cleanroom"

REPORT_PATH = Path(
    "reports/ledger_metrics_validation.json"
)

MEASUREMENT = "ledger_health"

EXPECTED_FIELDS = {
    "ledger_valid",
    "block_count",
    "approved_records",
    "quarantined_records",
    "rejected_records",
    "integrity_failure_detected",
    "latest_block_index",
    "latest_hash_short",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

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

    parser.add_argument(
        "--range",
        default="-30m",
        dest="time_range",
    )

    return parser.parse_args()


def query_latest(
    *,
    influx_url: str,
    token: str,
    org: str,
    bucket: str,
    time_range: str,
) -> list[Any]:
    query = f'''
from(bucket: "{bucket}")
  |> range(start: {time_range})
  |> filter(fn: (r) => r._measurement == "{MEASUREMENT}")
  |> last()
'''

    with InfluxDBClient(
        url=influx_url,
        token=token,
        org=org,
    ) as client:
        return client.query_api().query(
            query=query,
            org=org,
        )


def main() -> int:
    args = parse_args()

    errors: list[str] = []
    values: dict[str, Any] = {}
    tags: dict[str, Any] = {}
    latest_timestamp = None

    try:
        tables = query_latest(
            influx_url=args.influx_url,
            token=args.token,
            org=args.org,
            bucket=args.bucket,
            time_range=args.time_range,
        )
    except Exception as exc:
        print(
            "ERROR: Unable to query ledger metrics:",
            exc,
        )
        return 1

    for table in tables:
        for record in table.records:
            field = record.get_field()

            if field:
                values[field] = record.get_value()

            if latest_timestamp is None:
                latest_timestamp = record.get_time()

            for tag_name in [
                "chain_status",
                "component",
                "hash_algorithm",
                "project",
            ]:
                value = record.values.get(tag_name)

                if value is not None:
                    tags[tag_name] = value

    found_fields = set(values)
    missing_fields = sorted(
        EXPECTED_FIELDS - found_fields
    )

    unexpected_fields = sorted(
        found_fields - EXPECTED_FIELDS
    )

    if missing_fields:
        errors.append(
            "Missing fields: "
            + ", ".join(missing_fields)
        )

    if not values:
        errors.append(
            "No ledger_health metrics were returned."
        )

    expected_values = {
        "ledger_valid": 1,
        "integrity_failure_detected": 0,
    }

    for field, expected in expected_values.items():
        actual = values.get(field)

        if actual != expected:
            errors.append(
                f"{field} expected {expected!r}, "
                f"received {actual!r}."
            )

    if tags.get("component") != "simulated-ledger":
        errors.append(
            "Unexpected component tag: "
            f"{tags.get('component')!r}"
        )

    if tags.get("project") != "topic127":
        errors.append(
            "Unexpected project tag: "
            f"{tags.get('project')!r}"
        )

    if tags.get("chain_status") != "VALID":
        errors.append(
            "Unexpected chain_status tag: "
            f"{tags.get('chain_status')!r}"
        )

    status = "PASS" if not errors else "FAIL"

    report = {
        "status": status,
        "measurement": MEASUREMENT,
        "influx_url": args.influx_url,
        "org": args.org,
        "bucket": args.bucket,
        "time_range": args.time_range,
        "latest_timestamp": (
            latest_timestamp.isoformat()
            if latest_timestamp
            else None
        ),
        "expected_fields": sorted(
            EXPECTED_FIELDS
        ),
        "found_fields": sorted(
            found_fields
        ),
        "missing_fields": missing_fields,
        "unexpected_fields": unexpected_fields,
        "values": values,
        "tags": tags,
        "errors": errors,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )

    print("Measurement     :", MEASUREMENT)
    print("Fields found    :", len(found_fields))
    print("Latest timestamp:", latest_timestamp)
    print("Chain status    :", tags.get("chain_status"))
    print("Ledger valid    :", values.get("ledger_valid"))
    print(
        "Integrity fail  :",
        values.get(
            "integrity_failure_detected"
        ),
    )
    print()
    print(
        f"Ledger metrics validation: {status}"
    )
    print("Report:", REPORT_PATH)

    if errors:
        for error in errors:
            print("ERROR:", error)

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
