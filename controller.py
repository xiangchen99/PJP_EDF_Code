import tkinter as tk
import serial
import time
import threading
from tkinter import StringVar

# Define serial port and baud rate
arduino_port = "/dev/cu.usbmodem1101"  # Replace with your actual port
arduino_baudrate = 9600

# Initialize serial communication
ser = serial.Serial(arduino_port, arduino_baudrate)

# Define duty cycle bounds
MIN_PWM_BOUND = 60
MAX_PWM_BOUND = 90

# Global variable to store the last sent signal
lastSentSignal = 0

# Delay update mechanism for slider
delayed_action_id = None

# Define function to send duty cycle to Arduino
def send_duty_cycle(event=None):
    global lastSentSignal
    # Validate and set the duty cycle from the entry field if possible
    try:
        duty_cycle_text = entry_field.get()
        if duty_cycle_text:  # Check if the entry field is not empty
            duty_cycle = int(duty_cycle_text)
            if MIN_PWM_BOUND <= duty_cycle <= MAX_PWM_BOUND:
                # Update the slider and the global lastSentSignal
                slider.set(duty_cycle)
                lastSentSignal = duty_cycle
                ser.write(str(duty_cycle).encode())
                print(f"Sent duty cycle: {duty_cycle}")
            else:
                raise ValueError(f"Value out of range: Please enter a value between {MIN_PWM_BOUND} and {MAX_PWM_BOUND}.")
        else:  # Fallback to slider value if no textbox input
            duty_cycle = slider.get()
            lastSentSignal = duty_cycle
            ser.write(str(duty_cycle).encode())
            print(f"Sent duty cycle: {duty_cycle}")

        time.sleep(0.1)  # Short delay for Arduino processing
        update_last_sent_label()  # Update the label with the last sent signal
        entry_field.delete(0, tk.END)  # Clear the entry field after sending

    except ValueError as error:  # Handle errors from invalid entry inputs
        print(error)
        entry_field.delete(0, tk.END)  # Clear the entry field if error



def update_last_sent_label():
    last_sent_label.config(text=f"Last Sent Speed: {lastSentSignal}")

# Function to handle slider changes with a delay
def on_slider_change(val):
    global delayed_action_id
    if delayed_action_id:
        window.after_cancel(delayed_action_id)
    delayed_action_id = window.after(300, send_duty_cycle)  # 300ms delay

# Define tkinter window
window = tk.Tk()
window.title("EDF Speed Control")

# Autoscale window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Define slider
slider = tk.Scale(window, from_=MIN_PWM_BOUND, to=MAX_PWM_BOUND, orient='horizontal', label="Duty Cycle", command=on_slider_change)
slider.pack(pady=20)

# Define entry field and Set button for direct input
entry_field = tk.Entry(window, width=10)
entry_field.pack(pady=10)

set_button = tk.Button(window, text="Set", command=send_duty_cycle)
set_button.pack(pady=5)

# Getting received data
received_data_var = StringVar()
received_data_label = tk.Label(window, textvariable=received_data_var, text="Waiting for Arduino data...")
received_data_label.pack(pady=10)

def read_from_arduino():
    while True:
        if ser.inWaiting() > 0:
            data_line = ser.readline().decode('utf-8').strip()
            received_data_var.set(f"Data from Arduino: {data_line}")

# Start the thread for reading serial data
thread = threading.Thread(target=read_from_arduino, daemon=True)
thread.start()

# Bind the Enter key to the send_duty_cycle function for the entry field
entry_field.bind('<Return>', lambda event=None: send_duty_cycle())

# Label to display the last sent speed
last_sent_label = tk.Label(window, text="Current Speed: 0")
last_sent_label.pack(pady=10)

# Start main event loop
window.mainloop()

# Close serial communication
ser.close()
