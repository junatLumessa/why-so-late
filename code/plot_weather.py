import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
import get_weather as weather
import numpy as np

def plot_hist(type, start, end):
    df = weather.get_daily_weather_observations(start, end)
    df = weather.delete_minuses(df, type)
    print(df)

    init_notebook_mode(connected=False)
    data = [go.Bar(
            x=df['datetime'],
            y=df[type]
    )]
    plotly.offline.plot({
        "data": data,
        "layout": Layout(title='Amount of ' + type
    )
    }, image='png', image_filename=type)

def plot_hist_weather(type, start, end):
    df = weather.get_weather_observations(start, end)
    print(df)


    init_notebook_mode(connected=False)
    data = [go.Bar(
            x=df['datetime'],
            y=df[type]
    )]
    plotly.offline.plot({
        "data": data,
        "layout": Layout(title= type
    )
    }, image='png', image_filename=type)

if __name__ == "__main__":
    #plot_hist('rrday', '2016-10-15T00:00:00Z', '2017-10-15T00:00:00Z')

    plot_hist_weather('wg_10min', '2017-10-10T00:00:00Z', '2017-10-17T00:00:00Z')