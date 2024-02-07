# pip install dash first
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd 

app = dash.Dash(__name__) # initialize the Dash app

df = pd.DataFrame({
    'x' : range(1, 11),
    'y' : [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
})

plots = [px.line(df, x='x', y='y', title=f'Plot{i}') for i in range(1, 11)]

app.layout = html.Div([
    html.H1('Dashboard with Multiple Plots'),
    html.Div([
        dcc.Graph(figure=plot) for plot in plots # dcc.Graph is used to render plots on webpage
    ], style={'columnCount' : 2})
])

if __name__ == '__main__':
    app.run_server(debug=True)