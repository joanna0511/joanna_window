from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/single_plot', methods=['POST'])
def single_plot():
    data = request.json
    # 處理數據邏輯
    return jsonify({"message": "成功接收到數據", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
