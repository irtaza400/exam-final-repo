# Topic 127 — Final Evidence Capture Checklist

**Repository:** `irtaza400/exam-final-repo`
**Branch:** `main`
**Architecture baseline:** A01–A06 locked
**Primary execution:** `scripts/run_exam_demo.sh`

---

# 1. Purpose

This checklist converts the Final Examination Evidence Matrix into an executable evidence-capture procedure.

The objective is to complete one controlled final demonstration and collect sufficient evidence to prove:

```text
Architecture
    ↓
Implementation
    ↓
Execution
    ↓
Output
    ↓
Examiner Evidence
```

The checklist must be completed **after** the final repository baseline is frozen.

---

# 2. Evidence Rules

## Rule 1 — Source code is not runtime proof

A source file proves that functionality exists in the repository.

It does NOT prove that the capability executed successfully during the final demonstration.

Therefore:

```text
Source file = implementation evidence

Execution output / report / screenshot
          =
runtime evidence
```

---

## Rule 2 — Do not treat overall demo completion as universal PASS

`scripts/run_exam_demo.sh` orchestrates the laboratory and records a master log, but some components are intentionally allowed to continue after warnings or non-zero optional results.

Therefore every critical capability must be individually checked.

---

## Rule 3 — Preserve the repository commit

Record the exact Git commit used for the evidence run.

Required:

```text
git rev-parse HEAD
git status
```

The evidence package must identify the commit from which the evidence was generated.

---

## Rule 4 — Do not alter A01–A06

A01–A06 are the locked architecture baseline.

No architecture modification should be introduced during evidence capture.

---

# 3. Phase A — Pre-Demo Preparation

## A01. Repository clean state

Run:

```bash
git status
```

PASS condition:

```text
nothing to commit, working tree clean
```

Capture:

```text
Evidence/00_PreDemo/repository_status.txt
```

---

## A02. Record exact commit

Run:

```bash
git rev-parse HEAD
git log -1 --oneline
```

Capture:

```text
Evidence/00_PreDemo/repository_commit.txt
```

---

## A03. Verify branch

Run:

```bash
git branch --show-current
```

Expected:

```text
main
```

Capture:

```text
Evidence/00_PreDemo/branch.txt
```

---

## A04. Validate the demonstration script

Run:

```bash
test -x scripts/run_exam_demo.sh && echo PASS || echo FAIL
```

Expected:

```text
PASS
```

---

## A05. Verify required Python environment

Run:

```bash
source venv/bin/activate
python --version
python -m pip check
```

Capture:

```text
Evidence/00_PreDemo/python_environment.txt
```

Expected:

```text
pip check
=
no broken requirements
```

---

## A06. Validate Docker configuration

Run:

```bash
docker compose config >/dev/null && echo PASS || echo FAIL
```

Expected:

```text
PASS
```

Capture:

```text
Evidence/00_PreDemo/docker_config.txt
```

---

# 4. Phase B — Start Final Examiner Demonstration

Run:

```bash
cd ~/exam-final-repo
source venv/bin/activate
./scripts/run_exam_demo.sh
```

Do NOT use:

```text
SKIP_TAMPER_DEMO=1
```

for the final evidence run.

The recipe-tamper demonstration is part of the required evidence.

Do not use:

```text
STOP_MONITORING_AFTER_DEMO=1
```

because Grafana/FUXA monitoring evidence must remain available.

---

# 5. Master Demonstration Evidence

The examiner demo creates:

```text
logs/exam_demo_<timestamp>.log
```

and:

```text
reports/exam_demo_summary_<timestamp>.txt
```

from the demonstration orchestration.

After completion identify:

```bash
ls -t logs/exam_demo_*.log | head -1
ls -t reports/exam_demo_summary_*.txt | head -1
```

Copy the selected files into:

```text
Evidence/01_Master_Demo/
```

Required:

```text
master_demo.log
demo_summary.txt
```

---

# 6. Deployment Evidence

## B01. Docker services

