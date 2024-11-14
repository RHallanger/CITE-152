import random
import time

# Network layout with 5 switches removed
devices = {
    "Desktop 1": {"type": "desktop", "ip": "192.168.1.2", "connected_devices": ["Switch 1"], "gateway": "Router 1"},
    "Desktop 2": {"type": "desktop", "ip": "192.168.1.3", "connected_devices": ["Switch 2"], "gateway": "Router 1"},
    "Desktop 3": {"type": "desktop", "ip": "192.168.1.4", "connected_devices": ["Switch 3"], "gateway": "Router 2"},
    "Desktop 4": {"type": "desktop", "ip": "192.168.1.5", "connected_devices": ["Switch 4"], "gateway": "Router 2"},
    "Desktop 5": {"type": "desktop", "ip": "192.168.1.6", "connected_devices": ["Switch 5"], "gateway": "Router 1"},
    "Desktop 6": {"type": "desktop", "ip": "192.168.1.7", "connected_devices": ["Switch 1"], "gateway": "Router 1"},
    "Desktop 7": {"type": "desktop", "ip": "192.168.1.8", "connected_devices": ["Switch 2"], "gateway": "Router 1"},
    "Desktop 8": {"type": "desktop", "ip": "192.168.1.9", "connected_devices": ["Switch 3"], "gateway": "Router 2"},
    "Desktop 9": {"type": "desktop", "ip": "192.168.1.10", "connected_devices": ["Switch 4"], "gateway": "Router 2"},
    "Desktop 10": {"type": "desktop", "ip": "192.168.1.11", "connected_devices": ["Switch 5"], "gateway": "Router 1"},
    "Switch 1": {"type": "switch", "connected_devices": ["Desktop 1", "Desktop 6", "Router 1"]},
    "Switch 2": {"type": "switch", "connected_devices": ["Desktop 2", "Desktop 7", "Router 1"]},
    "Switch 3": {"type": "switch", "connected_devices": ["Desktop 3", "Desktop 8", "Router 2"]},
    "Switch 4": {"type": "switch", "connected_devices": ["Desktop 4", "Desktop 9", "Router 2"]},
    "Switch 5": {"type": "switch", "connected_devices": ["Desktop 5", "Desktop 10", "Router 1"]},
    "Router 1": {"type": "router", "connected_devices": ["Switch 1", "Switch 2", "Switch 5"]},
    "Router 2": {"type": "router", "connected_devices": ["Switch 3", "Switch 4"]},
}

# Password hints based on device names
password_hints = {
    "Switch 1": "The second letter of the device name.",
    "Switch 2": "The third letter of the device name.",
    "Switch 3": "The fourth letter of the device name.",
    "Switch 4": "The fifth letter of the device name.",
    "Switch 5": "The sixth letter of the device name.",
    "Router 1": None,  # No password for the default gateway router
    "Router 2": None   # No password for Router 2 (can access directly)
}

# Simulate device interactions
def display_prompt(device_name, ip, device_type):
    print(f"\nYou are at {device_name} with IP {ip}.")
    print("Available commands:")
    print("1. 'show run' - View the device's interfaces and hints.")
    print("2. 'show lldp neighbors' - List connected devices.")
    print("3. 'show arp' (only for routers) - Show the ARP table.")
    print("4. 'end' - Exit and return to your desktop.")
    print("5. 'RDP <IP>' - Connect to another desktop via RDP.")
    print("6. 'ssh -l admin <IP>' - Connect to a device using SSH.")
    print("7. 'ipconfig /all' - Display the IP configuration of the desktop.")

# Execute commands based on device type and command
def execute_command(device, command, current_device):
    if command == "show run":
        if device["type"] == "switch":
            print("Listing interfaces... (Hint: the password is related to the second letter of the device name.)")
            print("eth0 - admin access")
            print(f"Password hint: {password_hints.get(device['connected_devices'][0], 'No hint available')}")
        elif device["type"] == "router":
            print("Router interfaces listed. Hint for the ARP table.")
        return True

    elif command == "show lldp neighbors":
        print("Listing connected devices:")
        for connected_device in device["connected_devices"]:
            print(f"- {connected_device}")
        return True

    elif command == "show arp":
        if device["type"] == "router":
            print("ARP table of the router (IP addresses):")
            # Simulate IPs in the network
            for i in range(1, 11):
                print(f"192.168.1.{i} - {random.choice(['Switch', 'Router', 'Desktop'])}")
        else:
            print("This command is only available on routers.")
        return True

    elif command == "ipconfig /all":
        # This command is only available on desktop devices
        if device["type"] == "desktop":
            print(f"IP Configuration for {current_device}:")
            print(f"IP Address: {device['ip']}")
            print(f"Default Gateway: {devices[device['gateway']]['ip']}")
        return True

    elif command == "end":
        print("You have exited the device.")
        return False
    
    return True

def ssh_connect(target_device_ip, password):
    # SSH logic - if password is correct, connect to the device
    for device_name, device_info in devices.items():
        if device_info["ip"] == target_device_ip:
            if device_name == "Router 1":  # No password required for Router 1 (default gateway)
                print(f"Connected to {device_name} (Router 1) via SSH without password.")
                return device_name
            # Check if the password is correct based on password hints
            required_password = password_hints.get(device_name)
            if required_password and password == required_password:
                print(f"Connected to {device_name} via SSH.")
                return device_name
            else:
                print("Incorrect password. Access denied.")
                return None
    print("Device with that IP not found.")
    return None

# Main game loop
def main():
    current_device = "Desktop 1"
    current_ip = devices[current_device]["ip"]
    visited_devices = set()

    while True:
        print(f"\nYou are currently at {current_device}. Your IP is {current_ip}.")
        
        # Check if the player has visited this device
        if current_device not in visited_devices:
            visited_devices.add(current_device)
            print(f"You've discovered {current_device} for the first time!")

        # Show the available commands for the current device
        display_prompt(current_device, current_ip, devices[current_device]["type"])

        # Input handling for commands
        command = input("> ").strip().lower()
        
        # Handle RDP command
        if command.startswith("rdp "):
            target_ip = command.split(" ")[1]
            for device_name, device in devices.items():
                if device["type"] == "desktop" and device["ip"] == target_ip:
                    if device_name != current_device:
                        current_device = device_name
                        current_ip = device["ip"]
                        print(f"\nYou are now connected to {device_name}.")
                    else:
                        print("You are already at this desktop.")
                    break
            else:
                print("Invalid IP address.")
            continue

        # Handle SSH command
        if command.startswith("ssh -l admin "):
            target_ip = command.split(" ")[-1]
            password = input("Enter password for admin: ").strip()
            new_device = ssh_connect(target_ip, password)
            if new_device:
                current_device = new_device
                current_ip = devices[current_device]["ip"]
            continue

        # Execute device-specific commands
        if devices[current_device]["type"] == "desktop":
            execute_command(devices[current_device], command, current_device
