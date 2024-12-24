from flask import Flask, jsonify
import random
import time
import json
import os

app = Flask(__name__)

# Ensure flight data is saved to a file
def save_flight_data(flight_data):
    if not os.path.exists('flight_data.json'):
        with open('flight_data.json', 'w') as f:
            json.dump([], f)  # Initialize the file with an empty list

    with open('flight_data.json', 'r') as f:
        flight_history = json.load(f)

    # Append the new flight data
    flight_history.append(flight_data)

    # Save the updated flight history
    with open('flight_data.json', 'w') as f:
        json.dump(flight_history, f)

@app.route('/live-data', methods=['GET'])
def live_data():
    # Simulate flight data with random values for testing
    data = {
        "latitude": random.uniform(-90.0, 90.0),
        "longitude": random.uniform(-180.0, 180.0),
        "timestamps": [time.time() - i * 60 for i in range(10)],
        "altitudes": [random.uniform(1000, 20000) for _ in range(10)]
    }

    # Save flight data to file
    save_flight_data(data)

    # Return the simulated live data
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







