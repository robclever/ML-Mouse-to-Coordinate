# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:19:49 2020

@author: robcl
"""

from datetime import datetime
import numpy as np

# Simulation Parameters (dont change these)
START_TIME = datetime.now().strftime("%H:%M:%S")

# Simulation Parameters (change these)
# Processing Parameters
PROCESSING_REDUCTION = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]) # Divide

# Training Parameters
TRAIN_PERCENTAGE = np.array([.2, .3, .4, .5])
TRAIN_DROPOUT = np.array([0, .05, .1, .15, .18, .2, .22, .25, .30, .35, .4]) # Percentage

# Duration Parameters
DURATION_BROAD_SEARCH = 0; # In hours
DURATION_FINE_SEARCH = 0; # In hours

# Net Architecture Parameters
NET_MIN_HIDDEN_LAYERS = 1
NET_MAX_HIDDEN_LAYERS = 11

# 

class tune_network():
    def __init__():
        pass
    
    def start():
        pass
    
    def _broad_search():
        pass
        
    def _fine_serach():
        pass
    
    def _determine_variables():
        pass
    
    def _test():
        pass
        
    def _train():
        pass

    
    
    

# Setting up simulation
print("Current Time =", START_TIME)
layer_vector = np.linspace(1, 11, 10)
