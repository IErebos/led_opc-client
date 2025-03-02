from opcua import Client
import time
import random

# OPC UA Server information
url = "opc.tcp://localhost:4840"
nodeId = "ns=2;i=2"

client = Client(url)
client.connect()
print("Connected to OPC UA server")
print("Press Ctrl+C to stop the client")

try:
    while True:
        value = random.randint(0, 100)
        

        node = client.get_node(nodeId)
        content = node.get_value()
        print(f"Current value of node {nodeId}: {content}")
        print("---")
        print(f"Sending value {value} to node {nodeId}")
        value = float(value)
        node.set_data_value(value)
        time.sleep(10)

except KeyboardInterrupt:
    pass

client.disconnect()
print("Disconnected from OPC UA server")