from dash import Dash, dcc, html, Input, Output, callback

app = Dash(__name__)

count = 0

app.layout = html.Div([
    html.H3('Testing Radio Button Callbacks'),
    dcc.RadioItems(options=['Hello', 'World', 'Testing', '1', '2', '3'], value='Hello', id='radio-button-control'),
    html.H3('Output: ', id='test-output')
])

@callback(
    Output(component_id='test-output', component_property='children'),
    Input(component_id='radio-button-control', component_property='value')
)
def update_output(input_value):
    return input_value

if __name__ == '__main__':
    app.run(debug=True)