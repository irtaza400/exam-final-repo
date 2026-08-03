"""Import or update the Simulated Ledger Health view in FUXA."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_FUXA_URL = "http://127.0.0.1:1881"

DEFAULT_VIEW_PATH = Path(
    "fuxa/project/topic127_ledger_health.json"
)

VIEW_ID = "v_topic127_ledger_health"


def request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> Any:
    data = None
    headers: dict[str, str] = {}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
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

            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {
                    "http_status": response.status,
                    "body": body,
                }

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


def load_view(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(
            f"FUXA ledger-health view not found: {path}"
        )

    view = json.loads(
        path.read_text(encoding="utf-8")
    )

    if view.get("id") != VIEW_ID:
        raise ValueError(
            f"Unexpected view ID: {view.get('id')!r}"
        )

    if not view.get("svgcontent"):
        raise ValueError(
            "Ledger-health view has no SVG content."
        )

    return view


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

    args = parser.parse_args()

    base_url = args.fuxa_url.rstrip("/")
    project_url = f"{base_url}/api/project"
    update_url = f"{base_url}/api/projectData"

    view = load_view(args.view)

    project = request_json(project_url)

    current_views = (
        project.get("hmi", {}).get("views", [])
    )

    existing = [
        item
        for item in current_views
        if item.get("id") == VIEW_ID
    ]

    payload = {
        "cmd": "set-view",
        "data": view,
    }

    response = request_json(
        update_url,
        method="POST",
        payload=payload,
    )

    updated_project = request_json(project_url)

    updated_views = (
        updated_project.get(
            "hmi",
            {},
        ).get(
            "views",
            [],
        )
    )

    view_ids = [
        item.get("id")
        for item in updated_views
    ]

    if VIEW_ID not in view_ids:
        raise RuntimeError(
            "Ledger-health view was not persisted by FUXA."
        )

    operations_count = sum(
        1
        for item in updated_views
        if item.get("id")
        == "v_topic127_operations_overview"
    )

    if operations_count != 1:
        raise RuntimeError(
            "Existing Operations Overview was not preserved."
        )

    ledger_views = [
        item
        for item in updated_views
        if item.get("id") == VIEW_ID
    ]

    if len(ledger_views) != 1:
        raise RuntimeError(
            "Expected exactly one Ledger Health view."
        )

    print(
        "Action          :",
        "UPDATE" if existing else "CREATE",
    )
    print(
        "Imported view   :",
        view["name"],
    )
    print(
        "View ID         :",
        view["id"],
    )
    print(
        "Total views     :",
        len(updated_views),
    )
    print(
        "Operations view :",
        "PRESERVED",
    )
    print(
        "FUXA response   :",
        response,
    )
    print()
    print(
        "FUXA ledger-health view import: PASS"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
