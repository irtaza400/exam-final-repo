import json
import os
from datetime import datetime, timezone

REPORT = "reports/final_project_report.md"
os.makedirs("reports", exist_ok=True)

files = {
    "Cleanroom ML incidents": "reports/incidents.csv",
    "OPC-UA process security": "reports/process_security_incidents.csv",
    "Modbus PLC security": "reports/modbus_security_incidents.csv",
    "Recipe tamper detection": "reports/recipe_tamper_incidents.csv",
    "EHS incidents": "reports/ehs_incidents.csv",
    "Supply chain ledger": "reports/supply_chain_ledger.json",
    "Simulated ledger status JSON": "reports/simulated_ledger_status.json",
    "Simulated ledger status text": "reports/simulated_ledger_status.txt",
    "Simulated ledger tamper status JSON": "reports/simulated_ledger_tamper_status.json",
    "Simulated ledger tamper status text": "reports/simulated_ledger_tamper_status.txt",
    "Simulated ledger restored status JSON": "reports/simulated_ledger_restored_status.json",
    "Simulated ledger restored status text": "reports/simulated_ledger_restored_status.txt",
    "Ledger verification report": "reports/ledger_verification_report.json",
    "Ledger tamper verification report": "reports/ledger_tamper_verification_report.json",
    "Compliance report": "reports/compliance_report.md",
    "Audit log": "reports/audit_log.csv",
    "Security scan report": "reports/security_scan_report.txt",
    "Incident summary": "reports/incident_summary.csv",
    "Dashboard healthcheck": "reports/dashboard_healthcheck.txt",
}

def load_json_report(path):
    """Return a JSON report dictionary or None if unavailable."""

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None

    return data if isinstance(data, dict) else None


ledger_status = load_json_report(
    "reports/simulated_ledger_status.json"
)

ledger_tamper_status = load_json_report(
    "reports/simulated_ledger_tamper_status.json"
)

ledger_restored_status = load_json_report(
    "reports/simulated_ledger_restored_status.json"
)


