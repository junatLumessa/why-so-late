import pandas as pd
import datetime
import numpy as np
from datetime import date, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn import linear_model


def get_departures():
    data = pd.read_csv('../data/data/a-train-timetablerows.csv')
    data = data[data['type'] == 'DEPARTURE']
    temp = []
    percents = []
    dates = []
    current = data.iloc[0]['scheduledTime'][:10]

    i = 0
    j = 0
    # sum = 0
    for index, row in data.iterrows():

        date = row['scheduledTime'][:10]

        if (date > current):
            all_len = len(temp)
            late = [1 for i in temp if i >= 3]
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
    print(mean_data.head(n=5))

    mean_data.to_csv('a-train-percents.csv', index=False)

    return mean_data


def date_shaper(df):
    df['date'] = [x[:10] for x in df['datetime']]
    return df


def some_regression_thing():
    training_data, test_data, train_target, test_target = divide_data()

    dummy = linear_model.LinearRegression()
    dummy.fit(training_data, train_target)

    pr = dummy.score(test_data, test_target)
    print('Linear regression score: ')
    print(pr)

    return 0

def make_binarys(df, threshold, name, bool):
    new_name = name + '_binary'
    if(bool):
        df[new_name] = df[name] < threshold
    else:
        df[new_name] = df[name] > threshold

def divide_data():
    # A - train data: percentages of trains late that day
    td = pd.read_csv('a-train-percents.csv')

    # Weather data
    wd = pd.read_csv('weather.csv')
    date_shaper(wd)

    make_binarys(td, 5, 'percents', False)
    make_binarys(wd, 0, 'tday', True)

    df = pd.merge(td, wd, how='inner', sort=True,
                  suffixes=('_t', '_w'), copy=True, indicator=False)
    # print(df.head(n=5))
    df = df.sample(frac=1)

    perc = df['percents_binary']
    temp = df['tday_binary']

    training_data, test_data, train_target, test_target = train_test_split(temp, perc, train_size=0.8)
    print('training_data size = ', len(training_data))
    # print('test_data size = ', range(len(test_data[0])))
    train_target = train_target.reshape(-1, 1)
    training_data = training_data.reshape(-1, 1)
    test_target = test_target.reshape(-1, 1)
    test_data = test_data.reshape(-1, 1)

    return training_data, test_data, train_target, test_target


def logistic_regression():
    training_data, test_data, train_target, test_target = divide_data()
    logistic = LogisticRegression()

    logistic.fit(training_data, train_target)
    print(' Logistic regression score:')
    print(logistic.score(test_data, test_target))

def dummy_classifier():
    # not working yet :( sniff..
    training_data, test_data, train_target, test_target = divide_data()
    dummy = DummyClassifier('stratified')

    dummy.fit(training_data, train_target)

    print(' Dummy classifier score:')
    print(dummy.score(test_data, test_target, sample_weight=None))


if __name__ == "__main__":
    logistic_regression()
    #dummy_classifier()
