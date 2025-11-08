from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your data with GARAV credit
user_data = {
    "data": [
        {
            "mobile": "7278210621",
            "name": "Vikash Kumar",
            "fname": "Nawal Kishor Prasad Sinha",
            "address": "! !173/D PURBASHREE PALLY PICNIC GARDEN NASKAR HUT West Bengal! !South 24 Parganas! !700039",
            "alt": "7003445877",
            "circle": "AIRTEL KOL",
            "id": "472750027374"
        },
        {
            "mobile": "7003445877", 
            "name": "Rajesh Sharma",
            "fname": "Suresh Sharma",
            "address": "! !45 PARK STREET KOLKATA West Bengal! !Kolkata! !700016",
            "alt": "9876543210",
            "circle": "JIO KOL",
            "id": "472750027375"
        },
        {
            "mobile": "9876543210",
            "name": "Priya Singh",
            "fname": "Amit Singh", 
            "address": "! !78 SALT LAKE CITY West Bengal! !Kolkata! !700091",
            "alt": "7278210621",
            "circle": "AIRTEL KOL",
            "id": "472750027376"
        }
    ],
    "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀",
    "developer": "@oxmzoo - APNA BANDAY KA BANAYA HUA"
}

@app.route('/')
def home():
    return jsonify({
        "message": "API is running!",
        "garav": "YEHI TO GARAV KI BAAT HAI!",
        "endpoints": {
            "all_data": "/api/data",
            "mobile_data": "/api/mobile", 
            "search_mobile": "/api/search/<mobile_number>",
            "search_by_alt": "/api/search/alt/<alt_number>",
            "user_by_id": "/api/user/<id>",
            "developer": "/api/developer",
            "garav": "/api/garav",
            "health": "/health"
        },
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Get all data
@app.route('/api/data')
def get_all_data():
    return jsonify(user_data)

# Get mobile numbers only
@app.route('/api/mobile')
def get_mobile_data():
    mobiles = [user["mobile"] for user in user_data["data"]]
    return jsonify({
        "mobiles": mobiles,
        "count": len(mobiles),
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀",
        "message": "APNA DATA, APNA GARAV!"
    })

# Search by mobile number (MAIN FEATURE)
@app.route('/api/search/<mobile>')
def search_by_mobile(mobile):
    results = []
    
    # Search in mobile field
    mobile_results = [user for user in user_data["data"] if user["mobile"] == mobile]
    
    # Search in alt mobile field
    alt_results = [user for user in user_data["data"] if user["alt"] == mobile]
    
    # Combine both results
    results = mobile_results + alt_results
    
    # Remove duplicates
    unique_results = []
    seen_ids = set()
    for user in results:
        if user["id"] not in seen_ids:
            unique_results.append(user)
            seen_ids.add(user["id"])
    
    return jsonify({
        "search_query": mobile,
        "results": unique_results,
        "total_found": len(unique_results),
        "search_type": "mobile_number",
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀",
        "message": "DHOONDNE WALA KOI NAHI, SERVE KARNE WALA EK HUM HI HAI!"
    })

# Search by alternate mobile number
@app.route('/api/search/alt/<alt_number>')
def search_by_alt(alt_number):
    results = [user for user in user_data["data"] if user["alt"] == alt_number]
    
    return jsonify({
        "search_query": alt_number,
        "search_type": "alternate_mobile",
        "results": results,
        "total_found": len(results),
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Get all available mobile numbers for reference
@app.route('/api/all-numbers')
def get_all_numbers():
    all_mobiles = []
    for user in user_data["data"]:
        all_mobiles.append({
            "primary": user["mobile"],
            "alternate": user["alt"],
            "name": user["name"]
        })
    
    return jsonify({
        "available_numbers": all_mobiles,
        "total_numbers": len(all_mobiles),
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Get user by ID
@app.route('/api/user/<user_id>')
def get_user_by_id(user_id):
    for user in user_data["data"]:
        if user["id"] == user_id:
            return jsonify({
                **user,
                "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
            })
    return jsonify({"error": "User not found"}), 404

# Health check with garav
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "user-data-api",
        "garav_level": "100%",
        "message": "GARAV SE CHAL RAHA HAI!",
        "search_feature": "ACTIVE ✅"
    })

# Get developer info with full garav
@app.route('/api/developer')
def developer_info():
    return jsonify({
        "developer": user_data["developer"],
        "credit": user_data["credit"],
        "total_users": len(user_data["data"]),
        "search_features": [
            "Mobile Number Search",
            "Alternate Number Search", 
            "Duplicate Removal",
            "Fast Response"
        ],
        "special_message": "🚀 GARAV HAI HUMKO APNI CODING PE! 🚀"
    })

# Special Garav endpoint
@app.route('/api/garav')
def garav_special():
    return jsonify({
        "message": "🚀 GARAV KI BAAT! 🚀",
        "description": "MOBILE SEARCH FEATURE BHI @oxmzoo NE HI BANAYA!",
        "credit": "SIRF EK BANDA - PAR KAM BOHOT BADA!",
        "search_capabilities": [
            "Primary mobile search",
            "Alternate mobile search", 
            "Duplicate handling",
            "Fast JSON response"
        ],
        "final_message": "GARAV HAI HUMKO APNE UPAR! 🔥"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
