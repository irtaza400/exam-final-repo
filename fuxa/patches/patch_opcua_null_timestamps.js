"use strict";

const fs = require("fs");

const filePath =
  "/usr/src/app/FUXA/server/runtime/devices/opcua/index.js";

const source = fs.readFileSync(filePath, "utf8");

const oldBlock = [
  "data.tags[id].serverTimestamp = " +
    "dataValue.serverTimestamp.toString();",
  "data.tags[id].timestamp = new Date().getTime();",
].join("\n");

const newBlock = [
  "// Topic 127 compatibility patch:",
  "// some educational OPC-UA servers omit serverTimestamp.",
  "const sourceTimestamp =",
  "    dataValue.serverTimestamp ||",
  "    dataValue.sourceTimestamp ||",
  "    new Date();",
  "data.tags[id].serverTimestamp =",
  "    sourceTimestamp.toString();",
  "data.tags[id].timestamp = new Date().getTime();",
].join("\n");

if (!source.includes(oldBlock)) {
  console.error(
    "ERROR: Expected FUXA OPC-UA timestamp block was not found."
  );
  process.exit(1);
}

const patched = source.replace(oldBlock, newBlock);

fs.writeFileSync(filePath, patched, "utf8");

const verification = fs.readFileSync(filePath, "utf8");

if (
  !verification.includes(
    "dataValue.serverTimestamp ||"
  ) ||
  !verification.includes(
    "dataValue.sourceTimestamp ||"
  )
) {
  console.error("ERROR: Timestamp patch verification failed.");
  process.exit(1);
}

console.log(
  "FUXA OPC-UA null timestamp compatibility patch: PASS"
);
