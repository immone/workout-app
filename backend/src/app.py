import os
import random
import math
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.scheduler import Scheduler
from models.encoder import Encoder

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

scheduler = Scheduler()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# Endpoint to receive schedule
@app.route('/api/schedule', methods=['POST'])
def receive_schedule():
    try:
        schedule_data = request.get_json()

        times = schedule_data.get("times", [])
        days = schedule_data.get("days", [])
        n = schedule_data.get("n", 0)  

        # Validate input data
        if not isinstance(days, list) or not isinstance(times, list):
            return jsonify({"error": "Days and times must be lists."}), 400
        
        if not isinstance(n, int) or n <= 0:
            return jsonify({"error": "Invalid value for n. It must be a positive integer."}), 400

        encoder = Encoder(days, times)

        lits, lits_weighted, hard_clauses, dates = encoder.get_encoded_values()
        print("Encoded Values:", lits)  # Print the encoded values
        print("Hard clauses:", hard_clauses)
        print("Dates", dates)
        
        if not lits:
            return jsonify({"error": "No valid literals generated."}), 400

        if not lits_weighted:
            return jsonify({"error": "lits_weighted not generated."}), 400
        
        lits_weighted = list(lits_weighted.values())

        # Map the first element of each tuple to the next nearest integer and convert it to float
        lits_weighted = [(int(math.ceil(weight)), count) for weight, count in lits_weighted]

        # lits_weighted_mock = [(-q, random.randint(1, 100)) for q in lits] ## For testing
        #print("Mock Weighted Values:", lits_weighted_mock)

        print("Modified Weighted Values:", lits_weighted)

        scheduler.set_lits(lits)
        scheduler.set_penalty(dates)
        scheduler.set_soft(lits_weighted)
        scheduler.set_hard(hard_clauses)

        cost, model = scheduler.solve_schedule(n)
        
        # Print the cost and found model
        print("Cost:", cost)
        print("Model Found:", model)

        positive_intersection = encoder.get_positive_intersection(lits, model)
        print("Positive Intersection:", positive_intersection)  # Print the positive intersection
        
        decoded_vals = encoder.decode_list(positive_intersection)
        modified_decoded_vals = [
        (
            decoded_val[0],
            decoded_val[1],
            f"{decoded_val[2].capitalize() if decoded_val[2].lower() != 'toolo' else 'Töölö'}"
            f"{' (Outdoor gym)' if decoded_val[2] in ['Hietaniemi', 'Paloheinä', 'Pirkkola'] else ' (Unisport)'}"
        )
        for decoded_val in decoded_vals
        ]   

        print("Decoded Values:", modified_decoded_vals)  # Print the decoded values

        # Prepare the response including the decoded values
        response = {
            "message": "Schedule received successfully!",
            "received_times": times,
            "received_days": days,
            "n": n,
            "solution": modified_decoded_vals  # Include the decoded values in the response
        }
        return jsonify(response), 200

    except Exception as e:
        print('Error processing request:', e)
        return jsonify({"error": "Invalid data", "details": str(e)}), 400

if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)
