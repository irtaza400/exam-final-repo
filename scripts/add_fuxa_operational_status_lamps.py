"""Add Machine and Security status semaphores to the Topic 127 FUXA view."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VIEW_PATH = Path(
    "fuxa/project/topic127_operations_overview.json"
)

DEVICE_NAME = "Topic127 OPC-UA Process"

GREY = "#A0AEC0"
GREEN = "#18A558"
AMBER = "#E59B18"
RED = "#D64545"


def semaphore_item(
    *,
    item_id: str,
    name: str,
    variable: str,
    variable_id: str,
    ranges: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "id": item_id,
        "type": "svg-ext-gauge_semaphore",
        "name": name,
        "property": {
            "events": [],
            "variable": variable,
            "variableId": variable_id,
            "variableSrc": DEVICE_NAME,
            "alarmId": "",
            "alarmSrc": "",
            "alarm": "",
            "alarmColor": "",
            "ranges": ranges,
        },
        "label": "HtmlSemaphore",
    }


def semaphore_svg(
    *,
    group_id: str,
    lamp_id: str,
    cx: int,
    cy: int,
) -> str:
    return (
        f'<g id="{group_id}" '
        f'type="svg-ext-gauge_semaphore" '
        f'fill="#000000" stroke="#000000" '
        f'font-family="Arial, sans-serif">'
        f'<ellipse id="{lamp_id}" '
        f'cx="{cx}" cy="{cy}" '
        f'rx="18" ry="18" '
        f'fill="{GREY}" stroke="#486581" '
        f'stroke-width="2"/>'
        f'</g>'
    )


def main() -> None:
    view = json.loads(
        VIEW_PATH.read_text(encoding="utf-8")
    )

    items = view["items"]
    svg = view["svgcontent"]

    definitions = [
        {
            "item_id": "GSE_TOPIC127_MACHINE_STATUS",
            "lamp_id": "LAMP_TOPIC127_MACHINE_STATUS",
            "name": "Machine Status Indicator",
            "variable": "MachineStatusCode",
            "variable_id": (
                "Topic127 OPC-UA Process^~^ns=2;i=9"
            ),
            "cx": 570,
            "cy": 560,
            "ranges": [
                {
                    "type": "range",
                    "min": "-999",
                    "max": "0.9999",
                    "color": GREY,
                },
                {
                    "type": "range",
                    "min": "1",
                    "max": "1",
                    "color": GREEN,
                },
                {
                    "type": "range",
                    "min": "1.0001",
                    "max": "999",
                    "color": AMBER,
                },
            ],
        },
        {
            "item_id": "GSE_TOPIC127_SECURITY_STATUS",
            "lamp_id": "LAMP_TOPIC127_SECURITY_STATUS",
            "name": "Security Status Indicator",
            "variable": "SecurityStateCode",
            "variable_id": (
                "Topic127 OPC-UA Process^~^ns=2;i=10"
            ),
            "cx": 1185,
            "cy": 560,
            "ranges": [
                {
                    "type": "range",
                    "min": "-999",
                    "max": "0.9999",
                    "color": GREY,
                },
                {
                    "type": "range",
                    "min": "1",
                    "max": "1",
                    "color": GREEN,
                },
                {
                    "type": "range",
                    "min": "1.0001",
                    "max": "999",
                    "color": RED,
                },
            ],
        },
    ]

    # Deterministic reruns.
    for definition in definitions:
        items.pop(definition["item_id"], None)

    for definition in definitions:
        items[definition["item_id"]] = semaphore_item(
            item_id=definition["item_id"],
            name=definition["name"],
            variable=definition["variable"],
            variable_id=definition["variable_id"],
            ranges=definition["ranges"],
        )

    start_marker = (
        "<!-- TOPIC127_OPERATIONAL_STATUS_LAMPS_START -->"
    )
    end_marker = (
        "<!-- TOPIC127_OPERATIONAL_STATUS_LAMPS_END -->"
    )

    if start_marker in svg and end_marker in svg:
        before, remainder = svg.split(start_marker, 1)
        _, after = remainder.split(end_marker, 1)
        svg = before + after

    additions = [
        start_marker,
        *[
            semaphore_svg(
                group_id=definition["item_id"],
                lamp_id=definition["lamp_id"],
                cx=definition["cx"],
                cy=definition["cy"],
            )
            for definition in definitions
        ],
        end_marker,
    ]

    if "</svg>" not in svg:
        raise SystemExit("ERROR: Closing SVG tag not found.")

    svg = svg.replace(
        "</svg>",
        "\n".join(additions) + "\n</svg>",
        1,
    )

    view["svgcontent"] = svg

    for definition in definitions:
        item_id = definition["item_id"]

        if item_id not in view["items"]:
            raise SystemExit(
                f"ERROR: Missing FUXA item: {item_id}"
            )

        if f'id="{item_id}"' not in svg:
            raise SystemExit(
                f"ERROR: Missing SVG group: {item_id}"
            )

        ranges = view["items"][item_id]["property"]["ranges"]

        if len(ranges) != 3:
            raise SystemExit(
                f"ERROR: Invalid ranges for {item_id}"
            )

    if len(view["items"]) != 12:
        raise SystemExit(
            "ERROR: Expected 12 dynamic items, "
            f"found {len(view['items'])}"
        )

    VIEW_PATH.write_text(
        json.dumps(view, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Existing dynamic items :", 10)
    print("Operational semaphores :", len(definitions))
    print("Total dynamic items    :", len(view["items"]))
    print("Updated                :", VIEW_PATH)
    print("FUXA operational status-lamp generation: PASS")


if __name__ == "__main__":
    main()
