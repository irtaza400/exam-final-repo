FROM frangoteam/fuxa:1.3.3

USER root

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
    && npm cache clean --force

WORKDIR /usr/src/app/FUXA
