import pandas as pd
from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import plotly.offline as offline
from plotly.graph_objs import Layout
import analyze as az


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


def plot_a_train_late():
    df = az.get_departures()
    print(df.head(n=5))
    init_notebook_mode(connected=True)
    trace1 = [go.Bar(
        x=df['date'],
        y=df['percents'],
        text=df['percents'],
        textposition='auto',
        marker=dict(
            color='#f46542',

        )
    )]
    data = trace1
    layout = go.Layout(

        yaxis=dict(
            range=[0, 20.5]
        ), title="Late departures of A-train, more than 3 minutes late"
    )

    offline.plot({
        "data": data,
        "layout": layout
    }, image='png', image_filename="lateThreeMinutes")

def plot_delay_causes():
    #run get_data/process_causes() before running this
    df = pd.read_csv('../data/a-train-timetablerows.csv')
    codes = pd.read_csv('delay_codes.csv')
    delays = df[df.causes.notnull()]
    delays = delays[['causes','actualTime','differenceInMinutes','stationUICCode']]

    counts = delays.causes.value_counts().reset_index()
    counts.columns = ['causes', 'count']
    counts = counts.merge(codes, on="causes")

    delayInMinutesMean = delays.groupby(['causes'])['differenceInMinutes'].mean().reset_index()
    counts = counts.merge(delayInMinutesMean, on="causes")
    print(counts)

if __name__ == "__main__":
    # plot_a_train()
    # plot_a_train_late()
    plot_a_train_late()
