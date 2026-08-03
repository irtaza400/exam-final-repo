# FUXA SCADA/HMI Integration Plan

## Branch

`feature/fuxa-scada`

## Classification

FUXA is a real open-source SCADA/HMI application.

The connected OPC-UA process server is a custom educational industrial-process simulation.

## Primary Protocol

OPC-UA

## Planned FUXA Endpoint

`opc.tcp://host.docker.internal:4840/topic127/opcua/server/`

## Available OPC-UA Tags

- RecipeID
- ProcessName
- TemperatureSetpoint
- PressureSetpoint
- EtchTimeSeconds
- MachineStatus
- SecurityState

## Minimum HMI Screen

The first FUXA screen will show:

- process name;
- recipe ID;
- temperature setpoint;
- pressure setpoint;
- etch time;
- machine status;
- security state;
- normal condition;
- warning or alarm condition;
- operator acknowledgement area.

## FUXA Responsibilities

- real-time operator visualization;
- live OPC-UA tag display;
- process mimic;
- alarm indication;
- operator-facing HMI.

## Grafana Responsibilities

- historical time-series trends;
- monitoring KPIs;
- anomaly analytics;
- compliance and audit evidence.

## Deployment Boundary

FUXA runs as a Docker container.

The current OPC-UA simulator runs as a Python process on the Docker host. FUXA reaches it through `host.docker.internal`.

## Production Extension

A production implementation would use authenticated and encrypted OPC-UA connections inside a segmented industrial network and would connect to real PLCs or industrial gateways.
