# Topic 127 — Final Examination Evidence Matrix

**Repository:** `irtaza400/exam-final-repo`
**Branch:** `main`
**Architecture baseline:** A01–A06 locked

---

## 1. Purpose

This matrix provides traceability between:

```text
Topic 127 Requirement
        ↓
Implemented Capability
        ↓
Repository Implementation
        ↓
Architecture Reference
        ↓
Evidence Output
        ↓
Final Examiner Evidence
```

The matrix is intended to support:

* final examination preparation
* examiner traceability
* live demonstration planning
* evidence collection
* presentation defence
* viva questioning
* final submission packaging

---

## 2. Evidence Status Definitions

| Status                            | Meaning                                                                                                             |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **IMPLEMENTED / CAPTURE PENDING** | The repository contains the implementation; final runtime evidence still needs to be generated or captured.         |
| **IMPLEMENTED / REUSE**           | Existing repository material can be reused as supporting evidence without creating a new implementation artifact.   |
| **TARGET / NOT CURRENT**          | Future architecture only; must not be presented as currently implemented.                                           |
| **PACKAGING REQUIRED**            | The evidence exists or will exist after execution, but should be copied into the separate final submission package. |

---

# 3. Master Evidence Matrix

| #  | Examination Area            | Capability / Requirement               | Repository Implementation                                                                   | Primary Evidence Output                            | Architecture Reference  | Runtime / Examiner Evidence to Capture                     | Status                        |
| -- | --------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------- | ---------------------------------------------------------- | ----------------------------- |
| 1  | Cleanroom / IoT             | Cleanroom sensor telemetry generation  | `src/sensor_simulator.py`                                                                   | Sensor simulator output / log                      | A01, A03, A04           | Terminal evidence showing telemetry generation             | IMPLEMENTED / CAPTURE PENDING |
| 2  | Cleanroom / IoT             | MQTT messaging                         | `src/sensor_simulator.py`, `src/edge_gateway.py`, Mosquitto in `docker-compose.yml`         | MQTT topic activity                                | A01, A02, A03           | Evidence for `topic127/raw/cleanroom`                      | IMPLEMENTED / CAPTURE PENDING |
| 3  | Cleanroom / IoT             | Telemetry validation and enrichment    | `src/edge_gateway.py`                                                                       | Validated telemetry / gateway log                  | A01, A03, A04, A05      | Gateway output showing validation and routing              | IMPLEMENTED / CAPTURE PENDING |
| 4  | Monitoring                  | MQTT → InfluxDB ingestion              | `src/mqtt_to_influx.py`                                                                     | InfluxDB cleanroom data                            | A01, A02, A03, A04      | Query proving recent cleanroom data                        | IMPLEMENTED / CAPTURE PENDING |
| 5  | Monitoring                  | Grafana monitoring                     | `dashboards/json/topic127_cleanroom_dashboard.json` + provisioning                          | Grafana dashboard                                  | A01, A02, A03           | Actual Grafana screenshot with populated panels            | IMPLEMENTED / CAPTURE PENDING |
| 6  | HMI / SCADA                 | FUXA operational visualization         | `fuxa/` + FUXA import/validation scripts                                                    | FUXA project/view                                  | A01, A02, A03           | FUXA Operations Overview screenshot                        | IMPLEMENTED / CAPTURE PENDING |
| 7  | AI / ML                     | scikit-learn anomaly detection         | `src/ml_anomaly_engine.py`                                                                  | `reports/incidents.csv`, `reports/incidents.jsonl` | A01, A03, A04, A05      | Terminal output + generated incident report                | IMPLEMENTED / CAPTURE PENDING |
| 8  | AI / ML                     | TensorFlow/Keras anomaly detection     | `src/tensorflow_anomaly_engine.py`                                                          | `reports/tensorflow_anomaly_incidents.csv`         | A01, A03, A04           | TensorFlow execution output + report                       | IMPLEMENTED / CAPTURE PENDING |
| 9  | AI / ML                     | Separate AI/ML paths                   | `src/edge_ai_engine.py`, `src/ml_anomaly_engine.py`, `src/tensorflow_anomaly_engine.py`     | Source/configuration evidence                      | A01, A03, A05, A06      | Explain separation during architecture/viva defence        | IMPLEMENTED / REUSE           |
| 10 | Industrial Process Security | OPC-UA process simulation              | `src/opcua_server.py`                                                                       | OPC-UA server output                               | A01, A02, A03, A04, A05 | Server reachability + validator execution                  | IMPLEMENTED / CAPTURE PENDING |
| 11 | Industrial Process Security | OPC-UA validation                      | `src/opcua_client_validator.py`                                                             | `reports/process_security_incidents.csv`           | A01, A03, A04, A05      | Validator output and finding evidence                      | IMPLEMENTED / CAPTURE PENDING |
| 12 | Industrial Process Security | Modbus / PLC simulation                | `src/modbus_server.py`                                                                      | Modbus server output                               | A01, A02, A03, A04, A05 | Server reachability + validator execution                  | IMPLEMENTED / CAPTURE PENDING |
| 13 | Industrial Process Security | Modbus validation                      | `src/modbus_client_validator.py`                                                            | `reports/modbus_security_incidents.csv`            | A01, A03, A04, A05      | Validator output and finding evidence                      | IMPLEMENTED / CAPTURE PENDING |
| 14 | Recipe Integrity            | SHA-256 integrity verification         | `src/recipe_integrity_check.py`, `data/approved_recipe.json`, `data/approved_recipe.sha256` | `reports/recipe_tamper_incidents.csv`              | A01, A03, A04, A05      | Integrity PASS + controlled tamper detection + restoration | IMPLEMENTED / CAPTURE PENDING |
| 15 | Supply Chain                | Supplier registry validation           | `src/supplier_validator.py`, `config/approved_suppliers.json`                               | Validation output                                  | A01, A03, A04, A05      | Approved / unknown / suspended scenario output             | IMPLEMENTED / CAPTURE PENDING |
| 16 | Supply Chain                | Material risk assessment               | `src/material_risk_engine.py`, `config/material_risk_rules.json`                            | `reports/supply_chain_risk_report.csv`             | A01, A03, A04, A05      | Risk score and decision output                             | IMPLEMENTED / CAPTURE PENDING |
| 17 | Supply Chain                | Traceability ledger                    | `src/supply_chain_ledger.py`                                                                | `reports/supply_chain_ledger.json`                 | A01, A03, A04, A05      | Ledger generation and validation evidence                  | IMPLEMENTED / CAPTURE PENDING |
| 18 | Supply Chain                | Ledger verification                    | `src/ledger_verifier.py`, `scripts/verify_ledger.sh`                                        | Ledger verification report                         | A01, A04, A05           | Verification PASS evidence                                 | IMPLEMENTED / CAPTURE PENDING |
| 19 | Supply Chain                | Controlled ledger tamper demonstration | `scripts/simulate_ledger_tamper.sh`                                                         | Tamper verification reports                        | A04, A05                | PASS → tamper detected → restored PASS sequence            | IMPLEMENTED / CAPTURE PENDING |
| 20 | Worker Safety / EHS         | EHS event detection                    | `src/ehs_incident_engine.py`, `data/ehs_events.json`                                        | `reports/ehs_incidents.csv`                        | A01, A03, A04, A05      | EHS execution output + report                              | IMPLEMENTED / CAPTURE PENDING |
| 21 | Worker Safety / EHS         | Emergency response recommendation      | `src/ehs_incident_engine.py`                                                                | EHS report action field                            | A04, A05                | Evidence of recommended response generation                | IMPLEMENTED / CAPTURE PENDING |
| 22 | Cybersecurity / IDS         | Controlled Suricata demonstration      | `suricata/rules/topic127.rules`, `scripts/run_suricata_ids_demo.sh`                         | Suricata logs / alerts                             | A01, A02, A05           | Successful controlled-PCAP demonstration                   | IMPLEMENTED / CAPTURE PENDING |
| 23 | DevSecOps                   | Bandit scanning                        | `src/devsecops_scan.py`, `security/bandit.yml`                                              | `reports/security_scan_report.txt`                 | A01, A05                | Bandit output and exit code                                | IMPLEMENTED / CAPTURE PENDING |
| 24 | DevSecOps                   | Semgrep scanning                       | `src/devsecops_scan.py`, `security/semgrep.yml`                                             | `reports/security_scan_report.txt`                 | A01, A05                | Semgrep output and exit code                               | IMPLEMENTED / CAPTURE PENDING |
| 25 | DevSecOps                   | Trivy filesystem scanning              | `src/devsecops_scan.py`, `security/trivy-ignore.txt`                                        | `reports/security_scan_report.txt`                 | A01, A05                | Trivy output and HIGH/CRITICAL findings                    | IMPLEMENTED / CAPTURE PENDING |
| 26 | Governance                  | Incident aggregation                   | `src/incident_manager.py`                                                                   | `reports/incident_summary.csv`                     | A01, A04, A05           | Incident summary evidence                                  | IMPLEMENTED / CAPTURE PENDING |
| 27 | Governance                  | Audit logging                          | `src/audit_logger.py`                                                                       | `reports/audit_log.csv`                            | A01, A04, A05           | Generated audit log                                        | IMPLEMENTED / CAPTURE PENDING |
| 28 | Compliance                  | Compliance evidence generation         | `src/compliance_report_generator.py`                                                        | `reports/compliance_report.md`                     | A01, A04, A05           | Generated compliance report                                | IMPLEMENTED / CAPTURE PENDING |
| 29 | Final Reporting             | Final project report                   | `src/final_report_generator.py`                                                             | `reports/final_project_report.md`                  | A01–A06                 | Final report + evidence status                             | IMPLEMENTED / CAPTURE PENDING |
| 30 | Dashboard Verification      | Dashboard healthcheck                  | `src/dashboard_healthcheck.py`                                                              | `reports/dashboard_healthcheck.txt`                | A02, A03, A04           | PASS output plus dashboard screenshot                      | IMPLEMENTED / CAPTURE PENDING |
| 31 | Ledger Health               | Simulated ledger health metrics        | `src/publish_ledger_metrics.py`                                                             | InfluxDB ledger-health metrics                     | A01, A03, A04, A05      | Publication output + Grafana/FUXA evidence                 | IMPLEMENTED / CAPTURE PENDING |
| 32 | Examination Orchestration   | Complete laboratory execution          | `scripts/run_exam_demo.sh`, `scripts/run_complete_lab.sh`                                   | Combined logs and reports                          | A04                     | Complete examiner-demo terminal capture                    | IMPLEMENTED / CAPTURE PENDING |
| 33 | Deployment                  | AWS EC2 / Ubuntu execution             | `scripts/install_ec2_dependencies.sh`, `docker-compose.yml`                                 | Deployment output                                  | A02, A06                | EC2 environment + Docker Compose status                    | IMPLEMENTED / CAPTURE PENDING |
| 34 | Deployment                  | Docker + host-Python placement         | `docker-compose.yml`, `scripts/run_complete_lab.sh`                                         | Container/process evidence                         | A02, A06                | `docker compose ps` + host-service evidence                | IMPLEMENTED / CAPTURE PENDING |
| 35 | Future Architecture         | Hybrid OT/Edge + central cloud target  | A06 architecture document                                                                   | A06 architecture                                   | A06                     | Presentation/viva only; never claim current implementation | TARGET / NOT CURRENT          |

