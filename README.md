# Topic 127 — Advanced Nanotechnology Manufacturing Security Platform

## RQF Level 6 Diploma in Artificial Intelligence Operations (AIOps)

**Repository:** `exam-final-repo`

### Project Title

**Orchestrating Advanced Nanotechnology Manufacturing Security Platform with Cleanroom Monitoring, Process Control, and Environmental Safety for Semiconductor and Advanced Materials Production**

---

# 1. Project Overview

This repository implements an enterprise-style **educational and simulated nanotechnology manufacturing security platform** aligned with Topic 127 of the RQF Level 6 AIOps assessment.

The platform demonstrates the integration of:

* AI and machine-learning monitoring
* Cleanroom environmental monitoring
* IoT telemetry
* Edge Gateway processing
* Edge AI anomaly detection
* MQTT messaging
* Time-series data storage
* Grafana monitoring
* FUXA HMI/SCADA-style visualization
* OPC-UA process-control simulation
* Modbus/PLC simulation
* Recipe integrity verification
* Supply-chain traceability
* Material risk assessment
* Worker safety and PPE monitoring
* Environmental health and safety (EHS)
* Industrial cybersecurity
* Suricata IDS demonstration
* DevSecOps security scanning
* Audit logging
* Compliance evidence generation
* Automated reporting

The platform is designed for deployment on **AWS EC2 Ubuntu** using Docker Compose and Python-based simulators and validation services.

---

# 2. Important Scope Statement

This is an **educational simulation and proof-of-concept platform**.

The repository uses real open-source software such as:

* Docker
* Mosquitto
* InfluxDB
* Grafana
* FUXA
* TensorFlow/Keras
* scikit-learn
* OPC-UA libraries
* Modbus libraries
* Suricata
* Bandit
* Semgrep
* Trivy

Physical semiconductor fabrication equipment, cleanroom particle counters, PLCs, industrial sensors and manufacturing machines are represented by software simulators.

The architecture is intentionally designed so that simulated components could conceptually be replaced by real industrial devices in a controlled production architecture.

---

# 3. High-Level Architecture

```text
                    TOPIC 127 MANUFACTURING ENVIRONMENT
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ▼                                 ▼
     Cleanroom Sensors                  Industrial Process
      / Simulators                      Simulators
             │                                 │
             ▼                                 ├── OPC-UA
          MQTT                                  └── Modbus
             │
             ▼
      Edge Gateway
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
   Validation    Edge AI
       │           │
       └─────┬─────┘
             ▼
          InfluxDB
             │
       ┌─────┴──────┐
       │            │
       ▼            ▼
    Grafana        FUXA
   Monitoring   HMI / SCADA
       │            │
       └─────┬──────┘
             ▼
      Incident / Evidence
             │
   ┌─────────┼──────────┐
   │         │          │
   ▼         ▼          ▼
  EHS    Supply Chain  Security
   │         │          │
   │         ▼          ├── Suricata IDS
   │      Ledger         ├── Recipe Integrity
   │      Verification   └── DevSecOps
   │
   └─────────┬──────────┘
             ▼
      Compliance Reports
             │
             ▼
       Audit Evidence
```

---

# 4. Industrial Process Security

The platform simulates manufacturing process-control security through multiple layers.

## OPC-UA

OPC-UA is used to simulate industrial process variables and validate process behaviour.

Examples include:

* process monitoring
* equipment variables
* out-of-specification detection
* industrial protocol validation

## Modbus

Modbus is used to simulate PLC-style industrial communication and validation.

## Recipe Integrity

Approved manufacturing recipes are protected using SHA-256 integrity verification.

```text
Approved Recipe
      │
      ▼
SHA-256 Hash
      │
      ▼
Integrity Validation
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Valid    Tampered
 │         │
 ▼         ▼
Normal   Security Incident
```

This demonstrates the concept of detecting unauthorized recipe modification.

---

# 5. Cleanroom and Environmental Monitoring

The sensor simulation layer generates manufacturing-environment telemetry such as:

* particle count
* temperature
* humidity
* airflow
* gas/environmental indicators
* PPE compliance indicators

Telemetry is published through MQTT and processed by the platform.

The resulting data is stored in InfluxDB and visualized through Grafana.

---

# 6. Edge Gateway and Edge AI

