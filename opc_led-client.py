from opcua import Client
import time

def check_server_availability(servers):
    """Checks which OPC-UA servers are available."""
    print("\nChecking server availability...")
    available_servers = []
    
    for server_url in servers:
        client = Client(server_url)
        try:
            client.connect()
            print(f"✅ Server available: {server_url}")
            available_servers.append(server_url)
            client.disconnect()
        except Exception as e:
            print(f"❌ Server unreachable: {server_url} ({e})")
    
    print("\nServer availability check complete.")
    return available_servers

def read_variable_values(servers, namespaces, identifiers):
    """Reads values of 'dim', 'front', and 'back' from available OPC-UA servers."""
    print("\nReading variable values from servers...")
    for server_url in servers:
        client = Client(server_url)
        try:
            ns = namespaces[servers.index(server_url)]
            id = identifiers[servers.index(server_url)]
            client.connect()
            dim = client.get_node(f"{ns}{id[0]}").get_value()
            front = client.get_node(f"{ns}{id[1]}").get_value()
            back = client.get_node(f"{ns}{id[2]}").get_value()
            print(f"Server {server_url} -> dim: {dim}, front: {front}, back: {back}")
            client.disconnect()
        except Exception as e:
            print(f"❌ Failed to read from {server_url}: {e}")
    print("\nVariable reading complete.")

def reset_variables(servers, namespaces, identifiers):
    """Sets 'dim' to 0 and 'front' & 'back' to False on all available OPC-UA servers."""
    print("\nResetting variable values on servers...")
    for server_url in servers:
        client = Client(server_url)
        try:
            ns = namespaces[servers.index(server_url)]
            id = identifiers[servers.index(server_url)]
            client.connect()
            client.get_node(f"{ns}{id[0]}").set_value(0)
            client.get_node(f"{ns}{id[1]}").set_value(False)
            client.get_node(f"{ns}{id[2]}").set_value(False)
            print(f"✅ Variables reset on {server_url}")
            client.disconnect()
        except Exception as e:
            print(f"❌ Failed to reset variables on {server_url}: {e}")
    print("\nVariable reset complete.")

def set_variable_values(servers, namespaces=None, identifiers=None,dim_value=10000, delay=0):
    """Sets 'dim' to dim_value (default 10000) and 'front' & 'back' to True on all available OPC-UA servers with a delay between each server."""
    print("\nSetting variable values on servers...")
    print(f"Dim Value: {dim_value}, Delay: {delay}")
    for server_url in servers:
        client = Client(server_url)
        try:
            ns = namespaces[servers.index(server_url)]
            id = identifiers[servers.index(server_url)]
            client.connect()
            client.get_node(f"{ns}{id[0]}").set_value(dim_value)
            client.get_node(f"{ns}{id[1]}").set_value(True)
            client.get_node(f"{ns}{id[2]}").set_value(True)
            print(f"✅ Variables set on {server_url}")
            client.disconnect()
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Failed to set variables on {server_url}: {e}")
            time.sleep(delay)
    print("\nVariable set complete.")

def main():
    """Main function to handle user interaction."""
    # Hardcoded server addresses
    servers = [
        "opc.tcp://localhost:4840/",
        "opc.tcp://localhost:4841/",
        "opc.tcp://localhost:4842/",
        "opc.tcp://localhost:4843/",
        "opc.tcp://localhost:4844/",
        "opc.tcp://localhost:4845/",
        "opc.tcp://localhost:4846/",
        "opc.tcp://localhost:4847/",
        "opc.tcp://localhost:4848/",
        "opc.tcp://localhost:4849/",
        "opc.tcp://localhost:4850/",
        "opc.tcp://localhost:4851/"
    ]  
    
    # Hardcoded server nodes
    namespaces = [
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;",
        "ns=2;"
    ]
    
    # Hardcoded server identifiers
    identifiers = [
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"],
        ["i=2", "i=3", "i=4"]
    ]
    
    while True:
        print("\nSelect a mode:")
        print("1: Check Server availability")
        print("2: Read current values")
        print("3: All Off")
        print("4: All On")
        print("5: Set all at once to specific value")
        print("6: Set all timed to specific value")
        print("0: Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            check_server_availability(servers)
        elif choice == "2":
            read_variable_values(servers, namespaces, identifiers)
        elif choice == "3":
            reset_variables(servers, namespaces, identifiers)
        elif choice == "4":
            set_variable_values(servers, namespaces=namespaces, identifiers=identifiers)
        elif choice == "5":
            dim_value = int(input("Enter value brightness (0-10000): "))
            set_variable_values(servers, namespaces, identifiers, dim_value)
        elif choice == "6":
            dim_value = int(input("Enter value brightness (0-10000): "))
            delay = float(input("Enter delay between each server (in seconds): "))
            set_variable_values(servers, namespaces, identifiers, dim_value, delay)
        elif choice == "0":
            print("Exiting OPC-UA Client.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
