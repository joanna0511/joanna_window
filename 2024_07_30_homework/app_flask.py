from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/api/single_plot', methods=['POST'])
def single_plot():
    data = request.json
    return jsonify({"message": "成功接收到數據", "data": data})

@app.route('/api/multi_plot', methods=['POST'])
def multi_plot():
    data = request.json
    return jsonify({"message": "成功接收到數據", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