---

# 4. Architecture Cross-Reference

| Architecture                                          | Authoritative Question                                                       | Evidence Role                         |
| ----------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| **A01 — System Architecture**                         | What functional components make up Topic 127?                                | Master functional architecture        |
| **A02 — Network / Deployment Architecture**           | Where do components run and how are they connected?                          | Deployment / placement evidence       |
| **A03 — Data Flow Architecture**                      | How does data move, transform, store and produce evidence?                   | Data-flow evidence                    |
| **A04 — Process & Operational Workflow Architecture** | How do workflows and demonstrations execute?                                 | Operational / workflow evidence       |
| **A05 — Security Architecture & Trust Boundaries**    | Where are security controls, trust boundaries and security decisions?        | Security / trust evidence             |
| **A06 — Cloud / Hybrid Architecture**                 | How does the current EC2 platform evolve toward a future hybrid/cloud model? | Current-vs-target deployment evidence |

---

# 5. Core Examination Evidence Groups

## 5.1 Cleanroom / IoT / Monitoring

Primary repository components:

```text
src/sensor_simulator.py
src/edge_gateway.py
src/mqtt_to_influx.py
Mosquitto
InfluxDB
Grafana
```

Required runtime evidence:

```text
Sensor telemetry
↓
MQTT
↓
Edge validation
↓
InfluxDB
↓
Grafana
```

