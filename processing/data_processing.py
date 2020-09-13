# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 15:35:52 2020

@author: robcl
"""

import os
import pandas as pd


def decrease_time_sample_train(input_file, amount):
    data = pd.read_csv(input_file)
    new_data = []
    total_time = 0;
    counter = 0;
    for i in range(0, len(data)):
        
        if (i + amount) >= len(data):
            new_df = pd.DataFrame(data=new_data, columns=['time', 'x', 'y', 'x_error', 'y_error'])
            new_df.to_csv(os.path.splitext(input_file)[0] + '_reduced.csv', index=False)
            return (os.path.splitext(input_file)[0] + '_reduced.csv')
        
        # Add together the frames
        total_time += data['time'].iloc[i]

        if (i%amount == 0) and (i != 0):
            new_data.append([total_time, data['x'].iloc[i],  data['y'].iloc[i], data['x_error'].iloc[i], data['y_error'].iloc[i]])
            counter = counter + 1
            # reset totals
            total_time = 0;
            
    new_df = pd.DataFrame(data=new_data, columns=['time', 'x', 'y', 'x_error', 'y_error'])
    new_df.to_csv(os.path.splitext(input_file)[0] + '_reduced.csv', index=False)
    return (os.path.splitext(input_file)[0] + '_reduced.csv')
    
def decrease_time_sample_target(input_file, amount):
    data = pd.read_csv(input_file)
    new_data = []
    total_x = 0; total_y = 0; total_time = 0;
    counter = 0;
    for i in range(0, len(data)):
        
        if (i + amount) >= len(data):
            new_df = pd.DataFrame(data=new_data, columns=['dt', 'dx', 'dy'])
            new_df.to_csv(os.path.splitext(input_file)[0] + '_reduced.csv', index=False)
            return (os.path.splitext(input_file)[0] + '_reduced.csv')
        
        # Add together the frames
        total_time += data['dt'].iloc[i]
        total_x += data['dx'].iloc[i]
        total_y += data['dy'].iloc[i]
        
        if (i%amount == 0) and (i != 0):
            new_data.append([total_time, total_x, total_y])
            counter = counter + 1
            # reset totals
            total_x = 0; total_y = 0; total_time = 0;
            
    new_df = pd.DataFrame(data=new_data, columns=['dt', 'dx', 'dy'])
    new_df.to_csv(os.path.splitext(input_file)[0] + '_reduced.csv', index=False)
    return (os.path.splitext(input_file)[0] + '_reduced.csv')

result = decrease_time_sample_target('data/output.csv', 1)
print(result)

result = decrease_time_sample_train('data/train.csv', 1)
print(result)