Run:

```bash
docker compose ps
```

Capture:

```text
Evidence/02_Deployment/docker_compose_ps.txt
```

Expected important services include the repository's configured infrastructure such as:

```text
Mosquitto
InfluxDB
Grafana
FUXA
```

---

## B02. EC2 / Ubuntu environment

Run:

```bash
hostname
uname -a
docker --version
docker compose version
```

Capture:

```text
Evidence/02_Deployment/ec2_environment.txt
```

---

## B03. Runtime service processes

Run:

```bash
for f in .runtime/*.pid; do
  printf '%s: ' "$f"
  pgrep -F "$f" >/dev/null 2>&1 && echo RUNNING || echo CHECK
done
```

Also inspect:

```bash
cat .runtime/edge_gateway.pid
cat .runtime/edge_ai.pid
cat .runtime/mqtt_to_influx.pid
cat .runtime/sensor_simulator.pid
```

Capture only the relevant PID/process evidence.

---

# 7. Cleanroom / IoT Evidence

## C01. Sensor simulator

Evidence source:

```text
src/sensor_simulator.py
```

Capture:

```text
sensor_simulator.log
```

Required proof:

```text
Sensor data generated
Cleanroom variables present
MQTT publishing active
```

---

## C02. MQTT

Verify raw telemetry:

```bash
grep -E 'topic127/raw/cleanroom|topic127/edge/validated' logs/*.log | tail -20
```

Capture:

```text
Evidence/03_Cleanroom/mqtt_topics.txt
```

---

## C03. Edge Gateway

Evidence source:

```text
src/edge_gateway.py
```

Capture:

```text
logs/edge_gateway.log
```

Required proof:

```text
Input received
Validation performed
Enrichment/routing performed
Validated telemetry produced
```

---

## C04. InfluxDB

Verify recent cleanroom data using the repository's configured InfluxDB deployment.

Capture:

```text
Evidence/03_Cleanroom/influxdb_verification.txt
```

Required proof:

```text
cleanroom_monitoring data exists
recent records exist
```

---

## C05. Grafana

Open:

```text
http://EC2_PUBLIC_IP:3000
```

Capture screenshot:

```text
Evidence/03_Cleanroom/grafana_cleanroom.png
```

The screenshot must show populated—not blank—monitoring panels.

Priority panels:

```text
Cleanroom telemetry
Environmental data
Operational data
Ledger health
```

---

# 8. FUXA Evidence

Open the FUXA Operations Overview.

Capture:

```text
Evidence/04_FUXA/fuxa_operations_overview.png
```

Required:

```text
HMI / SCADA-style visualization visible
Process variables/status visible
No empty/broken view
```

Also capture ledger-health view:

```text
Evidence/04_FUXA/fuxa_ledger_health.png
```

---

# 9. AI / ML Evidence

## D01. scikit-learn

Repository implementation:

```text
src/ml_anomaly_engine.py
```

It trains an `IsolationForest`, evaluates demonstration events, and writes:

```text
reports/incidents.csv
reports/incidents.jsonl
```

Capture:

```text
Evidence/05_AI_ML/scikit_learn_output.txt
Evidence/05_AI_ML/incidents.csv
```

Required:

```text
Model execution
Anomaly / incident output
Recommended action
```

---

## D02. TensorFlow / Keras

Repository implementation:

```text
src/tensorflow_anomaly_engine.py
```

It uses a Keras autoencoder and writes:

```text
reports/tensorflow_anomaly_incidents.csv
```

Capture:

```text
Evidence/05_AI_ML/tensorflow_output.txt
Evidence/05_AI_ML/tensorflow_anomaly_incidents.csv
```

Required:

```text
TensorFlow version
Autoencoder threshold
Normal/anomaly decisions
Incident evidence
```

---

## D03. AI architecture separation

Capture one architecture/viva evidence page showing:

```text
Custom Edge AI
        ≠
scikit-learn
        ≠
TensorFlow/Keras
```

