# Topic 127 Version 3 Architecture

## Current Cloud / Deployment Foundation — Terraform Option B

The current examination deployment is provisioned using **Terraform Option B**.

```text
Terraform Option B
        |
        v
AWS VPC
        |
        v
Public Subnet
        |
        v
Internet Gateway + Public Route Table
        |
        v
AWS Security Group
        |
        v
AWS EC2 / Ubuntu
        |
        v
Docker Compose + Host-side Python
        |
        v
Topic 127 Laboratory
```

Terraform Option B is the current infrastructure provisioning layer. The Topic 127 application remains the existing Docker Compose and host-side Python laboratory.

### Network Exposure

External administrator access is limited to:

```text
22    SSH
3000  Grafana
1881  FUXA
```

The following laboratory endpoints remain EC2-local/internal:

```text
1883  Mosquitto MQTT
8086  InfluxDB
4840  OPC-UA
5020  Modbus
```

## Core Application Architecture



```text
Cleanroom Sensors / Simulators
        |
        v
MQTT Broker - Mosquitto
        |
        v
Python Ingestion Service
        |
        v
InfluxDB Time-Series Storage
        |
        v
Grafana Dashboard
```

Later phases add ML anomaly detection, OPC-UA, Modbus, EHS, supply chain, compliance and DevSecOps.

## Phase 3 — Process Control Security

```text
OPC-UA Server -> OPC-UA Validator -> process_security_incidents.csv
Modbus Server -> Modbus Validator -> modbus_security_incidents.csv
Approved Recipe -> SHA-256 Check -> recipe_tamper_incidents.csv
```

## TensorFlow/Keras Autoencoder Layer

```text
Cleanroom feature vector
  ├── particle_count
  ├── temperature
  ├── humidity
  ├── airflow
  ├── gas_ppm
  └── ppe_compliant
        ↓
TensorFlow/Keras Autoencoder
        ↓
Reconstruction Error Threshold
        ↓
Anomaly / Normal Decision
        ↓
reports/tensorflow_anomaly_incidents.csv
```
