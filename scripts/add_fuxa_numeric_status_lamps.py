"""Add native FUXA range semaphores to the Topic 127 Operations view."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VIEW_PATH = Path(
    "fuxa/project/topic127_operations_overview.json"
)

DEVICE_NAME = "Topic127 OPC-UA Process"

GREEN = "#18A558"
RED = "#D64545"
GREY = "#A0AEC0"


def semaphore_item(
    *,
    item_id: str,
    variable: str,
    variable_id: str,
    ranges: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "id": item_id,
        "type": "svg-ext-gauge_semaphore",
        "name": f"{variable} Status",
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
        f'rx="13" ry="13" '
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
            "item_id": "GSE_TOPIC127_TEMPERATURE",
            "lamp_id": "LAMP_TOPIC127_TEMPERATURE",
            "variable": "TemperatureSetpoint",
            "variable_id": (
                "Topic127 OPC-UA Process^~^ns=2;i=4"
            ),
            "cx": 365,
            "cy": 332,
            "ranges": [
                {
                    "type": "range",
                    "min": "-999",
                    "max": "19.9999",
                    "color": RED,
                },
                {
                    "type": "range",
                    "min": "20",
                    "max": "25",
                    "color": GREEN,
                },
                {
                    "type": "range",
                    "min": "25.0001",
                    "max": "999",
                    "color": RED,
                },
            ],
        },
        {
            "item_id": "GSE_TOPIC127_PRESSURE",
            "lamp_id": "LAMP_TOPIC127_PRESSURE",
            "variable": "PressureSetpoint",
            "variable_id": (
                "Topic127 OPC-UA Process^~^ns=2;i=5"
            ),
            "cx": 775,
            "cy": 332,
            "ranges": [
                {
                    "type": "range",
                    "min": "-999",
                    "max": "0.8999",
                    "color": RED,
                },
                {
                    "type": "range",
                    "min": "0.90",
                    "max": "1.10",
                    "color": GREEN,
                },
                {
                    "type": "range",
                    "min": "1.1001",
                    "max": "999",
                    "color": RED,
                },
            ],
        },
        {
            "item_id": "GSE_TOPIC127_ETCH_TIME",
            "lamp_id": "LAMP_TOPIC127_ETCH_TIME",
            "variable": "EtchTimeSeconds",
            "variable_id": (
                "Topic127 OPC-UA Process^~^ns=2;i=6"
            ),
            "cx": 1185,
            "cy": 332,
            "ranges": [
                {
                    "type": "range",
                    "min": "-999",
                    "max": "54.9999",
                    "color": RED,
                },
                {
                    "type": "range",
                    "min": "55",
                    "max": "65",
                    "color": GREEN,
                },
                {
                    "type": "range",
                    "min": "65.0001",
                    "max": "999",
                    "color": RED,
                },
            ],
        },
    ]

    # Make reruns deterministic.
    for definition in definitions:
        items.pop(definition["item_id"], None)

    for definition in definitions:
        items[definition["item_id"]] = semaphore_item(
            item_id=definition["item_id"],
            variable=definition["variable"],
            variable_id=definition["variable_id"],
            ranges=definition["ranges"],
        )

    # Remove previously generated status-lamp SVG groups on rerun.
    start_marker = "<!-- TOPIC127_STATUS_LAMPS_START -->"
    end_marker = "<!-- TOPIC127_STATUS_LAMPS_END -->"

    if start_marker in svg and end_marker in svg:
        before, remainder = svg.split(start_marker, 1)
        _, after = remainder.split(end_marker, 1)
        svg = before + after

    status_svg = [
        start_marker,
        *[
            semaphore_svg(
                group_id=item["item_id"],
                lamp_id=item["lamp_id"],
                cx=item["cx"],
                cy=item["cy"],
            )
            for item in definitions
        ],
        end_marker,
    ]

    if "</svg>" not in svg:
        raise SystemExit("ERROR: Closing SVG tag not found.")

    svg = svg.replace(
        "</svg>",
        "\n".join(status_svg) + "\n</svg>",
        1,
    )

    view["svgcontent"] = svg

    for definition in definitions:
        item_id = definition["item_id"]

        if item_id not in view["items"]:
            raise SystemExit(
                f"ERROR: Missing item: {item_id}"
            )

        if f'id="{item_id}"' not in svg:
            raise SystemExit(
                f"ERROR: Missing SVG group: {item_id}"
            )

        ranges = view["items"][item_id]["property"]["ranges"]

        if len(ranges) != 3:
            raise SystemExit(
                f"ERROR: Expected three ranges for {item_id}"
            )

    VIEW_PATH.write_text(
        json.dumps(view, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Dynamic value widgets :", 7)
    print("Status semaphores     :", len(definitions))
    print("Total dynamic items   :", len(view["items"]))
    print("Updated               :", VIEW_PATH)
    print("FUXA numeric status-lamp generation: PASS")


if __name__ == "__main__":
    main()