Required examiner explanation:

```text
Custom Edge AI = rule-based inference

scikit-learn = IsolationForest demonstration

TensorFlow/Keras = autoencoder demonstration
```

Do not present them as one production pipeline.

---

# 10. OPC-UA Evidence

## E01. OPC-UA server

Verify endpoint:

```bash
timeout 2 bash -c 'echo > /dev/tcp/127.0.0.1/4840' \
  && echo "OPC-UA PORT PASS" \
  || echo "OPC-UA PORT CHECK"
```

Capture:

```text
Evidence/06_Process_Control/opcua_port.txt
```

---

## E02. OPC-UA validator

Capture:

```text
logs/opcua_client_validator.log
```

and:

```text
reports/process_security_incidents.csv
```

Required:

```text
Validator executed
Process/security findings generated where expected
```

---

# 11. Modbus Evidence

## F01. Modbus server

Verify:

```bash
timeout 2 bash -c 'echo > /dev/tcp/127.0.0.1/5020' \
  && echo "MODBUS PORT PASS" \
  || echo "MODBUS PORT CHECK"
```

Capture:

```text
Evidence/06_Process_Control/modbus_port.txt
```

---

## F02. Modbus validator

Capture:

```text
logs/modbus_client_validator.log
reports/modbus_security_incidents.csv
```

Required:

```text
Validator executed
Security findings / validation output present
```

---

# 12. Recipe Integrity Evidence

This is a mandatory evidence chain.

## G01. Normal integrity state

Required:

```text
Recipe integrity verified
```

Capture:

```text
Evidence/07_Recipe_Integrity/01_integrity_pass.txt
```

---

## G02. Controlled tampering

The repository uses SHA-256 comparison between the approved recipe and reference hash.

Capture:

```text
Evidence/07_Recipe_Integrity/02_tamper_detection.txt
Evidence/07_Recipe_Integrity/recipe_tamper_incidents.csv
```

Required:

```text
Tampering detected
Critical incident generated
```

---

## G03. Restoration

Required sequence:

```text
PASS
 ↓
Tamper
 ↓
DETECTED
 ↓
Restore approved recipe
 ↓
PASS
```

Capture:

```text
Evidence/07_Recipe_Integrity/03_restoration_pass.txt
```

This sequence should be explicitly demonstrated to the examiner.

---

# 13. Supply Chain Evidence

## H01. Supplier validation

Repository implementation:

```text
src/supplier_validator.py
```

It checks supplier existence, supplier ACTIVE status and approved material scope.

Capture:

```text
Evidence/08_Supply_Chain/01_supplier_validation.txt
```

Include scenarios demonstrating:

```text
Approved supplier
Unknown supplier
Suspended supplier
Material approval mismatch
```

---

## H02. Material risk

Repository implementation:

```text
src/material_risk_engine.py
```

Capture:

```text
Evidence/08_Supply_Chain/02_material_risk.txt
reports/supply_chain_risk_report.csv
```

Required:

```text
Risk score
Risk reasons
Decision
Control actions
```

The implemented decision model distinguishes approval, quarantine/QMS review and reject/legal-review outcomes.

---

## H03. Ledger

Repository implementation:

```text
src/supply_chain_ledger.py
```

Capture:

```text
Evidence/08_Supply_Chain/03_ledger.txt
reports/supply_chain_ledger.json
```

Required:

```text
Records
previous_hash
current_hash
risk decision
traceability information
```

The repository explicitly implements a hash-chained ledger with chain verification.

---

# 14. Ledger Tamper Evidence

This should be captured as a complete sequence.

## I01. Initial ledger PASS

Capture:

```text
Evidence/09_Ledger_Tamper/01_initial_pass.txt
```

---

## I02. Controlled tamper

Capture:

```text
Evidence/09_Ledger_Tamper/02_tamper_detected.txt
```

Required:

```text
Integrity failure detected
First failing record / verification error
```

---

## I03. Restoration

Capture:

