import requests
import os
import pandas as pd
from xml.etree import ElementTree

#for linux
fmiUrl = 'http://data.fmi.fi/fmi-apikey/' + os.environ['FMI_API_KEY'] + '/wfs'
#for windows
#fmiUrl = 'http://data.fmi.fi/fmi-apikey/' + str(os.getenv('FMI_API_KEY')) + '/wfs'

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
        'timestep': 60
    }

    r = requests.get(fmiUrl, params=parameters)
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

    df = result_to_df(r.text)
    del df['TG_PT12H_min']
    return df

def delete_minuses(df, type):
    df[type] = df[type].astype(str).astype(float)
    df.ix[df[type] == -1, [type]] = 0
    return df

def result_to_df(xml):
    tree = ElementTree.fromstring(xml)

    data = []
    j = -1
    prevDate = None

    for node in tree.findall('.//{http://xml.fmi.fi/schema/wfs/2.0}BsWfsElement'):
        date = node[1].text
        if (prevDate != date):
            j += 1
            prevDate = date
            data.append({'datetime': date})

        variable = node[2].text
        value = node[3].text
        data[j][variable] = value

    return pd.DataFrame(data)

if __name__ == "__main__":
    daily = get_daily_weather_observations('2016-10-15T00:00:00Z', '2017-10-15T00:00:00Z')
    daily.to_csv('weather.csv', index=False)
