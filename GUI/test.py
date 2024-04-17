from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Testing for basic callback
'''
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Test'),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph')
])

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)

def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

button_name = 'Start'


app.layout = html.Div([
    html.Button(button_name, id='button'),
    html.Div(id='output')
])

@app.callback(
    Output('button', 'children'),
    Input('button', 'n_clicks'),
    State('button', 'children')
)
def update_output(n_clicks, button_name):
    if n_clicks:
        if button_name == 'Start':
            button_name = 'Stop'
        elif button_name == 'Stop':
            button_name = 'Start'
    return button_name

if __name__ == '__main__':
    app.run_server(debug=True)

