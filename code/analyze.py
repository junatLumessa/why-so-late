import pandas as pd
import datetime
import numpy as np
from get_data import process_departure_percentages
from datetime import date, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score

LINE_IDS = ['A', 'D', 'E', 'G', 'I', 'K', 'L', 'N', 'P', 'R', 'T', 'U', 'X', 'Y', 'Z']
BINARY_THRESHOLDS = {'rrday': 0, 'snow': 0, 'tday': 0, 'percents': 5}
MULTIPLE_BINARY_THRESHOLDS = {'tday': [-10, -5, 0]}


####################### Data preparing #########################################

def make_more_binarys(df, column):
    def to_binary(x):
        idx = 0
        for t in MULTIPLE_BINARY_THRESHOLDS[column]:
            if x < t:
                return idx
            idx += 1
        return idx

    df[column] = df[column].map(to_binary)


# Get's data and divides dataset into training and test set
# Parameters:
# lineId: train line id
# column: weather data column used for classification, if none, all of the columns rrday, snow and tday will be used
# binaryColumns: columns which are converted to binary values
# multipleBinaryColumns: columns which are converted to multiple binary columns
def prepare_data(lineId = 'A', column=None, binaryColumns=[], multipleBinaryColumns=[]):
    if column:
        wdColumns = [column, 'datetime']
    else:
        wdColumns = ['rrday', 'snow', 'tday', 'datetime']

    # Train data: percentages of trains late that day for given line id
    td = process_departure_percentages(lineId)

    # Weather data
    wd = pd.read_csv('../data/weather.csv')
    wd = wd[wdColumns]

    wd['date'] = wd['datetime'].str.slice(0, 10)

    if (len(binaryColumns) >= 1):
        for column in binaryColumns:
            wd[column] = (wd[column] >= BINARY_THRESHOLDS[column]).astype('int')

    if (len(multipleBinaryColumns) >= 1):
        for column in multipleBinaryColumns:
            make_more_binarys(wd, column)

    td = td.merge(wd, on="date")
    perc = (td['percents'] >= BINARY_THRESHOLDS['percents']).astype('int')
    td = td.drop(['date', 'datetime', 'percents'], axis=1)

    # suffles and splits data
    return train_test_split(td, perc, test_size=0.2)


########################## Classificators #####################################

def some_regression_thing(lineId, column):
    training_data, test_data, train_target, test_target = prepare_data(lineId, column, [column])

    dummy = linear_model.LinearRegression()
    dummy.fit(training_data, train_target)
    dummy.predict(test_data)

    pr = dummy.score(test_data, test_target)
    print('Linear regression score: ')
    print(pr)

    return 0

#Logistic regression with two binary variables (True/False)
def logistic_regression(lineId, column):
    training_data, test_data, train_target, test_target = prepare_data(lineId, column, [column])
    print(training_data)
    logistic = LogisticRegression()

    logistic.fit(training_data, train_target)
    predicted_log = logistic.predict(test_data)
    score = logistic.score(test_data, test_target)
    print(' Logistic regression score:')
    print(score)

    wrong = [1 for i in test_target if i != predicted_log[test_target.tolist().index(i)]]
    print('Amount of wrong classified: %d ' % len(wrong))

#Nice try, prediction accuracy too good.... Maybe use floats rounded as ints for prediction? TODO
def oneVSRest(lineId, column):
    training_data, test_data, train_target, test_target = prepare_data(lineId, column, [], [column])
    OVR = OneVsRestClassifier(LogisticRegression()).fit(training_data, train_target)
    print('One vs rest accuracy: % .3f' % OVR.score(test_data, test_target))



def dummy_classifier(lineId, column):
    # not working yet :( sniff..
    training_data, test_data, train_target, test_target = prepare_data(lineId, column, [column])
    dummy = DummyClassifier('stratified')

    dummy.fit(training_data, train_target)

    print(' Dummy classifier score:')
    print(dummy.score(test_data, test_target, sample_weight=None))

def randomForestClassifier(lineId):
    Xtrain, Xtest, ytrain, ytest = prepare_data(lineId)

    #unique, counts = np.unique(ytest, return_counts=True)
    #print(dict(zip(unique, counts)))

    RFC = RandomForestClassifier(200)
    RFC.fit(Xtrain, ytrain)
    ypred = RFC.predict(Xtest)

    print('Accuracy score for OVR classifier without binarys for {} trains: {:0.2f}'.format(lineId, accuracy_score(ytest, ypred)))

    Xtrain, Xtest, ytrain, ytest = prepare_data(lineId, None, ['rrday', 'tday'], ['tday'])
    RFC = RandomForestClassifier(200)
    RFC.fit(Xtrain, ytrain)
    ypred = RFC.predict(Xtest)

    print('Accuracy score for OVR classifier with binarys for {} trains: {:0.2f}'.format(lineId, accuracy_score(ytest, ypred)))
    print('')
################################################################################

def get_classifier_for_all_line_ids():
    for lineId in LINE_IDS:
        RFC = randomForestClassifier(lineId)

if __name__ == "__main__":
    #logistic_regression('A', 'tday')
    #oneVSRest('A', 'tday')
    #some_regression_thing('A', 'snow')
    #dummy_classifier('A', 'tday')
    get_classifier_for_all_line_ids()