with open(REPORT, "w", encoding="utf-8", newline="\n") as f:
    f.write("# Topic 127 Version 3 Final Project Report\n\n")
    f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
    f.write("## Executive Summary\n\n")
    f.write("This EC2-ready enterprise lab implements a nanotechnology manufacturing security platform with IoT monitoring, AI anomaly detection, OPC-UA/Modbus process control security, supply chain traceability, worker safety, compliance automation, audit logging, and DevSecOps evidence.\n\n")
    f.write("## Evidence Files\n\n")
    for label, path in files.items():
        status = "PRESENT" if os.path.exists(path) else "MISSING - run related module"
        f.write(f"- {label}: `{path}` — **{status}**\n")

    f.write(
        "\n## Simulated Blockchain Ledger Evidence\n\n"
    )

    f.write(
        "The project implements an educational, single-node, "
        "tamper-evident supply-chain and QMS ledger. "
        "Each record is linked using SHA-256 hashes and the "
        "previous block hash. This provides deterministic "
        "integrity verification without claiming to be a "
        "distributed production blockchain network.\n\n"
    )

    if ledger_status:
        latest_block = ledger_status.get(
            "latest_block",
            {},
        )
        decisions = ledger_status.get(
            "decision_counts",
            {},
        )
        integrity = ledger_status.get(
            "integrity_failure",
            {},
        )

        f.write("### Current Ledger Health\n\n")
        f.write(
            f"- Component: "
            f"**{ledger_status.get('component', 'N/A')}**\n"
        )
        f.write(
            f"- Implementation: "
            f"**{ledger_status.get('implementation_type', 'N/A')}**\n"
        )
        f.write(
            f"- Deployment model: "
            f"**{ledger_status.get('deployment_model', 'N/A')}**\n"
        )
        f.write(
            f"- Hash algorithm: "
            f"**{ledger_status.get('hash_algorithm', 'N/A')}**\n"
        )
        f.write(
            f"- Genesis anchor: "
            f"**{ledger_status.get('genesis_anchor', 'N/A')}**\n"
        )
        f.write(
            f"- Chain status: "
            f"**{ledger_status.get('chain_status', 'UNKNOWN')}**\n"
        )
        f.write(
            f"- Block count: "
            f"**{ledger_status.get('block_count', 0)}**\n"
        )
        f.write(
            f"- Latest record ID: "
            f"**{latest_block.get('record_id', 'N/A')}**\n"
        )
        f.write(
            f"- Latest batch ID: "
            f"**{latest_block.get('batch_id', 'N/A')}**\n"
        )
        f.write(
            f"- Latest block hash: "
            f"`{latest_block.get('current_hash_short', 'N/A')}`\n"
        )
        f.write(
            f"- Stored hash verified: "
            f"**{latest_block.get('stored_hash_matches_recalculated', False)}**\n"
        )
        f.write(
            f"- Integrity failure detected: "
            f"**{integrity.get('detected', False)}**\n"
        )

        f.write("\n### QMS Decision Summary\n\n")
        f.write(
            f"- Approved for use: "
            f"**{decisions.get('approved', 0)}**\n"
        )
        f.write(
            f"- Quarantined for QMS review: "
            f"**{decisions.get('quarantined', 0)}**\n"
        )
        f.write(
            f"- Rejected or legal review: "
            f"**{decisions.get('rejected_or_legal_review', 0)}**\n"
        )
    else:
        f.write(
            "- Current ledger status report: "
            "**MISSING — run "
            "`python -m src.simulated_ledger_status`**\n"
        )

    f.write("\n### Controlled Tamper Demonstration\n\n")

    if ledger_tamper_status:
        tamper_integrity = ledger_tamper_status.get(
            "integrity_failure",
            {},
        )

        f.write(
            f"- Tampered chain status: "
            f"**{ledger_tamper_status.get('chain_status', 'UNKNOWN')}**\n"
        )
        f.write(
            f"- Tamper detected: "
            f"**{tamper_integrity.get('detected', False)}**\n"
        )
        f.write(
            f"- First failing record: "
            f"**{tamper_integrity.get('first_failing_record', 'N/A')}**\n"
        )
        f.write(
            f"- First verification error: "
            f"`{tamper_integrity.get('first_error', 'N/A')}`\n"
        )
    else:
        f.write(
            "- Tamper-status report: "
            "**MISSING — run "
            "`bash scripts/run_simulated_ledger_evidence.sh`**\n"
        )

    if ledger_restored_status:
        f.write(
            f"- Restored chain status: "
            f"**{ledger_restored_status.get('chain_status', 'UNKNOWN')}**\n"
        )
        f.write(
            f"- Restored ledger valid: "
            f"**{ledger_restored_status.get('ledger_valid', False)}**\n"
        )
    else:
        f.write(
            "- Restored-chain report: **MISSING**\n"
        )

    f.write("\n### Implementation Scope and Limitations\n\n")
    f.write(
        "- Educational simulated blockchain ledger: **YES**\n"
    )
    f.write(
        "- SHA-256 tamper-evident hash chaining: **YES**\n"
    )
    f.write(
        "- Supplier, certificate, material and QMS provenance: **YES**\n"
    )
    f.write(
        "- Independent chain verification: **YES**\n"
    )
    f.write(
        "- Controlled tamper detection and restoration: **YES**\n"
    )
    f.write(
        "- Distributed peer-to-peer consensus: **NO**\n"
    )
    f.write(
        "- Mining or staking: **NO**\n"
    )
    f.write(
        "- Smart contracts: **NO**\n"
    )

    f.write(
        "\nThis implementation is therefore presented accurately "
        "as an educational simulated blockchain and tamper-evident "
        "hash-chain control, not as a production distributed ledger.\n"
    )

    f.write("\n## Topic 127 Mapping\n\n")
    f.write("- AI Cleanroom Monitoring: MQTT, InfluxDB, Grafana, ML anomaly engine\n")
    f.write("- Manufacturing Process Control Security: OPC-UA, Modbus, recipe integrity\n")
    f.write("- Supply Chain Security: supplier ledger, material traceability, dual-use risk flag\n")
    f.write("- Worker Safety: PPE, gas, spill, nanoparticle exposure incidents\n")
    f.write("- DevSecOps: Bandit, Semgrep, Trivy scan orchestration\n")
    f.write("- Compliance: ISO 14644, ISO 14001, OSHA, EPA, IEC 62443, NIST CSF evidence\n")

print(f"Final report generated: {REPORT}")
