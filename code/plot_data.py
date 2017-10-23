import pandas as pd
from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import plotly.offline as offline
from plotly.graph_objs import Layout
import analyze as az
import get_weather as weather


def plot_a_train():
    df = pd.read_csv('../data/a-train-timetablerows.csv')

    init_notebook_mode(connected=False)
    data = [go.Histogram(
        x=df['differenceInMinutes'],
        xbins=dict(
            start=-1.5,
            end=20.5,
            size=1
        ),
    )]

    plot({
        "data": data,
        "layout": Layout(title="Difference in minutes for A-train")
    }, image='png', image_filename="differenceInMinutes")


def plot_a_train_late():
    df = pd.read_csv('../data/a-train-timetablerows.csv')

    init_notebook_mode(connected=False)
    data = [go.Histogram(
        x=df['differenceInMinutes'],
        xbins=dict(
            start=2.5,
            end=20.5,
            size=1
        ),
        marker=dict(
            color='#f46542',
        )
    )]

    plot({
        "data": data,
        "layout": Layout(title="Difference in minutes for A-train, more than 3 minutes late")
    }, image='png', image_filename="differenceInMinutesThree")

def plot_delay_causes():
    #run get_data/process_causes() before running this
    df = pd.read_csv('../data/a-train-timetablerows.csv')
    codes = pd.read_csv('../data/delay_codes.csv')
    delays = df[df.causes.notnull()]
    delays = delays[['causes','actualTime','differenceInMinutes','stationUICCode']]

    counts = delays.causes.value_counts().reset_index()
    counts.columns = ['causes', 'count']
    counts = counts.merge(codes, on="causes")

    delayInMinutesMean = delays.groupby(['causes'])['differenceInMinutes'].mean().reset_index()
    counts = counts.merge(delayInMinutesMean, on="causes")
    print(counts)

def plot_a_train_and_weather(column):
    #A - train data: percentages of trains late that day
    td = pd.read_csv('../data/a-train-percents.csv')

    #Weather data
    wd = pd.read_csv('../data/weather.csv')
    if column is not 'tday':
        wd = weather.delete_minuses(wd, column)

    init_notebook_mode(connected=False)
    trace1 = go.Scatter(
        x=wd['datetime'],
        y=wd[column]
    )
    trace2 = go.Bar(
        x=td['date'],
        y=td['percents']
    )

    data = [trace1, trace2]
    offline.plot({
        "data": data
    }, image='png', image_filename="bar-plot")

# todo
"""
def plot_time_and_late():
    data = pd.read_csv('../data/all-train-timetablerows.csv')

    data = data[data['type'] == 'DEPARTURE']
    data['late'] = (data['differenceInMinutes'] >= 3).astype('int')
    data['time'] = data['scheduledTime'].str.slice(11, 13)

    late = data[data['late'] == 1]

    init_notebook_mode(connected=False)
    hist = [
    go.Histogram(
        x=data['time']
    ),
    go.Histogram(
        x=late['time'],
        y=late['late'],
        marker=dict(
            color='#f46542',
        )
    )
    ]

    plot({
        "data": hist,
        "layout": Layout(title="Time, late")
    }, image='png', image_filename="timeLate")
"""

def plot_average_delays_by_lineid():
    df = pd.read_csv('../data/all-train-timetablerows.csv')
    trainInfo = pd.read_csv('../data/all-train.csv')
    trainInfo = trainInfo.rename(columns = {'Unnamed: 0': 'idx'})
    trainInfo = trainInfo[['idx', 'commuterLineID']]

    df = df.merge(trainInfo, on="idx")

    result = df.groupby(['commuterLineID'])['differenceInMinutes'].mean().reset_index()
    #result2 = df.groupby(['commuterLineID']).count().reset_index()

    init_notebook_mode(connected=False)
    hist = [
    go.Bar(
        x=result['commuterLineID'],
        y=result['differenceInMinutes'],
        marker=dict(
            color='green',
        )
    )
    ]

    plot({
        "data": hist,
        "layout": Layout(title="Average delays of commuter trains")
    }, image='png', image_filename="averageDelays")


if __name__ == "__main__":
    # plot_a_train()
    # plot_a_train_late()
    # plot_a_train_and_weather('tday')
    #plot_time_and_late()
    plot_average_delays_by_lineid()
