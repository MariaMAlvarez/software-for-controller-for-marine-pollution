# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:30:00 2023

@author: MMA
"""
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, messagebox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
#import random
#import shutil
from PIL import Image, ImageTk
import Graph
#import matplotlib.pyplot as plt
from tkinter import filedialog
import os


TEXT_FONT = ('Arial', 13)
TITLE_FONT = ('Arial', 17)
LETTER_COLOR = '#0a1929'
BACKGROUND_COLOR = '#83a2de'
SCREEN_WIDTH = None
SCREEN_HEIGHT = None
VCG_MAXIMUM_VALUE = 5


def get_screen_size():
    """
    get_screen_size: . -> .
    Description: This function creates a hidden temporary tkinter window with 
    tkinter library to retrieve the screen width and height in pixels. Uses 
    The global variables SCREEN_WIDTH and SCREEN_HEIGH are then updated with 
    the obtained values. The temporary root window is then destroyed after the 
    variables are updated.
    """
    global SCREEN_WIDTH, SCREEN_HEIGHT
    root = tk.Tk()
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()
    root.destroy()


get_screen_size()


def intro_window():
    main_win = tk.Tk()
    main_win.title("Introduction")
    
    def submit():
        global ans
        ans = True
        main_win.destroy()
    
    window_width, window_height = 500, 340
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=15, pady=15)
    title = "Welcome"
    text = "This is the CMISFET Software for the SeaSenseX project. \n\n Here you will be able to use your CMISET sensor to test pH in samples. At the end you will be able to see your results in plots. \n\n Simply connect the sensor to the PCB, the PCB to the Arduino and the Arduino to your computer. \n\n All the next steps are explained and there will always be a 'HELP' button in case you have any questions."
    # title
    ttk.Label(main_win, text=title, padding=5,
              font=TITLE_FONT, background=BACKGROUND_COLOR,
              foreground=LETTER_COLOR).grid(row=0, column=0,
                                            sticky='n', pady=(0, 5))
    ttk.Label(main_win, text=text, 
              font = TEXT_FONT, background = BACKGROUND_COLOR, 
              foreground = LETTER_COLOR,  wraplength=460, justify='center').grid(row = 1, column = 0, pady=(5,10))
    
    # button style
    style = ttk.Style()
    style.configure('Custom.TButton', font = TEXT_FONT,
                    background = BACKGROUND_COLOR, foreground = LETTER_COLOR,
                    relief = 'raised')
    # button
    button_1 = ttk.Button(main_win, text = 'Continue', width = 10,
                          command = submit, style = 'Custom.TButton')
    button_1.grid(row = 2, column = 0, pady = (5, 0))

    main_win.mainloop()
    return ans

def get_analysis_type():
    """
    get_analysis_type: . -> .
    Description: This function creates a GUI window for users to choose between 
    two options of analysis. A Help button is provided to give further 
    instructions to the user. The interface includes labels, imaged, and buttons, 
    and it uses a custom style for the buttons.
    """
    
    main_win = tk.Tk()
    main_win.title("Select type of analysis")

    window_width, window_height = 565, 290
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=15, pady=15)
    
    def show_help():
        help_text = """
        This window allows you to choose the type of analysis.
        Click on 'Voltage Sweep' for an analysis that varies the voltage along time, and 'Real-time Monitoring' an analysis that has a constat voltage along time.
        """
        messagebox.showinfo("Help", help_text)
    
    help_button = ttk.Button(
        main_win, text="Help", command=show_help, width=7, style='Custom.TButton')
    help_button.grid(row=0, column=1, sticky='ne')
    
    
    def vcg_analysis():
        global ANALYSIS_TYPE
        ANALYSIS_TYPE = 'vcg_analysis'
        main_win.destroy()

    def time_analysis():
        global ANALYSIS_TYPE
        ANALYSIS_TYPE = 'time_analysis'
        main_win.destroy()

    # title
    ttk.Label(main_win, text='Choose the type of analysis:', padding=5,
              font=TITLE_FONT, background=BACKGROUND_COLOR,
              foreground=LETTER_COLOR).grid(row=0, column=0, columnspan=2,
                                            sticky='n', pady=(0, 25))
    # set button style
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT,
                    background=BACKGROUND_COLOR, foreground=LETTER_COLOR,
                    relief='raised')
    
    button_vadc_vcg_analysis = ttk.Button(
        main_win, text='Voltage Sweep', width=25,
        command=vcg_analysis,  style='Custom.TButton')
    button_vadc_vcg_analysis.grid(row=2, column=0, padx=(10, 10))
    
    button_vadc_time_analysis = ttk.Button(
        main_win, text='Real-time Monitoring', width=25, command=time_analysis,
        style='Custom.TButton')
    button_vadc_time_analysis.grid(row=2, column=1, padx=(30, 10))

    # sweep analysis image
    vcg_analysis_image = Image.open("images//vcg_analysis.png")
    vcg_analysis_image = vcg_analysis_image.resize((150, 150))
    vcg_analysis_photo = ImageTk.PhotoImage(vcg_analysis_image)
    vcg_analysis_image_label = tk.Label(
        main_win, image=vcg_analysis_photo, bg=BACKGROUND_COLOR)
    vcg_analysis_image_label.grid(row=1, column=0, padx=(10, 10))

    # time analysis image
    time_analysis_image = Image.open("images//time_analysis.png")
    time_analysis_image = time_analysis_image.resize((150, 150))
    time_analysis_photo = ImageTk.PhotoImage(time_analysis_image)
    time_analysis_image_label = tk.Label(
        main_win, image=time_analysis_photo, bg=BACKGROUND_COLOR)
    time_analysis_image_label.grid(row=1, column=1, padx=(30, 10))

    main_win.mainloop()
    return ANALYSIS_TYPE

def get_vcg_measurement_values():
    """
    get_vcg_measurement_values: . -> [float, float, int, int]
    Description: This function creates a GUI window using tkinter to prompt the
    user to input in the Vcg sweep parameters. There are four different input 
    values, namely the Vcg initial value, Vcg final value, number of cycles,
    sweep steps, and number of datapoints per step. The user can then submit 
    the values or cancel the input operation using the respective buttons. If 
    the user cancels the input operation, an empty list is returned. The 
    interface includes labels, an image, text entries and buttons, and it uses 
    a custom style for the buttons.
    """
    main_win = tk.Tk()
    main_win.title("Select Vcg sweep parameters")

    window_width, window_height = 460, 260
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=15, pady=15)
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT)

    values_list = []

    def submit_values():
        try:
            vcg_initial_value = float(vcg_initial_entry.get())
            vcg_final_value = float(vcg_final_entry.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter a valid number. Vcg can be a natural or decimal (separated by '.') value.")
            return
        try:
            cycles_value = int(cycles_entry.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter a valid number. Cycles needs to be a natural value.")
            return
        try:
            data_value = int(data_entry.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter a valid number. Data points needs to be a natural value.")
            return
        if vcg_initial_value < 0 or vcg_final_value <= 0 or cycles_value <= 0 or data_value <= 0:
            messagebox.showerror(
                "Input Error", "Please enter positive values.")
            return
        if vcg_initial_value >= vcg_final_value:
            messagebox.showerror(
                "Input Error", 
                "Vcg initial value needs to be smaller than Vcg final value.")
            return
        if vcg_final_value > VCG_MAXIMUM_VALUE:
            error_message = "Vcg final value needs to be smaller or equal to " + \
                str(VCG_MAXIMUM_VALUE) + " V."
            messagebox.showerror("Input Error", error_message)
            return
        values_list.extend(
            [vcg_initial_value, vcg_final_value, cycles_value, data_value])
        main_win.destroy()
    
    def show_help():
        help_text = """
        This window allows you to input voltage sweep parameters. 
        The initial and final Vcg values creates the range of voltages that will be applied to the sensor.
        The number of cycles represents the number of times you would like to perform the sweep consecutively. 
        Note that afterwards you can analyse one sweep at a time or all at the same time, but they will be divided.
        Lastly, the number of points per step indicates the number of points to be retrieve for every wiper step (~100mV).
        Click 'Submit' to input your values.
        """
        messagebox.showinfo("Help", help_text)

    # label
    ttk.Label(main_win, text='Introduce the Vcg sweep parameters', padding=5, 
              font=TITLE_FONT, background=BACKGROUND_COLOR, 
              foreground=LETTER_COLOR).grid(
                  row=1, column=0, columnspan=3, sticky='n', pady=(0, 10))
    ttk.Label(main_win, text='Vcg initial value (V):', padding=5, font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR
              ).grid(row=2, column=0)
    ttk.Label(main_win, text='Vcg final value (V):', padding=5, font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR
              ).grid(row=3, column=0)
    ttk.Label(main_win, text='Number of cycles:', padding=5, font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR
              ).grid(row=4, column=0)
    ttk.Label(main_win, text='Number of datapoints per step:', padding=5, 
              font=TEXT_FONT, background=BACKGROUND_COLOR, 
              foreground=LETTER_COLOR).grid(row=5, column=0)

    # image
    image = Image.open("images//sensor.png")
    image = image.resize((60, 130))
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(main_win, image=photo, bg=BACKGROUND_COLOR)
    image_label.grid(row=2, column=2, rowspan=4, sticky='e', padx=(25, 0))

    # text entries
    vcg_initial_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    vcg_initial_entry.grid(row=2, column=1)

    vcg_final_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    vcg_final_entry.grid(row=3, column=1)

    cycles_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    cycles_entry.grid(row=4, column=1)

    data_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    data_entry.grid(row=5, column=1)

    # button style
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT,
                    background=BACKGROUND_COLOR, foreground=LETTER_COLOR,
                    relief='raised')
    # submit button
    button_submit = ttk.Button(
        main_win, text='Submit', width=10, command=submit_values,
        style='Custom.TButton')
    button_submit.grid(row=6, column=1, pady=(20, 0))
    # help button
    button_help = ttk.Button(
        main_win, text='Help', width=10, command=show_help, style='Custom.TButton')
    button_help.grid(row=6, column=0, pady=(20, 0))
    
    main_win.mainloop()
    return values_list


def get_time_measurement_values():
    """
    get_time_measurement_values: . -> [float, int]
    Description: This function creates a GUI window using tkinter to prompt the
    user to input in the real time analysis parameters. There are two different 
    input values, namely the Vcg value, and time to perform the analysis. The 
    user can then submit the values or cancel the input operation using the 
    respective buttons. If the user cancels the input operation, an empty list 
    is returned. The interface includes labels, an image, text entries and 
    buttons, and it uses a custom style for the buttons.
    Error detecting mechanisms were created along with messages for correcting it.
    """
    main_win = tk.Tk()
    main_win.title("Select real time analysis parameters")

    window_width, window_height = 430, 240
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=15, pady=15)
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT)

    values_list = []

    def submit_values():
        try:
            vcg_value = float(vcg_entry.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter a valid number. Vcg value can be a natural or decimal (separated by '.') value.")
            return
        try:
            time_value = int(time_entry.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter a valid number. Time needs to be a natural value.")
            return
        try:
            points_per_sec = int(points_per_sec_entry.get())
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter a valid number. Points per second needs to be a natural value.")
            return
        if vcg_value < 0 or time_value <= 0 or points_per_sec <= 0:
            messagebox.showerror(
                "Input Error", "Please enter only positive values.")
            return
        if vcg_value > VCG_MAXIMUM_VALUE:
            error_message = "Vcg needs to be smaller or equal to " + \
                str(VCG_MAXIMUM_VALUE) + " V."
            messagebox.showerror("Input Error", error_message)
            return
        values_list.extend([vcg_value, time_value, points_per_sec])
        main_win.destroy()
        
    def show_help():
        help_text = """
        This window allows you to input real-time analysis parameters. 
        The Vcg value indicated the voltage that will be applied to the sensor.
        The Time represents the amount of time that the analysis will last.
        The Points per second indicates the amount of points to be retrieved each second of the analysis.
        Click 'Submit' to input your values.
        """
        messagebox.showinfo("Help", help_text)

    # label
    ttk.Label(main_win, text='Introduce real time analysis parameters', 
              padding=5, font=TITLE_FONT,background=BACKGROUND_COLOR, 
              foreground=LETTER_COLOR
              ).grid(row=1, column=0, columnspan=4, sticky='n', pady=(5, 10))
    ttk.Label(main_win, text='Vcg value (V):', padding=5, font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR
              ).grid(row=2, column=0)
    ttk.Label(main_win, text='Time (seconds):', padding=5, font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR
              ).grid(row=3, column=0)
    ttk.Label(main_win, text='Points per second:', padding=5, font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR
              ).grid(row=4, column=0)

    # image
    image = Image.open("images//sensor.png")
    image = image.resize((50, 110))
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(main_win, image=photo, bg=BACKGROUND_COLOR)
    image_label.grid(row=2, column=2, rowspan=3, sticky='e', padx=(0, 0))

    # text entries
    vcg_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    vcg_entry.grid(row=2, column=1)

    time_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    time_entry.grid(row=3, column=1)

    points_per_sec_entry = ttk.Entry(main_win, width=7, font=TEXT_FONT)
    points_per_sec_entry.grid(row=4, column=1)

    # button style
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT,
                    background=BACKGROUND_COLOR, foreground=LETTER_COLOR,
                    relief='raised')
    # submit button
    button_submit = ttk.Button(main_win, text='Submit', width=10,
                               command=submit_values,  style='Custom.TButton')
    button_submit.grid(row=5, column=1, pady=(15, 0))
    
    #help button
    button_help = ttk.Button(
        main_win, text='Help', width=10, command=show_help, style='Custom.TButton')
    button_help.grid(row=5, column=0, pady=(15, 0))

    main_win.mainloop()
    return values_list

def upload_arduino():
    '''
    upload_arduino: . -> bool
    Description: This function creates a GUI window using tkinter to prompt the
    user to confirm if the Arduino file has been uploaded. The interface 
    includes a label and a button. The user clicks the "Yes" button to confirm 
    the upload, which sets the function's return value to True. The GUI window 
    can be cancelled using the window's close button or the "X" button in the 
    title bar. The function waits for user input and blocks the main thread 
    until the input is received or the window is closed. The function returns
    a boolean value indicating whether the upload has been confirmed (True) 
    or not (False).
    '''
    def submit():
        global ans
        ans = True
        main_win.destroy()
        
    def show_help():
        help_text = """
        Right now an Arduino file has been created with the parameters previously choosen. 
        It is now necessary to upload this file into the Arduino.
        Please open the Arduino IDE and select the file RUNME that has been created inside the RUNME folder in the software's folder.
        Now select the board you are using (Arduino Mega or Arduino Mega 2560) and the COMPort the Arduino is connected to.
        Click 'Yes' after this process.
        """
        messagebox.showinfo("Help", help_text)

    main_win = tk.Tk()
    main_win.title('Upload Arduino')

    window_width, window_height = 395, 100
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=15, pady=15)

    # label
    ttk.Label(main_win, text='Has the Arduino file been uploaded?', 
              font = TITLE_FONT, background = BACKGROUND_COLOR, 
              foreground = LETTER_COLOR).grid(row = 0, column = 0, columnspan=2)

    # button style
    style = ttk.Style()
    style.configure('Custom.TButton', font = TEXT_FONT,
                    background = BACKGROUND_COLOR, foreground = LETTER_COLOR,
                    relief = 'raised')
    # button
    submit_button = ttk.Button(main_win, text = 'Yes', width = 10,
                          command = submit, style = 'Custom.TButton')
    submit_button.grid(row = 1, column = 1, pady = (15, 0))
    
    #help button
    button_help = ttk.Button(
        main_win, text='Help', width=10, command=show_help, style='Custom.TButton')
    button_help.grid(row=1, column=0, pady=(15, 0))

    main_win.mainloop()
    return ans

def get_com_port():
    """
    get_com_port: . -> str
    Description: This function creates a GUI window using tkinter to prompt the
    user to input the COM port that the Arduino is connected to. The interface 
    includes a label, an image, a text entry field, and a button. The user 
    inputs the COM port number in the text entry field and clicks the "Done" 
    button to submit the input. The function returns the entered COM port number 
    as a string. The GUI window can be cancelled using the window's close 
    button or the "X" button in the title bar. The function waits for user 
    input and blocks the main thread until the input is received or the window 
    is closed.
    """
    def submit():
        global COM
        COM = com_port_entry.get()
        main_win.destroy()
        
    def show_help():
        help_text = """
        Now it is time to retrieve the data from Arduino considering the analysis that was chosen.
        Please indicate the COMPort that the Arduino is connected to (same as in last step).
        Note that once you click 'Submit' the analysis will start and values will start being retrieved, so be ready with the samples.
        """
        messagebox.showinfo("Help", help_text)
    
    main_win = tk.Tk()
    main_win.title('Select COM Port')

    window_width, window_height = 425, 245
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=15, pady=15)

    # label
    ttk.Label(main_win, text='Select COM Port.', font=TITLE_FONT, 
              background=BACKGROUND_COLOR,
              foreground=LETTER_COLOR).grid(row=0, column=0, columnspan=3,
                                            sticky='n', pady=(0, 10))
    ttk.Label(main_win, text = 
              'COM port is the port that the Arduino is connected to.',
              font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=1, column=1, columnspan=2, sticky='n', pady=(0, 0))
    ttk.Label(main_win, text='(e.g. COM3, com3, com5, COM5)',
              font = TEXT_FONT, background = BACKGROUND_COLOR, 
              foreground = LETTER_COLOR
              ).grid(row = 2, column = 0, columnspan = 3, sticky = 'n', 
                     pady = (0, 15))

    # entry
    com_port_entry = ttk.Entry(main_win, width=10, font=TEXT_FONT)
    com_port_entry.grid(row=3, column=1, padx=(70, 0))

    # button style
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT,
                    background=BACKGROUND_COLOR, foreground=LETTER_COLOR, 
                    relief='raised')
    #submit button
    submit_button = ttk.Button(main_win, text='Submit', width=10,
                          command=submit, style='Custom.TButton')
    submit_button.grid(row=5, column=1, padx=(70, 0))
    
    #help button
    button_help = ttk.Button(
        main_win, text='Help', width=10, command=show_help, style='Custom.TButton')
    button_help.grid(row=4, column=1, padx=(70, 0), pady=(15,15))

    # image
    image = Image.open("images//usb-connection.png")
    image = image.resize((85, 85))
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(main_win, image=photo, bg=BACKGROUND_COLOR)
    image_label.grid(row=3, column=2, rowspan=4, sticky='e', padx=(0, 60))

    main_win.mainloop()
    return COM

def treat_or_plot_data(dataframe, points_per_steps, num_sweeps):
    """
    treat_or_plot_data: . -> .
    Description: this window shows a sample of the data that was retrived. It
    also presents the user with two options, saving the displayed data or
    ploting it. A third option is semi-created, the treat data option. This
    option is not displayed.
    """
    main_win = tk.Tk()
    main_win.title("Data Analysis Options")

    window_width, window_height = 570, 375
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    main_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    main_win.config(background=BACKGROUND_COLOR)
    main_win.config(padx=35, pady=20)
    
    def show_help():
        help_text = """
        This window allows you to see a portion of the acquired data.
        Click on 'Save Data' you can store the data in CSV format in a directory of your choosing for further analysis as it is presented in this page.
        The 'Calculate Data' allows for a number of data calculations and convertions that might be usefull.
        You can save the data or plot it as many times as you like.
        By choosing any of these options you will always be able to come back to this window.
        """
        messagebox.showinfo("Help", help_text)

    global current_dataframe
    current_dataframe = dataframe

    def display_data():
        # Clear the table
        for row in data_table.get_children():
            data_table.delete(row)
        # Display the data in the table
        for index, row in dataframe.iterrows():
            data_table.insert("", "end", values=row.tolist())

    def save_data():
        save_directory = filedialog.askdirectory()
        if save_directory:
            file_path = os.path.join(save_directory, "data.csv")
            dataframe.to_csv(file_path, index=False)

    def treat_data():
        data_treatment(main_win, current_dataframe, data_table)

    def plot_data():
        choose_parameters(main_win, dataframe, points_per_steps, num_sweeps)

    # title
    ttk.Label(main_win, text="This is a portion of the data:", font=TITLE_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=1, column=1, columnspan=4, sticky='n', pady=(0, 15), 
                  padx=(0, 0))

    # Create a Frame to hold the Treeview and scrollbar
    table_frame = ttk.Frame(main_win)
    table_frame.grid(row=2, column=1, columnspan=4)

    # Create a Treeview widget to display the DataFrame
    data_table = ttk.Treeview(
        table_frame, columns=list(dataframe.columns), show="headings")
    data_table.grid(row=2, column=1, columnspan=2, sticky="nsew")

    # Add the column headings to the table
    for column in dataframe.columns:
        data_table.heading(column, text=column)

    column_width = 80
    for column in dataframe.columns:
        data_table.column(column, minwidth=0, width=column_width, anchor=tk.CENTER)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(
        table_frame, orient="vertical", command=data_table.yview)
    scrollbar.grid(row=2, column=3, sticky="ns")
    data_table.configure(yscrollcommand=scrollbar.set)

    # Limit the displayed rows to 20 (adjust as needed)
    displayed_rows = 20

    # Add the data rows to the table
    for index, row in dataframe.head(displayed_rows).iterrows():
        data_table.insert("", "end", values=row.tolist())

    # Buttons
    style = ttk.Style()
    style.configure('Custom.TButton', font=TEXT_FONT,
                    background=BACKGROUND_COLOR, foreground=LETTER_COLOR,
                    relief='raised')

    # save data
    save_data_button = ttk.Button(
        main_win, text='Save Data', width=10, command=save_data, 
        style='Custom.TButton')
    save_data_button.grid(row=4, column=1, pady=(25, 0))

    # treat data
    #treat_data_button = ttk.Button(
    #    main_win, text='Treat Data', width=10, command=treat_data, 
    #    style='Custom.TButton')
    #treat_data_button.grid(row=4, column=2, pady=(25, 0))

    # plot data
    plot_data_button = ttk.Button(
        main_win, text='Plot Data', width=10, command=plot_data, 
        style='Custom.TButton')
    plot_data_button.grid(row=4, column=2, pady=(25, 0))
    
    # help button
    help_button = ttk.Button(
        main_win, text="Help", command=show_help, width=10, style='Custom.TButton')
    help_button.grid(row=4, column=3, pady=(25,0))

    main_win.mainloop()


def data_treatment(parent_window, dataframe, data_table):
    """
    data_treatment: . -> .
    Description: This function should allow for the treatment of the data. As of
    now it is possible to multiply one of the columns by 1000. By clicking the 
    button, the data shown in the previous window is updated. There was 
    unfortunately no time to further develop this functionality.
    """
    data_window = tk.Toplevel(parent_window)
    data_window.title('graph_title')

    window_width, window_height = 720, 500
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    data_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    data_window.config(background=BACKGROUND_COLOR)
    data_window.config(padx=15, pady=15)
    
    def divide_time():
        modified_dataframe = dataframe
        modified_dataframe['Time'] = modified_dataframe['Time']/1000
        
        # Clear the table
        data_table.delete(*data_table.get_children())

        # Display the modified dataframe in the table
        for index, row in modified_dataframe.iterrows():
            data_table.insert("", "end", values=row.tolist())
            
        # Update the global variable with the modified dataframe
        global current_dataframe
        current_dataframe = modified_dataframe
        
        data_window.destroy()   

    # title
    ttk.Label(data_window, text="Treat the data:", font=TITLE_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=1, column=1, columnspan=3, sticky='n', pady=(0, 15), 
                  padx=(0, 0))
    # labels
    ttk.Label(data_window, text='Divide the time column by 1000:', font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=2, column=1, padx=(0, 0), pady=(0, 10))
    
    # Button Style
    style = ttk.Style()
    style.configure('Custom.TButton', font = TEXT_FONT,
                    background = BACKGROUND_COLOR, foreground = LETTER_COLOR, 
                    relief='raised')

    # submit button
    divide_button = ttk.Button(
        data_window, text = 'Calculate', width = 10, command = divide_time, 
        style = 'Custom.TButton')
    divide_button.grid(row=9, column=2, pady=(25, 0))
    
    data_window.mainloop()

    

def make_plots(parent_window, dataframe, x_axis, y_axis, curves,
                        data_mode, points_per_steps, num_sweeps):
    """
    make_plots: . -> .
    Description: This function creates the plots given the users specifications.
    a toolkit is added to the plot window with which the user can interact with
    the plot.
    """
    plots_window = tk.Toplevel(parent_window)
    title = y_axis + ' by ' + x_axis
    plots_window.title(title)

    window_width, window_height = 720, 500
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    plots_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    plots_window.config(background=BACKGROUND_COLOR)
    plots_window.config(padx=15, pady=15)

    figure = Figure(figsize=(4, 4), dpi=100)
    canvas = FigureCanvasTkAgg(figure, master=plots_window)
    canvas.draw()

    if data_mode == 'Data Averaged':
        dataframe = Graph.average_values(dataframe, points_per_steps)

    # Filter the dataframe based on selected curves
    filtered_dataframes = Graph.divide_sweeps(dataframe, num_sweeps)

    # Plot each selected sweep with different colors
    axes = figure.add_subplot(111)

    # Define a list of colors for the curves
    colors = ['#498ab6', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#1f77b4', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    for sweep, df in filtered_dataframes.items():
        if sweep in curves:
            x_data = df[x_axis]
            y_data = df[y_axis]
            color = colors[(sweep - 1) % len(colors)]
            axes.scatter(x_data, y_data,
                         label=f'Sweep {sweep}', color=color, s=2)
    if x_axis[0]=='V' or x_axis[0]=='v' :
        x_axis_label = x_axis + ' (V)'
    else:
        x_axis_label = x_axis + ' (ms)'
        print(x_axis[0])
    
    if y_axis[0]=='V' or y_axis[0]=='v':
        y_axis_label = y_axis + ' (V)'
    else:
        y_axis_label = y_axis + ' (ms)'
    
    axes.set_xlabel(x_axis_label)
    axes.set_ylabel(y_axis_label)
    axes.set_title(title)
    axes.legend()  # Add legend to show the different sweeps

    canvas = FigureCanvasTkAgg(figure, master=plots_window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, plots_window)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas.get_tk_widget().pack()


def choose_parameters(parent_window, dataframe, points_per_steps, num_sweeps):
    """
    choose_parameters: . -> .
    Description: This window allow for the selection of parameters for creating
    a plot. The user chooses values for x and y axis, and amount of data used.
    Here, the options are already created by the data that was retrieved do the 
    user wont make mistakes. 
    Error detecting mechanisms were created along with messages for correcting it.
    """
    
    parameters_win = tk.Toplevel(parent_window)
    parameters_win.title("Plot's Parameters")

    window_width, window_height = 390, 350
    x = int((SCREEN_WIDTH/2) - (window_width/2))
    y = int((SCREEN_HEIGHT/2) - (window_height/2))
    parameters_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    parameters_win.config(background=BACKGROUND_COLOR)
    parameters_win.config(padx=35, pady=20)

    def submit():
        x_selected = x_axis_var.get()
        y_selected = y_axis_var.get()
        data_mode = data_mode_var.get()
        curves_selected = [int(var.get().split()[1])
                           for var in curve_variables if var.get()]
        if x_selected == '' or y_selected == '':
            messagebox.showerror(
                "Input Error", "Please choose values for both axis.")
            return
        if data_mode == '':
            messagebox.showerror("Input Error", "Please choose a data mode.")
            return
        if x_selected == y_selected:
            ans = messagebox.askquestion(
                "Input Warning",
                "Are you sure you want the same values for x-axis and y-axis?")
            if ans == 'no':
                return
        make_plots(parameters_win, dataframe, x_selected, y_selected,
                            curves_selected, data_mode, points_per_steps,
                            num_sweeps)

    def show_help():
        help_text = """
        This window allows for the development of a plot of the acquired data.
        It is possible to choose the values for x and y axis.
        There are three options of Data Mode: 
        - All Data - Displays all acquired data
        - Averaged Data - Averages the data through the points per seconds or datapoint per step previously chosen.
        - Averaged Data - Averages the data as before and displays error bars.
        It is also possible to choose if all data is presented or analyse certain sweeps, if the voltage sweep analysis was choosen and multiple sweeps were performed.
        After Submiting these parameters, a plot will be shown, which can be stored it in JPEG format if needed.
        It is always possible to come back to this window and make other plots.
        """
        messagebox.showinfo("Help", help_text)
    

    # title
    ttk.Label(parameters_win, text="Choose the plot's parameters:", font=TITLE_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=1, column=1, columnspan=3, sticky='n', pady=(0, 15), 
                  padx=(0, 0))
    # labels
    ttk.Label(parameters_win, text='Value for x axis:', font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=2, column=1, padx=(0, 0), pady=(0, 10))
    ttk.Label(parameters_win, text='Value for y axis:', font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=3, column=1, padx=(0, 0), pady=(5, 10))
    ttk.Label(parameters_win, text='Data Mode:', font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=4, column=1,  padx=(0, 0))
    ttk.Label(parameters_win, text='Curves Displayed:', font=TEXT_FONT,
              background=BACKGROUND_COLOR, foreground=LETTER_COLOR).grid(
                  row=5, column=1, padx=(0, 0))

    # Comboboxes for x-axis and y-axis
    x_axis_var = tk.StringVar()
    y_axis_var = tk.StringVar()
    axis_choices = list(dataframe.columns)

    x_axis_combobox = ttk.Combobox(
        parameters_win, textvariable=x_axis_var, state='readonly', width=23)
    x_axis_combobox.grid(row=2, column=2, padx=(20, 0), pady=(5, 10))
    x_axis_combobox['values'] = axis_choices

    y_axis_combobox = ttk.Combobox(
        parameters_win, textvariable=y_axis_var, state='readonly', width=23)
    y_axis_combobox.grid(row=3, column=2, padx=(20, 0), pady=(5, 10))
    y_axis_combobox['values'] = axis_choices

    # data mode combobox
    data_mode_var = tk.StringVar()
    data_mode_combobox = ttk.Combobox(
        parameters_win, textvariable=data_mode_var, state='readonly', width=23)
    data_mode_combobox.grid(row=4, column=2, padx=(20, 0), pady=(5, 10))
    data_mode_choices = ['All Data', 'Data Averaged',
                         'Data Averaged & Error Bars']
    data_mode_combobox['values'] = data_mode_choices

    # Scrollable box for curve selection
    curve_scrollbox = ScrolledText(parameters_win, height=5, width=9)
    curve_scrollbox.grid(row=5, column=2, rowspan=4, padx=(0, 0), pady=(10, 0))

    # Create check buttons inside the scrollable box
    curve_variables = []
    for i in range(1, num_sweeps+1):
        var = tk.StringVar(value=f'Sweep {i}')
        check_button = ttk.Checkbutton(
            curve_scrollbox, text=f'Sweep {i}', variable=var, 
            onvalue=f'Sweep {i}', offvalue='')
        curve_scrollbox.window_create(tk.END, window=check_button)
        curve_scrollbox.insert(tk.END, '\n')
        curve_variables.append(var)

    # Button Style
    style = ttk.Style()
    style.configure('Custom.TButton', font = TEXT_FONT,
                    background = BACKGROUND_COLOR, foreground = LETTER_COLOR, 
                    relief='raised')

    # submit button
    submit_button = ttk.Button(
        parameters_win, text = 'Submit', width = 10, command = submit, 
        style = 'Custom.TButton')
    submit_button.grid(row=9, column=2, pady=(25, 0))

    # cancel button
    button_cancel = ttk.Button(
        parameters_win, text = 'Help', width = 10, command = show_help,
        style = 'Custom.TButton')
    button_cancel.grid(row = 9, column = 1, pady = (25, 0))

    parameters_win.mainloop()

#intro_window()
#scatter_plot(Graph.vcg_time_data('1704.csv', 10))
# get_analysis_type()
# get_vcg_measurement_values()
# get_time_measurement_values()
# upload_arduino()
# countdown_timer(70)
# get_com_port()
#data = pd.read_csv("./data/test.csv")
#treat_or_plot_data(data, 10, 2)
