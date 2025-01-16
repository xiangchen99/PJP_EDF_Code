# This is the previous code for the EDF. The new edition of the code is available at:
https://github.com/LanceGuy5/PJP_EDF_Code

## The Interface for the EDF

This combines Python with Arduino to control the Arduino digitally using user input in a GUI. 

## How to run the code:
First, make sure you are using the local Python 3.11 or newer (anything other than local might not work)

### In terminal:
1. pip install pyserial, serial, tkinter
### In Code:
2. Connect the Arduino and run the arduino code first
3. In the python code, change the COM3 into what port it is actually connected to (use the port detector script to find the port you want in the terminal) \
     Note: On macs it could be /dev/cu.usbmodem1101 but on windows it might be COM#
4. Make sure you kill the arduino program. For macs, the command is **sudo lsof /dev/cu.usbmodem1101** (if that is the port) as well as close the arduino program itself.
5. Run the python code


## Things to note:
The slider works perfectly, but **you need to enter the number twice in the textbox** for it to register


## New Web Dev Steps
pip install -r requirements.txt
