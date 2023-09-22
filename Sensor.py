# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:01:38 2023

@author: MMA
"""

import time, GUI, File, Graph
import pandas as pd


class Sensor:
    '''
    Sensor: a class that representsa sensor with various atributes and methods.
    Atributes:
        self.name: str 
            representing the name of the sensor with the format 'YYYYMMDD-HHMMSS'.
        self.port: str 
            representing the COM port of the connected sensor.
        self.analysis: str 
            representing the type of analysis for that measurement; either Vcg
            or time analysis.
        self.vcg_initial_value: float 
            representing the initial value of Vcg.
        self.vcg_final_value: int
            representing the final value of Vcg.
        self.cycles: int 
            representing the number of cycles to perform.
        self.points_per_step: int 
            representing the number of data points to collect per sweep step.
        self.vcg_value: float
            representing the value of Vcg for the real time analysis.
    '''

    def __init__(self):
        self.name = time.strftime("%Y%m%d-%H%M%S")
        self.port = ''
        self.analysis = ''
        self.wait_time = 0

        # vg analysis values
        self.vcg_initial_value = 0
        self.vcg_final_value = 0
        self.cycles = 0
        self.points_per_step = 0

        # time analysis values
        self.vcg_value = 0
        self.time_value = 0
        self.points_per_second = 0

    def set_analysis(self):
        '''
        set_analysis: . -> .
        Description:This method calls a GUI function to prompt the user to
        choose the type of analysis that is going to be made. It then stores
        that str in the atribute self.analysis.
        '''
        self.analysis = GUI.get_analysis_type()
        print(self.analysis)

    def set_values(self):
        '''
        set_values: . -> .
        Description: This method calls a GUI function to prompt the user to 
        input the parameters used for the intended analysis. It first checks
        which type of analysis choosen from the atribute self.analysis. It then
        retrieves the values from the GUI function and stores them into their 
        corresponding atributes. For the the Vcg sweep it calls the 
        get_vcg_measurement_values fuction and the values are: Vcg initial value,
        Vg final value, number of cycles, and number of datapoints per step.
        For  the real time analysis, it calls the get_time_measurement_values
        function and the values are: Vcg steady value, time the analysis 
        should last and number of points per second.
        '''
        if self.analysis == 'vcg_analysis':
            self.vcg_initial_value, self.vcg_final_value, self.cycles, self.points_per_step = GUI.get_vcg_measurement_values()
        else:
            self.vcg_value, self.time_value, self.points_per_second = GUI.get_time_measurement_values()

    def create_ard_file(self):
        '''
        create_ard_file: . -> .
        Description: This method calls a File function to create an arduino file
        considering the values set by the user from previous fuctions. It first 
        checks which type of analysis is being requested by the user and either 
        calls the create_ino_vcg_analysis_file function for the Vcg sweep 
        analysis, or the create_ino_time_analysis_file function for the real time
        analysis.'''
        if self.analysis == 'vcg_analysis':
            self.wait_time = File.create_ino_vcg_analysis_file(
                self.vcg_initial_value, self.vcg_final_value, self.cycles, self.points_per_step)
        else:
            File.create_ino_time_analysis_file(self.vcg_value)

    def upload_arduino_file(self):
        '''
        arduino: . -> bool
        Description: This method calls the GUI function upload_arduino to prompt 
        the user to upload the "RunMe.ino" file to the connected Arduino board. 
        If the upload is successful, the method returns True, otherwise it 
        repeats the prompt until a successful upload is performed. Returns a 
        boolean indicating whether the "RunMe.ino" file was successfully 
        uploaded to the connected Arduino board.
        '''
        ans = False
        while ans == False:
            ans = GUI.upload_arduino()
        return ans

    def create_csv_file(self):
        '''
        create_csv_file: .->.
        Description: This method prompts the user to select the COM port using 
        the GUI.get_com_port() function, thhen calls the File function 
        create_csv to create a CSV file  with the name 'self.name.csv' with 
        the data acquired from the connected Arduino. It also sets the 
        self.port atribute of the Sensor to the selected COM port.
        '''
        self.port = GUI.get_com_port()
        File.create_csv_file(self.name, self.port)

    def plots(self):
        '''
        curves: . -> .
        Description: Plots and displays the curves for the sensor using the 
        curves function from Graph.'''
        df = pd.read_csv(self.name)
        GUI.make_plots(df, self.points_per_step, self.cycles)
        
