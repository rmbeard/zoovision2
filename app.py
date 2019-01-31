from flask import Flask, render_template  # this has changed
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

app = Flask(__name__)


@app.route('/')
def index():
    bar = create_plot()
    bar = slider()
    return render_template('index.html', plot=bar)


def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe

    data = [
        go.Bar(
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def slider():
    plotly.tools.set_credentials_file(username='rmbeard', api_key='BHH2yeIwQ6NAneWRj3J1')

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

    data = [dict(type='choropleth',
                 locations=df['code'].astype(str),
                 z=df['total exports'].astype(float),
                 locationmode='USA-states')]

    # let's create some additional, random data
    for i in range(5):
        data.append(data[0].copy())
        data[-1]['z'] = data[0]['z'] * np.random.rand(*data[0]['z'].shape)

    # let's create the steps for the slider
    steps = []
    for i in range(len(data)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data)],
                    label='Year {}'.format(i + 1980))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0,
                    pad={"t": 1},
                    steps=steps)]
    layout = dict(geo=dict(scope='usa',
                           projection={'type': 'albers usa'}),
                  sliders=sliders)

    fig = dict(data=data,
               layout=layout)
    # py.plot(fig)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def slider2():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

    data = [dict(type='choropleth',
                 locations=df['code'].astype(str),
                 z=df['total exports'].astype(float),
                 locationmode='USA-states')]

    # let's create some additional, random data
    for i in range(5):
        data.append(data[0].copy())
        data[-1]['z'] = data[0]['z'] * np.random.rand(*data[0]['z'].shape)

    # let's create the steps for the slider
    steps = []
    for i in range(len(data)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data)],
                    label='Year {}'.format(i + 1980))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0,
                    pad={"t": 1},
                    steps=steps)]
    layout = dict(geo=dict(scope='usa',
                           projection={'type': 'albers usa'}),
                  sliders=sliders)

    fig = dict(data=data,
               layout=layout)
    # py.plot(fig)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == '__main__':
    app.run()
