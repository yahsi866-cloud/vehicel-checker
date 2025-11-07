from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Browser se direct access ke liye

# Main API endpoint - GET aur POST dono allow karega
@app.route('/api/check-vehicle', methods=['GET', 'POST', 'OPTIONS'])
def check_vehicle():
    try:
        # GET request handle karein (browser ke liye)
        if request.method == 'GET':
            vehicle_no = request.args.get('vehicle_no')
            if not vehicle_no:
                return jsonify({
                    'status': False,
                    'message': 'vehicle_no parameter missing. Use: /api/check-vehicle?vehicle_no=UP61S6030'
                }), 400
        else:
            # POST request handle karein
            data = request.get_json() or {}
            vehicle_no = data.get('vehicle_no', '')
        
        vehicle_no = vehicle_no.strip().upper()
        
        if not vehicle_no:
            return jsonify({
                'status': False,
                'message': 'Vehicle number is required'
            }), 400

        # GTPlay API call
        url = "https://gtplay.in/API/vehicle_challan_info/testapi.php"
        form_data = f'vehicle_no={vehicle_no}'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'okhttp/5.1.0',
            'Accept-Encoding': 'gzip',
            'Content-Length': str(len(form_data)),
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        
        response = requests.post(url, data=form_data, headers=headers, timeout=10)
        api_result = response.json()
        
        return jsonify(api_result)
        
    except requests.exceptions.Timeout:
        return jsonify({
            'status': False,
            'message': 'API request timeout'
        }), 408
    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': False,
            'message': f'Network error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'status': False,
            'message': f'Server error: {str(e)}'
        }), 500

# Simple test endpoint - browser mein directly check karne ke liye
@app.route('/test', methods=['GET'])
def test_vehicle():
    """Browser mein directly test karne ke liye"""
    vehicle_no = request.args.get('vehicle_no', 'UP61S6030')
    
    try:
        url = "https://gtplay.in/API/vehicle_challan_info/testapi.php"
        form_data = f'vehicle_no={vehicle_no}'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'okhttp/5.1.0',
            'Accept-Encoding': 'gzip',
            'Content-Length': str(len(form_data)),
            'Accept': 'application/json',
        }
        
        response = requests.post(url, data=form_data, headers=headers, timeout=10)
        api_result = response.json()
        
        return jsonify(api_result)
        
    except Exception as e:
        return jsonify({
            'status': False,
            'message': f'Error: {str(e)}'
        }), 500

# API information
@app.route('/', methods=['GET'])
def api_info():
    return jsonify({
        'api_name': 'Vehicle Challan Check API',
        'endpoints': {
            'GET_test': '/test?vehicle_no=UP61S6030',
            'GET_api': '/api/check-vehicle?vehicle_no=UP61S6030',
            'POST_api': 'POST /api/check-vehicle with JSON body'
        },
        'example_urls': [
            'https://vehicel-checker.onrender.com/test?vehicle_no=UP61S6030',
            'https://vehicel-checker.onrender.com/api/check-vehicle?vehicle_no=UP61S6030'
        ]
    })

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'vehicle-api'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
