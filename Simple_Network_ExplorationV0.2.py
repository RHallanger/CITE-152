import random
import time

# Network layout with devices
devices = {
    "Desktop 1": {"type": "desktop", "ip": "192.168.1.2", "connected_devices": ["Switch 1"]},
    "Desktop 2": {"type": "desktop", "ip": "192.168.1.3", "connected_devices": ["Switch 2"]},
    "Desktop 3": {"type": "desktop", "ip": "192.168.1.4", "connected_devices": ["Switch 3"]},
    "Desktop 4": {"type": "desktop", "ip": "192.168.1.5", "connected_devices": ["Switch 4"]},
    "Desktop 5": {"type": "desktop", "ip": "192.168.1.6", "connected_devices": ["Switch 5"]},
    "Desktop 6": {"type": "desktop", "ip": "192.168.1.7", "connected_devices": ["Switch 6"]},
    "Desktop 7": {"type": "desktop", "ip": "192.168.1.8", "connected_devices": ["Switch 7"]},
    "Desktop 8": {"type": "desktop", "ip": "192.168.1.9", "connected_devices": ["Switch 8"]},
    "Desktop 9": {"type": "desktop", "ip": "192.168.1.10", "connected_devices": ["Switch 9"]},
    "Desktop 10": {"type": "desktop", "ip": "192.168.1.11", "connected_devices": ["Switch 10"]},
    "Switch 1": {"type": "switch", "connected_devices": ["Desktop 1", "Router 1"]},
    "Switch 2": {"type": "switch", "connected_devices": ["Desktop 2", "Router 1"]},
    "Switch 3": {"type": "switch", "connected_devices": ["Desktop 3", "Router 2"]},
    "Switch 4": {"type": "switch", "connected_devices": ["Desktop 4", "Router 2"]},
    "Switch 5": {"type": "switch", "connected_devices": ["Desktop 5", "Router 1"]},
    "Switch 6": {"type": "switch", "connected_devices": ["Desktop 6", "Router 1"]},
    "Switch 7": {"type": "switch", "connected_devices": ["Desktop 7", "Router 2"]},
    "Switch 8": {"type": "switch", "connected_devices": ["Desktop 8", "Router 2"]},
    "Switch 9": {"type": "switch", "connected_devices": ["Desktop 9", "Router 1"]},
    "Switch 10": {"type": "switch", "connected_devices": ["Desktop 10", "Router 1"]},
    "Router 1": {"type": "router", "connected_devices": ["Switch 1", "Switch 2", "Switch 5", "Switch 6", "Switch 9", "Switch 10"]},
    "Router 2": {"type": "router", "connected_devices": ["Switch 3", "Switch 4", "Switch 7", "Switch 8"]},
}

# Password hints based on device names
password_hints = {
    "Switch 1": "First letter of the device name.",
    "Switch 2": "Second letter of the device name.",
    "Switch 3": "Third letter of the device name.",
    "Switch 4": "Fourth letter of the device name.",
    "Switch 5": "Fifth letter of the device name.",
    "Switch 6": "Sixth letter of the device name.",
    "Switch 7": "Seventh letter of the device name.",
    "Switch 8": "Eighth letter of the device name.",
    "Switch 9": "Ninth letter of the device name.",
    "Switch 10": "Tenth letter of the device name.",
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

# Execute commands based on device type and command
def execute_command(device, command, current_device):
    if command == "show run":
        if device["type"] == "switch":
            print("Listing interfaces... (Hint: the password is related to the first letter of the device name.)")
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

    elif command == "end":
        print("You have exited the device.")
        return False
    
    return True

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

        # Execute device-specific commands
        if devices[current_device]["type"] == "desktop":
            execute_command(devices[current_device], command, current_device)
        else:
            if not execute_command(devices[current_device], command, current_device):
                print("\nReturning to your desktop...")
                break  # Return to desktop if "end" is selected

        # Handle returning to desktop
        if command == "end":
            print("\nReturning to your desktop...")
            time.sleep(2)
            current_device = "Desktop 1"
            current_ip = devices[current_device]["ip"]
            visited_devices.clear()  # Clear visited devices to reset

if __name__ == "__main__":
    main()
