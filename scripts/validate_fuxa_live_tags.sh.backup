#!/usr/bin/env bash
set -euo pipefail

FUXA_URL="${FUXA_URL:-http://127.0.0.1:1881}"
REPORT_DIR="${REPORT_DIR:-reports}"
OUTPUT_FILE="${REPORT_DIR}/fuxa_live_tags_validation.json"

mkdir -p "${REPORT_DIR}"

TAG_IDS='[
  "ns=2;i=2",
  "ns=2;i=3",
  "ns=2;i=4",
  "ns=2;i=5",
  "ns=2;i=6",
  "ns=2;i=7",
  "ns=2;i=8"
]'

echo "Requesting seven live OPC-UA values from FUXA..."

HTTP_CODE="$(
    curl -sS \
      --get \
      --data-urlencode "ids=${TAG_IDS}" \
      --output "${OUTPUT_FILE}" \
      --write-out '%{http_code}' \
      "${FUXA_URL}/api/getTagValue"
)"

echo "FUXA HTTP status: ${HTTP_CODE}"

if [[ "${HTTP_CODE}" != "200" ]]; then
    echo "ERROR: FUXA live-tag endpoint returned HTTP ${HTTP_CODE}."
    cat "${OUTPUT_FILE}" 2>/dev/null || true
    exit 1
fi

python - "${OUTPUT_FILE}" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
values = json.loads(path.read_text(encoding="utf-8"))

expected = {
    "ns=2;i=2": "RecipeID",
    "ns=2;i=3": "ProcessName",
    "ns=2;i=4": "TemperatureSetpoint",
    "ns=2;i=5": "PressureSetpoint",
    "ns=2;i=6": "EtchTimeSeconds",
    "ns=2;i=7": "MachineStatus",
    "ns=2;i=8": "SecurityState",
}

if not isinstance(values, list):
    raise SystemExit(
        "ERROR: FUXA response is not a JSON array."
    )

received = {
    item.get("id"): item
    for item in values
    if isinstance(item, dict)
}

errors = []

for tag_id, name in expected.items():
    item = received.get(tag_id)

    if item is None:
        errors.append(f"{name}: missing tag {tag_id}")
        continue

    value = item.get("value")
    timestamp = item.get("ts")

    if value is None:
        errors.append(f"{name}: null value")

    if not isinstance(timestamp, int) or timestamp <= 0:
        errors.append(f"{name}: invalid timestamp {timestamp!r}")

    print(
        f"{name:<24} "
        f"id={tag_id:<10} "
        f"value={value!r:<20} "
        f"timestamp={timestamp}"
    )

if len(received) != len(expected):
    errors.append(
        f"Expected 7 values, received {len(received)}"
    )

if errors:
    print()
    print("FUXA live-tag validation errors:")

    for error in errors:
        print(f"  - {error}")

    raise SystemExit(1)

print()
print("FUXA seven live OPC-UA tags: PASS")
PY
