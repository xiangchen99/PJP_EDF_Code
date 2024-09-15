import os
import django
import serial
import time

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arduino_monitor.settings")
django.setup()

from monitor.models import SensorData

# Configure the serial port and baud rate (ensure it matches your Arduino code)
SERIAL_PORT = 'COM5'  # Replace with your serial port (e.g., '/dev/ttyACM0' on Linux or 'COM3' on Windows)
BAUD_RATE = 9600

def read_from_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        value = float(line)
                        data = SensorData(value=value)
                        data.save()
                        print(f"Saved value: {value}")
                    except ValueError:
                        print(f"Invalid data: {line}")
            time.sleep(0.1)
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    read_from_serial()