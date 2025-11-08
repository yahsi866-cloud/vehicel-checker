from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Mobile Search API",
        "developer": "@gaurav_cyber",
        "usage": "Use ?mobile=number to search"
    })

# Search mobile number
@app.route('/api/search')
def search_by_mobile():
    mobile = request.args.get('mobile', '')
    
    if not mobile:
        return jsonify({
            "error": "Mobile number required",
            "example": "/api/search?mobile=7003445877"
        }), 400
    
    try:
        # Call external API
        api_url = f"https://seller-ki-mkc.taitanx.workers.dev/?mobile={mobile}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Add credit
            if isinstance(data, dict):
                data["credit"] = "@gaurav_cyber"
            return jsonify(data)
        else:
            return jsonify({
                "error": "External API error",
                "status_code": response.status_code
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "External API timeout"
        }), 504
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Bulk search multiple numbers
@app.route('/api/bulk-search')
def bulk_search():
    mobiles_param = request.args.get('mobiles', '')
    if not mobiles_param:
        return jsonify({
            "error": "Mobile numbers required",
            "example": "/api/bulk-search?mobiles=7003445877,9876543210,7278210621"
        }), 400
    
    mobiles = [m.strip() for m in mobiles_param.split(',')]
    results = {}
    
    for mobile in mobiles:
        try:
            api_url = f"https://seller-ki-mkc.taitanx.workers.dev/?mobile={mobile}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                results[mobile] = response.json()
            else:
                results[mobile] = {"error": f"API returned {response.status_code}"}
                
        except Exception as e:
            results[mobile] = {"error": str(e)}
    
    # Add credit to final response
    results["credit"] = "@gaurav_cyber"
    return jsonify(results)

# Health check
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "mobile-search-api"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
