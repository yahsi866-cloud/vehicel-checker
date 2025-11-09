from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Simple API keys - yahan se manage karo
ACTIVE_KEYS = ["rc123", "rc456", "test789", "19f740eba84398bb"]

@app.route('/')
def home():
    return jsonify({
        "message": "RC Search API",
        "usage": "Use ?rc=number&api_key=your_key to search",
        "example": "/api/search?rc=UP61S6030&api_key=19f740eba84398bb"
    })

# Generate new API key (simple)
@app.route('/get-key')
def get_key():
    import secrets
    new_key = secrets.token_hex(8)
    ACTIVE_KEYS.append(new_key)
    return jsonify({
        "api_key": new_key,
        "message": "Save this key! Use in all requests.",
        "usage": "Add ?api_key=YOUR_KEY to requests"
    })

# RC Search API
@app.route('/api/search')
def search_by_rc():
    rc = request.args.get('rc', '')
    api_key = request.args.get('api_key', '')
    
    # API key check
    if api_key not in ACTIVE_KEYS:
        return jsonify({
            "error": "Invalid API Key",
            "message": "Use /get-key to get API key or contact admin",
            "your_key": api_key,
            "valid_keys": ACTIVE_KEYS
        }), 401
    
    if not rc:
        return jsonify({
            "error": "RC number required",
            "example": "/api/search?rc=UP61S6030&api_key=your_key"
        }), 400
    
    try:
        # Call external RC API
        api_url = f"https://vehicle-inf.gauravyt566.workers.dev/?rc={rc}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Clean response
            if isinstance(data, dict):
                if "developer" in data:
                    del data["developer"]
                if "credit" in data:
                    del data["credit"]
                
                # Add our credit
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

# Bulk search multiple RC numbers
@app.route('/api/bulk-search')
def bulk_search():
    api_key = request.args.get('api_key', '')
    rcs_param = request.args.get('rcs', '')
    
    # API key check
    if api_key not in ACTIVE_KEYS:
        return jsonify({
            "error": "Invalid API Key",
            "message": "Use /get-key to get API key",
            "your_key": api_key
        }), 401
    
    if not rcs_param:
        return jsonify({
            "error": "RC numbers required",
            "example": "/api/bulk-search?rcs=UP61S6030,DL4CAM8855&api_key=your_key",
            "credit": "@gaurav_cyber"
        }), 400
    
    rcs = [r.strip() for r in rcs_param.split(',')]
    results = {}
    
    for rc in rcs:
        try:
            api_url = f"https://vehicle-inf.gauravyt566.workers.dev/?rc={rc}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Clean data
                if isinstance(data, dict):
                    if "developer" in data:
                        del data["developer"]
                    if "credit" in data:
                        del data["credit"]
                results[rc] = data
            else:
                results[rc] = {"error": f"API returned {response.status_code}"}
                
        except Exception as e:
            results[rc] = {"error": str(e)}
    
    # Add credit to final response
    results["credit"] = "@gaurav_cyber"
    return jsonify(results)

# View active keys (admin only - simple)
@app.route('/admin/keys')
def view_keys():
    # Simple password protection
    password = request.args.get('password', '')
    if password != "admin123":
        return jsonify({"error": "Unauthorized"}), 401
    
    return jsonify({
        "active_keys": ACTIVE_KEYS,
        "total_keys": len(ACTIVE_KEYS),
        "message": "Remove key from ACTIVE_KEYS list to deactivate"
    })

# Health check
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "rc-search-api",
        "total_active_keys": len(ACTIVE_KEYS)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
