# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 15:24:21 2020

@author: robcl
"""
# Array/Data frame manipulation
import pandas as pd
import numpy as np

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

# Data Definition
data = 'data/train_reduced.csv'
target = 'data/output_reduced.csv'
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
with open("models/model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
# serialize weights to HDF5
abc = model.save("models/model.h5")
print(abc)
print("Saved model to disk")

# dump scales
if scaling is True:
    dump(scaler_input, open('models/scaler_input.pkl', 'wb'))
    dump(scaler_output, open('models/scaler_output.pkl', 'wb'))