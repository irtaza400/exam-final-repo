"""Validate live Machine and Security FUXA status-lamp states."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


FUXA_URL = "http://127.0.0.1:1881"

VIEW_PATH = Path(
    "fuxa/project/topic127_operations_overview.json"
)

REPORT_PATH = Path(
    "reports/fuxa_operational_status_lamps_validation.json"
)

TAG_IDS = [
    "ns=2;i=7",
    "ns=2;i=8",
    "ns=2;i=9",
    "ns=2;i=10",
]

GREEN = "#18A558"
AMBER = "#E59B18"
RED = "#D64545"


def get_live_values() -> dict[str, dict[str, Any]]:
    query = urllib.parse.urlencode(
        {"ids": json.dumps(TAG_IDS)}
    )

    url = f"{FUXA_URL}/api/getTagValue?{query}"

    with urllib.request.urlopen(url, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(
                f"FUXA returned HTTP {response.status}"
            )

        payload = json.loads(
            response.read().decode("utf-8")
        )

    return {
        item["id"]: item
        for item in payload
        if isinstance(item, dict)
    }


def validate_view() -> dict[str, dict[str, Any]]:
    view = json.loads(
        VIEW_PATH.read_text(encoding="utf-8")
    )

    expected = {
        "machine": {
            "item_id": "GSE_TOPIC127_MACHINE_STATUS",
            "variable": "MachineStatusCode",
            "binding": (
                "Topic127 OPC-UA Process^~^ns=2;i=9"
            ),
            "normal_color": GREEN,
            "abnormal_color": AMBER,
        },
        "security": {
            "item_id": "GSE_TOPIC127_SECURITY_STATUS",
            "variable": "SecurityStateCode",
            "binding": (
                "Topic127 OPC-UA Process^~^ns=2;i=10"
            ),
            "normal_color": GREEN,
            "abnormal_color": RED,
        },
    }

    results: dict[str, dict[str, Any]] = {}

    for key, config in expected.items():
        item = view["items"].get(config["item_id"])

        if item is None:
            raise RuntimeError(
                f"Missing semaphore: {config['item_id']}"
            )

        if item["type"] != "svg-ext-gauge_semaphore":
            raise RuntimeError(
                f"Invalid widget type: {config['item_id']}"
            )

        prop = item["property"]

        if prop["variable"] != config["variable"]:
            raise RuntimeError(
                f"Variable mismatch: {config['item_id']}"
            )

        if prop["variableId"] != config["binding"]:
            raise RuntimeError(
                f"Binding mismatch: {config['item_id']}"
            )

        ranges = prop["ranges"]

        if len(ranges) != 3:
            raise RuntimeError(
                f"Invalid range count: {config['item_id']}"
            )

        colors = {
            rule["color"]
            for rule in ranges
        }

        if config["normal_color"] not in colors:
            raise RuntimeError(
                f"Normal colour missing: {config['item_id']}"
            )

        if config["abnormal_color"] not in colors:
            raise RuntimeError(
                f"Abnormal colour missing: {config['item_id']}"
            )

        results[key] = {
            **config,
            "ranges": ranges,
        }

    return results


def machine_state(code: int) -> tuple[str, str]:
    if code == 1:
        return "RUNNING", "GREEN"

    if code == 2:
        return "MAINTENANCE", "AMBER"

    return "UNKNOWN", "GREY"


def security_state(code: int) -> tuple[str, str]:
    if code == 1:
        return "NORMAL", "GREEN"

    if code == 2:
        return "CHECK_REQUIRED", "RED"

    return "UNKNOWN", "GREY"


def main() -> None:
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    configured = validate_view()
    live = get_live_values()

    machine_text = str(live["ns=2;i=7"]["value"])
    security_text = str(live["ns=2;i=8"]["value"])

    machine_code = int(live["ns=2;i=9"]["value"])
    security_code = int(live["ns=2;i=10"]["value"])

    expected_machine_text, machine_lamp = machine_state(
        machine_code
    )

    expected_security_text, security_lamp = security_state(
        security_code
    )

    errors: list[str] = []

    if machine_text != expected_machine_text:
        errors.append(
            "Machine text/code mismatch: "
            f"text={machine_text!r}, code={machine_code}"
        )

    if security_text != expected_security_text:
        errors.append(
            "Security text/code mismatch: "
            f"text={security_text!r}, code={security_code}"
        )

    report = {
        "status": "PASS" if not errors else "FAIL",
        "machine": {
            "text_value": machine_text,
            "code_value": machine_code,
            "expected_lamp_state": machine_lamp,
            "timestamp": live["ns=2;i=9"].get("ts"),
            "semaphore_item": configured["machine"]["item_id"],
        },
        "security": {
            "text_value": security_text,
            "code_value": security_code,
            "expected_lamp_state": security_lamp,
            "timestamp": live["ns=2;i=10"].get("ts"),
            "semaphore_item": configured["security"]["item_id"],
        },
        "errors": errors,
    }

    print(
        f"{'Machine Status':<20} "
        f"text={machine_text:<16} "
        f"code={machine_code} "
        f"lamp={machine_lamp}"
    )

    print(
        f"{'Security State':<20} "
        f"text={security_text:<16} "
        f"code={security_code} "
        f"lamp={security_lamp}"
    )

    REPORT_PATH.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    if errors:
        print()
        for error in errors:
            print("ERROR:", error)

        raise SystemExit(1)

    print()
    print("FUXA operational status-lamp validation: PASS")
    print("Report:", REPORT_PATH)


if __name__ == "__main__":
    main()
