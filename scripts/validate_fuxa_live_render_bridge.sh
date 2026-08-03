#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${FUXA_CONTAINER_NAME:-topic127-fuxa}"

BRIDGE_FILE="/usr/src/app/FUXA/client/dist/assets/topic127_live_render_bridge.js"
INDEX_FILE="/usr/src/app/FUXA/client/dist/index.html"

if ! docker inspect "${CONTAINER_NAME}" >/dev/null 2>&1; then
    echo "ERROR: FUXA container not found: ${CONTAINER_NAME}"
    exit 1
fi

docker exec "${CONTAINER_NAME}" \
    test -s "${BRIDGE_FILE}"

docker exec "${CONTAINER_NAME}" \
    grep -F \
    'topic127_live_render_bridge.js' \
    "${INDEX_FILE}" >/dev/null

docker exec "${CONTAINER_NAME}" \
    grep -F \
    '/api/getTagValue' \
    "${BRIDGE_FILE}" >/dev/null

docker exec "${CONTAINER_NAME}" \
    grep -F \
    'VAL_TOPIC127_TEMPERATURE' \
    "${BRIDGE_FILE}" >/dev/null

echo "FUXA live-render bridge installation: PASS"
