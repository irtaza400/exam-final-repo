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

COPY fuxa/bridge/topic127_live_render_bridge.js \
     /usr/src/app/FUXA/client/dist/assets/topic127_live_render_bridge.js

RUN grep -q '</body>' /usr/src/app/FUXA/client/dist/index.html \
    && sed -i \
       's#</body>#<script src="/assets/topic127_live_render_bridge.js"></script></body>#' \
       /usr/src/app/FUXA/client/dist/index.html \
    && grep -q 'topic127_live_render_bridge.js' \
       /usr/src/app/FUXA/client/dist/index.html

WORKDIR /usr/src/app/FUXA/server
