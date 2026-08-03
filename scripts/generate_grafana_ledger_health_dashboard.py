"""Generate the Grafana Simulated Ledger Health dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


OUTPUT_PATH = Path(
    "dashboards/json/topic127_ledger_health_dashboard.json"
)

DASHBOARD_UID = "topic127-ledger-health"
DASHBOARD_TITLE = "Simulated Ledger Health"
DATASOURCE_UID = "influxdb-topic127"
BUCKET = "cleanroom"
MEASUREMENT = "ledger_health"


def flux_query(field: str) -> str:
    """Return a latest-value Flux query for one ledger field."""

    return (
        f'from(bucket: "{BUCKET}")\n'
        "  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n"
        f'  |> filter(fn: (r) => r._measurement == "{MEASUREMENT}")\n'
        f'  |> filter(fn: (r) => r._field == "{field}")\n'
        "  |> last()\n"
    )


def stat_panel(
    *,
    panel_id: int,
    title: str,
    field: str,
    x: int,
    y: int,
    width: int = 6,
    height: int = 7,
    unit: str = "short",
    decimals: int = 0,
    thresholds: list[dict[str, Any]] | None = None,
    value_mappings: list[dict[str, Any]] | None = None,
    text_mode: str = "auto",
    color_mode: str = "background",
) -> dict[str, Any]:
    """Build a Grafana stat panel."""

    defaults: dict[str, Any] = {
        "decimals": decimals,
        "unit": unit,
    }

    if thresholds is not None:
        defaults["thresholds"] = {
            "mode": "absolute",
            "steps": thresholds,
        }

    if value_mappings is not None:
        defaults["mappings"] = value_mappings

    return {
        "datasource": {
            "type": "influxdb",
            "uid": DATASOURCE_UID,
        },
        "fieldConfig": {
            "defaults": defaults,
            "overrides": [],
        },
        "gridPos": {
            "h": height,
            "w": width,
            "x": x,
            "y": y,
        },
        "id": panel_id,
        "options": {
            "colorMode": color_mode,
            "graphMode": "none",
            "justifyMode": "center",
            "orientation": "auto",
            "reduceOptions": {
                "calcs": [
                    "lastNotNull",
                ],
                "fields": "",
                "values": False,
            },
            "textMode": text_mode,
            "wideLayout": True,
        },
        "targets": [
            {
                "query": flux_query(field),
                "refId": "A",
            }
        ],
        "title": title,
        "type": "stat",
    }


def build_dashboard() -> dict[str, Any]:
    """Build the complete Ledger Health dashboard."""

    healthy_thresholds = [
        {
            "color": "red",
            "value": None,
        },
        {
            "color": "green",
            "value": 1,
        },
    ]

    failure_thresholds = [
        {
            "color": "green",
            "value": None,
        },
        {
            "color": "red",
            "value": 1,
        },
    ]

    warning_thresholds = [
        {
            "color": "green",
            "value": None,
        },
        {
            "color": "orange",
            "value": 1,
        },
    ]

    rejected_thresholds = [
        {
            "color": "green",
            "value": None,
        },
        {
            "color": "red",
            "value": 1,
        },
    ]

    panels = [
        stat_panel(
            panel_id=1,
            title="Ledger State",
            field="ledger_valid",
            x=0,
            y=0,
            thresholds=healthy_thresholds,
            value_mappings=[
                {
                    "options": {
                        "0": {
                            "color": "red",
                            "index": 0,
                            "text": "INVALID",
                        },
                        "1": {
                            "color": "green",
                            "index": 1,
                            "text": "VALID",
                        },
                    },
                    "type": "value",
                }
            ],
        ),
        stat_panel(
            panel_id=2,
            title="Block Count",
            field="block_count",
            x=6,
            y=0,
        ),
        stat_panel(
            panel_id=3,
            title="Approved Records",
            field="approved_records",
            x=12,
            y=0,
            thresholds=[
                {
                    "color": "green",
                    "value": None,
                }
            ],
        ),
        stat_panel(
            panel_id=4,
            title="Quarantined Records",
            field="quarantined_records",
            x=18,
            y=0,
            thresholds=warning_thresholds,
        ),
        stat_panel(
            panel_id=5,
            title="Rejected / Legal Review",
            field="rejected_records",
            x=0,
            y=7,
            thresholds=rejected_thresholds,
        ),
        stat_panel(
            panel_id=6,
            title="Integrity Failure",
            field="integrity_failure_detected",
            x=6,
            y=7,
            thresholds=failure_thresholds,
            value_mappings=[
                {
                    "options": {
                        "0": {
                            "color": "green",
                            "index": 0,
                            "text": "NO",
                        },
                        "1": {
                            "color": "red",
                            "index": 1,
                            "text": "YES",
                        },
                    },
                    "type": "value",
                }
            ],
        ),
        stat_panel(
            panel_id=7,
            title="Latest Block Index",
            field="latest_block_index",
            x=12,
            y=7,
        ),
        stat_panel(
            panel_id=8,
            title="Latest Hash",
            field="latest_hash_short",
            x=18,
            y=7,
            unit="string",
            decimals=0,
            text_mode="value",
            color_mode="none",
        ),
    ]

    return {
        "annotations": {
            "list": [],
        },
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "id": None,
        "links": [],
        "liveNow": False,
        "panels": panels,
        "refresh": "10s",
        "schemaVersion": 39,
        "tags": [
            "topic127",
            "simulated-ledger",
            "supply-chain",
            "qms",
        ],
        "templating": {
            "list": [],
        },
        "time": {
            "from": "now-30m",
            "to": "now",
        },
        "timepicker": {},
        "timezone": "browser",
        "title": DASHBOARD_TITLE,
        "uid": DASHBOARD_UID,
        "version": 1,
        "weekStart": "",
    }


def main() -> int:
    dashboard = build_dashboard()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            dashboard,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print("Dashboard UID   :", dashboard["uid"])
    print("Dashboard title :", dashboard["title"])
    print("Panel count     :", len(dashboard["panels"]))
    print("Datasource UID  :", DATASOURCE_UID)
    print("Measurement     :", MEASUREMENT)
    print("Written         :", OUTPUT_PATH)
    print()
    print("Grafana ledger-health dashboard generation: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
