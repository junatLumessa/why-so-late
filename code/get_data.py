import json
import requests
import pandas as pd
from datetime import date, timedelta

def get_history(d1, d2, lineId):

    delta = d2 - d1         # timedelta
    data = pd.DataFrame()

    for i in range(delta.days + 1):
        departure_date = d1 + timedelta(days=i)
        print(departure_date)
        url = "https://rata.digitraffic.fi/api/v1/history?departure_date="+str(departure_date)
        df = pd.read_json(url)
        df = df[(df['trainCategory'] == 'Commuter') & (df['commuterLineID'] == lineId) & (df['cancelled'] == False)]
        df = df.drop(['operatorShortCode','timetableAcceptanceDate','timetableType','version','operatorUICCode','trainCategory'],axis=1)
        data = data.append(df, ignore_index=True)

    return data

def process_time_table_rows(df):
    cols = ['stationUICCode', 'cancelled', 'causes', 'differenceInMinutes', 'scheduledTime', 'actualTime', 'commercialTrack']
    data = []

    for index, row in df.iterrows():
        #jsonString = row['timeTableRows'].replace("'", '"').replace('True', 'true').replace('False', 'false')
        for timeTableRow in row['timeTableRows']:
            if timeTableRow['trainStopping']:
                val = {'idx': index}
                for col in cols:
                    if col in timeTableRow:
                        val[col] = timeTableRow[col]
                data.append(val)

    return pd.DataFrame.from_dict(data)

# date range have to be divisible by three
def get_data_in_three_parts(d1, d2, lineId):
    delta = (d2 - d1 + timedelta(days=1)) / 3

    data = get_history(d1, d1 + delta - timedelta(days=1), lineId)
    data.to_csv('temp1.csv')
    data2 = get_history(d1 + delta, d1 + 2 * delta - timedelta(days=1), lineId)
    data2.to_csv('temp2.csv')
    data3 = get_history(d1 + 2 * delta, d2, lineId)
    data3.to_csv('temp3.csv')

    data = data.append(data2, ignore_index=True)
    data = data.append(data3, ignore_index=True)

    timeTableRows = process_time_table_rows(data)
    timeTableRows.to_csv('../data/{}-train-timetablerows.csv'.format(lineId), index=False)

    del data['timeTableRows']
    data.to_csv('../data/{}-train.csv'.format(lineId))


if __name__ == "__main__":
    #get_data_in_three_parts(date(2016, 10, 15), date(2017, 10, 15), 'A')
    get_data_in_three_parts(date(2017, 10, 14), date(2017, 10, 16), 'R')
