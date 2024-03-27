from dash import Dash, html, dcc, callback, Output, Input
import numpy as np
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    dcc.Interval(
        id='interval',
        interval=100,  # Update every 100 milliseconds
        n_intervals=0
    ),
    html.Div(
        dcc.Graph(
            id='Trajectory-Plot',
            config={'displayModeBar': False}
        ),
        style={'width': '50%', 'margin': 'auto'}
    )
])

@app.callback(
    Output('Trajectory-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_trajectory(n):
    x = np.linspace(0, n/10, 1000)
    y = (-0.5*(x-14)**2)+100
    if np.any(y < 0):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines')]
        layout = go.Layout(
            title='Trajectory-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Altitude'),
            height=500,
            width=650
        )
        return {'data': data, 'layout': layout}


if __name__ == '__main__':
    app.run_server(debug=True)
