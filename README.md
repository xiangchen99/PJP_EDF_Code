# The Interface for the EDF

This combines Python with Arduino to control the Arduino digitally using user input in a GUI. 

## How to run the code:
First, make sure you are using the local Python 3.11 or newer (anything other than local might not work)

### In terminal:
1. pip install pyserial, serial, tkinter

2. Connect the Arduino and run the arduino code first
3. In the python code, change the COM3 into what port it is actually connected to (use the port detector script to find the port you want in the terminal) \n
     Note: On macs it could be /dev/cu.usbmodem1101 but on windows it might be COM#
5. Run the python code
