from opcua import Server
import time
from datetime import datetime

server = Server()
server_url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(server_url)

name = "Dummy OPC Server #1"
namespace = server.register_namespace(name)

node = server.get_objects_node()
param = node.add_object(namespace, "Parameters")

var = param.add_variable(namespace, "Temperature", 0.0)
var.set_writable()

server.start()
print("OPC UA Server started at {}".format(server_url))
print("Press Ctrl+C to stop the server")

try:
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current time:", current_time)
        value = var.get_value()
        print("Current value:", value)
        time.sleep(1)

except KeyboardInterrupt:
    pass

server.stop()
print("OPC UA Server stopped")