from sklearn import preprocessing
import pandas as pd
import numpy as np
from math import pi, sin, cos
from datetime import datetime
from holidays_es import get_provinces, Province
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from tensorflow.keras import layers
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
import mlflow
from tensorflow.keras.callbacks import EarlyStopping


def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)        
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)


def create_model(preprocessed_data):
    train_size = int(len(preprocessed_data) * 0.8)
    test_size = len(preprocessed_data) - train_size
    train, test = preprocessed_data.iloc[0:train_size], preprocessed_data.iloc[train_size:len(temp_model)]
    print(len(train), len(test))
    time_steps = 24

    # reshape to [samples, time_steps, n_features]

    X_train, y_train = create_dataset(train, train.dock_bikes, time_steps)
    X_test, y_test = create_dataset(test, test.dock_bikes, time_steps)
    
    #MLFLOW TRACKING
    mlflow.set_tracking_uri("https://mlflow.lewagon.ai")
    mlflow.set_experiment(experiment_name="BiciMad")

    model = Sequential()
    model.add(
        layers.Bidirectional(
        layers.LSTM(
        units=100,
        input_shape=(X_train.shape[1], X_train.shape[2]),
        ), 
    )
    )
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(units=1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    early_stop = EarlyStopping(monitor="val_loss", mode="min", verbose=1, patience = 10)

    batch_size = 64
    epochs = 20
    #fitting model
    history = model.fit(
        X_train, y_train, 
        epochs=epochs, 
        batch_size=batch_size, 
        validation_data=(X_test, y_test),
        shuffle=False,
        callbacks = [early_stop]
    )