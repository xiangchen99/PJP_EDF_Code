import tkinter as tk
import serial
import time

# Define serial port and baud rate
arduino_port = "COM3"  # Replace with your actual port
arduino_baudrate = 9600
lastSentSignal = 0

# Initialize serial communication
ser = serial.Serial(arduino_port, arduino_baudrate)

# Define duty cycle bounds
MIN_PWM_BOUND = 60
MAX_PWM_BOUND = 90

# Define function to send duty cycle to Arduino
def send_duty_cycle():
    try:
        duty_cycle = int(entry_field.get())
        lastSentSignal = duty_cycle
        # validate duty cycle within limits
        if duty_cycle < MIN_PWM_BOUND or duty_cycle > MAX_PWM_BOUND:
            raise ValueError(f"Invalid duty cycle. Please enter a value between {MIN_PWM_BOUND} and {MAX_PWM_BOUND}.")
        # send duty cycle to Arduino
        ser.write(str(duty_cycle).encode())
        print(f"Sent duty cycle: {duty_cycle}")
        time.sleep(0.1)  # add a delay to give Arduino time to process the data
        update_last_sent_label()  # Update the label in the new window
    except ValueError as error:
        print(error)
        
# Define function to update the last sent label
def update_last_sent_label():
    last_sent_label.config(text=f"Last Sent Speed: {lastSentSignal}")
    
# Define tkinter window
window = tk.Tk()
window.title("EDF Speed Control")

# Define entry field and button
entry_field = tk.Entry(window, width=10)
entry_field.pack()

set_button = tk.Button(window, text="Set", command=send_duty_cycle)
set_button.pack()

# Create a new window for displaying the last sent speed
new_window = tk.Toplevel(window)
new_window.title("Current Speed")

# Label to display the last sent speed
last_sent_label = tk.Label(new_window, text=f"Current Speed: {lastSentSignal}")
last_sent_label.pack()

# Start main event loop
window.mainloop()

# Close serial communication
ser.close()
