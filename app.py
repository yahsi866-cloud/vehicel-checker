from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# HTML directly Python mein
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🚗 Vehicle Checker</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .container { background: #f9f9f9; padding: 20px; border-radius: 10px; }
        input, button { padding: 10px; margin: 10px 0; width: 100%; font-size: 16px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; display: none; }
        .success { background: #d4edda; }
        .error { background: #f8d7da; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 Vehicle Checker</h1>
        <input type="text" id="vehicleInput" placeholder="e.g., UP61S6030">
        <button onclick="checkVehicle()">Check Vehicle</button>
        <div id="result" class="result"></div>
    </div>

    <script>
        async function checkVehicle() {
            const vehicleNo = document.getElementById('vehicleInput').value;
            const resultDiv = document.getElementById('result');
            
            if (!vehicleNo) {
                alert('Please enter vehicle number');
                return;
            }
            
            try {
                const response = await fetch('/api/check-vehicle', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ vehicle_no: vehicleNo })
                });
                
                const data = await response.json();
                
                resultDiv.style.display = 'block';
                
                if (data.status === true) {
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = `
                        <h3>✅ Vehicle Found!</h3>
                        <p><strong>🚗 Vehicle:</strong> ${data.data.maker_model}</p>
                        <p><strong>📝 Number:</strong> ${data.data.registration_no}</p>
                        <p><strong>👤 Owner:</strong> ${data.data.owner_name}</p>
                        <p><strong>⛽ Fuel:</strong> ${data.data.fuel_type}</p>
                    `;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `<strong>❌ Error:</strong> ${data.message}`;
                }
                
            } catch (error) {
                resultDiv.style.display = 'block';
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `<strong>🔴 Network Error:</strong> ${error.message}`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/api/check-vehicle', methods=['POST'])
def check_vehicle():
    try:
        data = request.json
        vehicle_no = data.get('vehicle_no', '').strip().upper()
        
        if not vehicle_no:
            return jsonify({'status': False, 'message': 'Vehicle number required'})
        
        # API call
        url = "https://gtplay.in/API/vehicle_challan_info/testapi.php"
        form_data = f'vehicle_no={vehicle_no}'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'okhttp/5.1.0',
            'Accept-Encoding': 'gzip',
            'Content-Length': str(len(form_data)),
            'Accept': 'application/json'
        }
        
        response = requests.post(url, data=form_data, headers=headers, timeout=10)
        return jsonify(response.json())
        
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
