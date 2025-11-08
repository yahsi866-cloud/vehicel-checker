from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Simple API keys list - yahan se hatao to band ho jayega
ACTIVE_KEYS = ["key123", "key456", "test789"]

@app.route('/')
def home():
    return jsonify({
        "message": "Aadhar Search API",
        "usage": "Use ?aadhar=number&api_key=your_key"
    })

@app.route('/api/search')
def search_by_aadhar():
    aadhar = request.args.get('aadhar', '')
    api_key = request.args.get('api_key', '')
    
    # Simple API key check
    if api_key not in ACTIVE_KEYS:
        return jsonify({
            "error": "Invalid API Key",
            "message": "Contact admin for API key"
        }), 401
    
    if not aadhar:
        return jsonify({
            "error": "Aadhar number required",
            "example": "/api/search?aadhar=511238562953&api_key=your_key"
        }), 400
    
    try:
        api_url = f"https://seller-ki-mkc.taitanx.workers.dev/?aadhar={aadhar}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "developer" in data:
                del data["developer"]
            data["credit"] = "@gaurav_cyber"
            return jsonify(data)
        else:
            return jsonify({"error": "API error"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    
