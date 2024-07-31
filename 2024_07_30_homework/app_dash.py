from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests
import dash.dependencies as dd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1('股價指標圖形整合系統', style={'textAlign': 'center'}),
    html.Div([
        dcc.Link('Single Stock Analysis', href='/single', style={'display': 'block', 'margin': '20px auto', 'textAlign': 'center'}),
        dcc.Link('Multi Stock Analysis', href='/multi', style={'display': 'block', 'margin': '20px auto', 'textAlign': 'center'})
    ], style={'textAlign': 'center'})
])

single_page = html.Div([
    html.H1('Single Stock Chart API'),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'TSMC (台股)', 'value': '2330.TW'},
            {'label': 'TSMC (ADR)', 'value': 'TSM'},
            {'label': 'NVIDIA (NVDA)', 'value': 'NVDA'},
            {'label': 'Apple (AAPL)', 'value': 'AAPL'}
        ],
        value='2330.TW',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Dropdown(
        id='chart-type-dropdown',
        options=[
            {'label': 'KD指標圖', 'value': 'KD'},
            {'label': '均價指標圖', 'value': 'MA'},
            {'label': 'RSI', 'value': 'RSI'},
            {'label': '常態分佈圖', 'value': 'Normal Distribution'},
            {'label': '盒鬚圖', 'value': 'Boxplot'},
            {'label': '股價熱力圖', 'value': 'Heatmap'}
        ],
        value='MA',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2024-01-01',
        end_date='2024-07-30',
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Button('Get Chart', id='submit-button', n_clicks=0, style={'display': 'block', 'margin': '20px auto'}),
    html.Div(id='single-chart-output', style={'textAlign': 'center', 'marginTop': '20px'})
])

multi_page = html.Div([
    html.H1('Multi Stock Chart API'),
    dcc.Dropdown(
        id='multi-tickers-dropdown',
        options=[
            {'label': 'TSMC(ADR)xNVIDIA', 'value': 'TSM_NVDA'},
            {'label': 'TSMC(ADR)xAPPLE', 'value': 'TSM_AAPL'},
            {'label': 'NVIDIAxTSMC(ADR)', 'value': 'NVDA_TSM'},
            {'label': 'APPLExTSMC(ADR)', 'value': 'AAPL_TSM'}
        ],
        value='TSM_NVDA',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Dropdown(
        id='multi-chart-type-dropdown',
        options=[
            {'label': '散佈圖', 'value': 'Scatter'},
            {'label': '迴歸分析圖', 'value': 'Regression'},
            {'label': '多股票價格圖', 'value': 'Multi-Price'},
            {'label': '決策樹圖', 'value': 'Decision Tree'}
        ],
        value='Regression',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.DatePickerRange(
        id='multi-date-picker-range',
        start_date='2022-07-01',
        end_date='2024-07-30',
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Button('Get Multi-Stock Chart', id='multi-submit-button', n_clicks=0, style={'display': 'block', 'margin': '20px auto'}),
    html.Div(id='multi-chart-output', style={'textAlign': 'center', 'marginTop': '20px'})
])

@app.callback(dd.Output('page-content', 'children'),
              [dd.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/single':
        return single_page
    elif pathname == '/multi':
        return multi_page
    else:
        return index_page

@app.callback(
    dd.Output('single-chart-output', 'children'),
    [dd.Input('submit-button', 'n_clicks')],
    [dd.State('stock-dropdown', 'stock'),
     dd.State('chart-type-dropdown', 'chart_type'),
     dd.State('date-picker-range', 'start_date'),
     dd.State('date-picker-range', 'end_date')]
)
def update_single_chart(n_clicks, stock, chart_type, start_date, end_date):
    if n_clicks > 0:
        # 構造請求的數據
        payload = {
            'stock': stock,
            'chartType': chart_type,
            'startDate': start_date,
            'endDate': end_date
        }

        # 向後端 API 發送請求
        response = requests.post('http://127.0.0.1:5000/api/single_plot', json=payload)

        if response.status_code == 200:
            # 假設返回的是 Base64 字符串，將其作為圖像顯示
            img_data = response.json().get('image', '')
            return html.Img(src='data:image/png;base64,{}'.format(img_data))
        else:
            return html.Div('Error fetching data from API', style={'color': 'red'})
    
    return html.Div('Please submit the form to see the chart.')


@app.callback(
    dd.Output('multi-chart-output', 'children'),
    [dd.Input('multi-submit-button', 'n_clicks')],
    [dd.State('multi-tickers-dropdown', 'tickers'),
     dd.State('multi-chart-type-dropdown', 'chart_type'),
     dd.State('multi-date-picker-range', 'start_date'),
     dd.State('multi-date-picker-range', 'end_date')]
)
def update_multi_chart(n_clicks, tickers, chart_type, start_date, end_date):
    if n_clicks > 0:
        # 構造請求的數據
        payload = {
            'tickers': tickers,
            'chartType': chart_type,
            'startDate': start_date,
            'endDate': end_date
        }

        # 向後端 API 發送請求
        response = requests.post('http://127.0.0.1:5000/api/multi_plot', json=payload)

        if response.status_code == 200:
            # 假設返回的是 Base64 字符串，將其作為圖像顯示,確保回調函數的返回值 是一個單獨的 HTML 元素
            img_data = response.json().get('image', '')
            return html.Img(src='data:image/png;base64,{}'.format(img_data))
        else:
            return html.Div('Error fetching data from API', style={'color': 'red'})
            
    return html.Div('Please submit the form to see the chart.')


if __name__ == '__main__':
    app.run_server(debug=True)
