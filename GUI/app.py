import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd 

app = dash.Dash(__name__) # initialize the Dash app

df = pd.DataFrame({
    'x' : range(1, 11),
    'y' : [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
})

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

# basically doing HTML bullshit in Python
app.layout = html.Div([
    html.H1('Main Telemetry Display', style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    html.Div([
        dcc.Graph(figure=alt_plot),
        dcc.Graph(figure=velocity_plot),
        dcc.Graph(figure=temp_plot)
    ], style={'display': 'flex', 'justifyContent': 'center', 'paddingBottom': '0px'}),

    html.Div([
        dcc.Graph(figure=lin_accel_plot),
        dcc.Graph(figure=ang_accel_plot),
        dcc.Graph(figure=orientation_plot),
    ], style={'display': 'flex', 'justifyContent': 'center'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
