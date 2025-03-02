from opcua import Server, ua
import time
import threading

def start_opcua_server(port, shared_vars):
    """Starts an OPC UA server on the given port with test variables."""
    server = Server()
    server.set_endpoint(f"opc.tcp://localhost:{port}/")
    server.set_server_name(f"OPC-UA Test Server {port}")
    
    # Create a new namespace
    uri = f"urn:opcua:server:{port}"
    idx = server.register_namespace(uri)
    
    # Create an object to hold variables
    obj = server.nodes.objects.add_object(idx, "TestObject")
    
    # Define test variables
    dim = obj.add_variable(idx, "dim", 0, varianttype=ua.VariantType.UInt16)
    front = obj.add_variable(idx, "front", False, varianttype=ua.VariantType.Boolean)
    back = obj.add_variable(idx, "back", False, varianttype=ua.VariantType.Boolean)
    
    # Set variables writable
    dim.set_writable()
    front.set_writable()
    back.set_writable()
    
    # Store references for monitoring
    shared_vars[port] = {"dim": dim, "front": front, "back": back}
    
    server.start()
    print(f"OPC-UA Server started on port {port}")
    print(f"Namespace: {idx}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"Stopping server on port {port}")
        server.stop()

def monitor_servers(shared_vars):
    """Periodically prints the values of all server variables."""
    try:
        while True:
            print("\n--- Current OPC-UA Server Values ---")
            for port, vars in shared_vars.items():
                dim_value = vars["dim"].get_value()
                front_value = vars["front"].get_value()
                back_value = vars["back"].get_value()
                print(f"Server {port} -> dim: {dim_value}, front: {front_value}, back: {back_value}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping monitoring...")

if __name__ == "__main__":
    num_servers = int(input("Enter the number of OPC-UA servers to start: "))
    base_port = 4840  # Starting port
    
    shared_vars = {}
    threads = []
    for i in range(num_servers):
        port = base_port + i
        thread = threading.Thread(target=start_opcua_server, args=(port, shared_vars), daemon=True)
        thread.start()
        threads.append(thread)
    
    monitor_thread = threading.Thread(target=monitor_servers, args=(shared_vars,), daemon=True)
    monitor_thread.start()
    
    print(f"{num_servers} OPC-UA servers are running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all servers...")
