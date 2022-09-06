from sklearn import preprocessing
import pandas as pd
import numpy as np
from math import pi, sin, cos
from datetime import datetime
from holidays_es import get_provinces, Province
import sys


myfile= sys.argv[1]
station= int(sys.argv[2])

basename = myfile.split(".")[0]



df = pd.read_json( myfile,encoding_errors='ignore', lines=True)
weather = pd.read_csv("weather/weather_cleaned.csv")


df["time"] = "time"
df["date"] = "date"
for i in range(len(df['_id'])):
    item=df['_id'][i]
    groups= item.split("T")
    date = groups[0]
    raw_time = groups[1].split(":")
    time = raw_time[0]
    df["time"][i] = time
    df["date"][i] = date

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

holidays=[]
for year in [2018,2019,2020,2021]:
    temp = Province(name="madrid", year=year).holidays()
    for day in range(len(temp['national_holidays'])):
        holidays.append(temp['national_holidays'][day])
    for day in range(len(temp['regional_holidays'])):
        holidays.append(temp['regional_holidays'][day])
    for day in range(len(temp['local_holidays'])):
        holidays.append(temp['local_holidays'][day])


df_holidays=pd.DataFrame(holidays, columns=['date'])
df_holidays['date'] = pd.to_datetime(df_holidays['date'], format='%Y-%m-%d')
list_holidays=list(df_holidays['date'])
df['holidays']=df['date'].isin(list_holidays)

temp=pd.DataFrame()
#for final whole model
# for i in range(len(df)):
#     for j in range(len(df["stations"][1])):
#         new_dict= df['stations'][i][0]
#         new_dict['id']=df['_id'][i]
#         new_dict['time']=df['time'][i]
#         new_dict['date']=df['date'][i]
#         new_dict['holidays']=df['holidays'][i]
#         temp = temp.append(new_dict, ignore_index=True)


for i in range(len(df)):
    try:
        new_dict= df['stations'][i][station]
        new_dict['id']=df['_id'][i]
        new_dict['time']=df['time'][i]
        new_dict['date']=df['date'][i]
        new_dict['holidays']=df['holidays'][i]
        temp = temp.append(new_dict, ignore_index=True)
    except:
        quit()


df["datetime"] = df["day"].astype(str)+" "+df["time"].astype(str)
temp = temp.merge(weather, on="datetime")




temp['weekday'] = temp.apply(lambda x: x['date'].weekday(), axis=1)
temp['year'] = temp.apply(lambda x:x['date'].year, axis=1)
temp['month'] = temp.apply(lambda x: x['date'].month, axis=1)


temp['hour_sin'] = temp.apply(lambda x: sin(x['time'] / 24.0 * 2 * pi), axis=1)
temp['hour_cos'] = temp.apply(lambda x: cos(x['time'] / 24.0 * 2 * pi), axis=1)
temp['weekday_sin'] = temp.apply(lambda x: sin(x['weekday'] / 7.0 * 2 * pi), axis=1)
temp['weekday_cos'] = temp.apply(lambda x: cos(x['weekday'] / 7.0 * 2 * pi), axis=1)
temp['month_sin'] = temp.apply(lambda x: sin(((x['month'] - 5) % 12) / 12.0 * 2 * pi), axis=1)
temp['month_cos'] = temp.apply(lambda x:cos(((x['month'] - 5) % 12) / 12.0 * 2 * pi), axis=1)

temp.drop(columns=["name","longitude","address","month","time","weekday"])

temp.to_csv("../raw_data"+basename+"_processed.csv", index=False)
