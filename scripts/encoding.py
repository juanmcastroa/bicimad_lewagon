from sklearn import preprocessing
import pandas as pd
import numpy as np
from math import pi, sin, cos

from sklearn.preprocessing import StandardScaler, OneHotEncoder






def encode_columns(df):
    temp = df 
    #Transform the data
    f_transformer = StandardScaler()
    df[['activate', 'reservations_count', 'light', 'total_bases', 'free_bases', 'longitude', 'no_available', 'latitude', 'time',
       'feels_like', 'weekday', 'year', 'month', 'hour_sin', 'hour_cos',
        'weekday_sin', 'weekday_cos', 'month_sin', 'month_cos']] = f_transformer.fit_transform(df[['activate', 'reservations_count', 'light', 'total_bases', 'free_bases', 'longitude', 'no_available', 'latitude', 'time',
       'feels_like', 'weekday', 'year', 'month', 'hour_sin', 'hour_cos',
        'weekday_sin', 'weekday_cos', 'month_sin', 'month_cos']])

    temp.holidays = temp.holidays.astype('int')
    temp_model = temp.drop(columns=['name', 'number', 'address', 'id'])

    #Encode the data
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    categorical_features = ['year', 'month', 'weekday', 'weather_main']
    transformed_data = pd.DataFrame(ohe.fit_transform(temp_model[categorical_features]))
    transformed_data.columns = ohe.get_feature_names(categorical_features)
    concatenated_data = pd.concat([temp_model, transformed_data], axis=1)
    temp_model = concatenated_data.drop(columns=['year', 'month', 'weekday', 'weather_main','date'])
    temp_model['datetime'] = temp_model['datetime'].apply(lambda x: x[0:10]+' '+x[10:]+':00')
    temp_model['datetime']=pd.to_datetime(temp_model['datetime'], format='%Y-%m-%d %H:%M:%S')
    temp_model = temp_model.set_index('datetime')
    temp_model.sort_values(by='datetime')
    return temp_model
