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
    print(df.dtypes)

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

def plot_line(type, start, end):
    df = weather.get_daily_weather_observations(start, end)
    print(df.dtypes)

    init_notebook_mode(connected=False)
    y = df[type]
    x = df['datetime']
    # Create a trace
    trace = go.Scatter(
        x=x,
        y=y,  line = dict(
        color = ('green'))
    )
    data = [trace]
    plotly.offline.plot({
        "data": data,
        "layout": Layout(title=type
    )
    }, image='png', image_filename=type)
    #py.image.save_as(data, filename='a-simple-plot.png')

if __name__ == "__main__":
    plot_hist('rrday', '2016-10-15T00:00:00Z', '2017-10-15T00:00:00Z')

    #plot_line('snow', '2016-10-17T00:00:00Z', '2017-10-17T00:00:00Z')