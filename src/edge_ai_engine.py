#!/usr/bin/env python3
"""
Custom explainable Edge AI engine for the Topic 127 educational lab.

The engine consumes validated Edge Gateway telemetry, calculates a
weighted environmental and safety risk score, classifies each event,
and publishes inference results and alerts through MQTT.

Classification:
    normal
    warning
    critical

This implementation is custom rule-based inference. It is executable
Edge AI logic, but it is not represented as a trained ML model.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None


LOGGER = logging.getLogger("edge_ai_engine")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "edge_ai.json"


class ConfigurationError(ValueError):
    """Raised when the Edge AI configuration is missing or invalid."""


def load_config(path: Path) -> dict[str, Any]:
    """Load and validate the Edge AI JSON configuration."""

    if not path.is_file():
        raise ConfigurationError(f"Configuration file not found: {path}")

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigurationError(
            f"Invalid JSON in configuration file {path}: {exc}"
        ) from exc

    required_sections = {
        "engine",
        "mqtt",
        "thresholds",
        "risk",
    }

    missing_sections = sorted(required_sections - config.keys())

    if missing_sections:
        raise ConfigurationError(
            "Missing configuration section(s): "
            + ", ".join(missing_sections)
        )

    required_metrics = {
        "particle_count",
        "temperature",
        "humidity",
        "airflow",
        "gas_ppm",
        "ppe_compliant",
    }

    missing_metrics = sorted(
        required_metrics - config["thresholds"].keys()
    )

    if missing_metrics:
        raise ConfigurationError(
            "Missing threshold configuration(s): "
            + ", ".join(missing_metrics)
        )

    warning_score = float(config["risk"]["warning_score"])
    critical_score = float(config["risk"]["critical_score"])

    if not 0 <= warning_score < critical_score <= 1:
        raise ConfigurationError(
            "Risk thresholds must satisfy "
            "0 <= warning_score < critical_score <= 1."
        )

    return config


def read_number(
    telemetry: dict[str, Any],
    field_name: str,
) -> float | None:
    """Return a numeric telemetry field or None if missing/invalid."""

    value = telemetry.get(field_name)

    if value is None or isinstance(value, bool):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def score_high_value(
    value: float,
    warning: float,
    critical: float,
) -> tuple[float, str]:
    """Score a field where higher values represent greater risk."""

    if value >= critical:
        return 1.0, "critical"

    if value >= warning:
        span = max(critical - warning, 0.000001)
        position = (value - warning) / span
        return 0.5 + (0.5 * position), "warning"

    return 0.0, "normal"


def score_low_value(
    value: float,
    critical_low: float,
    warning_low: float,
) -> tuple[float, str]:
    """Score a field where lower values represent greater risk."""

    if value <= critical_low:
        return 1.0, "critical"

    if value <= warning_low:
        span = max(warning_low - critical_low, 0.000001)
        position = (warning_low - value) / span
        return 0.5 + (0.5 * position), "warning"

    return 0.0, "normal"


def parse_boolean(value: Any) -> bool:
    """Convert common boolean forms to a Python boolean."""

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in {"true", "yes", "1", "compliant"}:
            return True

        if normalized in {"false", "no", "0", "non-compliant"}:
            return False

    if isinstance(value, (int, float)):
        return bool(value)

    raise ValueError(f"Unsupported boolean value: {value!r}")


def analyse_telemetry(
    telemetry: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate one validated telemetry event."""

    if not isinstance(telemetry, dict):
        raise ValueError("Telemetry payload must be a JSON object.")

    thresholds = config["thresholds"]

    explanations: list[dict[str, Any]] = []
    total_weighted_score = 0.0
    total_active_weight = 0.0

    def add_result(
        *,
        metric: str,
        value: Any,
        score: float,
        status: str,
        weight: float,
        message: str,
    ) -> None:
        nonlocal total_weighted_score, total_active_weight

        total_weighted_score += score * weight
        total_active_weight += weight

        explanations.append(
            {
                "metric": metric,
                "value": value,
                "status": status,
                "score": round(score, 4),
                "weight": weight,
                "message": message,
            }
        )

    particle_count = read_number(telemetry, "particle_count")

    if particle_count is not None:
        rule = thresholds["particle_count"]
        score, status = score_high_value(
            particle_count,
            float(rule["warning"]),
            float(rule["critical"]),
        )

        add_result(
            metric="particle_count",
            value=particle_count,
            score=score,
            status=status,
            weight=float(rule["weight"]),
            message="Particle contamination risk evaluated.",
        )

    temperature = read_number(telemetry, "temperature")

    if temperature is not None:
        rule = thresholds["temperature"]

        if temperature < float(rule["minimum"]):
            score = 0.75
            status = "warning"
        else:
            score, status = score_high_value(
                temperature,
                float(rule["warning_high"]),
                float(rule["critical_high"]),
            )

        add_result(
            metric="temperature",
            value=temperature,
            score=score,
            status=status,
            weight=float(rule["weight"]),
            message="Cleanroom temperature risk evaluated.",
        )

    humidity = read_number(telemetry, "humidity")

    if humidity is not None:
        rule = thresholds["humidity"]

        if humidity < float(rule["minimum"]):
            score = 0.75
            status = "warning"
        else:
            score, status = score_high_value(
                humidity,
                float(rule["warning_high"]),
                float(rule["critical_high"]),
            )

        add_result(
            metric="humidity",
            value=humidity,
            score=score,
            status=status,
            weight=float(rule["weight"]),
            message="Cleanroom humidity risk evaluated.",
        )

    airflow = read_number(telemetry, "airflow")

    if airflow is not None:
        rule = thresholds["airflow"]
        score, status = score_low_value(
            airflow,
            float(rule["critical_low"]),
            float(rule["warning_low"]),
        )

        add_result(
            metric="airflow",
            value=airflow,
            score=score,
            status=status,
            weight=float(rule["weight"]),
            message="Airflow degradation risk evaluated.",
        )

    gas_ppm = read_number(telemetry, "gas_ppm")

    if gas_ppm is not None:
        rule = thresholds["gas_ppm"]
        score, status = score_high_value(
            gas_ppm,
            float(rule["warning"]),
            float(rule["critical"]),
        )

        add_result(
            metric="gas_ppm",
            value=gas_ppm,
            score=score,
            status=status,
            weight=float(rule["weight"]),
            message="Worker gas-exposure risk evaluated.",
        )

    if "ppe_compliant" in telemetry:
        rule = thresholds["ppe_compliant"]
        ppe_compliant = parse_boolean(telemetry["ppe_compliant"])

        score = 0.0 if ppe_compliant else 1.0
        status = "normal" if ppe_compliant else "critical"

        add_result(
            metric="ppe_compliant",
            value=ppe_compliant,
            score=score,
            status=status,
            weight=float(rule["weight"]),
            message="PPE compliance evaluated.",
        )

    if total_active_weight == 0:
        raise ValueError(
            "No supported telemetry fields were found in the payload."
        )

    risk_score = min(
        max(total_weighted_score / total_active_weight, 0.0),
        1.0,
    )

    warning_threshold = float(config["risk"]["warning_score"])
    critical_threshold = float(config["risk"]["critical_score"])

    has_critical_metric = any(
        item["status"] == "critical"
        for item in explanations
    )

    if risk_score >= critical_threshold or has_critical_metric:
        severity = "critical"
    elif risk_score >= warning_threshold:
        severity = "warning"
    else:
        severity = "normal"

    abnormal_metrics = [
        item["metric"]
        for item in explanations
        if item["status"] != "normal"
    ]

    recommendations: list[str] = []

    if "particle_count" in abnormal_metrics:
        recommendations.append(
            "Inspect contamination sources and filtration controls."
        )

    if "airflow" in abnormal_metrics:
        recommendations.append(
            "Inspect airflow, pressure control, and ventilation."
        )

    if "gas_ppm" in abnormal_metrics:
        recommendations.append(
            "Initiate EHS gas-safety verification."
        )

    if "ppe_compliant" in abnormal_metrics:
        recommendations.append(
            "Suspend unsafe work until PPE compliance is restored."
        )

    if (
        "temperature" in abnormal_metrics
        or "humidity" in abnormal_metrics
    ):
        recommendations.append(
            "Verify environmental control and process conditions."
        )

    if not recommendations:
        recommendations.append("Continue normal monitoring.")

    machine_id = (
        telemetry.get("machine_id")
        or telemetry.get("device_id")
        or telemetry.get("sensor_id")
        or "unknown"
    )

    source_timestamp = (
        telemetry.get("timestamp")
        or telemetry.get("event_timestamp")
        or telemetry.get("time")
    )

    return {
        "engine": config["engine"]["name"],
        "engine_version": config["engine"]["version"],
        "engine_mode": config["engine"]["mode"],
        "inference_timestamp": int(time.time()),
        "source_timestamp": source_timestamp,
        "machine_id": machine_id,
        "zone": telemetry.get("zone"),
        "process": telemetry.get("process"),
        "source_event_status": telemetry.get("event_status"),
        "risk_score": round(risk_score, 4),
        "severity": severity,
        "anomaly_detected": severity != "normal",
        "abnormal_metrics": abnormal_metrics,
        "recommendations": recommendations,
        "explanations": explanations,
        "source_telemetry": telemetry,
    }


