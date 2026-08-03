"""Validate the Grafana Simulated Ledger Health dashboard JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path


DASHBOARD_PATH = Path(
    "dashboards/json/topic127_ledger_health_dashboard.json"
)

DATASOURCE_PATH = Path(
    "grafana/provisioning/datasources/influxdb.yml"
)

EXPECTED_DASHBOARD_UID = "topic127-ledger-health"
EXPECTED_DASHBOARD_TITLE = "Simulated Ledger Health"
EXPECTED_DATASOURCE_UID = "influxdb-topic127"
EXPECTED_MEASUREMENT = "ledger_health"

EXPECTED_PANELS = {
    "Ledger State": "ledger_valid",
    "Block Count": "block_count",
    "Approved Records": "approved_records",
    "Quarantined Records": "quarantined_records",
    "Rejected / Legal Review": "rejected_records",
    "Integrity Failure": "integrity_failure_detected",
    "Latest Block Index": "latest_block_index",
    "Latest Hash": "latest_hash_short",
}


def main() -> int:
    errors: list[str] = []

    if not DASHBOARD_PATH.is_file():
        print(
            "ERROR: Dashboard JSON not found:",
            DASHBOARD_PATH,
        )
        return 1

    if not DATASOURCE_PATH.is_file():
        print(
            "ERROR: Datasource provisioning file not found:",
            DATASOURCE_PATH,
        )
        return 1

    dashboard = json.loads(
        DASHBOARD_PATH.read_text(
            encoding="utf-8"
        )
    )

    if dashboard.get("uid") != EXPECTED_DASHBOARD_UID:
        errors.append(
            "Dashboard UID mismatch."
        )

    if dashboard.get("title") != EXPECTED_DASHBOARD_TITLE:
        errors.append(
            "Dashboard title mismatch."
        )

    panels = dashboard.get("panels", [])

    if len(panels) != len(EXPECTED_PANELS):
        errors.append(
            f"Expected {len(EXPECTED_PANELS)} panels, "
            f"found {len(panels)}."
        )

    panel_ids: set[int] = set()
    found_titles: set[str] = set()

    for panel in panels:
        panel_id = panel.get("id")
        title = panel.get("title")
        panel_type = panel.get("type")
        datasource = panel.get(
            "datasource",
            {},
        )
        datasource_uid = datasource.get("uid")
        targets = panel.get("targets", [])

        if panel_id in panel_ids:
            errors.append(
                f"Duplicate panel ID: {panel_id}"
            )

        panel_ids.add(panel_id)

        if title not in EXPECTED_PANELS:
            errors.append(
                f"Unexpected panel title: {title}"
            )
            continue

        found_titles.add(title)

        if panel_type != "stat":
            errors.append(
                f"Panel '{title}' must use stat type."
            )

        if datasource_uid != EXPECTED_DATASOURCE_UID:
            errors.append(
                f"Panel '{title}' datasource UID mismatch."
            )

        if not targets:
            errors.append(
                f"Panel '{title}' has no query target."
            )
            continue

        combined_query = "\n".join(
            str(target.get("query", ""))
            for target in targets
        )

        expected_field = EXPECTED_PANELS[title]

        if EXPECTED_MEASUREMENT not in combined_query:
            errors.append(
                f"Panel '{title}' does not query "
                f"{EXPECTED_MEASUREMENT}."
            )

        if expected_field not in combined_query:
            errors.append(
                f"Panel '{title}' does not query "
                f"{expected_field}."
            )

        if "|> last()" not in combined_query:
            errors.append(
                f"Panel '{title}' does not use last()."
            )

        if title == "Latest Hash":
            defaults = panel.get(
                "fieldConfig",
                {},
            ).get(
                "defaults",
                {},
            )
            options = panel.get(
                "options",
                {},
            )

            if defaults.get("unit") != "string":
                errors.append(
                    "Latest Hash panel must use string unit."
                )

            if options.get("textMode") != "value":
                errors.append(
                    "Latest Hash panel must use value text mode."
                )

            if options.get("colorMode") != "none":
                errors.append(
                    "Latest Hash panel must disable background coloring."
                )

    missing_titles = (
        set(EXPECTED_PANELS)
        - found_titles
    )

    if missing_titles:
        errors.append(
            "Missing panel titles: "
            + ", ".join(
                sorted(missing_titles)
            )
        )

    datasource_text = DATASOURCE_PATH.read_text(
        encoding="utf-8"
    )

    datasource_pattern = re.compile(
        rf"^\s*uid:\s*"
        rf"{re.escape(EXPECTED_DATASOURCE_UID)}"
        rf"\s*$",
        re.MULTILINE,
    )

    if not datasource_pattern.search(
        datasource_text
    ):
        errors.append(
            "Expected datasource UID was not found "
            "in provisioning."
        )

    status = "PASS" if not errors else "FAIL"

    print("Dashboard UID  :", dashboard.get("uid"))
    print("Dashboard title:", dashboard.get("title"))
    print("Panel count    :", len(panels))
    print("Datasource UID :", EXPECTED_DATASOURCE_UID)
    print("Measurement    :", EXPECTED_MEASUREMENT)
    print()

    for panel in panels:
        print(
            f"{panel.get('id')}: "
            f"{panel.get('title')} "
            f"[{panel.get('type')}]"
        )

    print()
    print(
        f"Grafana ledger-health dashboard validation: {status}"
    )

    if errors:
        for error in errors:
            print("ERROR:", error)

        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
