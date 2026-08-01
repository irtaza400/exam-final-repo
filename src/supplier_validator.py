"""Supplier and material approval validation for Topic 127."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_SUPPLIERS_PATH = Path("config/approved_suppliers.json")


@dataclass(frozen=True)
class SupplierValidationResult:
    supplier_id: str
    supplier_found: bool
    supplier_active: bool
    material_approved: bool
    supplier_name: str | None
    supplier_status: str
    country_risk: str
    approval_reference: str | None
    reasons: tuple[str, ...]

    @property
    def approved(self) -> bool:
        return (
            self.supplier_found
            and self.supplier_active
            and self.material_approved
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "supplier_id": self.supplier_id,
            "supplier_found": self.supplier_found,
            "supplier_active": self.supplier_active,
            "material_approved": self.material_approved,
            "supplier_name": self.supplier_name,
            "supplier_status": self.supplier_status,
            "country_risk": self.country_risk,
            "approval_reference": self.approval_reference,
            "approved": self.approved,
            "reasons": list(self.reasons),
        }


def load_suppliers(path: Path = DEFAULT_SUPPLIERS_PATH) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        suppliers = json.load(handle)

    if not isinstance(suppliers, list):
        raise ValueError("Approved-supplier registry must contain a JSON list.")

    return suppliers


def validate_supplier(
    supplier_id: str,
    material: str,
    suppliers: list[dict[str, Any]],
) -> SupplierValidationResult:
    supplier = next(
        (
            item
            for item in suppliers
            if item.get("supplier_id") == supplier_id
        ),
        None,
    )

    if supplier is None:
        return SupplierValidationResult(
            supplier_id=supplier_id,
            supplier_found=False,
            supplier_active=False,
            material_approved=False,
            supplier_name=None,
            supplier_status="UNKNOWN",
            country_risk="HIGH",
            approval_reference=None,
            reasons=("Supplier is not present in the approved registry.",),
        )

    status = str(supplier.get("status", "UNKNOWN")).upper()
    supplier_active = status == "ACTIVE"

    approved_materials = {
        str(item).strip().lower()
        for item in supplier.get("approved_materials", [])
    }
    material_approved = material.strip().lower() in approved_materials

    reasons: list[str] = []

    if not supplier_active:
        reasons.append(
            f"Supplier status is {status}; ACTIVE status is required."
        )

    if not material_approved:
        reasons.append(
            "Material is not included in the supplier's approved scope."
        )

    if supplier_active and material_approved:
        reasons.append(
            "Supplier is active and approved for the requested material."
        )

    return SupplierValidationResult(
        supplier_id=supplier_id,
        supplier_found=True,
        supplier_active=supplier_active,
        material_approved=material_approved,
        supplier_name=supplier.get("name"),
        supplier_status=status,
        country_risk=str(
            supplier.get("country_risk", "HIGH")
        ).upper(),
        approval_reference=supplier.get("approval_reference"),
        reasons=tuple(reasons),
    )


def main() -> int:
    suppliers = load_suppliers()

    scenarios = [
        ("SUP-NANO-001", "photoresist precursor"),
        ("SUP-GAS-002", "etching gas"),
        ("SUP-UNKNOWN-999", "dual-use nanomaterial precursor"),
        ("SUP-SUSPENDED-003", "nanomaterial precursor"),
    ]

    for supplier_id, material in scenarios:
        result = validate_supplier(
            supplier_id,
            material,
            suppliers,
        )
        print(json.dumps(result.to_dict(), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
