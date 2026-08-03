#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"
REPO_ROOT="$(
    cd "${SCRIPT_DIR}/.."
    pwd
)"

PCAP_FILE="${SURICATA_PCAP_FILE:-${REPO_ROOT}/suricata/pcaps/topic127_industrial_ids_test.pcap}"
RULE_FILE="${SURICATA_RULE_FILE:-${REPO_ROOT}/suricata/rules/topic127.rules}"
LOG_DIR="${SURICATA_LOG_DIR:-${REPO_ROOT}/suricata/logs}"

cd "${REPO_ROOT}"

echo "============================================================"
echo "Nanomanufacturing — Suricata IDS Demonstration"
echo "============================================================"
echo "Timestamp : $(date -u --iso-8601=seconds)"
echo "PCAP      : ${PCAP_FILE}"
echo "Rules     : ${RULE_FILE}"
echo "Logs      : ${LOG_DIR}"
echo

if [[ ! -f "${PCAP_FILE}" ]]; then
    echo "Generating deterministic Suricata test PCAP..."
    python scripts/generate_suricata_test_pcap.py
fi

if [[ ! -s "${PCAP_FILE}" ]]; then
    echo "ERROR: Suricata test PCAP is missing or empty."
    exit 1
fi

if [[ ! -s "${RULE_FILE}" ]]; then
    echo "ERROR: Suricata custom rule file is missing or empty."
    exit 1
fi

mkdir -p "${LOG_DIR}"

rm -f \
    "${LOG_DIR}/eve.json" \
    "${LOG_DIR}/fast.log" \
    "${LOG_DIR}/stats.log" \
    "${LOG_DIR}/suricata.log"

echo "Pulling/verifying Suricata image..."
docker compose \
    --profile security-demo \
    pull suricata

echo
echo "Suricata version:"
docker compose \
    --profile security-demo \
    run --rm \
    --entrypoint suricata \
    suricata \
    -V

echo
echo "Testing custom rules and configuration..."
docker compose \
    --profile security-demo \
    run --rm \
    --entrypoint suricata \
    suricata \
    -T \
    -S /rules/topic127.rules

echo
echo "Processing controlled industrial-security PCAP..."
docker compose \
    --profile security-demo \
    run --rm \
    suricata

echo
echo "Generated Suricata files:"
ls -lh "${LOG_DIR}"

if [[ ! -s "${LOG_DIR}/eve.json" ]]; then
    echo "ERROR: Suricata did not generate eve.json."
    exit 1
fi

echo
echo "Suricata IDS PCAP processing: PASS"
