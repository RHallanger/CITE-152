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
    "Router 1": {"type": "router", "ip": "192.168.1.1", "connected_devices": ["Switch 1", "Switch 2", "Switch 5"]},
    "Router 2": {"type": "router", "ip": "192.168.2.1", "connected_devices": ["Switch 3", "Switch 4"]},
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

# Show commands based on device type
def display_prompt(device_name, ip, device_type):
    print(f"\nYou are at {device_name} with IP {ip}.")
    print("Available commands:")

    if device_type == "desktop":
        print("1. 'ssh -l admin <IP>' - Connect to a device using SSH.")
        print("2. 'ipconfig' - Display the IP configuration of the desktop.")

    elif device_type == "switch":
        print("1. 'show run' - View the device's interfaces and hints.")
        print("2. 'show lldp neighbors' - List connected devices.")
        print("3. 'ssh -l admin <IP>' - Connect to a device using SSH.")

    elif device_type == "router":
        print("1. 'show run' - View the device's interfaces and hints.")
        print("2. 'show lldp neighbors' - List connected devices.")
        print("3. 'show arp' - Show the ARP table.")
        print("4. 'ssh -l admin <IP>' - Connect to a device using SSH.")
    
    print("5. 'end' - Exit and return to your desktop.")

# Execute commands based on device type and command
def execute_command(device, command, current_device):
    print(f"Executing command: {command} on device: {current_device} of type: {device['type']}")  # Debug print

    if command == "show run" and device["type"] in ["switch", "router"]:
        print("Listing interfaces... (Hint: the password is related to the second letter of the device name.)")
        print("eth0 - admin access")
        print(f"Password hint: {password_hints.get(current_device, 'No hint available')}")
        return True

    elif command == "show lldp neighbors" and device["type"] in ["switch", "router"]:
        print("Listing connected devices:")
        for connected_device in device["connected_devices"]:
            print(f"- {connected_device}")
        return True

    elif command == "show arp" and device["type"] == "router":
        print("ARP table of the router (IP addresses):")
        for i in range(1, 11):
            print(f"192.168.1.{i} - {random.choice(['Switch', 'Router', 'Desktop'])}")
        return True

    elif command == "ipconfig" and device["type"] == "desktop":
        print(f"IP Configuration for {current_device}:")
        print(f"IP Address: {device['ip']}")

        # Debug print: Check what gateway device is set
        gateway_device_name = device.get("gateway")
        print(f"Gateway device for {current_device}: {gateway_device_name}")  # Debug print

        gateway_device = devices.get(gateway_device_name)
        
        # Debug print: Check if gateway device is found and has an IP address
        if gateway_device:
            print(f"Gateway device found: {gateway_device_name}")
            print(f"Gateway device IP: {gateway_device.get('ip', 'No IP assigned')}")
        else:
            print("Gateway device not found!")

        # If the gateway is found, print its IP, otherwise show "Not configured"
        if gateway_device and "ip" in gateway_device:
            print(f"Default Gateway: {gateway_device['ip']}")
        else:
            print("Default Gateway: Not configured")
        return True

    elif command == "end":
        print("You have exited the device.")
        return False
    
    print("Invalid command for this device type.")
    return True

def ssh_connect(target_device_ip, password):
    print(f"Attempting SSH connection to {target_device_ip} with password: {password}")  # Debug print
    
    # Search for the device by IP address
    target_device = None
    for device_name, device_info in devices.items():
        if device_info["ip"] == target_device_ip:
            target_device = device_name
            break
    
    if not target_device:
        print(f"Device with IP {target_device_ip} not found.")  # Debug print for device not found
        return None

    # Check if the device is a router with no password requirement
    if target_device == "Router 1":  # No password for Router 1
        print(f"Connected to {target_device} (Router 1) via SSH without password.")
        return target_device
    
    # Password check (only for devices with a password hint)
    required_password = password_hints.get(target_device)
    if required_password:
        print(f"Password hint for {target_device}: {required_password}")  # Debug print for password check
        if password == required_password:
            print(f"Connected to {target_device} via SSH.")
            return target_device
        else:
            print("Incorrect password. Access denied.")  # Debug print for incorrect password
            return None
    else:
        # No password required for this device (or any other logic you may need to implement)
        print(f"No password required to connect to {target_device}.")
        return target_device


# Main game loop
def main():
    current_device = "Desktop 1"
    current_ip = devices[current_device]["ip"]
    visited_devices = set()

    while True:
        print(f"\nYou are currently at {current_device}. Your IP is {current_ip}.")
        
        if current_device not in visited_devices:
            visited_devices.add(current_device)
            print(f"You've discovered {current_device} for the first time!")

        display_prompt(current_device, current_ip, devices[current_device]["type"])

        command = input("> ").strip().lower()
        
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

        if command.startswith("ssh -l admin "):
    target_ip = command.split(" ")[-1]
    password = input("Enter password for admin: ").strip()

    # Debug print to check the IP and password entered
    print(f"SSH command received. Target IP: {target_ip}, Password entered: {password}")

    new_device = ssh_connect(target_ip, password)
    
    if new_device:
        current_device = new_device
        current_ip = devices[current_device]["ip"]
    continue

if __name__ == "__main__":
    main()
