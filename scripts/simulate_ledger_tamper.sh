#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

LEDGER="reports/supply_chain_ledger.json"
BACKUP="reports/supply_chain_ledger.before-tamper.json"
TAMPERED_COPY="reports/supply_chain_ledger.tampered.json"
REPORT="reports/ledger_tamper_verification_report.json"

if [[ -f "${REPO_ROOT}/venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${REPO_ROOT}/venv/bin/activate"
fi

if [[ ! -f "${LEDGER}" ]]; then
    echo "ERROR: Ledger does not exist: ${LEDGER}"
    echo "Run: python -m src.supply_chain_ledger"
    exit 1
fi

cp "${LEDGER}" "${BACKUP}"
cp "${LEDGER}" "${TAMPERED_COPY}"

cleanup() {
    if [[ -f "${BACKUP}" ]]; then
        cp "${BACKUP}" "${LEDGER}"
        rm -f "${BACKUP}"
        echo "Original ledger restored."
    fi
}

trap cleanup EXIT

python - <<'PY'
import json
from pathlib import Path

path = Path("reports/supply_chain_ledger.tampered.json")

with path.open("r", encoding="utf-8") as handle:
    chain = json.load(handle)

if not chain:
    raise SystemExit("Ledger has no records to tamper.")

original = chain[0]["material"]
chain[0]["material"] = f"{original} [CONTROLLED-TAMPER]"

with path.open("w", encoding="utf-8", newline="\n") as handle:
    json.dump(chain, handle, indent=2)
    handle.write("\n")

print("Controlled modification applied to first ledger record.")
PY

set +e
python -m src.ledger_verifier \
  --ledger "${TAMPERED_COPY}" \
  --report "${REPORT}"

VERIFY_EXIT=$?
set -e

if [[ "${VERIFY_EXIT}" -eq 2 ]]; then
    echo "PASS: Controlled ledger tampering was detected."
    exit 0
fi

if [[ "${VERIFY_EXIT}" -eq 0 ]]; then
    echo "ERROR: Tampered ledger was incorrectly accepted."
    exit 1
fi

echo "ERROR: Ledger verifier returned unexpected code: ${VERIFY_EXIT}"
exit "${VERIFY_EXIT}"
