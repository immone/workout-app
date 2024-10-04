import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from models.scheduler import Scheduler

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

# Sample data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
]

scheduler = Scheduler()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():  
    new_item = request.get_json()
    new_item['id'] = len(items) + 1  # Simple ID apeotssignment
    items.append(new_item)
    return jsonify(new_item), 201

# Temp endpoint for response
@app.route('/api/schedule', methods=['POST'])
def receive_schedule():    
    try:
        schedule_data = request.get_json()
        times = schedule_data.get("times", [])
        days = schedule_data.get("days", [])
        response = {
            "message": "Schedule received successfully!",
            "received_times": schedule_data.get("times", []),
            "received_days": schedule_data.get("days", [])
        }
        return jsonify(response), 200
    except Exception as e:
        print('Error processing request:', e)  
        return jsonify({"error": "Invalid data"}), 400


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port) 
