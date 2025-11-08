from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Aadhar Search API",
        "usage": "Use ?aadhar=number to search",
        "example": "/api/search?aadhar=511238562953"
    })

# Search Aadhar number
@app.route('/api/search')
def search_by_aadhar():
    aadhar = request.args.get('aadhar', '')
    
    if not aadhar:
        return jsonify({
            "error": "Aadhar number required",
            "example": "/api/search?aadhar=511238562953"
        }), 400
    
    try:
        # Call external API
        api_url = f"https://seller-ki-mkc.taitanx.workers.dev/?aadhar={aadhar}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Remove developer field from external API response
            if isinstance(data, dict) and "developer" in data:
                del data["developer"]
            
            # Remove credit field if exists
            if isinstance(data, dict) and "credit" in data:
                del data["credit"]
            
            # Add our credit
            if isinstance(data, dict):
                data["credit"] = "@gaurav_cyber"
            
            return jsonify(data)
        else:
            return jsonify({
                "error": "External API error",
                "status_code": response.status_code,
                "credit": "@gaurav_cyber"
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "External API timeout",
            "credit": "@gaurav_cyber"
        }), 504
    except Exception as e:
        return jsonify({
            "error": str(e),
            "credit": "@gaurav_cyber"
        }), 500

# Bulk search multiple Aadhar numbers
@app.route('/api/bulk-search')
def bulk_search():
    aadhars_param = request.args.get('aadhars', '')
    if not aadhars_param:
        return jsonify({
            "error": "Aadhar numbers required",
            "example": "/api/bulk-search?aadhars=511238562953,511238562954,511238562955",
            "credit": "@gaurav_cyber"
        }), 400
    
    aadhars = [a.strip() for a in aadhars_param.split(',')]
    results = {}
    
    for aadhar in aadhars:
        try:
            api_url = f"https://seller-ki-mkc.taitanx.workers.dev/?aadhar={aadhar}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Remove developer field
                if isinstance(data, dict) and "developer" in data:
                    del data["developer"]
                if isinstance(data, dict) and "credit" in data:
                    del data["credit"]
                results[aadhar] = data
            else:
                results[aadhar] = {"error": f"API returned {response.status_code}"}
                
        except Exception as e:
            results[aadhar] = {"error": str(e)}
    
    # Add credit to final response
    results["credit"] = "@gaurav_cyber"
    return jsonify(results)

# Health check
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "aadhar-search-api"
    })

# Get API info
@app.route('/api/info')
def api_info():
    return jsonify({
        "api_name": "Aadhar Search API",
        "external_api": "https://seller-ki-mkc.taitanx.workers.dev/",
        "endpoints": {
            "single_search": "/api/search?aadhar=511238562953",
            "bulk_search": "/api/bulk-search?aadhars=number1,number2,number3",
            "health": "/health",
            "info": "/api/info"
        },
        "credit": "@gaurav_cyber"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
