import random
import time
import pdb  # Import pdb for debugging

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

# Simulate device interactions
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
        
# Simulate device interactions and command handling
def execute_command(device, command, current_device):
    print(f"Executing command: {command} on device: {current_device} of type: {device['type']}")

    try:
        if command == "show run":
            # For show run, create a list of interfaces and their descriptions
            interfaces = []
            if device["type"] == "switch" or device["type"] == "router":
                print(f"Showing interfaces for {device['type']}...")

                # Generate consistent interface information for show run
                for i in range(3):  # Limiting to 3 interfaces for simplicity
                    interface_type = random.choice(["FastEthernet", "GigabitEthernet"])
                    interface_id = f"{random.randint(0, 2)}/0/{random.randint(0, 24)}"
                    interfaces.append((interface_type, interface_id))

                    print(f"[{interface_type}] interface {interface_id}")
                    print(f"Description: {password_hints.get(device['connected_devices'][i % len(device['connected_devices'])], 'No hint available')}")

            device['interfaces'] = interfaces  # Store interfaces for use in show lldp neighbors
            return True

        elif command == "show lldp neighbors":
            if "interfaces" in device:  # Ensure we have interface information from show run
                print("Listing connected devices:")
                for i, connected_device in enumerate(device["connected_devices"]):
                    # Use the interfaces from show run to display the same ones in show lldp neighbors
                    interface_type, interface_id = device['interfaces'][i % len(device['interfaces'])]
                    print(f"{connected_device} connected on {interface_type} {interface_id}")
            return True

        elif command == "show arp":
            if device["type"] == "router":
                print("ARP table of the router (IP addresses):")
                
                # Loop over all devices and print their name and corresponding IP address
                for device_name, device_info in devices.items():
                    print(f"{device_name} {device_info['ip']}")
            else:
                print("This command is only available on routers.")
            return True

        elif command == "ipconfig":
            if device["type"] == "desktop":
                print(f"IP Configuration for {current_device}:")
                print(f"IP Address: {device['ip']}")
                gateway_device = devices.get(device['gateway'])
                if gateway_device:
                    print(f"Default Gateway: {gateway_device['ip']}")
                else:
                    print("No gateway defined.")
            return True

        elif command == "end":
            print("You have exited the device.")
            return False

        return True

    except Exception as e:
        print(f"Error occurred while executing command '{command}': {e}")
        return False

def ssh_connect(target_device_ip, password, verbose=False):
    # SSH logic - if password is correct, connect to the device
    if verbose:
        print(f"Attempting SSH connection to IP: {target_device_ip}")  # Debug print
    
    for device_name, device_info in devices.items():
        # Print debug info only if verbosity is enabled
        if verbose:
            print(f"Checking device {device_name}, IP: {device_info.get('ip')}, Target IP: {target_device_ip}")  # Debug print

        if device_info.get("ip") == target_device_ip:  # Ensure we check using .get() to prevent KeyError
            if verbose:
                print(f"Found device: {device_name} with IP: {target_device_ip}")  # Debug print
            
            # Special handling for Router 1: no password is required
            if device_name == "Router 1":
                if password == "":  # Allow connection without password
                    print(f"Connected to {device_name} (Router 1) via SSH without password.")
                    return device_name
                else:
                    print("Password should not be provided for Router 1.")
                    return None

            # For other devices, check if password is correct
            required_password = password_hints.get(device_name)
            if required_password:
                if password == required_password:
                    print(f"Connected to {device_name} via SSH.")
                    return device_name
                else:
                    print("Incorrect password. Access denied.")
                    return None
            else:
                # If no password required for this device, but none was entered, deny
                if password == "":
                    print(f"No password required for {device_name}, but none provided. Access denied.")
                    return None

    print("Device with that IP not found.")  # Debug print if device is not found
    return None

def main():
    current_device = "Desktop 1"
    current_ip = devices[current_device]["ip"]
    visited_devices = set()

    while True:
        print(f"\nYou are currently at {current_device}. Your IP is {current_ip}.")
        
        if current_device not in visited_devices:
            visited_devices.add(current_device)
            print(f"You've discovered {current_device} for the first time!")

        # Show available commands based on device type
        display_prompt(current_device, current_ip, devices[current_device]["type"])

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
        elif command.startswith("ssh -l admin "):
            target_ip = command.split(" ")[-1]
            password = input("Enter password for admin: ").strip()
            new_device = ssh_connect(target_ip, password)
            if new_device:
                current_device = new_device
                current_ip = devices[current_device]["ip"]
            continue

        # Execute commands
        if not execute_command(devices[current_device], command, current_device):
            break

if __name__ == "__main__":
    main()
