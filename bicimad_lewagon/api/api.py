from contextlib import redirect_stderr
from datetime import datetime
from re import X
from sklearn import preprocessing
import pandas as pd
import numpy as np
from math import pi, sin, cos
import datetime
from holidays_es import get_provinces, Province
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bicimad_lewagon.data.encoding_pickle import transform_OHE, transform_standard, concatenate
from bicimad_lewagon.data.registry import load_preprocessor,  load_model
import mlflow
import os
from colorama import Fore, Style
#from tensorflow.keras import Model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# $WIPE_BEGIN
# 💡 Preload the model to accelerate the predictions
# We want to avoid loading the heavy deep-learning model from MLflow at each `get("/predict")`
# The trick is to load the model in memory when the uvicorn server starts
# Then to store the model in an `app.state.model` global variable accessible across all routes!
# This will prove very useful for demo days


app.state.model = load_model()
app.state.preproc = load_preprocessor()

holidays=[datetime.date(2018, 1, 1),
 datetime.date(2018, 1, 6),
 datetime.date(2018, 3, 30),
 datetime.date(2018, 5, 1),
 datetime.date(2018, 8, 15),
 datetime.date(2018, 10, 12),
 datetime.date(2018, 11, 1),
 datetime.date(2018, 12, 6),
 datetime.date(2018, 12, 8),
 datetime.date(2018, 12, 25),
 datetime.date(2018, 3, 29),
 datetime.date(2018, 5, 2),
 datetime.date(2018, 5, 15),
 datetime.date(2018, 11, 9),
 datetime.date(2019, 1, 1),
 datetime.date(2019, 4, 19),
 datetime.date(2019, 5, 1),
 datetime.date(2019, 8, 15),
 datetime.date(2019, 10, 12),
 datetime.date(2019, 11, 1),
 datetime.date(2019, 12, 6),
 datetime.date(2019, 12, 25),
 datetime.date(2019, 1, 7),
 datetime.date(2019, 4, 18),
 datetime.date(2019, 5, 2),
 datetime.date(2019, 12, 9),
 datetime.date(2019, 5, 15),
 datetime.date(2019, 11, 9),
 datetime.date(2020, 1, 1),
 datetime.date(2020, 1, 6),
 datetime.date(2020, 4, 10),
 datetime.date(2020, 5, 1),
 datetime.date(2020, 8, 15),
 datetime.date(2020, 10, 12),
 datetime.date(2020, 12, 8),
 datetime.date(2020, 12, 25),
 datetime.date(2020, 4, 9),
 datetime.date(2020, 5, 2),
 datetime.date(2020, 11, 2),
 datetime.date(2020, 12, 7),
 datetime.date(2020, 5, 15),
 datetime.date(2020, 11, 9),
 datetime.date(2021, 1, 1),
 datetime.date(2021, 1, 6),
 datetime.date(2021, 4, 2),
 datetime.date(2021, 5, 1),
 datetime.date(2021, 10, 12),
 datetime.date(2021, 11, 1),
 datetime.date(2021, 12, 6),
 datetime.date(2021, 12, 8),
 datetime.date(2021, 12, 25),
 datetime.date(2021, 3, 19),
 datetime.date(2021, 4, 1),
 datetime.date(2021, 5, 3),
 datetime.date(2021, 5, 15),
 datetime.date(2021, 11, 9)]


# $WIPE_END

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(date: datetime.date,  # 2013-07-06 17:18:00
            time: datetime.time,    # -73.950655
            name: object,     # 40.783282
            ):      # 1


    holiday= date in holidays

    columns=['reservations_count',
         'number','dock_bikes', 'time','holidays',"date",
        'feels_like', 'weather_main', 'weekday', 'year', 'month', 'hour_sin',
        'hour_cos', 'weekday_sin', 'weekday_cos', 'month_sin', 'month_cos']
    temp = pd.DataFrame(columns=columns)

    #datetime=(str(date)+str(time.hour))

    weekday=date.weekday()
    weekday=int(weekday)


    year=date.year
    year=int(year)

    month=date.month
    month=int(month)

    hour_sin=  sin(time.hour / 24.0 * 2 * pi)
    hour_cos=  cos(time.hour / 24.0 * 2 * pi)
    weekday_sin= sin(weekday / 7.0 * 2 * pi)
    weekday_cos=  cos(weekday / 7.0 * 2 * pi)
    month_sin=  sin(((month - 5) % 12) / 12.0 * 2 * pi)
    month_cos= cos(((month - 5) % 12) / 12.0 * 2 * pi)

    time=int(time.hour)
    #new_row need to be updated by information from the station
    #number, light, total_bases, longitude, latitude, weather,

