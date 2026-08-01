FROM frangoteam/fuxa:1.3.3

USER root

COPY fuxa/patches/patch_opcua_null_timestamps.js \
     /tmp/patch_opcua_null_timestamps.js

RUN node /tmp/patch_opcua_null_timestamps.js \
    && rm -f /tmp/patch_opcua_null_timestamps.js

RUN mkdir -p /usr/src/app/FUXA/server/_pkg/runtime \
    && cd /usr/src/app/FUXA/server/_pkg/runtime \
    && printf '%s\n' \
       '{' \
       '  "name": "topic127-fuxa-plugin-runtime",' \
       '  "private": true,' \
       '  "version": "1.0.0",' \
       '  "dependencies": {' \
       '    "node-opcua": "2.149.0"' \
       '  }' \
       '}' \
       > package.json \
    && npm install --omit=dev --no-audit --no-fund \
    && npm cache clean --force \
    && test -f /usr/src/app/FUXA/server/main.js

WORKDIR /usr/src/app/FUXA/server