The platform includes an Edge Gateway layer between telemetry generation and downstream processing.

The Edge Gateway provides a conceptual industrial edge-processing boundary for:

* telemetry validation
* message enrichment
* routing
* edge processing

The Edge AI component performs anomaly analysis close to the telemetry source.

The platform therefore demonstrates the AIOps concept:

```text
Telemetry
   ↓
Edge Processing
   ↓
AI Inference
   ↓
Anomaly Detection
   ↓
Incident / Alert
   ↓
Operational Response
```

---

# 7. AI and Machine Learning

The project contains both traditional machine-learning and TensorFlow/Keras anomaly-detection components.

## scikit-learn

Used for cleanroom anomaly detection and incident generation.

## TensorFlow/Keras

A TensorFlow/Keras autoencoder is used as an additional AI demonstration.

The feature set can include:

* particle count
* temperature
* humidity
* airflow
* gas measurements
* PPE compliance

The autoencoder calculates reconstruction error and uses a configured threshold to identify abnormal conditions.

---

# 8. Monitoring and Visualization

## InfluxDB

InfluxDB provides time-series storage for cleanroom and operational telemetry.

## Grafana

Grafana provides monitoring dashboards for:

* environmental conditions
* cleanroom telemetry
* anomalies
* operational indicators
* ledger health
* security/evidence metrics

## FUXA

FUXA provides an HMI/SCADA-style operational visualization layer.

It is used for educational demonstration of industrial monitoring and operational status visualization.

FUXA does not represent a production semiconductor-fab control system.

---

# 9. Supply Chain Security

The platform includes a simulated supply-chain security and traceability workflow.

```text
Supplier
   ↓
Material
   ↓
Material Batch
   ↓
Supplier Validation
   ↓
Material Risk Assessment
   ↓
Traceability Ledger
   ↓
Ledger Verification
   ↓
Tamper Detection
   ↓
Evidence / Report
```

The implementation includes simulated:

* approved suppliers
* material batches
* supplier validation
* material-risk rules
* ledger records
* ledger verification
* ledger tamper simulation
* ledger-health visualization

This demonstrates how supply-chain integrity can be integrated into a manufacturing security platform.

---

# 10. Environmental Health and Safety

The EHS layer demonstrates monitoring and evidence generation for:

* worker safety
* PPE compliance
* hazardous-material indicators
* environmental events
* safety incidents
* compliance evidence

The project is an educational simulation and does not replace certified industrial safety systems.

---

# 11. Industrial Cybersecurity

The platform demonstrates multiple security concepts.

## Recipe Security

SHA-256 integrity verification detects unauthorized recipe modification.

## Protocol Security

OPC-UA and Modbus validation demonstrate industrial protocol monitoring.

## IDS Demonstration

Suricata is available as an optional security demonstration profile.

The Suricata demonstration uses controlled test traffic/PCAP evidence rather than attempting to attack a real industrial system.

## DevSecOps

The repository includes security tooling such as:

* Bandit
* Semgrep
* Trivy

These tools provide static-analysis, dependency/container and security-evidence capabilities appropriate to the educational project.

---

# 12. DevSecOps and Evidence

The repository is designed around repeatable validation and evidence generation.

Evidence can include:

* execution logs
* anomaly reports
* incident reports
* process-security reports
* recipe-integrity reports
* supply-chain reports
* ledger verification
* compliance reports
* security scan results
* dashboard evidence

The objective is not simply to run software, but to demonstrate a traceable engineering workflow.

---

# 13. Technology Stack

| Layer               | Technology                  |
| ------------------- | --------------------------- |
| Cloud               | AWS EC2                     |
| OS                  | Ubuntu                      |
| Containers          | Docker / Docker Compose     |
| Messaging           | Mosquitto MQTT              |
| Time-Series DB      | InfluxDB                    |
| Monitoring          | Grafana                     |
| HMI / SCADA         | FUXA                        |
| Edge Processing     | Python Edge Gateway         |
| Edge AI             | Python / ML inference       |
| ML                  | scikit-learn                |
| Deep Learning       | TensorFlow / Keras          |
| Industrial Protocol | OPC-UA                      |
| PLC Protocol        | Modbus                      |
| Recipe Security     | SHA-256                     |
| IDS                 | Suricata                    |
| SAST                | Bandit / Semgrep            |
| Container Security  | Trivy                       |
| Automation          | Bash / Python               |
| Evidence            | Logs / CSV / JSON / Reports |