#TODO:
#    dictionary between names and numbers
#

    new_row={'reservations_count':0, 'number':'1b', 'dock_bikes':0,'time':time, 'date':date, 'holidays':holiday,
             'feels_like':17.44, 'weather_main':'Clear', 'weekday':weekday, 'year':year, 'month':month, 'hour_sin':hour_sin,
        'hour_cos':hour_cos, 'weekday_sin':weekday_sin, 'weekday_cos':weekday_cos, 'month_sin':month_sin, 'month_cos':month_cos}


    temp=temp.append(new_row,ignore_index=True)

    temp = temp.drop(columns="date")               #date is not in the pipeline input requirements

    for column in ['reservations_count', 'dock_bikes', 'time', 'weekday',"month"]:
        temp[column]=temp[column].astype('int8')
    for column in ['year',"number"]:
        temp[column]=temp[column].astype('object')
    for column in ['feels_like',"hour_sin","hour_cos","weekday_sin","weekday_cos","month_sin","month_cos"]:
        temp[column]=temp[column].astype('float32')


    temp['holidays']=temp['holidays'].astype('bool')
    #temp.drop(columns=["name","longitude","address","month","time","weekday"])

    # encoded_standard=transform_standard(temp)
    # encoded_transform=transform_OHE(temp)

    # input_processed= concatenate(encoded_standard,encoded_transform)
    # input_processed=np.array([input_processed])
    # input_processed = np.asarray(input_processed).astype('float32')


    model = app.state.model
    preproc  = app.state.preproc

    x_proc = preproc.transform(temp)

    x_proc = x_proc[:,:-1]

    y_pred = model.predict(x_proc)

    result = {"number_bikes":str(round(y_pred[0]))}
    # ⚠️ fastapi only accepts simple python data types as a return value
    # among which dict, list, str, int, float, bool
    # in order to be able to convert the api response to json

    #dict(prediction=int(y_pred))
    return result


@app.get("/test")
def index(test: str):
    return {"ok": test}


@app.get("/")
def index():
    return {"ok": True}

    encoded_variable=encoding(temp)
#     # $CHA_BEGIN

#     # ⚠️ if the timezone conversion was not handled here the user would be assumed to provide an UTC datetime
#     # create datetime object from user provided date
#     # pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

#     # localize the user provided datetime with the NYC timezone
#     eastern = pytz.timezone("US/Eastern")
#     localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)

#     # convert the user datetime to UTC and format the datetime as expected by the pipeline
#     utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
#     formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")

#     # fixing a value for the key, unused by the model
#     # in the future the key might be removed from the pipeline input
#     key = "2013-07-06 17:18:00.000000119"

#     X_pred = pd.DataFrame(dict(
#         key=[key],  # useless but the pipeline requires it
#         pickup_datetime=[formatted_pickup_datetime],
#         pickup_longitude=[pickup_longitude],
#         pickup_latitude=[pickup_latitude],
#         dropoff_longitude=[dropoff_longitude],
#         dropoff_latitude=[dropoff_latitude],
#         passenger_count=[passenger_count]))

#     model = app.state.model
#     X_processed = preprocess_features(X_pred)
#     y_pred = model.predict(X_processed)

#     # ⚠️ fastapi only accepts simple python data types as a return value
#     # among which dict, list, str, int, float, bool
#     # in order to be able to convert the api response to json
#     return dict(fare=float(y_pred))
#     # $CHA_END


# @app.get("/")
# def root():
#     # $CHA_BEGIN
#     return dict(greeting="Hello")
#     # $CHA_END


if __name__=='__main__':
    now = datetime.datetime.now()
    date=now.date()
    time=now.time()

    name='Puerta del Sol B'

    print(predict(date=date,time=time,name=name))
