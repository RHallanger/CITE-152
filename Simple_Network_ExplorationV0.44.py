import random
import time

# Network layout with 5 switches removed
devices = {
    "Desktop 1": {
        "type": "desktop",
        "ip": "192.168.2.2",  # Updated to match 192.168.2.0 scheme
        "connected_devices": ["Switch 1"],
        "gateway": "Router 2"
    },
    "Desktop 2": {
        "type": "desktop",
        "ip": "192.168.2.3",  # Updated to match 192.168.2.0 scheme
        "connected_devices": ["Switch 1"],
        "gateway": "Router 2"
    },
    "Desktop 3": {
        "type": "desktop",
        "ip": "192.168.2.4",  # Updated to match 192.168.2.0 scheme
        "connected_devices": ["Switch 2"],
        "gateway": "Router 2"
    },
    "Desktop 4": {
        "type": "desktop",
        "ip": "192.168.2.5",  # Updated to match 192.168.2.0 scheme
        "connected_devices": ["Switch 2"],
        "gateway": "Router 2"
    },
    "Switch 1": {
        "type": "switch",
        "ip": "192.168.1.12",
        "connected_devices": ["Desktop 1", "Desktop 2"],
        "gateway": "Router 1",
        "password": "HTTP",  # Password for Switch 1
        "password_hint": "Port number for HTTP traffic"  # Hint for Switch 1
    },
    "Switch 2": {
        "type": "switch",
        "ip": "192.168.1.13",
        "connected_devices": ["Desktop 3", "Desktop 4"],
        "gateway": "Router 1",
        "password": "HTTPS",  # Password for Switch 2
        "password_hint": "Port number for secure HTTP traffic"  # Hint for Switch 2
    },
    "Switch 3": {
        "type": "switch",
        "ip": "192.168.1.14",
        "connected_devices": ["Desktop 5", "Desktop 6"],
        "gateway": "Router 1",
        "password": "FTP",  # Password for Switch 3
        "password_hint": "Port number for File Transfer Protocol"  # Hint for Switch 3
    },
    "Switch 4": {
        "type": "switch",
        "ip": "192.168.1.15",
        "connected_devices": ["Desktop 7", "Desktop 8"],
        "gateway": "Router 1",
        "password": "SSH",  # Password for Switch 4
        "password_hint": "Port number for Secure Shell connections"  # Hint for Switch 4
    },
    "Switch 5": {
        "type": "switch",
        "ip": "192.168.1.16",
        "connected_devices": ["Desktop 9", "Desktop 10"],
        "gateway": "Router 1",
        "password": "TELNET",  # Password for Switch 5
        "password_hint": "Port number for Telnet connections"  # Hint for Switch 5
    },
    "Router 1": {
        "type": "router",
        "ip": "192.168.1.1",
        "connected_devices": ["Switch 1", "Switch 2", "Switch 3", "Switch 4", "Switch 5", "Router 2"],
        "gateway": None
    },
    "Router 2": {
        "type": "router",
        "ip": "192.168.2.1",
        "connected_devices": ["Desktop 1", "Desktop 2", "Desktop 3", "Desktop 4"],
        "gateway": "Router 1"
    }
}

# Password hints based on device names
password_hints = {
    "Switch 1": "80 all caps",
    "Switch 2": "443 all caps",
    "Switch 3": "21 all caps",
    "Switch 4": "22 all caps",
    "Switch 5": "23 all caps",
    "Router 1": None,  # No password for the default gateway router
    "Router 2": None   # No password for Router 2 (can access directly)
}

