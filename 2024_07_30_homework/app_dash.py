from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

def create_dash_app(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    
    dash_app.layout = html.Div([
        html.H1('股價指標圖形整合系統', style={'textAlign': 'center'}),
        html.Div([
            dcc.Link('Single Stock Analysis', href='/single', style={'display': 'block', 'margin': '20px auto', 'textAlign': 'center'}),
            dcc.Link('Multi Stock Analysis', href='/multi', style={'display': 'block', 'margin': '20px auto', 'textAlign': 'center'})
        ], style={'textAlign': 'center'})
    ])
    
    return dash_app