Primary architecture references:

```text
A01
A02
A03
A04
```

---

## 5.2 AI / ML

The repository contains separate executable AI/ML paths:

```text
Custom Edge AI
    =
rule-based inference

scikit-learn
    =
IsolationForest demonstration

TensorFlow/Keras
    =
Autoencoder demonstration
```

Primary files:

```text
src/edge_ai_engine.py
src/ml_anomaly_engine.py
src/tensorflow_anomaly_engine.py
```

Required evidence:

```text
scikit-learn incident output
TensorFlow/Keras incident output
Architecture explanation of separation
```

Do not present the three as one combined production ML pipeline.

---

## 5.3 Industrial Process Security

```text
OPC-UA Server
      ↓
OPC-UA Validator
      ↓
Process Security Evidence
```

and:

```text
Modbus Server
      ↓
Modbus Validator
      ↓
PLC / Process Security Evidence
```

Primary files:

```text
src/opcua_server.py
src/opcua_client_validator.py
src/modbus_server.py
src/modbus_client_validator.py
```

Required evidence:

```text
OPC-UA execution
OPC-UA validation
Modbus execution
Modbus validation
```

---

## 5.4 Recipe Integrity

```text
Approved Recipe
      ↓
SHA-256
      ↓
Integrity Comparison
   ↙          ↘
MATCH       MISMATCH
 ↓             ↓
PASS       Tamper Incident
               ↓
          Restoration
```

