"""Align generated Topic 127 SVG widgets with native FUXA structure."""

from __future__ import annotations

import json
import re
from pathlib import Path


VIEW_PATH = Path(
    "fuxa/project/topic127_operations_overview.json"
)


def patch_value_group(svg: str, group_id: str) -> str:
    pattern = re.compile(
        rf'(<g\b[^>]*id="{re.escape(group_id)}"'
        rf'[^>]*type="svg-ext-value"[^>]*>)'
        rf'([\s\S]*?)'
        rf'(</g>)'
    )

    match = pattern.search(svg)

    if not match:
        raise RuntimeError(
            f"Value SVG group not found: {group_id}"
        )

    opening = match.group(1)
    body = match.group(2)
    closing = match.group(3)

    native_child_id = group_id.replace(
        "VAL_TOPIC127_",
        "VAL_CHILD_TOPIC127_",
        1,
    )

    body, replacements = re.subn(
        r'<text\b([^>]*)\bid="[^"]+"([^>]*)>',
        (
            f'<text id="{native_child_id}"'
            r'\1\2 xml:space="preserve">'
        ),
        body,
        count=1,
    )

    if replacements != 1:
        raise RuntimeError(
            f"Value child text not patched: {group_id}"
        )

    # Native FUXA value widgets use plain placeholders.
    body = re.sub(
        r'>##\.##\s*°C</text>',
        '>##.##</text>',
        body,
        count=1,
    )
    body = re.sub(
        r'>#\.##\s*bar</text>',
        '>##.##</text>',
        body,
        count=1,
    )
    body = re.sub(
        r'>##\s*sec</text>',
        '>##.##</text>',
        body,
        count=1,
    )

    replacement = opening + body + closing

    return (
        svg[:match.start()]
        + replacement
        + svg[match.end():]
    )


def patch_semaphore_group(
    svg: str,
    group_id: str,
) -> str:
    pattern = re.compile(
        rf'(<g\b[^>]*id="{re.escape(group_id)}"'
        rf'[^>]*type="svg-ext-gauge_semaphore"[^>]*>)'
        rf'([\s\S]*?)'
        rf'(</g>)'
    )

    match = pattern.search(svg)

    if not match:
        raise RuntimeError(
            f"Semaphore SVG group not found: {group_id}"
        )

    opening = match.group(1)
    body = match.group(2)
    closing = match.group(3)

    if 'font-size=' not in opening:
        opening = opening[:-1] + ' font-size="14">'

    native_child_id = group_id.replace(
        "GSE_TOPIC127_",
        "GSE_CHILD_TOPIC127_",
        1,
    )

    body, replacements = re.subn(
        r'<ellipse\b([^>]*)\bid="[^"]+"([^>]*)>',
        f'<ellipse id="{native_child_id}"' r'\1\2>',
        body,
        count=1,
    )

    if replacements != 1:
        raise RuntimeError(
            f"Semaphore ellipse not patched: {group_id}"
        )

    replacement = opening + body + closing

    return (
        svg[:match.start()]
        + replacement
        + svg[match.end():]
    )


def main() -> None:
    view = json.loads(
        VIEW_PATH.read_text(encoding="utf-8")
    )

    svg = view["svgcontent"]

    value_ids = [
        item_id
        for item_id, item in view["items"].items()
        if item["type"] == "svg-ext-value"
    ]

    semaphore_ids = [
        item_id
        for item_id, item in view["items"].items()
        if item["type"] == "svg-ext-gauge_semaphore"
    ]

    if len(value_ids) != 7:
        raise RuntimeError(
            f"Expected 7 value widgets, found {len(value_ids)}"
        )

    if len(semaphore_ids) != 5:
        raise RuntimeError(
            "Expected 5 semaphore widgets, "
            f"found {len(semaphore_ids)}"
        )

    for group_id in value_ids:
        svg = patch_value_group(svg, group_id)

    for group_id in semaphore_ids:
        svg = patch_semaphore_group(svg, group_id)

    view["svgcontent"] = svg

    for group_id in value_ids:
        child_id = group_id.replace(
            "VAL_TOPIC127_",
            "VAL_CHILD_TOPIC127_",
            1,
        )

        if f'id="{child_id}"' not in svg:
            raise RuntimeError(
                f"Missing native value child: {child_id}"
            )

    for group_id in semaphore_ids:
        child_id = group_id.replace(
            "GSE_TOPIC127_",
            "GSE_CHILD_TOPIC127_",
            1,
        )

        if f'id="{child_id}"' not in svg:
            raise RuntimeError(
                f"Missing native semaphore child: {child_id}"
            )

    VIEW_PATH.write_text(
        json.dumps(view, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Value widget groups :", len(value_ids))
    print("Semaphore groups    :", len(semaphore_ids))
    print("Updated             :", VIEW_PATH)
    print("FUXA native widget compatibility patch: PASS")


if __name__ == "__main__":
    main()
