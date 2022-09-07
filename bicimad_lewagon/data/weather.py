import urllib.parse
import requests
import datetime

def time_until_end_of_day(dt=None):
    if dt is None:
        now = datetime.datetime.now()
        dt = now.time()
    return (((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60)) //3600

####################
def choose_n(time_until_end_of_day):
    if time_until_end_of_day>=24:
        n=0
    elif time_until_end_of_day >= 15:
        n=0
    elif time_until_end_of_day >= 12:
        n=1
    elif time_until_end_of_day >= 9:
        n=2
    elif time_until_end_of_day >= 6:
        n=3
    elif time_until_end_of_day >= 3:
        n=4
    elif time_until_end_of_day >=0:
        n=5
    return n

#####################

def weather_forecast():
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    BASE_URL = "https://weather.lewagon.com"
    url = BASE_URL+f"/data/2.5/forecast?lat=40.4167047&lon=-3.703582&units=metric"

    response = requests.get(url).json()

    return response


#################
def strround(x):
    if x<10:
        r='0'+str(x)
    else:
        r=str(x)
    return r

##################

def weather(date_requested,time_requested):

    today = datetime.date.today()
    round_hour=round((time_requested.hour+time_requested.minute/60)/3)*3
    time_until=time_until_end_of_day(time_requested )
    n=choose_n(time_until)
    response = weather_forecast()
    delta = date_requested-today
    month_feels={1:5.0,2:6.0,3:10.0,4:12.0,5:16.0,6:22.0,7:26.0,8:25.0,9:21.0,10:15.0,11:9.0,12:6.0}
    dt_txt=f'{date_requested.year}-{strround(date_requested.month)}-{strround(date_requested.day)} {strround(round_hour)}:00:00'
    weather='test'

    if ((delta.days*8+n)< 39) & (delta.days>=0):
        forecast = weather_forecast()
        index=0
        for i in (response["list"]):
            if i['dt_txt']==dt_txt:
                feels_like = response["list"][index]["main"]["feels_like"]
                weather = response["list"][index]["weather"][0]["main"]
            index+=1

    else:

        if date_requested.month in [1, 2, 12]:
            weather = 'Cloudy'
            feels_like = month_feels[date_requested.month]
        else:
            weather = 'Sunny'
            feels_like = month_feels[date_requested.month]

    return weather, feels_like
