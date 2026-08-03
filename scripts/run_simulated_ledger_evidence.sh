#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

cd "${REPO_ROOT}"

LEDGER="reports/supply_chain_ledger.json"
TAMPERED_LEDGER="reports/supply_chain_ledger.tampered-evidence.json"

VALID_JSON="reports/simulated_ledger_status.json"
VALID_TEXT="reports/simulated_ledger_status.txt"

TAMPER_JSON="reports/simulated_ledger_tamper_status.json"
TAMPER_TEXT="reports/simulated_ledger_tamper_status.txt"

RESTORED_JSON="reports/simulated_ledger_restored_status.json"
RESTORED_TEXT="reports/simulated_ledger_restored_status.txt"

echo "============================================================"
echo "Simulated Blockchain Ledger — Evidence Workflow"
echo "============================================================"
echo "Timestamp: $(date -u --iso-8601=seconds)"
echo

if [[ ! -f "${LEDGER}" ]]; then
    echo "Ledger not found. Generating supply-chain ledger..."
    python -m src.supply_chain_ledger
fi

echo "=== Valid chain status ==="
python -m src.simulated_ledger_status \
    --ledger "${LEDGER}" \
    --json-report "${VALID_JSON}" \
    --text-report "${VALID_TEXT}"

cp "${LEDGER}" "${TAMPERED_LEDGER}"

python - <<'PY'
import json
from pathlib import Path

path = Path(
    "reports/supply_chain_ledger.tampered-evidence.json"
)

chain = json.loads(
    path.read_text(encoding="utf-8")
)

if not chain:
    raise SystemExit(
        "Ledger contains no records."
    )

original = chain[0]["material"]
chain[0]["material"] = (
    f"{original} [CONTROLLED-TAMPER-EVIDENCE]"
)

path.write_text(
    json.dumps(
        chain,
        indent=2,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)

print(
    "Controlled tamper applied to:",
    path,
)
PY

echo
echo "=== Tampered chain status ==="

set +e
python -m src.simulated_ledger_status \
    --ledger "${TAMPERED_LEDGER}" \
    --json-report "${TAMPER_JSON}" \
    --text-report "${TAMPER_TEXT}"
TAMPER_EXIT_CODE=$?
set -e

if [[ "${TAMPER_EXIT_CODE}" -ne 2 ]]; then
    echo "ERROR: Expected tampered-ledger exit code 2."
    echo "Actual exit code: ${TAMPER_EXIT_CODE}"
    exit 1
fi

echo
echo "Tampered ledger detection: PASS"

rm -f "${TAMPERED_LEDGER}"

echo
echo "=== Restored chain status ==="
python -m src.simulated_ledger_status \
    --ledger "${LEDGER}" \
    --json-report "${RESTORED_JSON}" \
    --text-report "${RESTORED_TEXT}"

python - <<'PY'
import json
from pathlib import Path

valid = json.loads(
    Path(
        "reports/simulated_ledger_status.json"
    ).read_text(encoding="utf-8")
)

tampered = json.loads(
    Path(
        "reports/simulated_ledger_tamper_status.json"
    ).read_text(encoding="utf-8")
)

restored = json.loads(
    Path(
        "reports/simulated_ledger_restored_status.json"
    ).read_text(encoding="utf-8")
)

assert valid["chain_status"] == "VALID"
assert valid["ledger_valid"] is True

assert tampered["chain_status"] == "TAMPER_DETECTED"
assert tampered["ledger_valid"] is False
assert tampered["chain_errors"]

assert restored["chain_status"] == "VALID"
assert restored["ledger_valid"] is True

assert (
    valid["latest_block"]["current_hash"]
    == restored["latest_block"]["current_hash"]
)

print("Before state  :", valid["chain_status"])
print("Tamper state  :", tampered["chain_status"])
print("Restored state:", restored["chain_status"])
print()
print("Simulated blockchain evidence workflow: PASS")
PY
