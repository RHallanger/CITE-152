import random
import time

# Revised network layout
devices = {
    # Desktops connected to Router 2
    "Desktop 1": {"type": "desktop", "ip": "192.168.2.2", "connected_devices": ["Switch 1"], "gateway": "Router 2"},
    "Desktop 2": {"type": "desktop", "ip": "192.168.2.3", "connected_devices": ["Switch 2"], "gateway": "Router 2"},
    "Desktop 3": {"type": "desktop", "ip": "192.168.2.4", "connected_devices": ["Switch 4"], "gateway": "Router 2"},
    "Desktop 4": {"type": "desktop", "ip": "192.168.2.5", "connected_devices": ["Switch 5"], "gateway": "Router 2"},
    "Switch 1": {"type": "switch", "ip": "192.168.1.12", "connected_devices": ["Desktop 1"], "gateway": "Router 1"},
    "Switch 2": {"type": "switch", "ip": "192.168.1.13", "connected_devices": ["Desktop 2"], "gateway": "Router 1"},
    "Switch 3": {"type": "switch", "ip": "192.168.1.14", "connected_devices": [], "gateway": "Router 1"},
    "Switch 4": {"type": "switch", "ip": "192.168.1.15", "connected_devices": ["Desktop 3"], "gateway": "Router 2"},
    "Switch 5": {"type": "switch", "ip": "192.168.1.16", "connected_devices": ["Desktop 4"], "gateway": "Router 2"},
    "Router 1": {"type": "router", "ip": "192.168.1.1", "connected_devices": ["Switch 1", "Switch 2", "Switch 3", "Router 2"], "gateway": None},
    "Router 2": {"type": "router", "ip": "192.168.2.1", "connected_devices": ["Switch 4", "Switch 5"], "gateway": "Router 1"}
}

password_hints = {
    "Switch 1": "80 all caps",
    "Switch 2": "443 all caps",
    "Switch 3": "21 all caps",
    "Switch 4": "22 all caps",
    "Switch 5": "23 all caps",
    "Router 1": None,
    "Router 2": None
}

# Simplified ssh_connect function
def ssh_connect(target_ip, password):
    try:
        for device_name, device_info in devices.items():
            if device_info["ip"] == target_ip:
                if device_info.get("password") == password or device_info.get("password") is None:
                    print(f"Connected to {device_name} successfully!")
                    return device_name
                else:
                    print("Incorrect password.")
                    return None
        print("Device not found.")
        return None
    except Exception as e:
        print(f"Error in SSH connection: {e}")
        return None

# Function to execute commands
def execute_command(device, command, current_device, visited_devices):
    try:
        if command == "show run":
            print(f"Displaying interfaces for {device['type']} ({current_device})...")
            for i, conn_device in enumerate(device["connected_devices"]):
                intf_type = random.choice(["FastEthernet", "GigabitEthernet"])
                intf_id = f"{random.randint(0, 2)}/0/{random.randint(1, 24)}"
                hint = password_hints.get(conn_device, "No hint")
                print(f"{intf_type} {intf_id} connected to {conn_device} - Hint: {hint}")

        elif command == "show lldp neighbors":
            print("Connected devices:")
            for conn_device in device["connected_devices"]:
                print(f"Neighbor: {conn_device}")

        elif command == "show arp" and device["type"] == "router":
            print("ARP Table:")
            for dev_name, dev_info in devices.items():
                print(f"{dev_name} - {dev_info['ip']}")

        elif command == "ipconfig" and device["type"] == "desktop":
            print(f"IP: {device['ip']}")
            gw_device = devices.get(device.get("gateway"))
            if gw_device:
                print(f"Gateway: {gw_device['ip']}")

        elif command == "progress":
            print(f"Visited {len(visited_devices)} out of {len(devices)} devices.")
        
        elif command == "end":
            return ("Desktop 1", devices["Desktop 1"]["ip"])
        
        return True
    except Exception as e:
        print(f"Error in execute_command: {e}")
        return False

# Main simulation loop
def main():
    current_device = "Desktop 1"
    visited_devices = set()

    while True:
        device_info = devices[current_device]
        visited_devices.add(current_device)
        display_prompt(current_device, device_info["ip"], device_info["type"], visited_devices)
        
        command = input("> ").strip().lower()
        if command.startswith("ssh -l admin "):
            target_ip = command.split()[-1]
            password = input("Enter password: ")
            new_device = ssh_connect(target_ip, password)
            if new_device:
                current_device = new_device
            continue
        elif command.startswith("rdp "):
            target_ip = command.split()[-1]
            new_device = next((d for d, info in devices.items() if info["type"] == "desktop" and info["ip"] == target_ip), None)
            if new_device:
                current_device = new_device
            else:
                print("Invalid desktop IP.")
            continue
        
        result = execute_command(device_info, command, current_device, visited_devices)
        if isinstance(result, tuple):
            current_device, _ = result
        elif not result:
            break

if __name__ == "__main__":
    main()
