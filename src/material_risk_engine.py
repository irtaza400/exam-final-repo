"""Material, certificate, quality, and export-risk evaluation for Topic 127."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from src.supplier_validator import SupplierValidationResult


DEFAULT_RULES_PATH = Path("config/material_risk_rules.json")


@dataclass(frozen=True)
class MaterialRiskResult:
    batch_id: str
    risk_score: int
    decision: str
    certificate_status: str
    quality_status: str
    export_risk: str
    country_risk: str
    reasons: tuple[str, ...]
    control_actions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "risk_score": self.risk_score,
            "decision": self.decision,
            "certificate_status": self.certificate_status,
            "quality_status": self.quality_status,
            "export_risk": self.export_risk,
            "country_risk": self.country_risk,
            "reasons": list(self.reasons),
            "control_actions": list(self.control_actions),
        }


def load_rules(path: Path = DEFAULT_RULES_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        rules = json.load(handle)

    if not isinstance(rules, dict):
        raise ValueError("Material-risk rules must contain a JSON object.")

    if "risk_weights" not in rules or "decision_thresholds" not in rules:
        raise ValueError(
            "Material-risk rules must contain risk_weights "
            "and decision_thresholds."
        )

    return rules


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Invalid ISO date: {value}") from exc


def determine_certificate_status(
    certificate: dict[str, Any],
    evaluation_date: date,
) -> str:
    certificate_id = certificate.get("certificate_id")
    configured_status = str(
        certificate.get("status", "MISSING")
    ).upper()

    if not certificate_id or configured_status == "MISSING":
        return "MISSING"

    if configured_status == "REVOKED":
        return "REVOKED"

    expiry_date = parse_iso_date(certificate.get("expires_at"))

    if configured_status == "EXPIRED":
        return "EXPIRED"

    if expiry_date is not None and expiry_date < evaluation_date:
        return "EXPIRED"

    if configured_status != "VALID":
        return "INVALID"

    return "VALID"


def determine_decision(
    score: int,
    thresholds: dict[str, Any],
) -> str:
    reject_min = int(thresholds["reject_min"])
    quarantine_max = int(thresholds["quarantine_max"])

    if score >= reject_min:
        return "REJECT_OR_LEGAL_REVIEW"

    if score <= quarantine_max and score >= 40:
        return "QUARANTINE_AND_QMS_REVIEW"

    return "APPROVE_FOR_USE"


def evaluate_material_batch(
    batch: dict[str, Any],
    supplier_result: SupplierValidationResult,
    rules: dict[str, Any],
    evaluation_date: date | None = None,
) -> MaterialRiskResult:
    if evaluation_date is None:
        evaluation_date = date.today()

    weights = rules["risk_weights"]
    thresholds = rules["decision_thresholds"]

    score = 0
    reasons: list[str] = []
    actions: list[str] = []

    if not supplier_result.supplier_found:
        score += int(weights["supplier_not_approved"])
        reasons.append("Supplier is not present in the approved registry.")
        actions.append("Block batch release and initiate supplier due diligence.")

    elif not supplier_result.supplier_active:
        score += int(weights["supplier_not_active"])
        reasons.append(
            f"Supplier status is {supplier_result.supplier_status}."
        )
        actions.append("Suspend receipt until supplier status is restored.")

    if not supplier_result.material_approved:
        score += int(weights["supplier_not_approved"])
        reasons.append("Material is outside the supplier's approved scope.")
        actions.append("Require QMS approval for material-scope exception.")

    certificate = batch.get("certificate", {})
    certificate_status = determine_certificate_status(
        certificate,
        evaluation_date,
    )

    if certificate_status == "MISSING":
        score += int(weights["certificate_missing"])
        reasons.append("Quality certificate is missing.")
        actions.append("Quarantine batch pending certificate submission.")

    elif certificate_status == "EXPIRED":
        score += int(weights["certificate_expired"])
        reasons.append("Quality certificate is expired.")
        actions.append("Quarantine batch pending renewed certification.")

    elif certificate_status == "REVOKED":
        score += int(weights["certificate_revoked"])
        reasons.append("Quality certificate has been revoked.")
        actions.append("Reject batch and initiate supplier investigation.")

    elif certificate_status == "INVALID":
        score += int(weights["certificate_missing"])
        reasons.append("Quality certificate status is invalid.")
        actions.append("Quarantine batch pending certificate validation.")

    quality_status = str(
        batch.get("quality_status", "UNKNOWN")
    ).upper()

    if quality_status == "FAILED":
        score += int(weights["quality_failed"])
        reasons.append("Batch quality status is FAILED.")
        actions.append("Reject batch and create a QMS non-conformance.")

    elif quality_status == "REVIEW_REQUIRED":
        score += int(weights["quality_review_required"])
        reasons.append("Batch requires additional quality review.")
        actions.append("Quarantine batch pending QMS assessment.")

    elif quality_status != "PASSED":
        score += int(weights["quality_review_required"])
        reasons.append(f"Unknown quality status: {quality_status}.")
        actions.append("Hold batch until quality status is resolved.")

    export_risk = str(batch.get("export_risk", "HIGH")).upper()

    if export_risk == "HIGH":
        score += int(weights["export_risk_high"])
        reasons.append("Material has a HIGH dual-use/export-risk rating.")
        actions.append("Require legal and export-control review.")

    elif export_risk == "MEDIUM":
        score += int(weights["export_risk_medium"])
        reasons.append("Material has a MEDIUM dual-use/export-risk rating.")
        actions.append("Record enhanced review and end-use justification.")

    country_risk = supplier_result.country_risk.upper()

    if country_risk == "HIGH":
        score += int(weights["country_risk_high"])
        reasons.append("Supplier country-risk classification is HIGH.")
        actions.append("Require enhanced supplier and legal review.")

    elif country_risk == "MEDIUM":
        score += int(weights["country_risk_medium"])
        reasons.append("Supplier country-risk classification is MEDIUM.")
        actions.append("Apply enhanced supplier monitoring.")

    score = min(score, 100)
    decision = determine_decision(score, thresholds)

    if not reasons:
        reasons.append("No material supply-chain risk exceptions detected.")

    if decision == "APPROVE_FOR_USE":
        actions.append("Release batch for controlled manufacturing use.")
    elif decision == "QUARANTINE_AND_QMS_REVIEW":
        actions.append("Keep batch quarantined until QMS approval.")
    else:
        actions.append("Prevent batch use pending legal or executive review.")

    return MaterialRiskResult(
        batch_id=str(batch["batch_id"]),
        risk_score=score,
        decision=decision,
        certificate_status=certificate_status,
        quality_status=quality_status,
        export_risk=export_risk,
        country_risk=country_risk,
        reasons=tuple(dict.fromkeys(reasons)),
        control_actions=tuple(dict.fromkeys(actions)),
    )
