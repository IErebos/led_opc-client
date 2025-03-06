from opcua import Client, ua
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


def set_variable_values(servers, namespaces=None, identifiers=None,dim_value=10000, delay=0, state=True):
    """Sets 'dim' to dim_value (default 10000) and 'front' & 'back' to True on all available OPC-UA servers with a delay between each server."""
    print("\nSetting variable values on servers...")
    print(f"Dim Value: {dim_value}, Delay: {delay}")
    for server_url in servers:
        client = Client(server_url)
        try:
            ns = namespaces[servers.index(server_url)]
            id = identifiers[servers.index(server_url)]
            client.connect()
            var_type = client.get_node(f"{ns}{id[0]}").get_data_type_as_variant_type()
            client.get_node(f"{ns}{id[0]}").set_value(ua.DataValue(ua.Variant(dim_value, var_type)))
            client.get_node(f"{ns}{id[1]}").set_value(state)
            client.get_node(f"{ns}{id[2]}").set_value(state)
            print(f"✅ Variables set on {server_url} | {dim_value}")
            dim_read = client.get_node(f"{ns}{id[0]}").get_value()
            front_read = client.get_node(f"{ns}{id[1]}").get_value()
            back_read = client.get_node(f"{ns}{id[2]}").get_value()
            print(f"Set values | dim: {dim_read}, front: {front_read}, back: {back_read}")
            client.disconnect()
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Failed to set variables on {server_url}: {e}")
            time.sleep(delay)
    print("\nVariable set complete.")

def set_variable_values_manually(servers, namespaces=None, identifiers=None,dim_value=10000, state=True):
    """Sets 'dim' to dim_value (default 10000) and 'front' & 'back' to True on all available OPC-UA servers with a delay between each server."""
    print("\nSetting variable values on servers...")
    print(f"Dim Value: {dim_value}")
    for server_url in servers:
        input("Make input for next.")
        client = Client(server_url)
        try:
            ns = namespaces[servers.index(server_url)]
            id = identifiers[servers.index(server_url)]
            client.connect()
            var_type = client.get_node(f"{ns}{id[0]}").get_data_type_as_variant_type()
            client.get_node(f"{ns}{id[0]}").set_value(ua.DataValue(ua.Variant(dim_value, var_type)))
            client.get_node(f"{ns}{id[1]}").set_value(state)
            client.get_node(f"{ns}{id[2]}").set_value(state)
            print(f"✅ Variables set on {server_url} | {dim_value}")
            dim_read = client.get_node(f"{ns}{id[0]}").get_value()
            front_read = client.get_node(f"{ns}{id[1]}").get_value()
            back_read = client.get_node(f"{ns}{id[2]}").get_value()
            print(f"Set values | dim: {dim_read}, front: {front_read}, back: {back_read}")
            client.disconnect()
        except Exception as e:
            print(f"❌ Failed to set variables on {server_url}: {e}")
    print("\nVariable set complete.")

def set_all_white_leds(servers, namespaces=None, identifiers=None, state=True):
    """Sets all modules to the defined state (True/False)"""
    print("\nSetting relais variable values on servers...")
    print(f"Set to value: {state}")
    for server_url in servers:
        client = Client(server_url)
        try:
            ns = namespaces[servers.index(server_url)]
            id = identifiers[servers.index(server_url)]
            client.connect()
            client.get_node(f"{ns}{id[1]}").set_value(state)
            client.get_node(f"{ns}{id[2]}").set_value(state)
            front_read = client.get_node(f"{ns}{id[1]}").get_value()
            back_read = client.get_node(f"{ns}{id[2]}").get_value()
            print(f"Set values | front: {front_read}, back: {back_read}")
            client.disconnect()
        except Exception as e:
                print(f"❌ Failed to set relais variables on {server_url}: {e}")

