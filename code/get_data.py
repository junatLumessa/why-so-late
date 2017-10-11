import json
import requests
import pandas as pd

def get_history():
    url = "https://rata.digitraffic.fi/api/v1/history?departure_date=2017-10-10"

    df = pd.read_json(url)

    data = df[df['trainCategory'] == 'Commuter' ]

    print(len(data))
    print(data)
    return data

if __name__ == "__main__":
    get_history()