# Simulate device interactions
def display_prompt(device_name, ip, device_type, visited_devices):
    print(f"\nYou are at {device_name} with IP {ip}.")
    print("Available commands:")

    if device_type == "desktop":
        print("1. 'ssh -l admin <IP>' - Connect to a device using SSH.")
        print("2. 'ipconfig' - Display the IP configuration of the desktop.")
        print("3. 'rdp <IP>' - Connect to another desktop using RDP.")
        # Show "end" only if the device is not Desktop 1
        if device_name != "Desktop 1":
            print("4. 'end' - Return to Desktop 1.")

    elif device_type == "switch":
        print("1. 'show run' - View the device's interfaces and hints.")
        print("2. 'show lldp neighbors' - List connected devices.")
        print("3. 'ssh -l admin <IP>' - Connect to a device using SSH.")
        print("4. 'progress' - Show how many devices have been visited out of the total network.")
        print("5. 'end' - Return to Desktop 1.")

    elif device_type == "router":
        print("1. 'show run' - View the device's interfaces and hints.")
        print("2. 'show lldp neighbors' - List connected devices.")
        print("3. 'show arp' - Show the ARP table.")
        print("4. 'ssh -l admin <IP>' - Connect to a device using SSH.")
        print("5. 'progress' - Show how many devices have been visited out of the total network.")
        print("6. 'end' - Return to Desktop 1.")


# Implement the "progress" command in the main loop to track visited devices
def execute_command(device, command, current_device, visited_devices):
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
                    # Only print devices that have an IP address
                    if 'ip' in device_info and device_info['ip']:
                        print(f"{device_name} {device_info['ip']}")
                    else:
                        print(f"{device_name} has no IP address.")
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

        elif command == "progress":
            # Show progress of visited devices
            total_devices = len(devices)
            visited_count = len(visited_devices)
            print(f"Progress: {visited_count}/{total_devices} devices visited.")
            return True

        elif command == "end":
            # Return the player to Desktop 1 instead of ending the game
            print("Returning to Desktop 1...")
            current_device = "Desktop 1"
            current_ip = devices[current_device]["ip"]
            return current_device, current_ip  # Return to update main loop with new location

        return True

    except Exception as e:
        print(f"Error occurred while executing command '{command}': {e}")
        return False


# Function for SSH connection with exception handling
def ssh_connect(target_ip, password):
    try:
        # Find the device by IP
        for device_name, device_info in devices.items():
            if device_info["ip"] == target_ip:
                # If the device is passwordless (password is None), allow empty password
                if device_info.get("password") is None and password == "":
                    print(f"Successfully connected to {device_name} (passwordless connection)!")
                    return device_name  # Return the connected device name

                # For devices with passwords, check if the entered password is correct
                elif device_info.get("password") == password:
                    print(f"Successfully connected to {device_name}!")
                    return device_name  # Return the connected device name
                
                # If the password doesn't match and the device requires one, show an error
                else:
                    raise ValueError("Incorrect password.")

        # If no device with the target IP is found, show an error
        raise ValueError("Device not found.")
    except ValueError as ve:
        print(f"Connection failed: {ve}")
    except Exception as e:
        print(f"An error occurred during SSH connection: {e}")
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
        display_prompt(current_device, current_ip, devices[current_device]["type"], visited_devices)

        command = input("> ").strip().lower()

        # Handle RDP command
        if command.startswith("rdp "):
            target_ip = command.split(" ")[1]
            
            # Check if the target IP belongs to a desktop device
            for device_name, device in devices.items():
                if device["type"] == "desktop" and device["ip"] == target_ip:
                    if device_name != current_device:
                        current_device = device_name
                        current_ip = device["ip"]
                        print(f"\nYou are now connected to {device_name} via RDP.")
                    else:
                        print("You are already at this desktop.")
                    break
            else:
                print("Invalid IP address or target is not a desktop.")
            continue

        # Handle SSH command
        elif command.startswith("ssh -l admin "):
            target_ip = command.split(" ")[-1]
            password = input("Enter password for admin (press Enter if none): ").strip()
            new_device = ssh_connect(target_ip, password)
            if new_device:
                current_device = new_device
                current_ip = devices[current_device]["ip"]
            continue

        # Execute commands
        result = execute_command(devices[current_device], command, current_device, visited_devices)
        
        # If execute_command returns a new device location (from "end" command), update location
        if isinstance(result, tuple):
            current_device, current_ip = result
        elif not result:
            break

if __name__ == "__main__":
    main()
