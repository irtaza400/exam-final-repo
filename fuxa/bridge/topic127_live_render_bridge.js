"use strict";

(() => {
  const BRIDGE_NAME = "Topic127 FUXA Live Render Bridge";
  const REFRESH_MS = 1000;

  const TAGS = {
    recipe: "t_ae97f8b5-21374127",
    process: "t_b3e17761-82294d16",
    temperature: "t_d8cf674e-e6fb43c2",
    pressure: "t_2e211a43-320c496d",
    etchTime: "t_771e56a1-45d64456",
    machineStatus: "t_85d620ad-7fcc4492",
    securityState: "t_51099579-440048d8",
    machineStatusCode: "t_2d4f07d8-f3d54284",
    securityStateCode: "t_c5ae2336-d2a14ee1",
  };

  const COLORS = {
    green: "#18A558",
    amber: "#E59B18",
    red: "#D64545",
    grey: "#A0AEC0",
  };

  let lastValues = {};

  function setText(groupId, value) {
    const element =
      document.querySelector(`#${groupId} text`) ||
      document.querySelector(`#${groupId}`);

    if (!element) {
      return false;
    }

    element.textContent = String(value);
    return true;
  }

  function setLamp(groupId, color) {
    const element =
      document.querySelector(`#${groupId} ellipse`) ||
      document.querySelector(`#${groupId} circle`);

    if (!element) {
      return false;
    }

    element.setAttribute("fill", color);
    return true;
  }

  function numericColor(value, minimum, maximum) {
    if (!Number.isFinite(value)) {
      return COLORS.grey;
    }

    return value >= minimum && value <= maximum
      ? COLORS.green
      : COLORS.red;
  }

  function machineColor(code) {
    if (Number(code) === 1) {
      return COLORS.green;
    }

    if (Number(code) === 2) {
      return COLORS.amber;
    }

    return COLORS.grey;
  }

  function securityColor(code) {
    if (Number(code) === 1) {
      return COLORS.green;
    }

    if (Number(code) === 2) {
      return COLORS.red;
    }

    return COLORS.grey;
  }

  function updateHmi(values) {
    const temperature = Number(values[TAGS.temperature]);
    const pressure = Number(values[TAGS.pressure]);
    const etchTime = Number(values[TAGS.etchTime]);

    setText(
      "VAL_TOPIC127_RECIPE",
      values[TAGS.recipe] ?? "UNKNOWN"
    );

    setText(
      "VAL_TOPIC127_PROCESS",
      values[TAGS.process] ?? "UNKNOWN"
    );

    if (Number.isFinite(temperature)) {
      setText(
        "VAL_TOPIC127_TEMPERATURE",
        `${temperature.toFixed(2)} °C`
      );
    }

    if (Number.isFinite(pressure)) {
      setText(
        "VAL_TOPIC127_PRESSURE",
        `${pressure.toFixed(2)} bar`
      );
    }

    if (Number.isFinite(etchTime)) {
      setText(
        "VAL_TOPIC127_ETCH_TIME",
        `${Math.round(etchTime)} sec`
      );
    }

    setText(
      "VAL_TOPIC127_MACHINE_STATUS",
      values[TAGS.machineStatus] ?? "UNKNOWN"
    );

    setText(
      "VAL_TOPIC127_SECURITY_STATE",
      values[TAGS.securityState] ?? "UNKNOWN"
    );

    setLamp(
      "GSE_TOPIC127_TEMPERATURE",
      numericColor(temperature, 20, 25)
    );

    setLamp(
      "GSE_TOPIC127_PRESSURE",
      numericColor(pressure, 0.90, 1.10)
    );

    setLamp(
      "GSE_TOPIC127_ETCH_TIME",
      numericColor(etchTime, 55, 65)
    );

    setLamp(
      "GSE_TOPIC127_MACHINE_STATUS",
      machineColor(values[TAGS.machineStatusCode])
    );

    setLamp(
      "GSE_TOPIC127_SECURITY_STATUS",
      securityColor(values[TAGS.securityStateCode])
    );
  }

  async function fetchValues() {
    const ids = Object.values(TAGS);

    const params = new URLSearchParams({
      ids: JSON.stringify(ids),
    });

    const response = await fetch(
      `/api/getTagValue?${params.toString()}`,
      {
        method: "GET",
        cache: "no-store",
      }
    );

    if (!response.ok) {
      throw new Error(
        `FUXA live-tag request failed: HTTP ${response.status}`
      );
    }

    const payload = await response.json();

    if (!Array.isArray(payload)) {
      throw new Error("Unexpected FUXA live-tag payload.");
    }

    const values = {};

    for (const item of payload) {
      if (
        item &&
        typeof item.id === "string" &&
        Object.prototype.hasOwnProperty.call(item, "value")
      ) {
        values[item.id] = item.value;
      }
    }

    lastValues = values;
    updateHmi(values);
  }

  async function refresh() {
    try {
      await fetchValues();
    } catch (error) {
      console.error(`${BRIDGE_NAME}:`, error);
    }
  }

  function start() {
    if (window.__topic127LiveRenderBridgeStarted) {
      return;
    }

    window.__topic127LiveRenderBridgeStarted = true;

    window.topic127LiveRenderBridge = {
      name: BRIDGE_NAME,
      refresh,
      getLastValues: () => ({ ...lastValues }),
    };

    console.info(`${BRIDGE_NAME}: STARTED`);

    refresh();
    window.setInterval(refresh, REFRESH_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      start,
      { once: true }
    );
  } else {
    start();
  }
})();
