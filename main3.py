import datetime
import random
import time
import threading
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from collections import deque
import binascii

app = Flask(__name__)
CORS(app)

data_history = deque(maxlen=1000)

# Simulated satellite data
current_position = {
    "imei": "300434065264590",  # RockBLOCK IMEI
    "username": "myUser",  # Your RockBLOCK username
    "password": "myPass",  # Your RockBLOCK password
    "latitude": 0.0,
    "longitude": 0.0,
    "altitude": 500,  
    "temperature": 25.0  
}

# Function to simulate realistic data generation
def generate_realistic_data():
    global current_position
    current_position["latitude"] += random.uniform(-0.05, 0.05)
    current_position["longitude"] += random.uniform(-0.05, 0.05)
    current_position["altitude"] += random.uniform(-10, 30)
    current_position["altitude"] = max(0, min(current_position["altitude"], 35000))
    current_position["temperature"] += random.uniform(-0.2, 0.2)

    # Convert simulated data to hex format for "data" field, simulating RockBLOCK message
    message = f"{current_position['latitude']},{current_position['longitude']},{current_position['altitude']},{current_position['temperature']}"
    hex_data = binascii.hexlify(message.encode()).decode()  # Convert message to hex

    # Print to see the generated hex data
    print(f"Generated data (hex): {hex_data}")

    # Save the data to history
    data_history.append({
        "imei": current_position["imei"],
        "username": current_position["username"],
        "password": current_position["password"],
        "data": hex_data
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
    return jsonify(data_history[-1])

@app.route('/history', methods=['GET'])
def history():
    """Return all historical data."""
    if not data_history:
        return jsonify({"message": "No data available"}), 404
    return jsonify(list(data_history))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Simulate receiving RockBLOCK MT data."""
    try:
        # Simulate receiving data from the RockBLOCK
        generate_realistic_data()  # Use same logic to generate data
        print("Received simulated RockBLOCK data")

        return jsonify({"message": "Simulated RockBLOCK data received"}), 200
    except Exception as e:
        return jsonify({"message": "Error processing data", "error": str(e)}), 500

if __name__ == "__main__":
    threading.Thread(target=continuous_data_simulation, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)




