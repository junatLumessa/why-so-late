import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
import get_weather as weather
import numpy as np

def plot_hist(type, start, end):
    df = weather.get_daily_weather_observations(start, end)
    print(df.dtypes)

    init_notebook_mode(connected=False)
    x = df['rrday']
    data = [go.Bar(
            x=df['datetime'],
            y=df[type]
    )]
    plotly.offline.plot({
        "data": data,
        "layout": Layout(title="hello world"
    )
    }, image='png', image_filename=type)

if __name__ == "__main__":
    plot_hist('snow', '2016-10-15T00:00:00Z', '2017-10-15T00:00:00Z')