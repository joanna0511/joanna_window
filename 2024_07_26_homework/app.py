from flask import Flask, request, jsonify, send_from_directory
import yfinance as yf
import matplotlib.pyplot as plt
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
def plot():
    try:
        data = request.json
        print("Received data:", data)
        stock = data['stock']
        chart_type = data['chartType']
        start_date = data['startDate']
        end_date = data['endDate']
        
        stock_data = yf.download(stock, start=start_date, end=end_date)
        ##print("Downloaded stock data:", stock_data.head())
        
        fig = None
        if chart_type == 'KD':
            fig = plot_kd_chart(stock_data)
        elif chart_type == 'MA':
            fig = plot_ma_chart(stock_data)
        # 添加其他圖表類型的處理
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