```text
Evidence/09_Ledger_Tamper/03_restored_pass.txt
```

Required:

```text
Ledger valid
Restoration successful
```

The final evidence should visibly demonstrate:

```text
VALID
  ↓
TAMPER
  ↓
INVALID / DETECTED
  ↓
RESTORE
  ↓
VALID
```

---

# 15. Worker Safety / EHS Evidence

Repository implementation:

```text
src/ehs_incident_engine.py
```

The engine evaluates:

```text
Gas exposure
PPE non-compliance
Chemical spill
Nanoparticle exposure
Hazardous waste
Emission threshold
```

Capture:

```text
Evidence/10_EHS/ehs_output.txt
Evidence/10_EHS/ehs_incidents.csv
```

Required:

```text
Incident
Severity
Issues
Recommended emergency action
```

Important examiner wording:

```text
"The system generates a recommended response and evidence record;
it does not directly actuate a physical evacuation system."
```

---

# 16. Suricata IDS Evidence

Run through the repository's controlled IDS demonstration.

Capture:

```text
Evidence/11_Suricata/suricata_demo_output.txt
Evidence/11_Suricata/suricata_alert_validation.txt
```

Required:

```text
Controlled input / PCAP
Suricata rule match
Alert validation
```

Important:

Describe this as a:

```text
controlled IDS demonstration
```

not continuous enterprise network monitoring.

---

# 17. DevSecOps Evidence

The repository's DevSecOps scanner runs:

```text
Bandit
Semgrep
Trivy
```

and writes:

```text
reports/security_scan_report.txt
```

Capture:

```text
Evidence/12_DevSecOps/security_scan_report.txt
Evidence/12_DevSecOps/devsecops_summary.txt
```

Required individual evidence:

```text
Bandit
Semgrep
Trivy
Exit code
Findings / warnings
```

Do not claim this is an automatic CI/CD blocking gate unless separately demonstrated.

---

# 18. Governance Evidence

## J01. Incident summary

Capture:

```text
reports/incident_summary.csv
```

Save:

```text
Evidence/13_Governance/incident_summary.csv
```

---

## J02. Audit log

Capture:

```text
reports/audit_log.csv
```

Save:

```text
Evidence/13_Governance/audit_log.csv
```

---

## J03. Compliance report

Capture:

```text
reports/compliance_report.md
```

Save:

```text
Evidence/13_Governance/compliance_report.md
```

The compliance generator aggregates evidence such as cleanroom, process security, recipe, supply-chain and EHS records.

---

## J04. Dashboard healthcheck

Capture:

```text
reports/dashboard_healthcheck.txt
```

Save:

```text
Evidence/13_Governance/dashboard_healthcheck.txt
```

---

## J05. Final project report

Capture:

```text
reports/final_project_report.md
```

Save:

```text
Evidence/13_Governance/final_project_report.md
```

The final report generator checks the availability of the major evidence outputs and reports their status.

---

# 19. Recommended Screenshot Set

Capture these screenshots during or immediately after the final run:

```text
01_ec2_docker_environment.png
02_docker_compose_services.png
03_cleanroom_grafana.png
04_fuxa_operations_overview.png
05_fuxa_ledger_health.png
06_ai_anomaly_evidence.png
07_opcua_modbus_validation.png
08_recipe_tamper_detection.png
09_supply_chain_risk_ledger.png
10_ledger_tamper_restore.png
11_ehs_incident.png
12_suricata_alert.png
13_devsecops_results.png
14_compliance_final_report.png
```

Do not create screenshots merely to make the package look larger.

Each screenshot must support an identifiable examination claim.

---

# 20. Final Evidence Folder

After the demonstration, organize evidence as:

