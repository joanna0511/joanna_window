

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_from_directory
import yfinance as yf

from matplotlib import font_manager

font_path = 'C:/Windows/Fonts/msjh.ttc'  # Windows 上的字體路徑
font_manager.fontManager.addfont(font_path)
matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'


from io import BytesIO
import base64
from plot_methods import (
    plot_kd_chart, plot_ma_chart, plot_rsi, plot_normal_distribution,
    plot_boxplot, plot_heatmap, plot_scatter_chart, plot_regression_chart, plot_price_chart, plot_decision_tree
)

# 創建 Flask 應用實例
app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/plot', methods=['POST'])
def single_plot():
    try:
        data = request.json
        stock = data['stock']
        chart_type = data['chartType']
        start_date = data['startDate']
        end_date = data['endDate']
        
        stock_data = yf.download(stock, start=start_date, end=end_date)
        
        fig = None
        if chart_type == 'KD':
            fig = plot_kd_chart(stock_data)
        elif chart_type == 'MA':
            fig = plot_ma_chart(stock_data)
        elif chart_type == 'RSI':
            fig = plot_rsi(stock_data)
        elif chart_type == 'Normal Distribution':
            fig = plot_normal_distribution(stock_data)
        elif chart_type == 'Boxplot':
            fig = plot_boxplot(stock_data)
        elif chart_type == 'Heatmap':
            fig = plot_heatmap(stock_data)
        else:
            return jsonify({'error': 'Unknown chart type'}), 400
        
        if fig is not None:
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
            return jsonify({'image': img_str})
        else:
            return jsonify({'error': 'Failed to generate chart'}), 500
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/multi_plot', methods=['POST'])
def multi_plot():
    try:
        data = request.json
        tickers = data['tickers']
        chart_type = data['chartType']
        start_date = data['startDate']
        end_date = data['endDate']
        
        stock_data = {ticker: yf.download(ticker, start=start_date, end=end_date) for ticker in tickers}
        
        fig = None
        if chart_type == 'Scatter':
            if len(tickers) == 2:
                fig = plot_scatter_chart(stock_data, tickers)
            else:
                return jsonify({'error': '散佈圖需要選擇兩個股票'}), 400
        elif chart_type == 'Regression':
            if len(tickers) == 2:
                fig = plot_regression_chart(stock_data, tickers)
            else:
                return jsonify({'error': '迴歸分析圖需要選擇兩個股票'}), 400
        elif chart_type == 'Multi-Price':
            fig = plot_price_chart(stock_data, tickers)
        else:
            return jsonify({'error': 'Unknown chart type'}), 400
        
        if fig is not None:
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
            return jsonify({'image': img_str})
        else:
            return jsonify({'error': 'Failed to generate chart'}), 500
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': str(e)}), 500
    

    
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found. Please check the URL.", 404

if __name__ == '__main__':
    app.run(debug=True)
