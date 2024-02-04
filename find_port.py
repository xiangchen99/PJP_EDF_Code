import serial.tools.list_ports

def list_all_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} - {hwid}")

# Call the function to list all ports
list_all_ports()
