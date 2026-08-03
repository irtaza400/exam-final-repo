"""Validate the persisted FUXA Simulated Ledger Health view."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any


FUXA_URL = "http://127.0.0.1:1881"

SOURCE_VIEW_PATH = Path(
    "fuxa/project/topic127_ledger_health.json"
)

REPORT_PATH = Path(
    "reports/fuxa_ledger_health_validation.json"
)

VIEW_ID = "v_topic127_ledger_health"

EXPECTED_TEXT = [
    "Simulated Blockchain Ledger Health",
    "LEDGER STATE",
    "BLOCK COUNT",
    "LATEST BLOCK HASH",
    "APPROVED FOR USE",
    "QUARANTINED",
    "REJECTED / LEGAL REVIEW",
    "INTEGRITY VERIFICATION",
    "SHA-256",
]


def load_live_project() -> dict[str, Any]:
    with urllib.request.urlopen(
        f"{FUXA_URL}/api/project",
        timeout=20,
    ) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


def main() -> int:
    errors: list[str] = []

    if not SOURCE_VIEW_PATH.is_file():
        errors.append(
            f"Missing source view: {SOURCE_VIEW_PATH}"
        )

    source_view = (
        json.loads(
            SOURCE_VIEW_PATH.read_text(
                encoding="utf-8"
            )
        )
        if SOURCE_VIEW_PATH.is_file()
        else {}
    )

    project = load_live_project()

    views = project.get(
        "hmi",
        {},
    ).get(
        "views",
        [],
    )

    matching = [
        view
        for view in views
        if view.get("id") == VIEW_ID
    ]

    if len(matching) != 1:
        errors.append(
            "Expected exactly one persisted Ledger Health view; "
            f"found {len(matching)}."
        )

    live_view = matching[0] if matching else {}
    svg = str(live_view.get("svgcontent", ""))

    for value in EXPECTED_TEXT:
        if value not in svg:
            errors.append(
                f"Missing expected SVG text: {value}"
            )

    operations_present = any(
        view.get("id")
        == "v_topic127_operations_overview"
        for view in views
    )

    if not operations_present:
        errors.append(
            "Operations Overview view is missing."
        )

    source_matches_live = (
        source_view.get("svgcontent")
        == live_view.get("svgcontent")
        if source_view and live_view
        else False
    )

    if not source_matches_live:
        errors.append(
            "Persisted Ledger Health SVG does not match source."
        )

    status = "PASS" if not errors else "FAIL"

    report = {
        "status": status,
        "view_id": VIEW_ID,
        "view_name": live_view.get("name"),
        "total_views": len(views),
        "operations_overview_preserved": (
            operations_present
        ),
        "source_matches_live": (
            source_matches_live
        ),
        "expected_text_count": len(
            EXPECTED_TEXT
        ),
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

    print(
        "View name       :",
        report["view_name"],
    )
    print(
        "Total views     :",
        report["total_views"],
    )
    print(
        "Operations view :",
        (
            "PRESERVED"
            if operations_present
            else "MISSING"
        ),
    )
    print(
        "Source matches  :",
        source_matches_live,
    )
    print()
    print(
        f"FUXA ledger-health validation: {status}"
    )
    print(
        "Report:",
        REPORT_PATH,
    )

    if errors:
        for error in errors:
            print("ERROR:", error)

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