def main():
    """Main function to handle user interaction."""
    # Hardcoded server addresses
    servers = [
        "opc.tcp://192.168.7.10:4840/",
        "opc.tcp://192.168.7.30:4840/",
        "opc.tcp://192.168.7.50:4840/",
        "opc.tcp://192.168.7.70:4840/",
        "opc.tcp://192.168.7.90:4840/",
        "opc.tcp://192.168.7.110:4840/",
        "opc.tcp://192.168.7.130:4840/",
        "opc.tcp://192.168.7.150:4840/",
        "opc.tcp://192.168.7.170:4840/",
        "opc.tcp://192.168.7.190:4840/",
        "opc.tcp://192.168.7.210:4840/",
        "opc.tcp://192.168.7.230:4840/"
    ]  
    
    # Hardcoded server nodes
    namespaces = [
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;",
        "ns=4;"
    ]
    
    # Hardcoded server identifiers
    identifiers = [
        # 10:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.aout_LEDDimmer", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_lightinFront", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_lightingBack"],
        # 30:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.aout_ledBrightness", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_ledFront", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_ledBack"],
        # 50:
        ["s=|var|CPX-E-CEC-M1-PN.Application.GVL_IO.aout_ledBrightness", "s=|var|CPX-E-CEC-M1-PN.Application.GVL_IO.dout_ledFront", "s=|var|CPX-E-CEC-M1-PN.Application.GVL_IO.dout_ledBack"],
        # 70:
        ["s=|var|CPX-E-CEC-C1-PN.Application.IoConfig_Globals_Mapping.aoutLedDriver", "s=|var|CPX-E-CEC-C1-PN.Application.IoConfig_Globals_Mapping.b_R01_LEDfront", "s=|var|CPX-E-CEC-C1-PN.Application.IoConfig_Globals_Mapping.b_R01_LEDback"],
        # 90:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.aout_LEDDimmer", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_LEDFrontRelais", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_LEDBackRelais"],
        #110:
        ["s=|var|CPX-E-CEC-M1-EP.Application.IoConfig_Globals_Mapping.aoutLedDriver", "s=|var|CPX-E-CEC-M1-EP.Application.IoConfig_Globals_Mapping.b_R01_LEDfront", "s=|var|CPX-E-CEC-M1-EP.Application.IoConfig_Globals_Mapping.b_R02_LEDback"],
        # 130:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.uintLedDriver", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_Relay1", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_Relay2"],
        # 150:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.aout_ledBrightness", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_ledFront", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_ledBack"],
        # 170:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.i_L01_LEDDriver", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.b_R01_LEDfront", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.b_R02_LEDback"],
        # 190:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.i_L01_LEDDriver", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.b_R06_LEDfront", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.b_R07_LEDback"],
        # 210:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.aout_LED_Driver", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_LED_Front", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.dout_LED_Back"],
        # 230:
        ["s=|var|CPX-E-CEC-C1.Application.GVL_IO.i_L01_LEDDriver", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.b_R01_LEDfront", "s=|var|CPX-E-CEC-C1.Application.GVL_IO.b_R02_LEDback"]
    ]
    
    while True:
        print("\nSelect a mode:")
        print("1: Check Server availability")
        print("2: Read current values")
        print("3: All Off")
        print("4: All On")
        print("5: Set all at once to specific value")
        print("6: Set all timed to specific value")
        print("7: Set all manually one by one to specific value")
        print("8: Just disable LED Relais")
        print("0: Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            check_server_availability(servers)
        elif choice == "2":
            read_variable_values(servers, namespaces, identifiers)
        elif choice == "3":
            set_variable_values(servers, namespaces=namespaces, identifiers=identifiers, dim_value=0, state=False)
        elif choice == "4":
            set_variable_values(servers, namespaces=namespaces, identifiers=identifiers, dim_value=10000, state=True)
        elif choice == "5":
            dim_value = int(input("Enter value brightness (0-10000): "))
            set_variable_values(servers, namespaces, identifiers, dim_value, state=True)
        elif choice == "6":
            dim_value = int(input("Enter value brightness (0-10000): "))
            delay = float(input("Enter delay between each server (in seconds): "))
            set_variable_values(servers, namespaces, identifiers, dim_value, delay, state=True)
        elif choice == "7":
            dim_value = int(input("Enter value brightness (0-10000): "))
            set_variable_values_manually(servers, namespaces, identifiers, dim_value, state=True)
        elif choice == "8":
            state_value = int(input("Select value (1: True | 2: False): "))
            if state_value == 1:
                set_all_white_leds(servers, namespaces, identifiers, state=True)
            elif state_value == 2:
                set_all_white_leds(servers, namespaces, identifiers, state=False)
            else:
                print("Wrong input!")
        elif choice == "0":
            print("Exiting OPC-UA Client.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
