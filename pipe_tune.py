# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:19:49 2020

@author: robcl
"""

from datetime import datetime
import numpy as np

# Neural Net
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping

# Simulation Parameters (dont change these)
START_TIME = datetime.now().strftime("%H:%M:%S")

# Simulation Parameters (change these)
# Processing Parameters
PROCESSING_REDUCTION = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])     # Divide

# Training Parameters
TRAIN_VAL_SPLIT = np.array([.2, .3, .4, .5])                                    # Percentage
TRAIN_DROPOUT = np.array([0, .05, .1, .15, .18, .2, .22, .25, .30, .35, .4])    # Percentage
TRAIN_OPTIMIZER = ['Adam', 'rmsprop']
TRAIN_PATIENCE = np.array([5, 10, 15, 20, 25, 50])
TRAIN_BATCH_SIZE = np.array([.05, .1, .2, .3, .5, .75])

# Duration Parameters
DURATION_BROAD_SEARCH = 0;                                                      # Hours
DURATION_FINE_SEARCH = 0;                                                       # Hours

# Net Architecture Parameters
NET_MIN_HIDDEN_LAYERS = 1
NET_MAX_HIDDEN_LAYERS = 5
NET_ACTIVATION_FUNC = ['sigmoid', 'linear', 'exponential', 'relu']
NET_HIDDEN_UNITS = np.linspace(1, 200, 99)


class tune():
    def __init__(self, input_data, target_data, input_size=3, duration=5):
        self.hidden_layers = []
        self.hidden_units = [] 
        self.drop = []
        self.act = []
        self.input_size = input_size
        self.batch_size = 0
        self.model = []
        pass
    
    def start():
        pass
    
    def _broad_search():
        pass
        
    def _fine_search():
        pass
    
    
    
    def _test():
        pass
        
    def _train(self):
        # Import data
        
        
        # Define training parameters
        self._def_training_param()
        
        # Define model
        self._def_model()
        
        # Compile model
        self.model.compile(loss='mse', optimizer='Adam', metrics=['accuracy', 'mse', 'mae'])
        
        # Early Stop Parameters
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
        
        # fit the keras model on the dataset
        history = self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5000, self.batch_size=100, callbacks=[es])
    
    def _def_training_param(self):
        pass
    
    def _def_model(self):
        self.model = Sequential()
        
        counter = 0
        last_index = np.size(self.hidden_layers, 2)
        
        for layer in self.hidden_layers:
            if counter is last_index:
                self.model.add(Dense(2, activation='sigmoid'))
            else:
                if counter == 1:
                    self.model.add(Dense(self.hidden_layers(1), input_dim=self.input_size, activation=self.act(1)))
                else:
                    self.model.add(Dense(self.hidden_layers[counter], activation=self.act(counter)))
                self.model.add(BatchNormalization())
                self.model.add(Dropout(self.drop(counter)))
                
            # Update index
            counter += 1

    
    
    

# Setting up simulation
print("Current Time =", START_TIME)
layer_vector = np.linspace(1, 11, 10)
