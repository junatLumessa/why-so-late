import pandas as pd
from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
from plotly.graph_objs import Layout

def plot_a_train():
    df = pd.read_csv('../data/a-train-timetablerows.csv')

    init_notebook_mode(connected=False)
    data = [go.Histogram(
            x=df['differenceInMinutes']
            )]

    plot({
        "data": data,
        "layout": Layout(title="Difference in minutes for A-train")
    }, image='png', image_filename="differenceInMinutes")


if __name__ == "__main__":
    plot_a_train()
