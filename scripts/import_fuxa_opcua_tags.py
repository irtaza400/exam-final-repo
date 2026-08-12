"""Import Topic127 OPC-UA tags into FUXA device."""

from __future__ import annotations

import json
import urllib.request


FUXA_URL = "http://127.0.0.1:1881"

DEVICE_ID = "d_598f1c2f-8c5748c5"


TAGS = {
    "RecipeID": {
        "id": "ns=2;s=RecipeID",
        "name": "RecipeID",
        "label": "RecipeID",
        "type": "string",
        "address": "ns=2;s=RecipeID",
    },
    "ProcessName": {
        "id": "ns=2;s=ProcessName",
        "name": "ProcessName",
        "label": "ProcessName",
        "type": "string",
        "address": "ns=2;s=ProcessName",
    },
    "TemperatureSetpoint": {
        "id": "ns=2;s=TemperatureSetpoint",
        "name": "TemperatureSetpoint",
        "label": "TemperatureSetpoint",
        "type": "number",
        "address": "ns=2;s=TemperatureSetpoint",
    },
    "PressureSetpoint": {
        "id": "ns=2;s=PressureSetpoint",
        "name": "PressureSetpoint",
        "label": "PressureSetpoint",
        "type": "number",
        "address": "ns=2;s=PressureSetpoint",
    },
    "EtchTimeSeconds": {
        "id": "ns=2;s=EtchTimeSeconds",
        "name": "EtchTimeSeconds",
        "label": "EtchTimeSeconds",
        "type": "number",
        "address": "ns=2;s=EtchTimeSeconds",
    },
    "MachineStatus": {
        "id": "ns=2;s=MachineStatus",
        "name": "MachineStatus",
        "label": "MachineStatus",
        "type": "string",
        "address": "ns=2;s=MachineStatus",
    },
    "SecurityState": {
        "id": "ns=2;s=SecurityState",
        "name": "SecurityState",
        "label": "SecurityState",
        "type": "string",
        "address": "ns=2;s=SecurityState",
    },
    "MachineStatusCode": {
        "id": "ns=2;s=MachineStatusCode",
        "name": "MachineStatusCode",
        "label": "MachineStatusCode",
        "type": "number",
        "address": "ns=2;s=MachineStatusCode",
    },
    "SecurityStateCode": {
        "id": "ns=2;s=SecurityStateCode",
        "name": "SecurityStateCode",
        "label": "SecurityStateCode",
        "type": "number",
        "address": "ns=2;s=SecurityStateCode",
    },
}


def request(method, url, payload=None):

    data = None
    headers = {}

    if payload:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


project = request(
    "GET",
    f"{FUXA_URL}/api/project"
)


device = project["devices"][DEVICE_ID]


device["tags"] = TAGS


payload = {
    "cmd": "set-device",
    "data": device,
}


response = request(
    "POST",
    f"{FUXA_URL}/api/project",
    payload,
)


print("FUXA OPC-UA tag import completed")
print("Device:", device["name"])
print("Tags:", len(TAGS))
print(response)
