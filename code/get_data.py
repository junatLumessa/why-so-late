import json
import requests
import pandas as pd
from datetime import date, timedelta

def get_history(d1 = date(2017, 10, 14), d2= date(2017, 10, 15)):
    
    delta = d2 - d1         # timedelta
    data = pd.DataFrame()    

    for i in range(delta.days + 1):
        departure_date = d1 + timedelta(days=i) 
        url = "https://rata.digitraffic.fi/api/v1/history?departure_date="+str(departure_date)
        df = pd.read_json(url)
        df = df[df['trainCategory'] == 'Commuter']
        df = df.drop(['operatorShortCode','timetableAcceptanceDate','timetableType','version','operatorUICCode','trainCategory'],axis=1)
        data = data.append(df, ignore_index=True)

    print(len(data))
    print(data.iloc[0]['timeTableRows'])
    return data

if __name__ == "__main__":
    data = get_history()
    




