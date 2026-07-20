import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import paho.mqtt.client as mqtt


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "config" / "edge_gateway.json"

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        return json.load(config_file)


CONFIG = load_config()

GATEWAY_ID = CONFIG["gateway_id"]
INPUT_TOPIC = os.getenv("MQTT_RAW_TOPIC", CONFIG["input_topic"])
OUTPUT_TOPIC = os.getenv("MQTT_VALIDATED_TOPIC", CONFIG["output_topic"])
REJECTED_TOPIC = os.getenv("MQTT_REJECTED_TOPIC", CONFIG["rejected_topic"])
STATUS_TOPIC = os.getenv("MQTT_STATUS_TOPIC", CONFIG["status_topic"])
REQUIRED_FIELDS = CONFIG["required_fields"]
VALIDATION_RANGES = CONFIG["validation_ranges"]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing_fields = [
        field for field in REQUIRED_FIELDS if field not in payload
    ]

    if missing_fields:
        errors.append(
            "Missing required fields: " + ", ".join(missing_fields)
        )

    if errors:
        return errors

    expected_string_fields = [
        "timestamp",
        "machine_id",
        "zone",
        "process",
        "event_status",
    ]

    for field in expected_string_fields:
        if not isinstance(payload[field], str) or not payload[field].strip():
            errors.append(f"{field} must be a non-empty string")

    if payload["event_status"] not in {"normal", "abnormal"}:
        errors.append(
            "event_status must be either 'normal' or 'abnormal'"
        )

    numeric_fields = [
        "particle_count",
        "temperature",
        "humidity",
        "airflow",
        "gas_ppm",
    ]

    for field in numeric_fields:
        value = payload[field]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field} must be numeric")
            continue

        limits = VALIDATION_RANGES[field]
        minimum = limits["min"]
        maximum = limits["max"]

        if not minimum <= value <= maximum:
            errors.append(
                f"{field} must be between {minimum} and {maximum}"
            )

    if not isinstance(payload["ppe_compliant"], bool):
        errors.append("ppe_compliant must be true or false")

    return errors


def enrich_payload(payload: dict[str, Any]) -> dict[str, Any]:
    enriched_payload = dict(payload)

    enriched_payload.update(
        {
            "gateway_id": GATEWAY_ID,
            "gateway_received_at": utc_timestamp(),
            "schema_valid": True,
            "data_quality": "valid",
        }
    )

    return enriched_payload


def publish_json(
    client: mqtt.Client,
    topic: str,
    payload: dict[str, Any],
) -> None:
    result = client.publish(topic, json.dumps(payload))

    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(
            f"WARNING: Failed to publish to {topic}. "
            f"MQTT result code: {result.rc}",
            flush=True,
        )


def reject_message(
    client: mqtt.Client,
    reason: str,
    original_payload: Any,
) -> None:
    rejection = {
        "gateway_id": GATEWAY_ID,
        "rejected_at": utc_timestamp(),
        "reason": reason,
        "original_payload": original_payload,
    }

    publish_json(client, REJECTED_TOPIC, rejection)
    print(f"REJECTED: {reason}", flush=True)


def on_connect(
    client: mqtt.Client,
    userdata: Any,
    flags: mqtt.ConnectFlags,
    reason_code: mqtt.ReasonCode,
    properties: mqtt.Properties | None,
) -> None:
    print(
        f"Connected to MQTT broker with reason code: {reason_code}",
        flush=True,
    )

    client.subscribe(INPUT_TOPIC)

    status = {
        "gateway_id": GATEWAY_ID,
        "status": "online",
        "timestamp": utc_timestamp(),
        "input_topic": INPUT_TOPIC,
        "output_topic": OUTPUT_TOPIC,
    }

    publish_json(client, STATUS_TOPIC, status)

    print(f"Subscribed to raw topic: {INPUT_TOPIC}", flush=True)


def on_message(
    client: mqtt.Client,
    userdata: Any,
    message: mqtt.MQTTMessage,
) -> None:
    processing_started = time.perf_counter()

    try:
        decoded_payload = message.payload.decode("utf-8")
        payload = json.loads(decoded_payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        reject_message(
            client,
            f"Invalid JSON payload: {error}",
            message.payload.decode("utf-8", errors="replace"),
        )
        return

    if not isinstance(payload, dict):
        reject_message(
            client,
            "MQTT payload must be a JSON object",
            payload,
        )
        return

    validation_errors = validate_payload(payload)

    if validation_errors:
        reject_message(
            client,
            "; ".join(validation_errors),
            payload,
        )
        return

    enriched_payload = enrich_payload(payload)

    processing_latency_ms = round(
        (time.perf_counter() - processing_started) * 1000,
        3,
    )

    enriched_payload["processing_latency_ms"] = processing_latency_ms

    publish_json(client, OUTPUT_TOPIC, enriched_payload)

    print(
        "VALIDATED: "
        f"{payload['machine_id']} -> {OUTPUT_TOPIC} "
        f"({processing_latency_ms} ms)",
        flush=True,
    )


def main() -> None:
    print("Topic 127 Edge Gateway starting.")
    print(f"Gateway ID     : {GATEWAY_ID}")
    print(f"MQTT broker    : {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Raw input      : {INPUT_TOPIC}")
    print(f"Validated output: {OUTPUT_TOPIC}")
    print(f"Rejected output : {REJECTED_TOPIC}")
    print(f"Status topic    : {STATUS_TOPIC}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nEdge Gateway stopped by user.")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
