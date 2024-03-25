import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_daq as daq
import plotly.express as px
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go


app = dash.Dash(__name__) # initialize the Dash app

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

'''
# function to customize plot characteristics
def update_plot_layout(plot, xaxis_title, yaxis_title, title_text):
    plot.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        }
    )
'''

'''
# Define plots
alt_plot = px.line(df, x='x', y='y', title='Altitude Plot', height=450, width=600)
velocity_plot = px.line(df, x='x', y='y', title='Velocity Plot', height=450, width=600)
temp_plot = px.line(df, x='x', y='y', title='Temperature Plot', height=450, width=600)
lin_accel_plot = px.line(df, x='x', y='y', title='Linear Acceleration', height=450, width=600)
ang_accel_plot = px.line(df, x='x', y='y', title='Angular Acceleration', height=450, width=600)
orientation_plot = px.line(df, x='x', y='y', title='Orientation', height=450, width=600)

# Update plot layout using the defined function
update_plot_layout(alt_plot, "Time (s)", "Altitude (ft)", "Altitude Plot")
update_plot_layout(velocity_plot, "Time (s)", "Velocity (m/s)", "Velocity Plot")
update_plot_layout(temp_plot, "Time (s)", "Temperature (C)", "Temperature Plot")
update_plot_layout(lin_accel_plot, "Time (s)", "Linear Acceleration (m/s^2)", "Linear Acceleration Plot")
update_plot_layout(ang_accel_plot, "Time (s)", "Angular Acceleration (m/s^2)", "Angular Acceleration Plot")
update_plot_layout(orientation_plot, "Time (s)", "Orientation", "Angular Acceleration Plot")
'''

# basically doing HTML bullshit in Python
app.layout = html.Div(children=[
    html.Div([
        dcc.Interval(
            id='interval',
            interval=100,
            n_intervals=0,
        ),
        html.H1('Main Telemetry Display', style={'textAlign': 'center', 'fontFamily': 'Arial', "color": "#FFFFFF"}),
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
    'backgroundColor': '#303030',
    'border': 'solid 5px #303030',
    'border-radius': '5px',
    'padding': '50px',
    'marginTop': '20px'
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
            height=500,
            width=650,
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
            height=500,
            width=650,
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
            height=500,
            width=650,
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
            height=500,
            width=650,
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
            height=500,
            width=650,
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
            height=500,
            width=650,
            plot_bgcolor='#303030',
            paper_bgcolor='#303030',
            font=dict(color='#FFFFFF')
        )
        return {'data': data, 'layout': layout}



if __name__ == '__main__':
    app.run_server(debug=True)