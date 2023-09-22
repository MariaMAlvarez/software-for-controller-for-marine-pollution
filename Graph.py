# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:33:45 2023

@author: MMA
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

def divide_sweeps(df, num_sweeps):
    total_rows = len(df)
    rows_per_sweep = total_rows // num_sweeps
    sweep_dataframes = {}
    for i in range(num_sweeps):
        start_index = i * rows_per_sweep
        end_index = start_index + rows_per_sweep
        sweep_df = df.iloc[start_index:end_index].copy()
        sweep_dataframes[i + 1] = sweep_df
    return sweep_dataframes

def average_values(df, points_per_step):
    df_avg = pd.DataFrame(columns=df.columns.tolist())
    start = 0
    while start < len(df):
        df_avg = pd.concat([df_avg, df.loc[start:start+points_per_step-1].mean().to_frame().T], ignore_index=True)
        start += points_per_step
    return df_avg

def rolling_average(df, pts_per_step):
    print(df)
    for column in df.columns.tolist():
        avg = column + '_averaged'
        std = column + '_std'
        se = column + '_se'
        df[avg] = df[column].rolling(window=pts_per_step).mean()
        df[std] = df[column].rolling(window=pts_per_step).std()
        df[se] = df[column].rolling(window=pts_per_step).std()/np.sqrt(pts_per_step)
        print(column)
    print(df.head(10))
    


def rolling_average_2(df, pts_per_step):
    print(df)
    
    # Calculate rolling mean, standard deviation, and standard error only for specific lines
    mean_list = []
    std_list = []
    se_list = []
    
    for i in range(0, len(df), pts_per_step):
        if i + pts_per_step <= len(df):
            subset = df.iloc[i:i + pts_per_step]
            mean_list.append(subset.mean())
            std_list.append(subset.std())
            se_list.append(subset.std() / np.sqrt(pts_per_step))
    
    # Create a new DataFrame with the calculated values
    result_df = pd.DataFrame({
        'Voltage Step': range(1, len(mean_list) + 1),
        'Mean': mean_list,
        'Standard Deviation': std_list,
        'Standard Error': se_list})
    
    # Print the resulting DataFrame
    print(result_df.head(10))
    return

df = pd.read_csv("./data/test.csv")
#divided = divide_sweeps(df, 2)
#divided[2]
#average_values(df, 10)

rolling_average(df, 10)
