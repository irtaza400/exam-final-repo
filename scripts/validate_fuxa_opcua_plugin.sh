#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="${FUXA_CONTAINER_NAME:-topic127-fuxa}"
EXPECTED_VERSION="${FUXA_OPCUA_VERSION:-2.149.0}"

if ! docker inspect "${CONTAINER_NAME}" >/dev/null 2>&1; then
    echo "ERROR: Container not found: ${CONTAINER_NAME}"
    exit 1
fi

ACTUAL_VERSION="$(
    docker exec "${CONTAINER_NAME}" sh -c '
      cd /usr/src/app/FUXA/server/_pkg/runtime
      node -e "
        process.stdout.write(
          require(\"node-opcua/package.json\").version
        )
      "
    '
)"

echo "Expected node-opcua version: ${EXPECTED_VERSION}"
echo "Actual node-opcua version  : ${ACTUAL_VERSION}"

if [[ "${ACTUAL_VERSION}" != "${EXPECTED_VERSION}" ]]; then
    echo "ERROR: node-opcua version validation failed."
    exit 1
fi

echo "FUXA node-opcua plugin validation: PASS"
