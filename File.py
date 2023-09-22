# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:12:53 2023

@author: MMA
"""

import serial
import os
import shutil
import pandas as pd


def create_ino_vcg_analysis_file(vcg_initial_value, vcg_final_value, cycles, points_per_step):
    '''
    create_ard_file: float, float, int, int -> .
    Description: Creates a new Arduino file based on a template file 
    ('copy.ino') and sets the necessary parameters (wiper position, number 
    of cycles, number of sweep steps, number of datapoints per step) 
    according to the current sensor instance. The new file is saved in a 
    new directory called 'RunMe', which is created in the current working 
    directory. If the directory already exists, it is deleted and a new 
    one is created.
    '''
    arduino_folder_path = os.getcwd() + '\\RunMe'
    arduino_file_path = os.path.join(arduino_folder_path, 'RunMe.ino')

    if os.path.isdir(arduino_folder_path):
        shutil.rmtree(arduino_folder_path)
    os.mkdir(arduino_folder_path)

    wiper_initial_value = 99 - round(vcg_initial_value * 99/5)
    wiper_final_value = 99 - round(vcg_final_value * 99/5)
    wiper_steps = wiper_initial_value - wiper_final_value

    wait_time = (610 + ((cycles*100)*(wiper_steps*50)
                 * (points_per_step*10)))/1000
    print('wait_time', wait_time)

    with open('vcg_analysis.ino', 'r') as infile, open(arduino_file_path, 'w') as outfile:
        lines = infile.read()
        lines = lines.replace('vcg_initial_value', str(wiper_initial_value))
        lines = lines.replace('wiper_steps', str(wiper_steps))
        lines = lines.replace('num_cycles', str(cycles))
        lines = lines.replace('num_data_points', str(points_per_step))
        outfile.write(lines)
    return wait_time


def create_arduino_time_analysis_file():
    return ''


def create_csv_file(name, COMPORT):
    '''
    create_csv: str, str ->
    Description: This function creates a CSV file from data acquired from a 
    serial port.  then reads in data from the port, which is 
    wxpected to be in the form of semicolon-separated values. The function 
    creates a pandas DataFrame from the data and converts the columns with 'V'
    in their name to their corresponding voltage values. The resulting 
    DataFrame is saved to a CSV file with the specified name. The function 
    returns the selected COM port as a string.
    '''
    BAUDRATE = 9600
    ser = serial.Serial(COMPORT, BAUDRATE, timeout=1)
    ser.reset_input_buffer()

    while True:
        line = ser.readline().decode().rstrip()
        line = line.replace(';/n', '')
        print('loading')
        if line and line.startswith('Time'):
            header = line.split(';')
            df = pd.DataFrame(columns=header)
        elif line and not line.startswith('fim'):
            line = line.split(';')
            df = pd.concat([df, pd.DataFrame([line], columns=header)])
        elif line.startswith('fim'):
            break
    ser.close()

    df = df.astype(int)
    df = df.set_index('Time')
    df = df.apply(lambda x: x*(5/1023) if x.name.startswith('V') else x)
    print(df)
    folder_path = os.getcwd() + '\\data'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_name = name + '.csv'
    file_path = os.path.join(folder_path, csv_name)
    df.to_csv(file_path, index=False)
