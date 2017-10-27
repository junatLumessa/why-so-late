from analyze import get_classifier_for_all_line_ids, make_more_binarys, BINARY_THRESHOLDS
from get_weather import get_weather_forecast_for_day
from get_data import get_data_for_day
import pandas as pd
from datetime import datetime
import pytz

# Trial to predict what trains are late on 26.10.2017
def predict_day(date='2017-10-26'):
    classifiers = get_classifier_for_all_line_ids()

    wd = get_weather_forecast_for_day(date)
    wd['Precipitation1h'] = wd['Precipitation1h'].replace('NaN', '0.0').astype('float')
    rainAndSnow = wd.groupby(['PrecipitationForm'])['Precipitation1h'].sum().reset_index()
    rainDf = rainAndSnow[rainAndSnow['PrecipitationForm'] == '2.0']
    snowDf = rainAndSnow[rainAndSnow['PrecipitationForm'] == '3.0']
    rain = rainDf.reset_index().get_value(0, 'Precipitation1h') if not rainDf.empty else 0
    snow = snowDf.reset_index().get_value(0, 'Precipitation1h') if not snowDf.empty else 0
    temperature = wd['Temperature'].astype('float').mean()

    weather = pd.DataFrame(data=[{'rrday': rain, 'snow': snow, 'tday': temperature}], columns=['rrday', 'snow', 'tday'])

    for column in ['rrday', 'snow']:
        weather[column] = (weather[column] >= BINARY_THRESHOLDS[column]).astype('int')

    make_more_binarys(weather, 'tday')

    commuterLineIDs = get_data_for_day(date)[0]['commuterLineID'].unique()

    result = []
    for classifier in classifiers:
        if classifier['lineId'] not in commuterLineIDs:
            continue
        prediction = classifier['classifier'].predict(weather)[0]
        print(prediction)
        result.append({'lineId': classifier['lineId'], 'prediction': prediction})

    res = pd.DataFrame(result)
    print(res)


if __name__ == "__main__":
    today = datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%Y-%m-%d')
    predict_day()
