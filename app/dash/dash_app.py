from dash import Dash, html
import dash_core_components as dcc

main_app_dash = Dash(__name__)

main_app_dash.layout = html.Div(
    children=[
        html.H1(children='Hello Dash'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ]
)

if __name__ == '__main__':
    app_dash.run_server()