---

# 14. Repository Structure

```text
exam-final-repo/
│
├── config/
│   ├── approved_suppliers.json
│   ├── edge_ai.json
│   ├── edge_gateway.json
│   ├── material_risk_rules.json
│   └── mosquitto/
│
├── dashboards/
│   ├── json/
│   └── provisioning/
│
├── data/
│   ├── approved_recipe.json
│   ├── approved_recipe.sha256
│   ├── ehs_events.json
│   ├── material_batches.json
│   └── suppliers.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── EC2_DEPLOYMENT_GUIDE.md
│   ├── FINAL_PROJECT_OVERVIEW.md
│   ├── TOPIC127_MAPPING.md
│   ├── PHASE1_RUNBOOK.md
│   ├── PHASE2_RUNBOOK.md
│   ├── PHASE3_RUNBOOK.md
│   ├── PHASE4_RUNBOOK.md
│   ├── PHASE5_RUNBOOK.md
│   └── TROUBLESHOOTING.md
│
├── fuxa/
│
├── models/
│
├── reports/
│
├── scripts/
│   ├── run_complete_lab.sh
│   ├── run_exam_demo.sh
│   ├── install_ec2_dependencies.sh
│   ├── simulate_recipe_tamper.sh
│   ├── generate_suricata_test_pcap.py
│   └── FUXA / ledger / validation utilities
│
├── security/
│
├── src/
│   ├── sensor_simulator.py
│   ├── mqtt_to_influx.py
│   ├── edge_gateway.py
│   ├── edge_ai_engine.py
│   ├── ml_anomaly_engine.py
│   ├── tensorflow_anomaly_engine.py
│   ├── opcua_server.py
│   ├── opcua_client_validator.py
│   ├── modbus_server.py
│   ├── modbus_client_validator.py
│   ├── recipe_integrity_check.py
│   └── supply-chain / EHS / compliance components
│
├── tests/
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 15. Deployment Environment

The primary demonstration environment is:

```text
AWS EC2
   │
   ▼
Ubuntu
   │
   ▼
Python Virtual Environment
   │
   ▼
Docker Compose
   │
   ├── Mosquitto
   ├── InfluxDB
   ├── Grafana
   ├── FUXA
   └── Optional Suricata Security Demo
```

Python-based industrial and AI services run alongside the containerized infrastructure.

---

# 16. Initial EC2 Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/irtaza400/exam-final-repo.git
cd exam-final-repo
```

Make scripts executable:

```bash
chmod +x scripts/*.sh
```

Install required dependencies:

```bash
./scripts/install_ec2_dependencies.sh
```

Create the environment file if required:

```bash
cp .env.example .env
```

Review `.env` before starting the platform.

---

# 17. Start the Platform

The primary platform startup workflow is:

```bash
./scripts/run_complete_lab.sh
```

This workflow starts the infrastructure and supporting monitoring/validation services required by the laboratory demonstration.

---

# 18. One-Command Examiner Demonstration

For the formal demonstration, use:

```bash
./scripts/run_exam_demo.sh
```

The examiner demonstration is designed to:

1. Validate the repository
2. Activate the Python environment
3. Start Docker infrastructure
4. Start the complete laboratory workflow
5. Keep live monitoring available
6. Demonstrate recipe tampering
7. Generate compliance evidence
8. Generate final evidence/report outputs
9. Produce an examination summary
10. Preserve logs for evidence review

---

# 19. Verification

Individual phase verification scripts can be used when troubleshooting or demonstrating individual project phases.

Where available:

```bash
./scripts/verify_phase1.sh
./scripts/verify_phase2.sh
./scripts/verify_phase3.sh
./scripts/verify_phase4.sh
./scripts/verify_phase5.sh
./scripts/verify_tensorflow_addon.sh
```

The exact available scripts should be checked against the current repository before execution.

---

# 20. Default Services

| Service  | Default Endpoint       | Purpose                       |
| -------- | ---------------------- | ----------------------------- |
| MQTT     | `localhost:1883`       | IoT telemetry                 |
| InfluxDB | `http://<EC2-IP>:8086` | Time-series storage           |
| Grafana  | `http://<EC2-IP>:3000` | Monitoring                    |
| FUXA     | `http://<EC2-IP>:1881` | HMI/SCADA-style visualization |
| OPC-UA   | `<EC2-IP>:4840`        | Industrial process simulation |
| Modbus   | `<EC2-IP>:5020`        | PLC/process simulation        |

