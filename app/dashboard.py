import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from flask import Flask

server = Flask(__name__)
app = dash.Dash(server=server, name=__name__, title='Twitter sentiment analyzer')

def _load_data_into_component():
    # Load dataFrame from the CSV
    df = pd.read_csv("tweets_output.csv", names=["tweet_text", "sentiment"])

    # Configure the bar chart
    fig = px.bar(df, y="sentiment", barmode="group")
    return fig

app.layout = html.Div(children=[
    html.H1(children='Twitter real-time sentiment analysis'),

    html.Div(children='''
        The tweets are being analyzed in real-time and the results are the following:
    '''),

    dcc.Graph(
        id='example-graph',
        figure=_load_data_into_component(),

    ),
    dcc.Interval(
            id='interval-component',
            interval=3*1000, # Will trigger the callback event every 3 seconds (3*1000 milisseconds)
            n_intervals=0
        )
])

# Configure callback of dcc.Interval propriety. He reloads the data and populate the figure component.
@app.callback(Output('example-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    return _load_data_into_component()

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port="8060")
