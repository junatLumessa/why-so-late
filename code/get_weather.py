import requests
import os
import pandas as pd
from xml.etree import ElementTree
from datetime import datetime
import pytz

fmiUrl = 'http://data.fmi.fi/fmi-apikey/' + str(os.getenv('FMI_API_KEY')) + '/wfs'

def get_weather_forecast_for_current_day():
    today = datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%Y-%m-%d')
    parameters = {
        'request': 'getFeature',
        'storedquery_id': 'fmi::forecast::hirlam::surface::obsstations::simple',
        'place': 'Helsinki',
        'starttime': today + 'T00:00:00Z',
        'endtime': today + 'T23:00:00Z',
        'timestep': 60
    }

    r = requests.get(fmiUrl, params=parameters)
    return result_to_df(r.text)

# tm2       temperature
# ws-10min  wind speed (m/s)
# wg-10min  gust speed (m/s)
# wd-10min  wind direction (deg)
# rh        relative humidity (%)
# td        dew-point temperature (degC)
# r-1h      rain 1h
# ri-10min  rain 10min
# snow-aws  snow depth (cm)
# p-sea     pressure (msl) (hPa)
# vis       horizontal visibility (vis)

def get_weather_observations(startTime, endTime):
    parameters = {
        'request': 'getFeature',
        'storedquery_id': 'fmi::observations::weather::simple',
        'place': 'Helsinki',
        'starttime': startTime,
        'endtime': endTime,
        'timestep': 1440
    }

    r = requests.get(fmiUrl, params=parameters)
    print(r.text)
    return result_to_df(r.text)

# rrday             precipitation amount (mm)
# snow              snow depth (cm)
# tday              air temperature (degC)
# tmin              minimum temperature (degC)
# tmax              maximum temperature (degC)
# TG_PT12H_min      ground minimum temperature (degC)

def get_daily_weather_observations(startTime, endTime):
    parameters = {
        'request': 'getFeature',
        'storedquery_id': 'fmi::observations::weather::daily::simple',
        'place': 'Helsinki',
        'starttime': startTime,
        'endtime': endTime,
        'timestep': 1440
    }

    r = requests.get(fmiUrl, params=parameters)
    print(r.text)
    df = result_to_df(r.text)
    del df['TG_PT12H_min']
    return df

def delete_minuses(df, type):
    df[type] = df[type].astype(str).astype(float)
    df.ix[df[type] == -1, [type]] = 0
    return df

def result_to_df(xml):
    tree = ElementTree.fromstring(xml)

    data = {}

    for node in tree.findall('.//{http://xml.fmi.fi/schema/wfs/2.0}BsWfsElement'):
        date = node[1].text
        if date not in data:
            data[date] = {'datetime': date}

        variable = node[2].text
        value = node[3].text
        data[date][variable] = value

    dataList = []

    for d in sorted(list(data.keys())):
        dataList.append(data[d])

    return pd.DataFrame(dataList)

if __name__ == "__main__":
    #daily = get_daily_weather_observations('2016-10-15T00:00:00Z', '2017-10-15T00:00:00Z')
    #daily.to_csv('../data/weather.csv', index=False)

    today = get_weather_forecast_for_current_day()
    today.to_csv('../data/weather_today.csv', index=False)
