# Copyright (c) [2024] [The Red Building Group LLC]
# This source code is licensed under the MIT License found in the
# LICENSE file in the root directory of this source tree.
#

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

VAPI_API_KEY = os.environ.get("VAPI_API_KEY")
VAPI_BASE_URL = os.environ.get("VAPI_BASE_URL")

@app.route('/create-assistant', methods=['POST'])
def create_assistant():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        assistant_data = request.json
        if not assistant_data:
            return jsonify({"error": "No data provided"}), 400
            
        print("Received assistant data:", assistant_data)  # Debug log
        
        headers = {
            'Authorization': f'Bearer {VAPI_API_KEY}',
            'Content-Type': 'application/json',
        }
        
        # Make sure VAPI_BASE_URL is set and has a trailing slash
        api_url = f"{VAPI_BASE_URL.rstrip('/')}/assistant"
        print(f"Making request to: {api_url}")  # Debug log
        
        response = requests.post(api_url, json=assistant_data, headers=headers)
        
        print(f"VAPI Response Status: {response.status_code}")  # Debug log
        print(f"VAPI Response: {response.text}")  # Debug log
        
        if response.status_code == 201:
            return jsonify(response.json()), 201
        else:
            return jsonify({
                "error": "Failed to create/update assistant",
                "vapi_status": response.status_code,
                "vapi_response": response.text
            }), response.status_code
            
    except Exception as e:
        print(f"Error in create_assistant: {str(e)}")  # Debug log
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
