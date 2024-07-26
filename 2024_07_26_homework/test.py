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
        print("Downloaded stock data:", stock_data.head())
        
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
