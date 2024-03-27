import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_daq as daq
import plotly.express as px
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go


app = dash.Dash(__name__) # initialize the Dash app

# general variables
plot_height = 400
plot_width = 550


# basically doing HTML bullshit in Python
app.layout = html.Div(children=[
    html.Div([

        # Allows tracking of time
        dcc.Interval(
            id='interval',
            interval=100,
            n_intervals=0,
        ),

        # Div for header and top functions
        html.Div([
            html.H1('Main Telemetry Display', style={'textAlign': 'center', 'fontFamily': 'Arial', "color": "#FFFFFF", 'display': 'flex', 'justifyContent': 'center', 'alignContent': 'center'}),
            ], style={'width': '25vw', 'height': '10vh', 'top': '0vh', 'left': '50vw', 'border': '5px solid white', 'display': 'flex', 'justifyContent': 'center', 'alignContent': 'center'}),
        
        # Div for 1st row of graphs
        html.Div([
            dcc.Graph(
                id='Altitude-Plot',
                config={'displayModeBar': False},
            ),
            dcc.Graph(
                id='Velocity-Plot',
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='Temperature-Plot',
                config={'displayModeBar': False}
            )
        ], style={'display': 'flex', 'justifyContent': 'center', 'paddingBottom': '5px'}),

        # Div for 2nd row of graphs
        html.Div([
            dcc.Graph(
                id='LinearAccel-Plot',
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='AngularAccel-Plot',
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='Orientation-Plot',
                config={'displayModeBar': False}
            ),
        ], style={'display': 'flex', 'justifyContent': 'center'})
    ]),
], style={
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'width': '100vw',
    'height': '100vh',
    'backgroundColor': '#303030',
})


# callback functions to update graphs
@app.callback(
    Output('Altitude-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_alt(n):
    x = np.linspace(0, n/10, 1000)
    y = (-0.5*(x-14)**2)+100 # placeholder value
    if np.any(y < 0):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines', line=dict(color='#FF10F0'))]
        layout = go.Layout(
            title='Altitude-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Altitude'),
            height=plot_height,
            width=plot_width,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}
    
@app.callback(
    Output('Velocity-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_vel(n):
    x = np.linspace(0, n/10, 1000)
    y = -x+14 # palceholder value
    if np.any(y < -14):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines', line=dict(color='#FF10F0'))]
        layout = go.Layout(
            title='Velocity-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Velocity'),
            height=plot_height,
            width=plot_width,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}
    
@app.callback(
    Output('Temperature-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_temp(n):
    x = np.linspace(0, n/10, 1000)
    y = x # placeholder value
    if np.any(y < 0):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines', line=dict(color='#FF10F0'))]
        layout = go.Layout(
            title='Temperature-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Temperature'),
            height=plot_height,
            width=plot_width,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}
    
@app.callback(
    Output('LinearAccel-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_lin_accel(n):
    x = np.linspace(0, n/10, 1000)
    y = x # placeholder value
    if np.any(y < 0):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines', line=dict(color='#FF10F0'))]
        layout = go.Layout(
            title='LinearAccel-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Acceleration'),
            height=plot_height,
            width=plot_width,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}

@app.callback(
    Output('AngularAccel-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_ang_accel(n):
    x = np.linspace(0, n/10, 1000)
    y = x # placeholder value
    if np.any(y < 0):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines', line=dict(color='#FF10F0'))]
        layout = go.Layout(
            title='AngularAccel-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Acceleration'),
            height=plot_height,
            width=plot_width,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}

@app.callback(
    Output('Orientation-Plot', 'figure'),
    Input('interval', 'n_intervals')
)
def update_orientation(n):
    x = np.linspace(0, n/10, 1000)
    y = x # placeholder value
    if np.any(y < 0):
        raise PreventUpdate
    else:
        data = [go.Scatter(x=x, y=y, mode='lines', line=dict(color='#FF10F0'))]
        layout = go.Layout(
            title='Orientation-Plot', 
            xaxis=dict(title='Time'), 
            yaxis=dict(title='Orientation'),
            height=plot_height,
            width=plot_width,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}



if __name__ == '__main__':
    app.run_server(debug=True)