"""Validate the Topic 127 Operations Overview view in the running FUXA project."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_FUXA_URL = "http://127.0.0.1:1881"

DEFAULT_VIEW_PATH = Path(
    "fuxa/project/topic127_operations_overview.json"
)

DEFAULT_REPORT_PATH = Path(
    "reports/fuxa_operations_overview_validation.json"
)

VIEW_ID = "v_topic127_operations_overview"
VIEW_NAME = "Operations Overview"

LEDGER_VIEW_ID = "v_topic127_ledger_health"
LEDGER_VIEW_NAME = "Simulated Ledger Health"

EXPECTED_DYNAMIC_ITEMS = 7

EXPECTED_BINDINGS = {
        "RecipeID":
    "Topic127 OPC-UA Process^~^t_ae97f8b5-21374127",

    "ProcessName":
    "Topic127 OPC-UA Process^~^t_b3e17761-82294d16",

    "TemperatureSetpoint":
    "Topic127 OPC-UA Process^~^t_d8cf674e-e6fb43c2",

    "PressureSetpoint":
    "Topic127 OPC-UA Process^~^t_2e211a43-320c496d",

    "EtchTimeSeconds":
    "Topic127 OPC-UA Process^~^t_771e56a1-45d64456",

    "MachineStatus":
    "Topic127 OPC-UA Process^~^t_85d620ad-7fcc4492",

    "SecurityState":
    "Topic127 OPC-UA Process^~^t_51099579-440048d8",
}


def request_json(url: str) -> Any:
    request = urllib.request.Request(
        url,
        method="GET",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=20,
        ) as response:
            body = response.read().decode(
                "utf-8",
                errors="replace",
            )

            if not body.strip():
                return {
                    "http_status": response.status,
                    "body": "",
                }

            return json.loads(body)

    except urllib.error.HTTPError as exc:
        body = exc.read().decode(
            "utf-8",
            errors="replace",
        )

        raise RuntimeError(
            f"HTTP {exc.code} for {url}: {body}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Unable to connect to {url}: {exc}"
        ) from exc


def load_source_view(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Operations Overview source file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        return json.load(handle)


def validate_source_view(
    view: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    if view.get("id") != VIEW_ID:
        errors.append(
            f"Unexpected source view ID: {view.get('id')!r}"
        )

    if view.get("name") != VIEW_NAME:
        errors.append(
            f"Unexpected source view name: {view.get('name')!r}"
        )

    if len(view.get("items", {})) != EXPECTED_DYNAMIC_ITEMS:
        errors.append(
            "Unexpected source dynamic-item count: "
            f"{len(view.get('items', {}))}; "
            f"expected {EXPECTED_DYNAMIC_ITEMS}"
        )

    if not view.get("svgcontent"):
        errors.append(
            "Source view has no SVG content."
        )

    return errors


def validate_runtime_view(
    view: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    if view.get("id") != VIEW_ID:
        errors.append(
            f"Unexpected runtime view ID: {view.get('id')!r}"
        )

    if view.get("name") != VIEW_NAME:
        errors.append(
            f"Unexpected runtime view name: {view.get('name')!r}"
        )

    items = view.get("items", {})

    if len(items) != EXPECTED_DYNAMIC_ITEMS:
        errors.append(
            "Unexpected runtime dynamic-item count: "
            f"{len(items)}; "
            f"expected {EXPECTED_DYNAMIC_ITEMS}"
        )

    if not view.get("svgcontent"):
        errors.append(
            "Runtime view has no SVG content."
        )

    for variable_name, expected_variable_id in (
        EXPECTED_BINDINGS.items()
    ):
        matching_items = [
            item
            for item in items.values()
            if item.get("name") == variable_name
        ]

        if len(matching_items) != 1:
            errors.append(
                f"Expected exactly one runtime item "
                f"for {variable_name}; "
                f"found {len(matching_items)}"
            )
            continue

        actual_variable_id = (
            matching_items[0]
            .get("property", {})
            .get("variableId")
        )

        if actual_variable_id != expected_variable_id:
            errors.append(
                f"Invalid binding for {variable_name}: "
                f"{actual_variable_id!r}; "
                f"expected {expected_variable_id!r}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fuxa-url",
        default=DEFAULT_FUXA_URL,
    )

    parser.add_argument(
        "--view",
        type=Path,
        default=DEFAULT_VIEW_PATH,
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
    )

    args = parser.parse_args()

    errors: list[str] = []

    source_view: dict[str, Any] | None = None
    runtime_views: list[dict[str, Any]] = []

    # ------------------------------------------------------------
    # 1. Validate source JSON
    # ------------------------------------------------------------

    try:
        source_view = load_source_view(args.view)
        errors.extend(
            validate_source_view(source_view)
        )
    except Exception as exc:
        errors.append(
            f"Source validation failed: {exc}"
        )

    # ------------------------------------------------------------
    # 2. Query running FUXA project
    # ------------------------------------------------------------

    try:
        base_url = args.fuxa_url.rstrip("/")
        project = request_json(
            f"{base_url}/api/project"
        )

        runtime_views = (
            project
            .get("hmi", {})
            .get("views", [])
        )

    except Exception as exc:
        errors.append(
            f"FUXA runtime query failed: {exc}"
        )

    # ------------------------------------------------------------
    # 3. Validate Operations Overview persistence
    # ------------------------------------------------------------

    operations_views = [
        view
        for view in runtime_views
        if view.get("id") == VIEW_ID
    ]

    if len(operations_views) != 1:
        errors.append(
            "Expected exactly one Operations Overview "
            f"view; found {len(operations_views)}"
        )
    else:
        errors.extend(
            validate_runtime_view(
                operations_views[0]
            )
        )

    # ------------------------------------------------------------
    # 4. Validate Ledger Health preservation
    # ------------------------------------------------------------

    ledger_views = [
        view
        for view in runtime_views
        if view.get("id") == LEDGER_VIEW_ID
    ]

    if len(ledger_views) != 1:
        errors.append(
            "Expected exactly one Simulated Ledger Health "
            f"view; found {len(ledger_views)}"
        )
    else:
        if ledger_views[0].get("name") != LEDGER_VIEW_NAME:
            errors.append(
                "Simulated Ledger Health view has unexpected "
                f"name: {ledger_views[0].get('name')!r}"
            )

    # ------------------------------------------------------------
    # 5. Validate final Topic 127 view set
    # ------------------------------------------------------------

    topic127_view_ids = {
        view.get("id")
        for view in runtime_views
        if view.get("id") in {
            VIEW_ID,
            LEDGER_VIEW_ID,
        }
    }

    expected_topic127_view_ids = {
        VIEW_ID,
        LEDGER_VIEW_ID,
    }

    if topic127_view_ids != expected_topic127_view_ids:
        errors.append(
            "Expected Topic 127 FUXA view set was not found: "
            f"{sorted(topic127_view_ids)}"
        )

    # ------------------------------------------------------------
    # 6. Build evidence report
    # ------------------------------------------------------------

    operations_runtime = (
        operations_views[0]
        if len(operations_views) == 1
        else {}
    )

    report = {
        "validation": {
            "status": "PASS" if not errors else "FAIL",
            "fuxa_url": args.fuxa_url,
        },
        "source": {
            "path": str(args.view),
            "exists": args.view.is_file(),
            "view_id": (
                source_view.get("id")
                if source_view
                else None
            ),
            "view_name": (
                source_view.get("name")
                if source_view
                else None
            ),
            "dynamic_items": (
                len(source_view.get("items", {}))
                if source_view
                else 0
            ),
            "svg_length": (
                len(source_view.get("svgcontent", ""))
                if source_view
                else 0
            ),
        },
        "runtime": {
            "total_views": len(runtime_views),
            "operations_overview": {
                "id": VIEW_ID,
                "name": (
                    operations_runtime.get("name")
                    if operations_runtime
                    else None
                ),
                "present": len(operations_views) == 1,
                "dynamic_items": len(
                    operations_runtime.get("items", {})
                ) if operations_runtime else 0,
                "svg_length": len(
                    operations_runtime.get(
                        "svgcontent",
                        "",
                    )
                ) if operations_runtime else 0,
            },
            "ledger_health": {
                "id": LEDGER_VIEW_ID,
                "name": (
                    ledger_views[0].get("name")
                    if ledger_views
                    else None
                ),
                "present": len(ledger_views) == 1,
            },
        },
        "expected_bindings": EXPECTED_BINDINGS,
        "errors": errors,
    }

    args.report.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.report.write_text(
        json.dumps(
            report,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "Source view       :",
        "PASS" if source_view and not validate_source_view(source_view) else "FAIL",
    )

    print(
        "Runtime API       :",
        "PASS" if runtime_views else "FAIL",
    )

    print(
        "Operations view   :",
        "PRESENT" if len(operations_views) == 1 else "MISSING",
    )

    print(
        "Operations items  :",
        len(operations_runtime.get("items", {}))
        if operations_runtime
        else 0,
    )

    print(
        "Ledger view       :",
        "PRESERVED" if len(ledger_views) == 1 else "MISSING",
    )

    print(
        "Total FUXA views  :",
        len(runtime_views),
    )

    print(
        "Report            :",
        args.report,
    )

    if errors:
        print()
        print("Validation errors:")

        for error in errors:
            print(
                " -",
                error,
            )

        print()
        print(
            "FUXA Operations Overview validation: FAIL"
        )

        return 1

    print()
    print(
        "FUXA Operations Overview validation: PASS"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
