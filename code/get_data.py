import json
import requests
import pandas as pd
from datetime import date, datetime, timedelta
import os.path
import pytz

digitrafficUrl = "https://rata.digitraffic.fi/api/v1/"
#FILL HERE YOUR DATA FOLDER PATH!
DATA_PATH = '../data/data/'

def get_data_for_day(day):
    url = digitrafficUrl + "trains/" + str(day)
    df = get_df_from_url(url)
    timeTableRows = process_time_table_rows(df, 0, False)
    process_causes(timeTableRows)
    del df["timeTableRows"]
    #df.to_csv("../data/today.csv")
    #timeTableRows.to_csv("../data/today-timetablerows.csv", index=False)
    return (df, timeTableRows)

def get_history(d1, d2, lineId=None):
    delta = d2 - d1         # timedelta
    data = pd.DataFrame()

    for i in range(delta.days + 1):
        departure_date = d1 + timedelta(days=i)
        print(departure_date)
        url = digitrafficUrl + "history?departure_date=" + str(departure_date)
        df = get_df_from_url(url, lineId)
        data = data.append(df, ignore_index=True)

    return data

def get_df_from_url(url, lineId=None):
    df = pd.read_json(url)
    if lineId is not None:
        df = df[(df['trainCategory'] == 'Commuter') & (df['commuterLineID'] == lineId) & (df['cancelled'] == False)]
    else:
        df = df[(df['trainCategory'] == 'Commuter') & (df['cancelled'] == False)]
    df = df.drop(['operatorShortCode','timetableAcceptanceDate','timetableType','version','operatorUICCode','trainCategory'],axis=1)
    return df

def process_time_table_rows(df, idx, isInJSON=True):
    cols = ['stationUICCode', 'cancelled', 'causes', 'differenceInMinutes', 'scheduledTime', 'actualTime', 'commercialTrack', 'type']
    data = []

    for index, row in df.iterrows():
        if isInJSON:
            jsonString = row['timeTableRows'].replace("'", '"').replace('True', 'true').replace('False', 'false')
            row['timeTableRows'] = json.load(jsonString)
        for timeTableRow in row['timeTableRows']:
            if timeTableRow['trainStopping']:
                val = {'idx': index + idx}
                for col in cols:
                    if col in timeTableRow:
                        val[col] = timeTableRow[col]
                data.append(val)

    return pd.DataFrame.from_dict(data)

# date range have to be divisible by three
def get_data_in_three_parts(d1, d2, lineId=None):
    delta = (d2 - d1 + timedelta(days=1)) / 3

    data = get_history(d1, d1 + delta - timedelta(days=1), lineId)
    data.to_csv('temp1.csv')
    data2 = get_history(d1 + delta, d1 + 2 * delta - timedelta(days=1), lineId)
    data2.to_csv('temp2.csv')
    data3 = get_history(d1 + 2 * delta, d2, lineId)
    data3.to_csv('temp3.csv')

def combine_three_parts():
    df = pd.read_csv('temp1.csv', index_col=0)
    timeTableRows = process_time_table_rows(df, 0)
    del df['timeTableRows']
    print(1)

    idx = timeTableRows.iloc[-1,:]['idx'] + 1
    df2  = pd.read_csv('temp2.csv', index_col=0, encoding = "ISO-8859-1")
    timeTableRows = timeTableRows.append(process_time_table_rows(df2, idx), ignore_index=True)
    del df2['timeTableRows']
    print(2)

    idx = timeTableRows.iloc[-1,:]['idx'] + 1
    df3 = pd.read_csv('temp3.csv', index_col=0)
    timeTableRows = timeTableRows.append(process_time_table_rows(df3, idx), ignore_index=True)
    del df3['timeTableRows']
    print(3)

    csv_path = DATA_PATH + 'all-train-timetablerows.csv'
    timeTableRows.to_csv(csv_path, index=False)
    print(4)
    df = df.append(df2, ignore_index=True)
    df = df.append(df3, ignore_index=True)
    df.to_csv('../data/all-train.csv')

