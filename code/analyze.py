import pandas as pd
import datetime
import numpy as np
from datetime import date, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn.multiclass import OneVsRestClassifier



def date_shaper(df):
    df['date'] = [x[:10] for x in df['datetime']]
    return df


def some_regression_thing(column):
    training_data, test_data, train_target, test_target = prepare_data(column)

    dummy = linear_model.LinearRegression()
    dummy.fit(training_data, train_target)
    dummy.predict(test_data)

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

#More classes than just True/False TODO
def make_more_binarys(df, threshold, name, bool):
    new_name = name + '_binary'
    if(bool):
        for val in threshold:
            df[new_name] = df.loc[df[name] < val, name] = val
    else:
        for val in threshold:
            df[new_name] = df.loc[df[name] > val, name] = val

#Get's data, makes binary variables and divides dataset into training and test set
def prepare_data(column, multiple=False):
    # A - train data: percentages of trains late that day
    td = pd.read_csv('../data/a-train-percents.csv')

    # Weather data
    wd = pd.read_csv('../data/weather.csv')
    date_shaper(wd)

    if(multiple):
        thresholds_trains = [20, 10, 5]
        make_more_binarys(td, thresholds_trains, 'percents', False)

        if (column is 'tday'):
            thresholds_temp = [0,-5,-10]
            make_more_binarys(wd, thresholds_temp, column, True)
        else:
            make_more_binarys(wd, thresholds_trains, column, False)
    else:
        make_binarys(td, 5, 'percents', False)

        if(column is 'tday'):
            make_binarys(wd, 0, column, True)
        else:
            make_binarys(wd, 0, column, False)

    df = pd.merge(td, wd, how='inner', sort=True,
                  suffixes=('_t', '_w'), copy=True, indicator=False)
    # print(df.head(n=5))
    df = df.sample(frac=1)

    perc = df['percents_binary']
    column_name = column + '_binary'
    explain = df[column_name]

    training_data, test_data, train_target, test_target = train_test_split(explain, perc, train_size=0.8)
    #print('training_data size = ', len(training_data))
    # print('test_data size = ', range(len(test_data[0])))
    if(not multiple):
        train_target = train_target.values.reshape(-1, 1)
        training_data = training_data.values.reshape(-1, 1)
        test_target = test_target.values.reshape(-1, 1)
        test_data = test_data.values.reshape(-1, 1)

    return training_data, test_data, train_target, test_target

#Logistic regression with two binary variables (True/False)
def logistic_regression(column):
    training_data, test_data, train_target, test_target = prepare_data(column)
    logistic = LogisticRegression()

    logistic.fit(training_data, train_target)
    predicted_log = logistic.predict(test_data)
    score = logistic.score(test_data, test_target)
    print(' Logistic regression score:')
    print(score)

    wrong = [1 for i in test_target if i != predicted_log[test_target.tolist().index(i)]]
    print('Amount of wrong classified: %d ' % len(wrong))

#Nice try, prediction accuracy too good.... Maybe use floats rounded as ints for prediction? TODO
def oneVSRest(column):
    training_data, test_data, train_target, test_target = prepare_data(column, True)
    OVR = OneVsRestClassifier(LogisticRegression()).fit(training_data, train_target)
    print('One vs rest accuracy: % .3f' % OVR.score(test_data, test_target))



def dummy_classifier(column):
    # not working yet :( sniff..
    training_data, test_data, train_target, test_target = prepare_data(column)
    dummy = DummyClassifier('stratified')

    dummy.fit(training_data, train_target)

    print(' Dummy classifier score:')
    print(dummy.score(test_data, test_target, sample_weight=None))


if __name__ == "__main__":
    logistic_regression('tday')
    #oneVSRest('tday')
    #some_regression_thing('snow')
    #dummy_classifier()
