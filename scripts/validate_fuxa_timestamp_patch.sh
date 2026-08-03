#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${FUXA_CONTAINER_NAME:-topic127-fuxa}"
TARGET_FILE="/usr/src/app/FUXA/server/runtime/devices/opcua/index.js"

if ! docker inspect "${CONTAINER_NAME}" >/dev/null 2>&1; then
    echo "ERROR: FUXA container not found: ${CONTAINER_NAME}"
    exit 1
fi

if docker exec "${CONTAINER_NAME}" \
    grep -F \
    'dataValue.serverTimestamp.toString()' \
    "${TARGET_FILE}" >/dev/null
then
    echo "ERROR: Unsafe serverTimestamp expression remains."
    exit 1
fi

docker exec "${CONTAINER_NAME}" \
    grep -F \
    'dataValue.sourceTimestamp' \
    "${TARGET_FILE}" >/dev/null

docker exec "${CONTAINER_NAME}" \
    grep -F \
    'new Date()).toString()' \
    "${TARGET_FILE}" >/dev/null

echo "FUXA null timestamp patch validation: PASS"
