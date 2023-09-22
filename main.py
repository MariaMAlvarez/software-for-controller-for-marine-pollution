# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:00:09 2023

@author: MMA
"""

from Sensor import Sensor
import GUI

answer = False
while answer == False:
    answer = GUI.intro_window()

measurement1 = Sensor()
print('Sensor')

measurement1.set_analysis()
print('set anaysis')

measurement1.set_values()
print('set vg values')

measurement1.create_ard_file()
print('created')

answer = False
print('answer initial:', answer)

answer = measurement1.upload_arduino_file()
print('answer after:', answer)

while answer == False:
    answer = measurement1.arduino()
    
measurement1.create_csv_file()


