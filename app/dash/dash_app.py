from dash import Dash, html, dcc
from flask import Flask

#main_app_dash = Dash(__name__, server=Flask(__name__), url_base_pathname='/dashboard/')
main_app_dash = Dash(__name__, server=Flask(__name__))

main_app_dash.title = 'Mi Dash App'




def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div(
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
    return dash_app.server