Primary evidence:

```text
PASS
Tamper detected
Approved recipe restored
PASS again
```

Primary files:

```text
src/recipe_integrity_check.py
data/approved_recipe.json
data/approved_recipe.sha256
reports/recipe_tamper_incidents.csv
```

---

## 5.5 Supply Chain

The implemented workflow is:

```text
Supplier Registry
      ↓
Material Batch
      ↓
Supplier Validation
      ↓
Material Risk Engine
      ↓
Risk / QMS Decision
      ↓
Hash-Chained Ledger
      ↓
Ledger Verification
      ↓
Evidence
```

Primary files:

```text
src/supplier_validator.py
src/material_risk_engine.py
src/supply_chain_ledger.py
src/ledger_verifier.py
```

Evidence:

```text
Supplier validation
Risk score
Risk decision
Ledger
Ledger verification
Tamper demonstration
Restored ledger
```

---

## 5.6 Worker Safety / EHS

Implemented event classes include:

```text
Gas exposure
PPE non-compliance
Chemical spill
Nanoparticle exposure
Hazardous waste condition
Emission threshold
```

Primary implementation:

```text
src/ehs_incident_engine.py
data/ehs_events.json
```

Evidence:

```text
EHS incident
Severity
Recommended action
Generated report
```

Important:

EHS output is evidence / recommended response logic.

Do not claim that the current repository directly controls physical evacuation systems.

---

## 5.7 Cybersecurity / IDS

Current Suricata scope:

```text
Controlled PCAP
      ↓
Suricata
      ↓
Rule Matching
      ↓
Security Evidence
```

Primary files:

