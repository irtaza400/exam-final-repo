"""Generate a separate FUXA view for simulated-ledger health evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_REPORT_PATH = Path(
    "reports/simulated_ledger_status.json"
)

DEFAULT_VIEW_PATH = Path(
    "fuxa/project/topic127_ledger_health.json"
)

VIEW_ID = "v_topic127_ledger_health"
VIEW_NAME = "Simulated Ledger Health"

NAVY = "#102A43"
BACKGROUND = "#F4F7FA"
WHITE = "#FFFFFF"
BORDER = "#D9E2EC"
TEXT = "#102A43"
MUTED = "#627D98"
GREEN = "#18A558"
AMBER = "#E59B18"
RED = "#D64545"
GREY = "#A0AEC0"


def escape_xml(value: Any) -> str:
    text = str(value)

    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def rect(
    *,
    element_id: str,
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    stroke: str = BORDER,
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


def text_element(
    *,
    element_id: str,
    x: int,
    y: int,
    text: Any,
    size: int,
    fill: str = TEXT,
    weight: int = 400,
) -> str:
    return (
        f'<text id="{element_id}" '
        f'x="{x}" y="{y}" '
        f'font-family="Arial, sans-serif" '
        f'font-size="{size}" '
        f'font-weight="{weight}" '
        f'fill="{fill}" '
        f'text-anchor="start">'
        f'{escape_xml(text)}'
        f'</text>'
    )


def status_color(status: str) -> str:
    if status == "VALID":
        return GREEN

    if status == "TAMPER_DETECTED":
        return RED

    return GREY


def build_view(report: dict[str, Any]) -> dict[str, Any]:
    chain_status = str(
        report.get("chain_status", "UNKNOWN")
    )

    latest = report.get("latest_block", {})
    decisions = report.get("decision_counts", {})
    integrity = report.get("integrity_failure", {})

    block_count = report.get("block_count", 0)
    latest_hash = latest.get(
        "current_hash_short",
        "N/A",
    )

    approved = decisions.get("approved", 0)
    quarantined = decisions.get("quarantined", 0)
    rejected = decisions.get(
        "rejected_or_legal_review",
        0,
    )

    failure_detected = bool(
        integrity.get("detected", False)
    )

    first_failing_record = integrity.get(
        "first_failing_record"
    )

    failure_text = (
        "YES"
        if failure_detected
        else "NO"
    )

    failing_record_text = (
        str(first_failing_record)
        if first_failing_record is not None
        else "N/A"
    )

    svg_parts = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'width="1280" height="720" '
            'viewBox="0 0 1280 720">'
        ),
        rect(
            element_id="BACKGROUND",
            x=0,
            y=0,
            width=1280,
            height=720,
            fill=BACKGROUND,
            stroke=BACKGROUND,
            radius=0,
        ),
        rect(
            element_id="HEADER",
            x=0,
            y=0,
            width=1280,
            height=105,
            fill=NAVY,
            stroke=NAVY,
            radius=0,
        ),
        text_element(
            element_id="TITLE",
            x=55,
            y=48,
            text="Simulated Blockchain Ledger Health",
            size=30,
            fill=WHITE,
            weight=700,
        ),
        text_element(
            element_id="SUBTITLE",
            x=55,
            y=79,
            text=(
                "Supply-chain provenance, QMS decisions "
                "and SHA-256 hash-chain evidence"
            ),
            size=16,
            fill="#D9EAF7",
        ),
        rect(
            element_id="STATE_CARD",
            x=55,
            y=135,
            width=350,
            height=145,
            fill=WHITE,
        ),
        text_element(
            element_id="STATE_LABEL",
            x=85,
            y=177,
            text="LEDGER STATE",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="STATE_VALUE",
            x=85,
            y=235,
            text=chain_status,
            size=30,
            fill=status_color(chain_status),
            weight=700,
        ),
        rect(
            element_id="BLOCK_CARD",
            x=465,
            y=135,
            width=350,
            height=145,
            fill=WHITE,
        ),
        text_element(
            element_id="BLOCK_LABEL",
            x=495,
            y=177,
            text="BLOCK COUNT",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="BLOCK_VALUE",
            x=495,
            y=235,
            text=block_count,
            size=34,
            fill=TEXT,
            weight=700,
        ),
        rect(
            element_id="HASH_CARD",
            x=875,
            y=135,
            width=350,
            height=145,
            fill=WHITE,
        ),
        text_element(
            element_id="HASH_LABEL",
            x=905,
            y=177,
            text="LATEST BLOCK HASH",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="HASH_VALUE",
            x=905,
            y=232,
            text=latest_hash,
            size=20,
            fill=TEXT,
            weight=700,
        ),
        rect(
            element_id="APPROVED_CARD",
            x=55,
            y=315,
            width=350,
            height=145,
            fill=WHITE,
        ),
        text_element(
            element_id="APPROVED_LABEL",
            x=85,
            y=357,
            text="APPROVED FOR USE",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="APPROVED_VALUE",
            x=85,
            y=417,
            text=approved,
            size=34,
            fill=GREEN,
            weight=700,
        ),
        rect(
            element_id="QUARANTINE_CARD",
            x=465,
            y=315,
            width=350,
            height=145,
            fill=WHITE,
        ),
        text_element(
            element_id="QUARANTINE_LABEL",
            x=495,
            y=357,
            text="QUARANTINED",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="QUARANTINE_VALUE",
            x=495,
            y=417,
            text=quarantined,
            size=34,
            fill=AMBER,
            weight=700,
        ),
        rect(
            element_id="REJECTED_CARD",
            x=875,
            y=315,
            width=350,
            height=145,
            fill=WHITE,
        ),
        text_element(
            element_id="REJECTED_LABEL",
            x=905,
            y=357,
            text="REJECTED / LEGAL REVIEW",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="REJECTED_VALUE",
            x=905,
            y=417,
            text=rejected,
            size=34,
            fill=RED,
            weight=700,
        ),
        rect(
            element_id="INTEGRITY_CARD",
            x=55,
            y=495,
            width=1170,
            height=155,
            fill=WHITE,
        ),
        text_element(
            element_id="INTEGRITY_TITLE",
            x=85,
            y=537,
            text="INTEGRITY VERIFICATION",
            size=15,
            fill=MUTED,
            weight=700,
        ),
        text_element(
            element_id="FAILURE_LABEL",
            x=85,
            y=588,
            text="Integrity Failure:",
            size=18,
            fill=TEXT,
            weight=700,
        ),
        text_element(
            element_id="FAILURE_VALUE",
            x=270,
            y=588,
            text=failure_text,
            size=18,
            fill=RED if failure_detected else GREEN,
            weight=700,
        ),
        text_element(
            element_id="RECORD_LABEL",
            x=470,
            y=588,
            text="First Failing Record:",
            size=18,
            fill=TEXT,
            weight=700,
        ),
        text_element(
            element_id="RECORD_VALUE",
            x=675,
            y=588,
            text=failing_record_text,
            size=18,
            fill=RED if failure_detected else TEXT,
            weight=700,
        ),
        text_element(
            element_id="ALGORITHM_LABEL",
            x=875,
            y=588,
            text="Hash Algorithm:",
            size=18,
            fill=TEXT,
            weight=700,
        ),
        text_element(
            element_id="ALGORITHM_VALUE",
            x=1030,
            y=588,
            text=report.get(
                "hash_algorithm",
                "SHA-256",
            ),
            size=18,
            fill=TEXT,
            weight=700,
        ),
        text_element(
            element_id="FOOTER",
            x=55,
            y=690,
            text=(
                "Educational simulated blockchain — "
                "tamper-evident single-node hash chain"
            ),
            size=14,
            fill=MUTED,
        ),
        "</svg>",
    ]

    return {
        "id": VIEW_ID,
        "name": VIEW_NAME,
        "profile": {
            "width": 1280,
            "height": 720,
            "bkcolor": BACKGROUND,
        },
        "items": {},
        "variables": {},
        "svgcontent": "\n".join(svg_parts),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_VIEW_PATH,
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.report.is_file():
        print(
            "ERROR: Ledger status report not found:",
            args.report,
        )
        return 1

    report = json.loads(
        args.report.read_text(encoding="utf-8")
    )

    view = build_view(report)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            view,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print("View ID      :", view["id"])
    print("View name    :", view["name"])
    print(
        "Chain status :",
        report.get("chain_status"),
    )
    print(
        "Block count  :",
        report.get("block_count"),
    )
    print("Written      :", args.output)
    print()
    print("FUXA ledger-health view generation: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
