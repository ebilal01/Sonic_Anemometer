from flask import Flask, request, jsonify, render_template
import random
import time
import json
import os

app = Flask(__name__)

# Define the path to store flight data
FLIGHT_DATA_FILE = 'flight_data.json'

# Load the flight data from the file if it exists
def load_flight_data():
    if os.path.exists(FLIGHT_DATA_FILE):
        with open(FLIGHT_DATA_FILE, 'r') as file:
            return json.load(file)
    return {
        'latitude': None,
        'longitude': None,
        'timestamps': [],
        'altitudes': []
    }

# Save flight data to the file
def save_flight_data(data):
    with open(FLIGHT_DATA_FILE, 'w') as file:
        json.dump(data, file)

# Load the current flight data
flight_data = load_flight_data()

@app.route('/')
def index():
    return render_template('index4.html')

@app.route('/live-data', methods=['GET'])
def live_data():
    # Return the most recent RockBLOCK data (if available)
    if flight_data['latitude'] is not None and flight_data['longitude'] is not None:
        return jsonify(flight_data)
    else:
        return jsonify({"error": "No live data available"}), 404

@app.route('/rockblock/MT', methods=['POST'])
def receive_mt():
    imei = request.args.get('imei')
    username = request.args.get('username')
    password = request.args.get('password')
    data = request.args.get('data')

    # Replace these with your actual RockBLOCK credentials
    VALID_IMEI = "your_imei_here"
    VALID_USERNAME = "your_username_here"
    VALID_PASSWORD = "your_password_here"

    # Validate input
    if imei != VALID_IMEI or username != VALID_USERNAME or password != VALID_PASSWORD:
        return "FAILED,10,Invalid login credentials", 400

    if not data:
        return "FAILED,16,No data", 400

    # Simulate decoding hex data
    try:
        decoded_message = bytes.fromhex(data).decode('utf-8')
        print(f"Decoded message: {decoded_message}")
    except ValueError:
        return "FAILED,14,Could not decode hex data", 400

    # Example: Parsing the decoded message for latitude, longitude, altitude
    try:
        lat, lon, alt = map(float, decoded_message.split(','))
    except ValueError:
        return "FAILED,14,Could not parse the data correctly", 400

    # Update the flight data with the received values
    flight_data['latitude'] = lat
    flight_data['longitude'] = lon
    flight_data['altitudes'].append(alt)
    flight_data['timestamps'].append(time.time())

    # Save the updated flight data to the file
    save_flight_data(flight_data)

    print(f"Received data - Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")

    return "OK,4114651"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)






