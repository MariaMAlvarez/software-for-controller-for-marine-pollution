# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:15:13 2023

@author: MMA
"""

import serial.tools.list_ports
import time
import os

# set the path to your Arduino code directory
path = os.getcwd() + '\\RunMe'
arduino_code_dir = os.path.join(path, 'RunMe.ino')

# set the name of the Arduino board and the serial port it is connected to
board = "mega2560"
port = 'COM4'
'''
# Find the serial port of the Arduino board
ports = serial.tools.list_ports.comports()
for p in ports:
    if board in p.description:
        port = p.device
        break

if port is None:
    raise Exception("Cannot find a connected Arduino board")
'''

# Open the serial port to communicate with the Arduino board
ser = serial.Serial(port, 9600, timeout=1)

# Wait for the bootloader to start (may take a few seconds)
time.sleep(2)

# Send the program code to the Arduino board
with open(arduino_code_dir, 'rb') as f:
    data = f.read()
    ser.write(b'\x10') # send XON character
    ser.write(data)
    ser.write(b'\x11') # send XOFF character

# Close the serial port
ser.close()

#exit() # to shut down the kernel process
