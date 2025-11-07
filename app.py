from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/check-vehicle', methods=['POST'])
def check_vehicle():
    try:
        data = request.get_json()
        
        if not data or 'vehicle_no' not in data:
            return jsonify({
                'status': False,
                'message': 'vehicle_no parameter is required'
            }), 400
        
        vehicle_no = data['vehicle_no'].strip().upper()
        
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

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Vehicle API is running',
        'endpoint': 'POST /api/check-vehicle'
    })

# Root endpoint - API info
@app.route('/', methods=['GET'])
def api_info():
    return jsonify({
        'message': 'Vehicle Challan Check API',
        'usage': 'POST /api/check-vehicle with {"vehicle_no": "VEHICLE_NUMBER"}',
        'example': 'curl -X POST https://vehicel-checker.onrender.com/api/check-vehicle -H "Content-Type: application/json" -d \'{"vehicle_no": "UP61S6030"}\''
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
