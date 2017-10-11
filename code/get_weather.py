import requests
import os
import pandas as pd
from xml.etree import ElementTree

fmiUrl = 'http://data.fmi.fi/fmi-apikey/' + os.environ['FMI_API_KEY'] + '/wfs'

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
    return result_to_df(r.text, 13)

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
        'timestep': 60 * 24
    }

    r = requests.get(fmiUrl, params=parameters)

    return result_to_df(r.text, 7)


def result_to_df(xml, nbrOfVariables):
    tree = ElementTree.fromstring(xml)

    data = []
    i = 0
    j = -1
    for node in tree.findall('.//{http://xml.fmi.fi/schema/wfs/2.0}BsWfsElement'):
        if (i % nbrOfVariables == 0):
            j += 1
            data.append({'datetime': node[1].text})

        variable = node[2].text
        value = node[3].text
        data[j][variable] = value
        i += 1
    return pd.DataFrame(data)

if __name__ == "__main__":
    print(get_weather_observations('2016-09-05T12:00:00Z', '2016-09-05T17:00:00Z'))
    print(get_daily_weather_observations('2016-09-02T00:00:00Z', '2016-09-05T00:00:00Z'))
