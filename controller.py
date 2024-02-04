import tkinter as tk
import serial
import time

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

# Delay update mechanism
delayed_action_id = None

# Define function to send duty cycle to Arduino
def send_duty_cycle():
    global lastSentSignal
    try:
        duty_cycle = slider.get()
        lastSentSignal = duty_cycle
        if duty_cycle < MIN_PWM_BOUND or duty_cycle > MAX_PWM_BOUND:
            raise ValueError(f"Invalid duty cycle. Please enter a value between {MIN_PWM_BOUND} and {MAX_PWM_BOUND}.")
        ser.write(str(duty_cycle).encode())
        print(f"Sent duty cycle: {duty_cycle}")
        time.sleep(0.1)
        update_last_sent_label()
    except ValueError as error:
        print(error)

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
slider = tk.Scale(window, from_=MIN_PWM_BOUND, to=MAX_PWM_BOUND, orient='horizontal', label="Duty Cycle",
                  command=on_slider_change)
slider.pack(pady=20)

# Label to display the last sent speed
last_sent_label = tk.Label(window, text="Current Speed: 0")
last_sent_label.pack(pady=10)

# Start main event loop
window.mainloop()

# Close serial communication
ser.close()
