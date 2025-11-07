from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Browser se direct access ke liye

@app.route('/api/check-vehicle', methods=['POST', 'GET', 'OPTIONS'])
def check_vehicle():
    try:
        # GET request handle karein browser ke liye
        if request.method == 'GET':
            vehicle_no = request.args.get('vehicle_no')
            if not vehicle_no:
                return jsonify({
                    'status': False,
                    'message': 'Use: /api/check-vehicle?vehicle_no=UP61S6030'
                })
        else:
            # POST request handle karein
            data = request.get_json() or {}
            vehicle_no = data.get('vehicle_no', request.form.get('vehicle_no'))
        
        if not vehicle_no:
            return jsonify({
                'status': False,
                'message': 'vehicle_no parameter is required'
            }), 400
        
        vehicle_no = vehicle_no.strip().upper()
        
        if not vehicle_no:
            return jsonify({
                'status': False,
                'message': 'Vehicle number cannot be empty'
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
        
    except Exception as e:
        return jsonify({
            'status': False,
            'message': f'Error: {str(e)}'
        }), 500

# Root endpoint - Simple API info
@app.route('/', methods=['GET'])
def api_info():
    return jsonify({
        'api_name': 'Vehicle Challan Check API',
        'endpoint': '/api/check-vehicle',
        'methods': ['GET', 'POST'],
        'usage_get': 'https://vehicel-checker.onrender.com/api/check-vehicle?vehicle_no=UP61S6030',
        'usage_post': 'POST with JSON: {"vehicle_no": "UP61S6030"}',
        'example_curl': 'curl "https://vehicel-checker.onrender.com/api/check-vehicle?vehicle_no=UP61S6030"'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
