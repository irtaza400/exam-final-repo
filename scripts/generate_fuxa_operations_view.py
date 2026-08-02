"""Generate the Topic 127 FUXA Operations Overview HMI view."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


BINDINGS_PATH = Path(
    "fuxa/project/topic127_operations_bindings.json"
)

OUTPUT_PATH = Path(
    "fuxa/project/topic127_operations_overview.json"
)

DEVICE_NAME = "Topic127 OPC-UA Process"


def load_bindings() -> dict[str, Any]:
    with BINDINGS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def value_item(
    *,
    item_id: str,
    name: str,
    variable_id: str,
    unit: str = "",
    minimum: float | int | None = None,
    maximum: float | int | None = None,
) -> dict[str, Any]:
    ranges: list[dict[str, Any]] = []

    if unit or minimum is not None or maximum is not None:
        range_item: dict[str, Any] = {
            "type": "unit",
        }

        if minimum is not None:
            range_item["min"] = minimum

        if maximum is not None:
            range_item["max"] = maximum

        if unit:
            range_item["text"] = unit

        ranges.append(range_item)

    return {
        "id": item_id,
        "type": "svg-ext-value",
        "name": name,
        "property": {
            "events": [],
            "variable": name,
            "variableId": variable_id,
            "variableSrc": DEVICE_NAME,
            "alarmId": "",
            "alarmSrc": "",
            "alarm": "",
            "alarmColor": "",
            "ranges": ranges,
        },
        "label": "Value",
    }


def text_element(
    *,
    element_id: str,
    x: int,
    y: int,
    text: str,
    size: int = 18,
    weight: int = 400,
    fill: str = "#102A43",
    anchor: str = "start",
) -> str:
    return (
        f'<text id="{element_id}" '
        f'x="{x}" y="{y}" '
        f'font-family="Arial, sans-serif" '
        f'font-size="{size}" '
        f'font-weight="{weight}" '
        f'fill="{fill}" '
        f'text-anchor="{anchor}">'
        f'{html.escape(text)}</text>'
    )


def rect_element(
    *,
    element_id: str,
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    stroke: str = "#D9E2EC",
    radius: int = 12,
) -> str:
    return (
        f'<rect id="{element_id}" '
        f'x="{x}" y="{y}" '
        f'width="{width}" height="{height}" '
        f'rx="{radius}" ry="{radius}" '
        f'fill="{fill}" stroke="{stroke}" '
        f'stroke-width="1"/>'
    )


def value_group(
    *,
    group_id: str,
    child_id: str,
    x: int,
    y: int,
    placeholder: str,
    size: int = 28,
    fill: str = "#102A43",
    anchor: str = "start",
) -> str:
    return (
        f'<g id="{group_id}" '
        f'type="svg-ext-value" '
        f'fill="{fill}" stroke="{fill}" '
        f'font-size="{size}" stroke-width="0" '
        f'font-family="Arial, sans-serif" '
        f'text-anchor="{anchor}">'
        f'<text id="{child_id}" '
        f'x="{x}" y="{y}" '
        f'fill="{fill}" stroke="{fill}" '
        f'font-size="{size}" '
        f'font-family="Arial, sans-serif" '
        f'font-weight="700" '
        f'text-anchor="{anchor}">'
        f'{html.escape(placeholder)}</text>'
        f'</g>'
    )


def build_view(config: dict[str, Any]) -> dict[str, Any]:
    view_config = config["view"]
    tags = config["tags"]

    ids = {
        "recipe_id": "VAL_TOPIC127_RECIPE",
        "process_name": "VAL_TOPIC127_PROCESS",
        "temperature": "VAL_TOPIC127_TEMPERATURE",
        "pressure": "VAL_TOPIC127_PRESSURE",
        "etch_time": "VAL_TOPIC127_ETCH_TIME",
        "machine_status": "VAL_TOPIC127_MACHINE_STATUS",
        "security_state": "VAL_TOPIC127_SECURITY_STATE",
    }

    items = {
        ids["recipe_id"]: value_item(
            item_id=ids["recipe_id"],
            name=tags["recipe_id"]["name"],
            variable_id=tags["recipe_id"]["variable_id"],
        ),
        ids["process_name"]: value_item(
            item_id=ids["process_name"],
            name=tags["process_name"]["name"],
            variable_id=tags["process_name"]["variable_id"],
        ),
        ids["temperature"]: value_item(
            item_id=ids["temperature"],
            name=tags["temperature"]["name"],
            variable_id=tags["temperature"]["variable_id"],
            unit=tags["temperature"]["unit"],
            minimum=tags["temperature"]["normal_min"],
            maximum=tags["temperature"]["normal_max"],
        ),
        ids["pressure"]: value_item(
            item_id=ids["pressure"],
            name=tags["pressure"]["name"],
            variable_id=tags["pressure"]["variable_id"],
            unit=tags["pressure"]["unit"],
            minimum=tags["pressure"]["normal_min"],
            maximum=tags["pressure"]["normal_max"],
        ),
        ids["etch_time"]: value_item(
            item_id=ids["etch_time"],
            name=tags["etch_time"]["name"],
            variable_id=tags["etch_time"]["variable_id"],
            unit=tags["etch_time"]["unit"],
            minimum=tags["etch_time"]["normal_min"],
            maximum=tags["etch_time"]["normal_max"],
        ),
        ids["machine_status"]: value_item(
            item_id=ids["machine_status"],
            name=tags["machine_status"]["name"],
            variable_id=tags["machine_status"]["variable_id"],
        ),
        ids["security_state"]: value_item(
            item_id=ids["security_state"],
            name=tags["security_state"]["name"],
            variable_id=tags["security_state"]["variable_id"],
        ),
    }

    svg_parts = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'width="1280" height="720" '
            'viewBox="0 0 1280 720">'
        ),
        rect_element(
            element_id="BACKGROUND",
            x=0,
            y=0,
            width=1280,
            height=720,
            fill="#F4F7FA",
            stroke="#F4F7FA",
            radius=0,
        ),
        rect_element(
            element_id="HEADER",
            x=0,
            y=0,
            width=1280,
            height=105,
            fill="#102A43",
            stroke="#102A43",
            radius=0,
        ),
        text_element(
            element_id="TITLE",
            x=55,
            y=48,
            text="Topic 127 Nanomanufacturing Operations HMI",
            size=30,
            weight=700,
            fill="#FFFFFF",
        ),
        text_element(
            element_id="SUBTITLE",
            x=55,
            y=79,
            text="Live OPC-UA process monitoring and industrial security status",
            size=16,
            fill="#D9EAF7",
        ),

        # Recipe and process cards
        rect_element(
            element_id="RECIPE_CARD",
            x=55,
            y=135,
            width=555,
            height=130,
            fill="#FFFFFF",
        ),
        text_element(
            element_id="RECIPE_LABEL",
            x=85,
            y=175,
            text="ACTIVE RECIPE",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["recipe_id"],
            child_id="TXT_TOPIC127_RECIPE",
            x=85,
            y=225,
            placeholder="RCP-LITHO-001",
            size=30,
        ),
        rect_element(
            element_id="PROCESS_CARD",
            x=670,
            y=135,
            width=555,
            height=130,
            fill="#FFFFFF",
        ),
        text_element(
            element_id="PROCESS_LABEL",
            x=700,
            y=175,
            text="CURRENT PROCESS",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["process_name"],
            child_id="TXT_TOPIC127_PROCESS",
            x=700,
            y=225,
            placeholder="nanolithography",
            size=30,
        ),

        # Parameter cards
        rect_element(
            element_id="TEMP_CARD",
            x=55,
            y=300,
            width=350,
            height=165,
            fill="#FFFFFF",
        ),
        text_element(
            element_id="TEMP_LABEL",
            x=85,
            y=342,
            text="TEMPERATURE SETPOINT",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["temperature"],
            child_id="TXT_TOPIC127_TEMPERATURE",
            x=85,
            y=397,
            placeholder="##.## °C",
            size=32,
        ),
        text_element(
            element_id="TEMP_LIMIT",
            x=85,
            y=438,
            text="Approved range: 20.00–25.00 °C",
            size=14,
            fill="#627D98",
        ),
        rect_element(
            element_id="PRESSURE_CARD",
            x=465,
            y=300,
            width=350,
            height=165,
            fill="#FFFFFF",
        ),
        text_element(
            element_id="PRESSURE_LABEL",
            x=495,
            y=342,
            text="PRESSURE SETPOINT",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["pressure"],
            child_id="TXT_TOPIC127_PRESSURE",
            x=495,
            y=397,
            placeholder="#.## bar",
            size=32,
        ),
        text_element(
            element_id="PRESSURE_LIMIT",
            x=495,
            y=438,
            text="Approved range: 0.90–1.10 bar",
            size=14,
            fill="#627D98",
        ),
        rect_element(
            element_id="ETCH_CARD",
            x=875,
            y=300,
            width=350,
            height=165,
            fill="#FFFFFF",
        ),
        text_element(
            element_id="ETCH_LABEL",
            x=905,
            y=342,
            text="ETCH TIME",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["etch_time"],
            child_id="TXT_TOPIC127_ETCH_TIME",
            x=905,
            y=397,
            placeholder="## sec",
            size=32,
        ),
        text_element(
            element_id="ETCH_LIMIT",
            x=905,
            y=438,
            text="Approved range: 55–65 seconds",
            size=14,
            fill="#627D98",
        ),

        # Status cards
        rect_element(
            element_id="MACHINE_CARD",
            x=55,
            y=500,
            width=555,
            height=125,
            fill="#EAF8F0",
            stroke="#A7D7BC",
        ),
        text_element(
            element_id="MACHINE_LABEL",
            x=85,
            y=540,
            text="MACHINE STATUS",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["machine_status"],
            child_id="TXT_TOPIC127_MACHINE_STATUS",
            x=85,
            y=588,
            placeholder="RUNNING",
            size=29,
            fill="#147D4A",
        ),
        rect_element(
            element_id="SECURITY_CARD",
            x=670,
            y=500,
            width=555,
            height=125,
            fill="#EAF8F0",
            stroke="#A7D7BC",
        ),
        text_element(
            element_id="SECURITY_LABEL",
            x=700,
            y=540,
            text="SECURITY STATE",
            size=15,
            weight=700,
            fill="#486581",
        ),
        value_group(
            group_id=ids["security_state"],
            child_id="TXT_TOPIC127_SECURITY_STATE",
            x=700,
            y=588,
            placeholder="NORMAL",
            size=29,
            fill="#147D4A",
        ),

        # Footer
        rect_element(
            element_id="FOOTER",
            x=55,
            y=650,
            width=1170,
            height=45,
            fill="#D9EAF7",
            stroke="#B8D4E8",
            radius=8,
        ),
        text_element(
            element_id="FOOTER_TEXT",
            x=640,
            y=680,
            text=(
                "Operator guidance: verify out-of-spec parameters "
                "before continuing manufacturing operations."
            ),
            size=15,
            fill="#243B53",
            anchor="middle",
        ),
        "</svg>",
    ]

    return {
        "id": view_config["id"],
        "name": view_config["name"],
        "profile": {
            "width": view_config["width"],
            "height": view_config["height"],
            "bkcolor": "#F4F7FA",
        },
        "items": items,
        "variables": {},
        "svgcontent": "\n".join(svg_parts),
    }


def validate_view(view: dict[str, Any]) -> None:
    required_keys = {
        "id",
        "name",
        "profile",
        "items",
        "variables",
        "svgcontent",
    }

    missing = required_keys - view.keys()

    if missing:
        raise ValueError(
            f"Missing view keys: {sorted(missing)}"
        )

    if len(view["items"]) != 7:
        raise ValueError(
            f"Expected 7 dynamic items, got {len(view['items'])}"
        )

    svg = view["svgcontent"]

    for item_id, item in view["items"].items():
        if f'id="{item_id}"' not in svg:
            raise ValueError(
                f"Item ID missing from SVG: {item_id}"
            )

        variable_id = item["property"]["variableId"]

        if not variable_id.startswith(
            "Topic127 OPC-UA Process^~^ns=2;i="
        ):
            raise ValueError(
                f"Invalid binding: {variable_id}"
            )


def main() -> None:
    config = load_bindings()
    view = build_view(config)
    validate_view(view)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(view, indent=2) + "\n",
        encoding="utf-8",
    )

    print("View ID      :", view["id"])
    print("View name    :", view["name"])
    print("Dimensions   :", view["profile"])
    print("Dynamic items:", len(view["items"]))
    print("SVG length   :", len(view["svgcontent"]))
    print("Written      :", OUTPUT_PATH)
    print("FUXA Operations Overview generation: PASS")


if __name__ == "__main__":
    main()
