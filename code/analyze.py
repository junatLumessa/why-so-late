import pandas as pd
import datetime
import numpy as np
from get_data import process_departure_percentages, process_service_lateness
from datetime import date, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

LINE_IDS = ['A', 'D', 'E', 'G', 'I', 'K', 'L', 'N', 'P', 'R', 'T', 'U', 'X', 'Y', 'Z']
BINARY_THRESHOLDS = {'rrday': 0, 'snow': 0, 'tday': 0, 'percents': 5}
MULTIPLE_BINARY_THRESHOLDS = {'tday': [-10, -5, 0]}
#FILL HERE YOUR DATA FOLDER PATH!
DATA_PATH = '../data/'
RFC_classifier = RandomForestClassifier(200)


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
    weather_path = DATA_PATH + 'weather.csv'
    wd = pd.read_csv(weather_path)
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
    #perc = td['percents']
    td = td.drop(['date', 'datetime', 'percents'], axis=1)

    # suffles and splits data
    return train_test_split(td, perc, test_size=0.2)

#Same as before, but we do not calculate daily percentages.
#Instead we have binary 0/1 indicating if service was late or not
def prepare_data_daily(lineId = 'A', column=None, binaryColumns=[], multipleBinaryColumns=[]):
    td = process_service_lateness('A')


    return 0


########################## Classificators #####################################

def some_regression_thing(lineId):
    training_data, test_data, train_target, test_target = prepare_data(lineId, None, [], [])

    dummy = linear_model.LinearRegression()
    dummy.fit(training_data, train_target)
    ypred = dummy.predict(test_data)

    #ypred = ypred.reshape(-1,1)
    #test_target = test_target.reshape(-1, 1)

    pr = dummy.score(training_data, train_target)



    test_target = [round(i) for i in test_target]
    ypred = [round(i) for i in ypred]
    print(ypred)
    print(list(test_target))

    correct = []
    i = 0
    for val, real in zip(ypred, test_target):
        if val == real:
            correct.append(val)
        i += 1

    correct_percent = len(correct)/len(test_target)
    print('Accuracy score for Linear regression with binarys for {} trains: {:0.2f}'.format(lineId,
                                                                                            correct_percent))
    print('')

    return correct_percent

#Logistic regression with two binary variables (True/False)
def logistic_regression(lineId):
    training_data, test_data, train_target, test_target = prepare_data(lineId, None, ['snow','rrday'], ['tday'])
    print(training_data)
    logistic = LogisticRegression()

    logistic.fit(training_data, train_target)
    predicted_log = logistic.predict(test_data)
    score = logistic.score(test_data, test_target)
    print(' Logistic regression score:')
    print(score)

    #wrong = [1 for i in test_target if i != predicted_log[test_target.tolist().index(i)]]
    #print('Amount of wrong classified: %d ' % len(wrong))
    return score

#Nice try, prediction accuracy too good.... Maybe use floats rounded as ints for prediction? TODO
def oneVSRest(lineId):
    training_data, test_data, train_target, test_target = prepare_data(lineId, None,  ['snow','rrday'], ['tday'])
    OVR = OneVsRestClassifier(LogisticRegression()).fit(training_data, train_target)
    print('One vs rest accuracy: % .3f' % OVR.score(test_data, test_target))



def dummy_classifier(lineId, column):
    # not working yet :( sniff..
    training_data, test_data, train_target, test_target = prepare_data(['snow','rrday'], ['tday'])
    dummy = DummyClassifier('stratified')

    dummy.fit(training_data, train_target)

    print(' Dummy classifier score:')
    print(dummy.score(test_data, test_target, sample_weight=None))

def randomForestClassifier(lineId):
    Xtrain, Xtest, ytrain, ytest = prepare_data(lineId, None, ['snow','rrday'], ['tday'])

    RFC = RandomForestClassifier(200)
    RFC.fit(Xtrain, ytrain)
    ypred = RFC.predict(Xtest)
    print('Accuracy score for OVR classifier with binarys for {} trains: {:0.2f}'.format(lineId, accuracy_score(ytest, ypred)))
    print('')
    return RFC

def gaussianProcessClassifier(lineId):
    Xtrain, Xtest, ytrain, ytest = prepare_data(lineId, None, ['snow', 'rrday'], ['tday'])
    gpc = GaussianProcessClassifier(1 * RBF(1.0))
    gpc.fit(Xtrain, ytrain)

    pred = gpc.predict(Xtest)
    print('Accuracy score for Gaussian Process Classifier with binarys for {} trains: {:0.2f}'.format(lineId,
                                                                                         accuracy_score(ytest, pred)))
    print('')

    return accuracy_score(ytest, pred)


# Trial to predict what trains are late on 26.10.2017
def predict_next_day(lineId = 'D', datetime = '26.10.2017'):
    Xtrain, Xtest, ytrain, ytest = prepare_data(lineId, None, ['snow', 'rrday'], ['tday'])
    RFC = RandomForestClassifier(200)
    RFC.fit(Xtrain, ytrain)
    #print(Xtest.dtype)

    d = {'rrday':1,  'snow':1, 'tday':3}
    weather_day = pd.DataFrame(data=[d], columns=['rrday', 'snow', 'tday'])
    print(weather_day)
    pred = RFC.predict(weather_day)

    print('Predicted: {}'.format(pred))

    return 0
################################################################################
'''
def save_scores():

    lineIds = []
    scores = []
    for lineId in LINE_IDS:
        RFC = randomForestClassifier(lineId)
        #GPC = gaussianProcessClassifier(lineId)
        #linear = some_regression_thing(lineId)
        #OVR = oneVSRest(lineId)
        #LOG = logistic_regression(lineId)
        lineIds.append(lineId)
        scores.append(RFC)
    csv_path = DATA_PATH + "oneVSRest.csv"
    df = pd.DataFrame({'lineId': lineIds, 'score':scores})
    df.to_csv(csv_path , index=False)
'''

def get_classifier_for_all_line_ids():
    classifiers = []
    for lineId in LINE_IDS:
        classifiers.append({'lineId': lineId, 'classifier': randomForestClassifier(lineId)})
    return classifiers

def save_predictions(df):
    csv_path = DATA_PATH + 'predictions.csv'
    df.to_csv(DATA_PATH , index=False)

if __name__ == "__main__":
    get_classifier_for_all_line_ids()


