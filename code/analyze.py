import pandas as pd
import datetime
import numpy as np
from datetime import date, timedelta



def get_departures():
    data = pd.read_csv('../data/data/a-train-timetablerows.csv')
    data = data[data['type'] == 'DEPARTURE']
    temp = []
    percents = []
    dates = []
    current = data.iloc[0]['scheduledTime'][:10]

    i = 0
    j = 0
    #sum = 0
    for index, row in data.iterrows():

        date = row['scheduledTime'][:10]

        if(  date > current):
            all_len = len(temp)
            late = [1 for i in temp if i >= 3]
            late_len = len(late)
            percents.append((late_len/all_len)*100)
            dates.append(current)
            current = row['scheduledTime'][:10]

            #print(temp)
           # print(j)
            temp = []
            j = 0


        else:
            temp.append(row['differenceInMinutes'])
            j +=1


    mean_data = pd.DataFrame({'date': dates, 'percents': percents})
    print(mean_data.head(n=5))

    mean_data.to_csv('a-train-percents.csv', index=False)

    return mean_data

def some_regression_thing():
    return 0




if __name__ == "__main__":
    get_departures()
