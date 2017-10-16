import json
import requests
import pandas as pd
from datetime import date, timedelta

def get_history(d1 = date(2016, 10, 15), d2= date(2017, 10, 15)):

    delta = d2 - d1         # timedelta
    data = pd.DataFrame()

    for i in range(delta.days + 1):
        departure_date = d1 + timedelta(days=i)
        url = "https://rata.digitraffic.fi/api/v1/history?departure_date="+str(departure_date)
        df = pd.read_json(url)
        df = df[df['trainCategory'] == 'Commuter']
        df = df.drop(['operatorShortCode','timetableAcceptanceDate','timetableType','version','operatorUICCode','trainCategory'],axis=1)
        data = data.append(df, ignore_index=True)

    timeTableData = process_time_table_rows(data)
    del data['timeTableRows']

    return (data, timeTableData)

def process_time_table_rows(df):
    cols = ['stationUICCode', 'cancelled', 'causes', 'differenceInMinutes', 'scheduledTime', 'actualTime', 'commercialTrack']
    data = []

    for index, row in df.iterrows():
        for timeTableRow in row['timeTableRows']:
            if timeTableRow['trainStopping']:
                val = {'idx': index}
                for col in cols:
                    if col in timeTableRow:
                        val[col] = timeTableRow[col]
                data.append(val)

    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    data, timeTableData = get_history()
    data.to_csv('data.csv')
    timeTableData.to_csv('timeTableData.csv', index=False)
