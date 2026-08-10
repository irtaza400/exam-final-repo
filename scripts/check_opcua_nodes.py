from opcua import Client

client = Client(
"opc.tcp://localhost:4840/topic127/opcua/server/"
)

client.connect()

print("Connected")

objects = client.get_objects_node()

def browse(node, level=0):

    print(
        "  "*level,
        node,
        node.get_browse_name()
    )

    for child in node.get_children():
        browse(child, level+1)


browse(objects)

client.disconnect()