def process_causes(df=None):
    if df is None:
        df = pd.read_csv('../data/all-train-timetablerows.csv')
        causes = df[df.causes != "[]"]
        df.causes.replace(['[]'], [None], inplace=True)
    else:
        causes = df[[len(y) == 0 for y in df.causes]]
        df.causes = df.causes.apply(lambda y: None if len(y) == 0 else y)

    for index, row in causes.iterrows():
        if(row.causes):
            if df is None:
                row.causes = json.loads(row.causes.replace("'", '"'))
            df.set_value(index, "causes", row.causes[0]['categoryCode'])

    if df is None:
        df.to_csv('../data/all-train-timetablerows.csv', index=False)

# This is for counting percentages of departures that are late
def process_departure_percentages(trainno):
    to_line = DATA_PATH +'-train-percents.csv'
    index = to_line.find('-')
    csvpath = to_line[:index] + trainno + to_line[index:]

    if (os.path.isfile(csvpath)):
        return pd.read_csv(csvpath)

    get_path = DATA_PATH + 'all-train-timetablerows.csv'
    data = pd.read_csv(get_path)
    traininfo_path = DATA_PATH + 'all-train.csv'
    trainInfo = pd.read_csv(traininfo_path)
    trainInfo = trainInfo.rename(columns = {'Unnamed: 0': 'idx'})
    trainInfo = trainInfo[['idx', 'commuterLineID']]
    data = data.merge(trainInfo, on="idx")
    if (trainno != 'all'):
        data = data[(data['type'] == 'DEPARTURE') & (data['commuterLineID'] == trainno)]
    else:
        data = data[(data['type'] == 'DEPARTURE') & (data['commuterLineID'] == trainno)]

    temp = []
    percents = []
    dates = []
    current = data.iloc[0]['scheduledTime'][:10]

    j = 0
    for index, row in data.iterrows():

        date = row['scheduledTime'][:10]

        if (date > current):
            all_len = len(temp)
            late = [1 for i in temp if i > 3]
            late_len = len(late)
            percents.append((late_len / all_len) * 100)
            dates.append(current)
            current = row['scheduledTime'][:10]

            # print(temp)
            # print(j)
            temp = []
            j = 0


        else:
            temp.append(row['differenceInMinutes'])
            j += 1

    mean_data = pd.DataFrame({'date': dates, 'percents': percents})
    #print(mean_data.head(n=5))

    to_line = '../data/-train-percents.csv'
    index = to_line.find('-')
    csvpath = to_line[:index] + trainno + to_line[index:]
    mean_data.to_csv(csvpath, index=False)

    return mean_data

#Same as above,  but binary variables to every service if late / or not
#TODO
def process_service_lateness(trainno):
    to_line = DATA_PATH +'-train-late.csv'
    index = to_line.find('-')
    csvpath = to_line[:index] + trainno + to_line[index:]

    if (os.path.isfile(csvpath)):
        return pd.read_csv(csvpath)

    get_path = DATA_PATH + 'all-train-timetablerows.csv'
    data = pd.read_csv(get_path)
    traininfo_path = DATA_PATH + 'all-train.csv'
    trainInfo = pd.read_csv(traininfo_path)
    trainInfo = trainInfo.rename(columns = {'Unnamed: 0': 'idx'})
    trainInfo = trainInfo[['idx', 'commuterLineID']]
    data = data.merge(trainInfo, on="idx")
    if (trainno != 'all'):
        data = data[(data['type'] == 'DEPARTURE') & (data['commuterLineID'] == trainno)]
    else:
        data = data[(data['type'] == 'DEPARTURE') & (data['commuterLineID'] == trainno)]

    temp = []
    percents = []
    dates = []
    current = data.iloc[0]['scheduledTime'][:10]

    for index, row in data.iterrows():
        late = row['differenceInMinutes'] > 3
        temp.append(late)
        dates.append(row['scheduledTime'])

    data = pd.DataFrame({'date': dates, 'late': temp})

    to_line = DATA_PATH + '-train-late.csv'
    index = to_line.find('-')
    csvpath = to_line[:index] + trainno + to_line[index:]
    data.to_csv(csvpath, index=False)

    return 0


if __name__ == "__main__":
    #get_data_in_three_parts(date(2016, 10, 15), date(2017, 10, 15))
    #combine_three_parts()
    #process_causes()
    #process_departure_percentages('a')
    #get_data_for_current_day()
    process_service_lateness('A')