---

# 21. Demonstration Credentials

The repository provides educational default credentials through environment configuration.

These credentials are intended **only for the isolated educational laboratory**.

They must be changed before any production deployment.

Do not expose an educational EC2 deployment directly to the public internet without appropriate network controls.

---

# 22. Security Limitations

The default laboratory configuration intentionally simplifies several controls for demonstration purposes.

For example, the MQTT demonstration permits anonymous communication.

A production implementation would require controls such as:

* MQTT authentication
* TLS certificates
* certificate rotation
* network segmentation
* firewall restrictions
* least-privilege access
* secure OPC-UA configuration
* secure Modbus architecture or compensating controls
* secrets management
* hardened containers
* centralized SIEM integration
* secure audit storage
* production-grade identity and access management

These limitations are deliberate and form part of the project's engineering discussion.

---

# 23. Simulation vs Production

| Laboratory Component          | Production Equivalent               |
| ----------------------------- | ----------------------------------- |
| Sensor simulator              | Certified industrial sensor         |
| OPC-UA simulator              | Industrial equipment / gateway      |
| Modbus simulator              | PLC / RTU                           |
| FUXA                          | Industrial HMI/SCADA                |
| Simulated cleanroom           | ISO-controlled cleanroom            |
| Simulated supply-chain ledger | Enterprise traceability system      |
| Simulated EHS events          | EHS/industrial safety systems       |
| Suricata PCAP demo            | Network IDS monitoring              |
| Python AI engine              | Validated production ML/AI pipeline |

The project demonstrates architecture and engineering principles rather than claiming production certification.

---

# 24. Topic 127 Coverage

The implementation demonstrates the following Topic 127 areas:

### Cleanroom and Environmental Monitoring

* IoT monitoring
* particle/environmental simulation
* temperature monitoring
* humidity monitoring
* airflow monitoring
* contamination/anomaly detection

### AI / AIOps

* machine-learning anomaly detection
* TensorFlow/Keras anomaly detection
* edge processing
* automated incident generation
* operational monitoring

### Manufacturing Process Control

* OPC-UA
* Modbus
* process validation
* recipe integrity
* industrial process-security evidence

### Cybersecurity

* recipe tamper detection
* protocol validation
* IDS demonstration
* Bandit
* Semgrep
* Trivy
* audit/evidence generation

### Supply Chain

* supplier validation
* material validation
* material risk assessment
* traceability
* ledger verification
* tamper simulation

### EHS

* PPE compliance
* safety events
* hazardous-material indicators
* environmental events
* compliance evidence

### Operations

* Grafana
* FUXA
* logs
* reports
* repeatable demonstration scripts

---

# 25. Evidence Philosophy

The project follows an evidence-driven approach.

Each major engineering capability should produce observable evidence such as:

```text
Input
  ↓
Processing
  ↓
Detection / Validation
  ↓
Decision
  ↓
Incident / Alert
  ↓
Report / Dashboard Evidence
```

This allows the examiner to evaluate not only whether a component exists, but whether the component participates in a demonstrable operational workflow.

---

# 26. Academic Level

The repository is designed to support an **RQF Level 6 AIOps practical assessment**.

The project demonstrates application and integration of:

* AI
* automation
* cloud infrastructure
* monitoring
* industrial protocols
* cybersecurity
* DevSecOps
* environmental safety
* supply-chain security
* evidence-based operations

The repository should be evaluated as an educational engineering prototype rather than a certified semiconductor manufacturing control system.

---

# 27. Related Documentation

Additional project documentation is available under `docs/`, including:

* Architecture
* EC2 deployment
* project overview
* phase runbooks
* Topic 127 mapping
* TensorFlow add-on
* troubleshooting
* presentation guidance

Start with:

```text
docs/ARCHITECTURE.md
docs/TOPIC127_MAPPING.md
docs/EC2_DEPLOYMENT_GUIDE.md
docs/FINAL_PROJECT_OVERVIEW.md
```

---

# 28. Author

RQF Level 6 Diploma in AIOps

Educational / Practical Demonstration Repository
