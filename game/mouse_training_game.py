# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 18:30:54 2020

@author: robcl
"""
# Depedency: teleport_cursor_to()
import pyautogui
# Dependency: find_system_model.record_data(), Recording mouse movement
import mouse
# Depedency: time.sleep(), using pauses
import time
# Screen training GUI
import graphics
import random
import pandas as pd
import numpy as np
import os

# Time conversion
#TODO:

    
class teleport_cursor_to():
    def __init__(self, x, y):
        self.init_location = (pyautogui.position().x, pyautogui.position().y);
        self.final_location_x = x;
        self.final_location_y = y;
        pyautogui.moveTo(self.final_location_x, self.final_location_y)

# Step 1.
class find_system_model():
    """
    
    """
    def __init__(self):
        self.events = []
        # Lists hold all data to send to training phase
        self.t = []; self.x_est = []; self.y_est = []; self.x_error = []; self.y_error = [];
        # List to hold 'deflections'
        self.deflection_x = []; self.deflection_y = []; self.deflection_t = [];
        # Pandas to store all train data
        self.train_data = []
        
    def record_data(self, until='escape'):
        
        self.init_location_x = pyautogui.position().x 
        self.init_location_y = pyautogui.position().y
        print('> Recording mouse movement!\n')
        print('> Hit escape when done recording movement.\n')
        self.iterations = 0

        if (pyautogui.position().x == self.init_location_x) or (pyautogui.position().y == self.init_location_y):
                print('> Waiting on user to move mouse...\n')
                time.sleep(.05)
        self.iterations += 1
        print('> Recording mouse')
        mouse.hook(self.events.append)
        print('> Spawning training gui')
        truth_x, truth_y = training_gui()
        mouse.unhook(self.events.append)
        self.organize_data(truth_x, truth_y)
        
        # Check if /_user/data/ directory exists, and make dir if DNE
        os.chdir("..")
        current = os.getcwd()
        if os.path.exists(current + '/_user/data/') is False:
            os.mkdir(current + '\\_user\\data\\')
            print('> Data directory created at {}'.format((current + '\\_user\\data\\')))
        
        # Output data to csv
        self.train_data.to_csv('./_user/data/train.csv', index=False)
        self.target_data.to_csv('./_user/data/output.csv', index=False)
        
    def organize_data(self, truth_x, truth_y):
        
        len_events = len(self.events)

        matching = [i for i, s in enumerate(self.events) if 'down' in s]
                
        counter = 0
        try:
            for i in range(0, len_events - 1):
                if counter >= len(matching):
                    self.train_data = pd.DataFrame(np.column_stack([self.t, self.x_est, self.y_est, self.x_error, self.y_error]), columns=['time', 'x', 'y', 'x_error', 'y_error'])
                    self.target_data = pd.DataFrame(np.column_stack([self.deflection_t, self.deflection_x, self.deflection_y]), columns=['dt', 'dx', 'dy'])
                    print(counter)
                    print(len(matching))
                    return
                
                if i not in matching:
                    if ('up' in self.events[i]):
                        pass
                    elif ('down' in self.events[i]):
                        pass
                    elif ('double' in self.events[i]):
                        pass
                    else:
                        self.x_est.append(self.events[i][0])
                        self.y_est.append(self.events[i][1])
                        self.t.append(self.events[i][2] - self.events[0][2])
                        self.x_error.append(float(self.events[matching[counter]-1][0]) - float(self.events[i][0]))
                        self.y_error.append(float(self.events[matching[counter]-1][1]) - float(self.events[i][1]))
                        if (i > 0) and (('up' not in self.events[i-1]) and ('down' not in self.events[i-1]) and ('double' not in self.events[i-1])):
                            self.deflection_x.append(float(self.events[i][0]) - float(self.events[i-1][0]));
                            self.deflection_y.append(float(self.events[i][1]) - float(self.events[i-1][1]));
                            self.deflection_t.append(float(self.events[i][2]) - float(self.events[i-1][2]));
                        else:
                            self.deflection_x.append(0);
                            self.deflection_y.append(0);
                            self.deflection_t.append(0);
                            
                else:
                    counter += 1
        except IndexError:
            i
        except Exception as ex:
            print(i)
            print(len(self.events))
            print(self.events[i])
            print('Unknown exception! {}'.format(ex))
        
        self.train_data = pd.DataFrame(np.column_stack([self.t, self.x_est, self.y_est, self.x_error, self.y_error]), columns=['time', 'x', 'y', 'x_error', 'y_error'])
        self.target_data = pd.DataFrame(np.column_stack([self.deflection_t, self.deflection_x, self.deflection_y]), columns=['dt', 'dx', 'dy'])
        
    def decrease_time_sample_train(data, amount):
        new_data = []
        total_time = 0;
        counter = 0;
        for i in range(0, len(data)):
            
            if (i + amount) >= len(data):
                new_df = pd.DataFrame(data=new_data, columns=['time', 'x', 'y', 'x_error', 'y_error'])
                return new_df
            
            # Add together the frames
            total_time += data['time'].iloc[i]

            if (i%amount == 0) and (i != 0):
                new_data.append([total_time, data['x'].iloc[i],  data['y'].iloc[i], data['x_error'].iloc[i], data['y_error'].iloc[i]])
                counter = counter + 1
                # reset totals
                total_time = 0;
                
        new_df = pd.DataFrame(data=new_data, columns=['time', 'x', 'y', 'x_error', 'y_error'])
        return new_df
    
    def decrease_time_sample_target(data, amount):
        new_data = []
        total_x = 0; total_y = 0; total_time = 0;
        counter = 0;
        for i in range(0, len(data)):
            
            if (i + amount) >= len(data):
                new_df = pd.DataFrame(data=new_data, columns=['dt', 'dx', 'dy'])
                return new_df
            
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
        return new_df
    
# Screen training
def training_gui():
    win = graphics.GraphWin("Mouse Training",1700,700)
    win.setBackground("black")
    win.redraw()
    score=0
    c,x,y = draw_circle(win)
    x_truth = []
    y_truth = []
    while score < num_runs:
        mouseClick2=win.getMouse()
        if mouseClick2.y >= y-50 and mouseClick2.y <= y +50 and mouseClick2.x >= x-50 and mouseClick2.x <= x+50:
            x, y = pyautogui.position()
            c.setFill("black")
            score += 1
        time.sleep(.1)
        c,x,y = draw_circle(win, c)
        x_truth.append(x)
        y_truth.append(y)
        c.setFill(graphics.color_rgb(200,0,0))
    win.close()
    return x_truth, y_truth
  
def draw_circle(win, c=None):
    x=random.randint(50,1650)
    y=random.randint(50,650)
    
    centa=graphics.Point(x,y)
    
    if c is not None:
        c.undraw()
        
    c = graphics.Circle(centa, random.randint(25, 25))
    c.setFill(graphics.color_rgb(200,0,0))
    c.draw(win)
        
    return (c, x, y)

### END Step 1.
num_runs = 5

mouse_data = find_system_model()
mouse_data.record_data() 
print('Done!')     