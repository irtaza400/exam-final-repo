"use strict";

const fs = require("fs");

const filePath =
  "/usr/src/app/FUXA/server/runtime/devices/opcua/index.js";

const source = fs.readFileSync(filePath, "utf8");

const unsafeExpression =
  "dataValue.serverTimestamp.toString()";

const safeExpression =
  "(dataValue.serverTimestamp || " +
  "dataValue.sourceTimestamp || " +
  "new Date()).toString()";

const occurrences =
  source.split(unsafeExpression).length - 1;

if (occurrences === 0) {
  console.error(
    "ERROR: Unsafe serverTimestamp expression was not found."
  );
  process.exit(1);
}

const patched = source
  .split(unsafeExpression)
  .join(safeExpression);

fs.writeFileSync(filePath, patched, "utf8");

const verification = fs.readFileSync(filePath, "utf8");

if (verification.includes(unsafeExpression)) {
  console.error(
    "ERROR: Unsafe timestamp expression still exists."
  );
  process.exit(1);
}

if (
  !verification.includes(
    "dataValue.serverTimestamp || " +
    "dataValue.sourceTimestamp || " +
    "new Date()"
  )
) {
  console.error(
    "ERROR: Safe timestamp fallback was not found."
  );
  process.exit(1);
}

console.log(
  "FUXA OPC-UA timestamp expressions patched:",
  occurrences
);

console.log(
  "FUXA OPC-UA null timestamp compatibility patch: PASS"
);
