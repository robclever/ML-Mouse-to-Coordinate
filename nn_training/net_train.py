# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 15:24:21 2020

@author: robcl
"""
# Array/Data frame manipulation
import pandas as pd
import numpy as np
import os

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior() 

# NN
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping

# Data Processing
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from pickle import dump

# Plotting
import matplotlib.pyplot as pyplot


os.chdir('..')
current = os.getcwd()
if os.path.exists(current + '/_user/models/') is False:
    os.mkdir(current + '\\_user\\models\\')
    print('> Models directory created at {}'.format((current + '\\_user\\models\\')))
    
# Data Definition
data = current + '/_user/data/train.csv'
target = current + '/_user/data/output.csv'

scaling = True
data_df = pd.read_csv(data)
target_df = pd.read_csv(target)
X = data_df.to_numpy()
y = target_df.to_numpy()
X = X[:, 3:5]
y = y[:, 1:3]

input_features = 2

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

if scaling is True:
    # Scaling input data
    scaler_input = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler_input.transform(X_train)
    X_test = scaler_input.transform(X_test)

    # Scaling output data
    scaler_output = preprocessing.MinMaxScaler(feature_range=(-1, 1)).fit(y_train)
    y_train = scaler_output.transform(y_train)
    y_test = scaler_output.transform(y_test)

# Compiling model
model = Sequential()
model.add(Dense(85, input_dim=input_features, activation='sigmoid'))
model.add(BatchNormalization())
model.add(Dropout(.2))
model.add(Dense(60, input_dim=input_features, activation='sigmoid'))
model.add(BatchNormalization())
model.add(Dropout(.2))

if scaling is True:
    model.add(Dense(2, activation='sigmoid'))
else:
    model.add(Dense(2, activation='linear'))
    
# compile the keras model
model.compile(loss='mse', optimizer='Adam', metrics=['accuracy', 'mse', 'mae'])
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

# fit the keras model on the dataset
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5000, batch_size=100, callbacks=[es])

score = model.evaluate(X_test, y_test)
print('Test final score: {}'.format(score[1]*100))

# plot training history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

# serialize model to YAML
model_yaml = model.to_yaml()
with open(current + "/_user/models/model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
# serialize weights to HDF5
model_location = model.save(current + "/_user/models/model.h5")
print(model_location)
print("> Saved model to disk")

# dump scales
if scaling is True:
    dump(scaler_input, open(current + '/_user/models/scaler_input.pkl', 'wb'))
    dump(scaler_output, open(current + '/_user/models/scaler_output.pkl', 'wb'))