```text
suricata/rules/topic127.rules
scripts/run_suricata_ids_demo.sh
scripts/validate_suricata_alerts.py
```

Important:

Suricata is a controlled demonstration.

It is not continuous enterprise production network monitoring.

---

## 5.8 DevSecOps

Implemented tools:

```text
Bandit
Semgrep
Trivy
```

Primary implementation:

```text
src/devsecops_scan.py
security/bandit.yml
security/semgrep.yml
security/trivy-ignore.txt
```

Primary output:

```text
reports/security_scan_report.txt
```

Required evidence:

```text
Bandit result
Semgrep result
Trivy result
Exit codes
```

Do not present this as an automatic CI/CD blocking gate unless such a gate is separately demonstrated.

---

## 5.9 Governance / Compliance

Implemented mechanisms:

```text
Operational incidents
      ↓
Incident Manager
      ↓
Incident Summary

Control events
      ↓
Audit Logger
      ↓
Audit Log

Defined evidence set
      ↓
Compliance Generator
      ↓
Compliance Report

Broader project evidence
      ↓
Final Report Generator
      ↓
Final Project Report
```

Primary files:

```text
src/incident_manager.py
src/audit_logger.py
src/compliance_report_generator.py
src/final_report_generator.py
```

---

# 6. Required Final Runtime Evidence Set

Before the final submission package is assembled, capture at least:

```text
01. docker compose ps
02. Cleanroom telemetry generation
03. MQTT telemetry
04. Edge Gateway validation
05. InfluxDB recent-data verification
06. Grafana populated dashboard
07. FUXA Operations Overview
08. scikit-learn anomaly output
09. TensorFlow/Keras anomaly output
10. OPC-UA server / validator
11. Modbus server / validator
12. Recipe integrity PASS
13. Recipe tamper detection
14. Recipe restoration PASS
15. Supplier validation
16. Material risk assessment
17. Supply-chain ledger
18. Ledger verification
19. Ledger tamper detection
20. Ledger restoration
21. EHS incidents
22. Suricata controlled IDS
23. Bandit
24. Semgrep
25. Trivy
26. Incident summary
27. Audit log
28. Compliance report
29. Dashboard healthcheck
30. Final project report
31. Complete examiner-demo execution
```

---

# 7. Recommended Screenshot Set

The final submission does not need screenshots of every individual source file.

Prioritize:

```text
Screenshot 01 — EC2 / Docker deployment
Screenshot 02 — Grafana Cleanroom Monitoring
Screenshot 03 — FUXA Operations Overview
Screenshot 04 — AI anomaly detection
Screenshot 05 — OPC-UA / Modbus validation
Screenshot 06 — Recipe tamper detection
Screenshot 07 — Supply-chain risk / ledger
Screenshot 08 — Ledger tamper + restoration
Screenshot 09 — EHS incident evidence
Screenshot 10 — Suricata IDS
Screenshot 11 — DevSecOps scan results
Screenshot 12 — Compliance / final evidence report
```

---

# 8. Final Submission Packaging Rule

Generated runtime evidence should be collected separately from the normal source repository.

Recommended structure:

```text
Topic127_Final_Submission/
│
├── 01_Presentation/
│
├── 02_Architecture/
│   ├── A01_System_Architecture/
│   ├── A02_Network_Architecture/
│   ├── A03_Data_Flow/
│   ├── A04_Process_Workflows/
│   ├── A05_Security_Architecture/
│   └── A06_Cloud_Hybrid_Architecture/
│
├── 03_Demonstration/
│
├── 04_Evidence/
│   ├── 01_Cleanroom/
│   ├── 02_AI_ML/
│   ├── 03_Process_Control/
│   ├── 04_Recipe_Integrity/
│   ├── 05_Supply_Chain/
│   ├── 06_EHS/
│   ├── 07_IDS/
│   └── 08_DevSecOps/
│
├── 05_Technical_Documentation/
│
├── 06_Reports/
│
├── 07_Code_Configuration/
│
└── 08_Submission_Index/
```

