# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 15:30:20 2020

@author: robcl
"""
import os
from numpy import array, shape
from keras.models import load_model
import pandas as pd
from pyautogui import move, position
from pickle import load

class use_multi_net():
    pass

class use_single_net():
    def __init__(self, model_location, input_scaler=None, output_scaler=None): 
        self.output = []
        self.model = load_model(model_location)
        self.scale = False
        # summarize model.
        self.model.summary()
        if (input_scaler is not None) and (output_scaler is not None):
            self.scale = True
            self.scaler_output = load(open(output_scaler, 'rb'))
            self.scaler_input = load(open(input_scaler, 'rb'))
    
    def run_net(self, x_target, y_target):
        if self.scale is True:
            # The run-time is larger for this net.
            print('> Running with scaling.')
            self._run_net_with_scaling(x_target, y_target)
        else:
            # The run-time should be smaller on this net.
            print('> Running without scaling.')
            self._run_net_without_scaling(x_target, y_target)
    
    def _run_net_without_scaling(self, x_target, y_target):
        x_error = 1000;
        y_error = 1000;
        while((abs(x_error) > 12) or (abs(y_error) > 12)):
            # Position Error update
            x_true, y_true = position()
            x_error = x_true - x_target;
            y_error = y_true - y_target;
 
            # Net update
            x_in = array((float(x_error), float(y_error)))
            
            self.output = self.model.predict(x_in.reshape(1, -1))
            
            # Update mouse position
            move(-self.output[0][0], -self.output[0][1])
            

            self.output = self.model.predict(x_in.reshape(1, -1))
     
            # Update mouse position
            move(-self.output[0][0], -self.output[0][1])
        
        x_true, y_true = position()
        print('Final cursor location ({0}, {1}):'.format(x_true, y_true))
            
    def _run_net_with_scaling(self, x_target, y_target):
        x_error = 1000;
        y_error = 1000;
        
        while((abs(x_error) > 5) or (abs(y_error) > 5)):
            # Position Error update
            x_true, y_true = position()
            x_error = x_true - x_target;
            y_error = y_true - y_target;
            
            # Net update
            x_in = array((float(x_error), float(y_error)))
            X = self.scaler_input.transform((x_in.reshape(1, -1)))

            self.output = self.scaler_output.inverse_transform(self.model.predict(X))
     
            # Update mouse position
            move(-self.output[0][0], -self.output[0][1])
        
        x_true, y_true = position()
        print('Position achieved!')
        print('Final cursor location ({0}, {1}):'.format(x_true, y_true))
        
            
    def close_to_target(self):
        """ This net will be utilized when we are close to the target. """
        pass
    
    
    def far_from_target(self):
        """ This net will be utilized when we are far from the target. """
        pass
        
        
            
        
# Test Functions:
print(os.getcwd())
#net = use_net('working/practical_model/models/model.h5', 'working/practical_model/models/scaler_input.pkl', 'working/practical_model/models/scaler_output.pkl')
net = use_single_net('models/model.h5', 'models/scaler_input.pkl', 'models/scaler_output.pkl')
#net = use_net('models/model.h5')
net.run_net(500, 500)
#profile.run('net.run_net(1800, 200)')
