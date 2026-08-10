from opcua import Client

client = Client(
"opc.tcp://172.31.43.88:4840/topic127/opcua/server/"
)

client.connect()

nodes = {
    "RecipeID": "ns=2;s=RecipeID",
    "ProcessName": "ns=2;s=ProcessName",
    "Temperature": "ns=2;s=TemperatureSetpoint",
    "Pressure": "ns=2;s=PressureSetpoint",
    "EtchTime": "ns=2;s=EtchTimeSeconds",
    "Status": "ns=2;s=MachineStatus",
    "Security": "ns=2;s=SecurityState",
}

for name,nodeid in nodes.items():
    value=client.get_node(nodeid).get_value()
    print(name,value)

client.disconnect()
