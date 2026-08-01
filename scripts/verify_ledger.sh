#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if [[ -f "${REPO_ROOT}/venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${REPO_ROOT}/venv/bin/activate"
fi

python -m src.ledger_verifier
