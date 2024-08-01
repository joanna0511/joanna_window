from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash.dependencies as dd
import requests
from flask import Flask, request, jsonify
from plot_methods import plot_kd_chart
import io
import base64

# 创建 Flask 服务器
server = Flask(__name__)

@server.route('/api/single_plot', methods=['POST'])
def single_plot():
    data = request.json
    print(f"Received data: {data}")
    
    # 使用 plot_methods 中的函数生成图表
    fig = None
    if data['chartType'] == 'KD':
        fig = plot_kd_chart(data)  # 假设 plot_kd_chart 接受 data 字典
        print(f"Generated chart for {data['chartType']} and stock {data['stock']}")

    if fig is None:
        print("Failed to generate chart.")
        return jsonify({"error": "Error generating chart."}), 500
    
    # 将图表转换为 Base64 字符串
    img_io = io.BytesIO()
    fig.savefig(img_io, format='png')
    img_io.seek(0)
    base64_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
    print(f"Generated Base64 image data length: {len(base64_img)}")

    return jsonify({"image": base64_img})

@server.route('/api/multi_plot', methods=['POST'])
def multi_plot():
    data = request.json
    # 处理多股票数据并生成图表逻辑
    base64_image = "base64encodedimagestring"
    return jsonify({"image": base64_image})

def create_dash_app(server):
    app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    index_page = html.Div([
        html.H1('股价指标图形整合系统', style={'textAlign': 'center'}),
        html.Div([
            dcc.Link('单一股票分析', href='/single', style={'display': 'block', 'margin': '20px auto', 'textAlign': 'center'}),
            dcc.Link('多股票分析', href='/multi', style={'display': 'block', 'margin': '20px auto', 'textAlign': 'center'})
        ], style={'textAlign': 'center'})
    ])

    single_page = html.Div([
        html.H1('单一股票图表 API'),
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
                {'label': 'KD 指标图', 'value': 'KD'},
                {'label': '均价指标图', 'value': 'MA'},
                {'label': 'RSI', 'value': 'RSI'},
                {'label': '常态分布图', 'value': 'Normal Distribution'},
                {'label': '盒须图', 'value': 'Boxplot'},
                {'label': '股价热力图', 'value': 'Heatmap'}
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
        html.H1('多股票图表 API'),
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
                {'label': '散布图', 'value': 'Scatter'},
                {'label': '回归分析图', 'value': 'Regression'},
                {'label': '多股票价格图', 'value': 'Multi-Price'},
                {'label': '决策树图', 'value': 'Decision Tree'}
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

    @app.callback(dd.Output('page-content', 'children'), [dd.Input('url', 'pathname')])
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
        [dd.State('stock-dropdown', 'value'),
         dd.State('chart-type-dropdown', 'value'),
         dd.State('date-picker-range', 'start_date'),
         dd.State('date-picker-range', 'end_date')]
    )
    def update_single_chart(n_clicks, stock, chart_type, start_date, end_date):
        if n_clicks > 0:
            try:
                payload = {
                    'stock': stock,
                    'chartType': chart_type,
                    'startDate': start_date,
                    'endDate': end_date
                }

                response = requests.post('http://127.0.0.1:5000/api/single_plot', json=payload)
                print(f"API response status code: {response.status_code}")
                if response.status_code == 200:
                    img_data = response.json().get('image', '')
                    print(f"Received Base64 image data length: {len(img_data)}")
                    if img_data:
                        return html.Img(src=f'data:image/png;base64,{img_data}')
                    else:
                        return html.Div('No image data received from API', style={'color': 'red'})
                else:
                    return html.Div(f'Error fetching data from API (status code: {response.status_code})', style={'color': 'red'})
        
            except Exception as e:
                print(f"Error during API request: {e}")
                return html.Div(f'Error during API request: {e}', style={'color': 'red'})
    
        return html.Div('Please submit the form to see the chart.')

    @app.callback(
        dd.Output('multi-chart-output', 'children'),
        [dd.Input('multi-submit-button', 'n_clicks')],
        [dd.State('multi-tickers-dropdown', 'value'),
         dd.State('multi-chart-type-dropdown', 'value'),
         dd.State('multi-date-picker-range', 'start_date'),
         dd.State('multi-date-picker-range', 'end_date')]
    )
    def update_multi_chart(n_clicks, tickers, chart_type, start_date, end_date):
        if n_clicks > 0:
            try:
                payload = {
                    'tickers': tickers,
                    'chartType': chart_type,
                    'startDate': start_date,
                    'endDate': end_date
                }

                response = requests.post('http://127.0.0.1:5000/api/multi_plot', json=payload)
                if response.status_code == 200:
                    img_data = response.json().get('image', '')
                    if img_data:
                        return html.Img(src='data:image/png;base64,{}'.format(img_data))
                    else:
                        return html.Div('No image data received from API', style={'color': 'red'})
                else:
                    return html.Div(f'Error fetching data from API (status code: {response.status_code})', style={'color': 'red'})
            
            except Exception as e:
                print(f"Error during API request: {e}")
                return html.Div(f'Error during API request: {e}', style={'color': 'red'})

        return html.Div('Please submit the form to see the chart.')

    return app

# 创建 Dash 应用并将其绑定到 Flask 服务器
app = create_dash_app(server)

# 启动 Flask 服务器
if __name__ == '__main__':
    server.run(debug=True)
