"""Validate Topic 127 numeric HMI lamp states from live FUXA values."""

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
    "reports/fuxa_numeric_status_lamps_validation.json"
)

TAG_IDS = [
    "ns=2;i=4",
    "ns=2;i=5",
    "ns=2;i=6",
]

EXPECTED = {
    "ns=2;i=4": {
        "name": "TemperatureSetpoint",
        "normal_min": 20.0,
        "normal_max": 25.0,
        "item_id": "GSE_TOPIC127_TEMPERATURE",
    },
    "ns=2;i=5": {
        "name": "PressureSetpoint",
        "normal_min": 0.90,
        "normal_max": 1.10,
        "item_id": "GSE_TOPIC127_PRESSURE",
    },
    "ns=2;i=6": {
        "name": "EtchTimeSeconds",
        "normal_min": 55.0,
        "normal_max": 65.0,
        "item_id": "GSE_TOPIC127_ETCH_TIME",
    },
}


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
    }


def expected_state(
    value: float,
    minimum: float,
    maximum: float,
) -> str:
    if minimum <= value <= maximum:
        return "GREEN"

    return "RED"


def validate_view() -> dict[str, Any]:
    view = json.loads(
        VIEW_PATH.read_text(encoding="utf-8")
    )

    items = view["items"]
    results: dict[str, Any] = {}

    for tag_id, config in EXPECTED.items():
        item = items.get(config["item_id"])

        if item is None:
            raise RuntimeError(
                f"Missing semaphore: {config['item_id']}"
            )

        if item["type"] != "svg-ext-gauge_semaphore":
            raise RuntimeError(
                f"Incorrect widget type: {config['item_id']}"
            )

        ranges = item["property"]["ranges"]

        results[tag_id] = {
            "item_id": config["item_id"],
            "ranges": ranges,
            "configured": True,
        }

    return results


def main() -> None:
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    configured = validate_view()
    live_values = get_live_values()

    report: dict[str, Any] = {
        "status": "PASS",
        "parameters": [],
    }

    for tag_id, config in EXPECTED.items():
        item = live_values.get(tag_id)

        if item is None:
            raise RuntimeError(
                f"Live value missing: {tag_id}"
            )

        value = float(item["value"])

        state = expected_state(
            value,
            config["normal_min"],
            config["normal_max"],
        )

        record = {
            "tag_id": tag_id,
            "name": config["name"],
            "value": value,
            "normal_min": config["normal_min"],
            "normal_max": config["normal_max"],
            "expected_lamp_state": state,
            "timestamp": item.get("ts"),
            "semaphore_item": configured[tag_id]["item_id"],
        }

        report["parameters"].append(record)

        print(
            f"{config['name']:<24} "
            f"value={value:<8} "
            f"normal={config['normal_min']}-"
            f"{config['normal_max']} "
            f"lamp={state}"
        )

    REPORT_PATH.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    print()
    print("FUXA numeric status-lamp validation: PASS")
    print("Report:", REPORT_PATH)


if __name__ == "__main__":
    main()