```text
Topic127_Final_Submission/
└── 04_Evidence/
    ├── 00_PreDemo/
    ├── 01_Master_Demo/
    ├── 02_Deployment/
    ├── 03_Cleanroom/
    ├── 04_FUXA/
    ├── 05_AI_ML/
    ├── 06_Process_Control/
    ├── 07_Recipe_Integrity/
    ├── 08_Supply_Chain/
    ├── 09_Ledger_Tamper/
    ├── 10_EHS/
    ├── 11_Suricata/
    ├── 12_DevSecOps/
    └── 13_Governance/
```

---

# 21. Evidence Naming Convention

Use stable names.

Good:

```text
grafana_cleanroom.png
recipe_tamper_detection.txt
supply_chain_risk_report.csv
audit_log.csv
```

Avoid:

```text
final_final2.png
new.png
test123.png
latest_report_REAL_FINAL.md
```

---

# 22. Final Evidence Completeness Check

Before packaging, verify:

```text
[ ] Repository clean before run
[ ] Commit SHA recorded
[ ] Master demo log saved
[ ] Demo summary saved
[ ] Docker status captured
[ ] EC2 environment captured
[ ] MQTT evidence captured
[ ] InfluxDB evidence captured
[ ] Grafana screenshot captured
[ ] FUXA screenshot captured
[ ] scikit-learn evidence captured
[ ] TensorFlow evidence captured
[ ] OPC-UA evidence captured
[ ] Modbus evidence captured
[ ] Recipe PASS captured
[ ] Recipe tamper captured
[ ] Recipe restoration PASS captured
[ ] Supplier validation captured
[ ] Material risk captured
[ ] Supply-chain ledger captured
[ ] Ledger PASS captured
[ ] Ledger tamper captured
[ ] Ledger restoration captured
[ ] EHS evidence captured
[ ] Suricata evidence captured
[ ] Bandit evidence captured
[ ] Semgrep evidence captured
[ ] Trivy evidence captured
[ ] Incident summary captured
[ ] Audit log captured
[ ] Compliance report captured
[ ] Dashboard healthcheck captured
[ ] Final project report captured
```

---

# 23. Evidence Quality Check

Every evidence item should answer at least one of:

```text
What happened?
Where did it happen?
Which component performed it?
What output was produced?
Was it successful?
What evidence proves it?
Is it implemented, simulated, controlled or future?
```

---

# 24. Examiner Defence Rule

When presenting evidence, use this sequence:

```text
"This is the architecture."
        ↓
"This is the repository implementation."
        ↓
"This is the execution."
        ↓
"This is the generated evidence."
        ↓
"This is the limitation."
```

Example:

```text
A05
 ↓
recipe_integrity_check.py
 ↓
controlled tamper demo
 ↓
recipe_tamper_incidents.csv
 ↓
SHA-256 mismatch detected
 ↓
approved recipe restored
```

---

# 25. Final Runtime Evidence Principle

Do not claim:

```text
"Everything is production-grade."
```

Instead accurately distinguish:

```text
IMPLEMENTED
SIMULATED
CONTROLLED DEMONSTRATION
RECOMMENDED RESPONSE
FUTURE TARGET
```

This distinction must remain consistent with A01–A06.

---

# 26. Final Completion Criteria

The evidence-capture phase is complete only when:

```text
A01–A06                    ✅ LOCKED
Evidence Matrix            ✅ PRESENT
Final demo executed        ✅
Master log captured        ✅
Required reports captured  ✅
Required screenshots       ✅
Critical PASS results      ✅
Limitations documented     ✅
Evidence organized         ✅
Commit SHA recorded        ✅
```

Only after all of the above should the final submission index and final examiner package be assembled.

---

# 27. Final Status

```text
ARCHITECTURE
A01–A06                     ✅

TRACEABILITY
EVIDENCE_MATRIX.md          ✅

RUNTIME EVIDENCE
Final execution             ⏳

SCREENSHOTS
Final capture               ⏳

REPORT PACKAGE
Final capture               ⏳

SUBMISSION INDEX
Pending evidence completion ⏳

FINAL SUBMISSION PACKAGE
Pending evidence completion ⏳
```

**END OF FINAL EVIDENCE CAPTURE CHECKLIST**