---

# 9. GitHub vs Local Evidence Rule

## GitHub

Keep the authoritative technical baseline:

```text
Source code
Configuration
Scripts
Tests
Architecture A01–A06
Runbooks
Technical documentation
Evidence Matrix
```

## Local final submission package

Keep examiner-facing runtime evidence:

```text
Screenshots
Execution logs
Generated reports
Grafana evidence
FUXA evidence
Terminal captures
Presentation PPTX
Presentation PDF
Final Submission Index
```

Do not unnecessarily duplicate generated runtime artifacts into GitHub.

---

# 10. Scope / Accuracy Rules

## Implemented

Use **IMPLEMENTED** when repository source/configuration and executable workflows support the capability.

## Simulated / Controlled

Clearly identify:

```text
Physical cleanroom sensors
Semiconductor equipment
PLC hardware
Industrial equipment
Worker-safety instrumentation
Industrial network traffic
Physical safety systems
```

when represented by software simulation or controlled test data.

## Recommended Actions

EHS, process-security and AI workflows may generate recommendations.

Do not claim current software directly actuates physical:

```text
Evacuation
Process isolation
Factory machinery
Safety interlocks
```

unless separately implemented and demonstrated.

## AI / ML

Maintain this distinction:

```text
Custom Edge AI
    =
rule-based

scikit-learn
    =
IsolationForest

TensorFlow/Keras
    =
Autoencoder
```

These are separate executable paths.

## IDS

Suricata is a controlled PCAP demonstration, not continuous production IDS monitoring.

## Compliance

Compliance reports provide evidence summaries.

They do not constitute regulatory certification.

## Future Cloud / Hybrid

A06 future architecture is:

```text
TARGET / NOT CURRENT
```

Current deployment remains:

```text
AWS EC2
Ubuntu
Docker Compose
Docker bridge network
Host-side Python services
```

---

# 11. Final Architecture Responsibility Model

```text
A01 → WHAT
A02 → WHERE
A03 → DATA FLOW
A04 → WORKFLOW
A05 → SECURITY
A06 → CLOUD / HYBRID EVOLUTION
```

The six architecture documents are therefore complementary rather than duplicate diagrams.

---

# 12. Final Evidence Principle

Every major examination claim should be defensible through:

```text
Architecture
     ↓
Repository implementation
     ↓
Execution
     ↓
Evidence output
     ↓
Examiner explanation
```

The goal is not merely to show that a file exists.

The goal is to demonstrate:

```text
"I can point to the architecture,
show the implementation,
execute the capability,
show its output,
and explain its limitations."
```

---

# 13. Final Evidence Readiness Status

```text
A01–A06 architecture                 ✅ LOCKED
Source code                           ✅ PRESENT
Configuration                         ✅ PRESENT
Execution scripts                     ✅ PRESENT
Tests                                 ✅ PRESENT
Runbooks                              ✅ PRESENT
Security tooling                      ✅ PRESENT
ML tooling                            ✅ PRESENT
Supply-chain tooling                  ✅ PRESENT
EHS tooling                           ✅ PRESENT
Compliance tooling                    ✅ PRESENT
Final report generator                ✅ PRESENT

Evidence Matrix                      ✅ THIS DOCUMENT
Runtime evidence                     ⏳ CAPTURE REQUIRED
Final screenshot set                 ⏳ CAPTURE REQUIRED
Final submission index               ⏳ TO CREATE
Final submission folder              ⏳ TO ASSEMBLE
Fresh EC2 reproducibility evidence    ⏳ TO PERFORM
```

---

## 14. Final Position

The repository is the authoritative technical implementation.

The A01–A06 architecture set is the locked architectural baseline.

The Evidence Matrix provides the traceability layer between:

```text
Topic 127
   ↓
Architecture
   ↓
Implementation
   ↓
Execution
   ↓
Evidence
   ↓
Viva Defence
```

No future architectural capability should be represented as currently implemented unless it is actually implemented and demonstrated in the repository.
