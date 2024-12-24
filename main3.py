from flask import Flask, request, jsonify, render_template
import random
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index4.html')  # Renders the front-end HTML

@app.route('/live-data', methods=['GET'])
def live_data():
    # Simulated RockBLOCK data payload
    data = {
        "latitude": random.uniform(-90.0, 90.0),
        "longitude": random.uniform(-180.0, 180.0),
        "timestamps": [time.time() - i * 60 for i in range(10)],
        "altitudes": [random.uniform(1000, 20000) for _ in range(10)]
    }
    return jsonify(data)

@app.route('/rockblock/MT', methods=['POST'])
def receive_mt():
    imei = request.args.get('imei')
    username = request.args.get('username')
    password = request.args.get('password')
    data = request.args.get('data')

    # Validate input (simulate simple validation for testing)
    if imei != "300434065264590" or username != "myUser" or password != "myPass":
        return "FAILED,10,Invalid login credentials", 400

    if not data:
        return "FAILED,16,No data", 400

    # Simulate decoding hex data
    try:
        decoded_message = bytes.fromhex(data).decode('utf-8')
    except ValueError:
        return "FAILED,14,Could not decode hex data", 400

    print(f"Received message: {decoded_message}")

    return "OK,4114651"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)





