import datetime
import random
import time
import threading
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from collections import deque

app = Flask(__name__)
CORS(app)

data_history = deque(maxlen=1000)

current_position = {
    "latitude": 0.0,
    "longitude": 0.0,
    "altitude": 500,
    "temperature": 25.0
}

def generate_realistic_data():
    """Generate realistic satellite movement and update history."""
    global current_position
    current_position["latitude"] += random.uniform(-0.05, 0.05)
    current_position["longitude"] += random.uniform(-0.05, 0.05)
    current_position["altitude"] += random.uniform(-10, 30)
    current_position["altitude"] = max(0, min(current_position["altitude"], 35000))
    current_position["temperature"] += random.uniform(-0.2, 0.2)

    # Debug print to see if data is generated
    print(f"Generated data: {current_position}")

    data_history.append({
        "time": datetime.datetime.utcnow().isoformat(),
        "latitude": current_position["latitude"],
        "longitude": current_position["longitude"],
        "altitude": current_position["altitude"],
        "temperature": current_position["temperature"]
    })

def continuous_data_simulation():
    """Continuously generate data for the satellite."""
    while True:
        generate_realistic_data()
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index4.html')

@app.route('/live-data', methods=['GET'])
def live_data():
    """Return the most recent satellite data."""
    if not data_history:
        return jsonify({"message": "No data available"}), 404
    # Debug print to see if live-data is called
    print(f"Returning live data: {data_history[-1]}")
    return jsonify(data_history[-1])

@app.route('/history', methods=['GET'])
def history():
    """Return all historical data."""
    # Debug print to see if history is called
    print(f"Returning history data: {list(data_history)}")
    return jsonify(list(data_history))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive simulated RockBLOCK HTML response."""
    try:
        # Simulate receiving RockBLOCK POST data
        generate_realistic_data()  # Using the same data generation logic
        print("Received webhook data and generated new data")

        return jsonify({"message": "Simulated RockBLOCK data received"}), 200
    except Exception as e:
        return jsonify({"message": "Error processing data", "error": str(e)}), 500


if __name__ == "__main__":
    threading.Thread(target=continuous_data_simulation, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)



