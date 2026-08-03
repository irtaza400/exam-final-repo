"""Validate deterministic Suricata IDS alerts for the lab."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


EVE_PATH = Path("suricata/logs/eve.json")
FAST_LOG_PATH = Path("suricata/logs/fast.log")
REPORT_PATH = Path("reports/suricata_ids_validation.json")

EXPECTED_ALERTS = {
    1270001: {
        "name": "Unauthorized OPC-UA Access Attempt",
        "destination_port": 4840,
    },
    1270002: {
        "name": "Suspicious MQTT Command Payload",
        "destination_port": 1883,
    },
    1270003: {
        "name": "Suspicious HMI Access Attempt",
        "destination_port": 1881,
    },
}


def load_alerts(path: Path) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at {path}:{line_number}: {exc}"
                ) from exc

            if event.get("event_type") == "alert":
                alerts.append(event)

    return alerts


def main() -> None:
    if not EVE_PATH.is_file():
        raise SystemExit(f"Missing Suricata EVE file: {EVE_PATH}")

    if not FAST_LOG_PATH.is_file():
        raise SystemExit(f"Missing Suricata fast log: {FAST_LOG_PATH}")

    alerts = load_alerts(EVE_PATH)

    by_signature_id = Counter(
        int(event["alert"]["signature_id"])
        for event in alerts
        if "alert" in event
        and "signature_id" in event["alert"]
    )

    findings: list[dict[str, Any]] = []
    errors: list[str] = []

    for signature_id, expected in EXPECTED_ALERTS.items():
        matching = [
            event
            for event in alerts
            if int(
                event.get("alert", {}).get("signature_id", -1)
            )
            == signature_id
        ]

        if not matching:
            errors.append(
                f"Expected Suricata alert SID {signature_id} was not found."
            )
            continue

        event = matching[0]
        actual_port = int(event.get("dest_port", -1))
        signature = str(
            event.get("alert", {}).get("signature", "")
        )

        if actual_port != expected["destination_port"]:
            errors.append(
                f"SID {signature_id} destination port mismatch: "
                f"expected {expected['destination_port']}, "
                f"got {actual_port}."
            )

        if expected["name"] not in signature:
            errors.append(
                f"SID {signature_id} signature text mismatch: "
                f"{signature!r}"
            )

        findings.append(
            {
                "signature_id": signature_id,
                "signature": signature,
                "count": by_signature_id[signature_id],
                "source_ip": event.get("src_ip"),
                "source_port": event.get("src_port"),
                "destination_ip": event.get("dest_ip"),
                "destination_port": actual_port,
                "protocol": event.get("proto"),
                "timestamp": event.get("timestamp"),
            }
        )

    status = "PASS" if not errors else "FAIL"

    report = {
        "status": status,
        "engine": "Suricata",
        "mode": "deterministic offline PCAP inspection",
        "eve_path": str(EVE_PATH),
        "fast_log_path": str(FAST_LOG_PATH),
        "total_alert_events": len(alerts),
        "expected_alerts": len(EXPECTED_ALERTS),
        "validated_alerts": len(findings),
        "findings": findings,
        "errors": errors,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    for finding in findings:
        print(
            f"SID={finding['signature_id']} "
            f"port={finding['destination_port']} "
            f"count={finding['count']} "
            f"signature={finding['signature']}"
        )

    print()
    print(f"Suricata alert validation: {status}")
    print(f"Report: {REPORT_PATH}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")

        raise SystemExit(1)


if __name__ == "__main__":
    main()