def create_mqtt_client(client_id: str) -> Any:
    """Create a Paho MQTT client compatible with v1 and v2."""

    if mqtt is None:
        raise RuntimeError(
            "paho-mqtt is not installed. Install project dependencies "
            "before starting MQTT mode."
        )

    try:
        return mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
        )
    except AttributeError:
        return mqtt.Client(client_id=client_id)


class EdgeAIService:
    """MQTT runtime wrapper for the Edge AI engine."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        mqtt_config = config["mqtt"]

        self.host = os.getenv(
            "MQTT_BROKER",
            os.getenv(
                "MQTT_HOST",
                str(mqtt_config["host"]),
            ),
        )

        self.port = int(
            os.getenv(
                "MQTT_PORT",
                str(mqtt_config["port"]),
            )
        )

        self.keepalive = int(mqtt_config["keepalive"])

        self.input_topic = os.getenv(
            "EDGE_AI_INPUT_TOPIC",
            str(mqtt_config["input_topic"]),
        )

        self.result_topic = os.getenv(
            "EDGE_AI_RESULT_TOPIC",
            str(mqtt_config["result_topic"]),
        )

        self.alert_topic = os.getenv(
            "EDGE_AI_ALERT_TOPIC",
            str(mqtt_config["alert_topic"]),
        )

        self.qos = int(
            os.getenv(
                "EDGE_AI_QOS",
                str(mqtt_config["qos"]),
            )
        )

        client_id = os.getenv(
            "EDGE_AI_CLIENT_ID",
            str(mqtt_config["client_id"]),
        )

        self.client = create_mqtt_client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        username = os.getenv("MQTT_USERNAME")
        password = os.getenv("MQTT_PASSWORD")

        if username:
            self.client.username_pw_set(username, password)

    def on_connect(
        self,
        client: Any,
        userdata: Any,
        flags: Any,
        reason_code: Any,
        properties: Any = None,
    ) -> None:
        del userdata, flags, properties

        if reason_code.is_failure:
            LOGGER.error(
                "MQTT connection failed with reason code %s.",
                reason_code,
            )
            return

        client.subscribe(self.input_topic, qos=self.qos)

        LOGGER.info(
            "Connected to MQTT broker %s:%s.",
            self.host,
            self.port,
        )

        LOGGER.info(
            "Subscribed to validated telemetry topic: %s",
            self.input_topic,
        )

    def on_disconnect(
        self,
        client: Any,
        userdata: Any,
        flags: Any,
        reason_code: Any = None,
        properties: Any = None,
    ) -> None:
        del client, userdata, flags, properties

        LOGGER.warning(
            "Disconnected from MQTT broker: %s",
            reason_code,
        )

    def on_message(
        self,
        client: Any,
        userdata: Any,
        message: Any,
    ) -> None:
        del userdata

        try:
            payload_text = message.payload.decode("utf-8")
            telemetry = json.loads(payload_text)

            result = analyse_telemetry(
                telemetry,
                self.config,
            )

            encoded_result = json.dumps(
                result,
                separators=(",", ":"),
            )

            publish_result = client.publish(
                self.result_topic,
                encoded_result,
                qos=self.qos,
            )

            if publish_result.rc != mqtt.MQTT_ERR_SUCCESS:
                LOGGER.error(
                    "Failed to publish Edge AI result. MQTT code: %s",
                    publish_result.rc,
                )

            if result["anomaly_detected"]:
                alert_result = client.publish(
                    self.alert_topic,
                    encoded_result,
                    qos=self.qos,
                )

                if alert_result.rc != mqtt.MQTT_ERR_SUCCESS:
                    LOGGER.error(
                        "Failed to publish Edge AI alert. MQTT code: %s",
                        alert_result.rc,
                    )

            LOGGER.info(
                "Inference machine=%s severity=%s risk_score=%.4f",
                result["machine_id"],
                result["severity"],
                result["risk_score"],
            )

        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ) as exc:
            LOGGER.error(
                "Rejected telemetry on topic %s: %s",
                message.topic,
                exc,
            )
        except Exception:
            LOGGER.exception(
                "Unexpected Edge AI processing error."
            )

    def stop(
        self,
        signum: int,
        frame: Any,
    ) -> None:
        del frame

        LOGGER.info(
            "Received signal %s; stopping Edge AI engine.",
            signum,
        )

        self.client.disconnect()

    def run(self) -> None:
        """Connect to MQTT and run until interrupted."""

        signal.signal(signal.SIGINT, self.stop)

        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, self.stop)

        LOGGER.info(
            "Starting Edge AI engine in %s mode.",
            self.config["engine"]["mode"],
        )

        LOGGER.info(
            "MQTT broker: %s:%s",
            self.host,
            self.port,
        )

        LOGGER.info(
            "Input topic: %s",
            self.input_topic,
        )

        LOGGER.info(
            "Result topic: %s",
            self.result_topic,
        )

        LOGGER.info(
            "Alert topic: %s",
            self.alert_topic,
        )

        self.client.connect(
            self.host,
            self.port,
            self.keepalive,
        )

        self.client.loop_forever()


def run_self_test(config: dict[str, Any]) -> int:
    """Run local deterministic inference tests without MQTT."""

    cases = [
        {
            "name": "normal",
            "payload": {
                "timestamp": "2026-07-20T10:00:00Z",
                "machine_id": "nano-tool-01",
                "zone": "cleanroom-a",
                "process": "deposition",
                "event_status": "normal",
                "particle_count": 250,
                "temperature": 22.5,
                "humidity": 45,
                "airflow": 0.45,
                "gas_ppm": 12,
                "ppe_compliant": True,
            },
            "expected": "normal",
        },
        {
            "name": "warning",
            "payload": {
                "timestamp": "2026-07-20T10:01:00Z",
                "machine_id": "nano-tool-02",
                "zone": "cleanroom-b",
                "process": "etching",
                "event_status": "warning",
                "particle_count": 1000,
                "temperature": 27,
                "humidity": 58,
                "airflow": 0.35,
                "gas_ppm": 55,
                "ppe_compliant": True,
            },
            "expected": "warning",
        },
        {
            "name": "critical",
            "payload": {
                "timestamp": "2026-07-20T10:02:00Z",
                "machine_id": "nano-tool-03",
                "zone": "cleanroom-c",
                "process": "chemical-processing",
                "event_status": "critical",
                "particle_count": 1500,
                "temperature": 31,
                "humidity": 68,
                "airflow": 0.18,
                "gas_ppm": 85,
                "ppe_compliant": False,
            },
            "expected": "critical",
        },
    ]

    failures = 0

    for case in cases:
        result = analyse_telemetry(
            case["payload"],
            config,
        )

        actual = result["severity"]
        passed = actual == case["expected"]

        print(
            f"{case['name']}: "
            f"expected={case['expected']} "
            f"actual={actual} "
            f"risk_score={result['risk_score']} "
            f"{'PASS' if passed else 'FAIL'}"
        )

        if not passed:
            failures += 1

    if failures:
        print(
            f"Edge AI self-test: FAIL "
            f"({failures} failure(s))"
        )
        return 1

    print("Edge AI self-test: PASS")
    return 0


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Topic 127 custom Edge AI inference engine."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            os.getenv(
                "EDGE_AI_CONFIG",
                str(DEFAULT_CONFIG_PATH),
            )
        ),
        help="Path to the Edge AI JSON configuration.",
    )

    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run deterministic tests without MQTT.",
    )

    parser.add_argument(
        "--analyse-json",
        help="Analyse one JSON object without starting MQTT.",
    )

    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        choices={
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        },
    )

    return parser.parse_args()


def main() -> int:
    """Program entry point."""

    args = parse_arguments()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format=(
            "%(asctime)s %(levelname)s "
            "%(name)s: %(message)s"
        ),
    )

    try:
        config = load_config(args.config)

        if args.self_test:
            return run_self_test(config)

        if args.analyse_json:
            telemetry = json.loads(args.analyse_json)

            if not isinstance(telemetry, dict):
                raise ValueError(
                    "--analyse-json requires a JSON object."
                )

            result = analyse_telemetry(
                telemetry,
                config,
            )

            print(json.dumps(result, indent=2))
            return 0

        service = EdgeAIService(config)
        service.run()
        return 0

    except (
        ConfigurationError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        LOGGER.error("%s", exc)
        return 1
    except KeyboardInterrupt:
        LOGGER.info("Edge AI engine stopped by user.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
