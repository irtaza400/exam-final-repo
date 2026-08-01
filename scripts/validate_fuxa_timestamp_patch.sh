#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${FUXA_CONTAINER_NAME:-topic127-fuxa}"
TARGET_FILE="/usr/src/app/FUXA/server/runtime/devices/opcua/index.js"

if ! docker inspect "${CONTAINER_NAME}" >/dev/null 2>&1; then
    echo "ERROR: FUXA container not found: ${CONTAINER_NAME}"
    exit 1
fi

docker exec "${CONTAINER_NAME}" sh -c "
    grep -F 'dataValue.serverTimestamp ||' '${TARGET_FILE}' \
      >/dev/null

    grep -F 'dataValue.sourceTimestamp ||' '${TARGET_FILE}' \
      >/dev/null
"

echo "FUXA null timestamp patch validation: PASS"
