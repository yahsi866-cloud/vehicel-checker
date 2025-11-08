from flask import Flask, jsonify
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
            "mobile": "7278210621", 
            "name": "Vikash Kumar",
            "fname": "Nawal Kishor Prasad Sinha",
            "address": "! !173/D PURBASHREE PALLY PICNIC GARDEN NASKAR HUT West Bengal! !South 24 Parganas! !700039",
            "alt": "7003445877",
            "circle": "AIRTEL KOL",
            "id": "472750027374"
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
            "user_by_id": "/api/user/<id>",
            "search": "/api/search/<mobile>",
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

# Search by mobile number
@app.route('/api/search/<mobile>')
def search_by_mobile(mobile):
    results = [user for user in user_data["data"] if user["mobile"] == mobile]
    return jsonify({
        "results": results,
        "count": len(results),
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀",
        "message": "DHOONDNE WALA KOI NAHI, SERVE KARNE WALA EK HUM HI HAI!"
    })

# Health check with garav
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "user-data-api",
        "garav_level": "100%",
        "message": "GARAV SE CHAL RAHA HAI!"
    })

# Get developer info with full garav
@app.route('/api/developer')
def developer_info():
    return jsonify({
        "developer": user_data["developer"],
        "credit": user_data["credit"],
        "total_users": len(user_data["data"]),
        "special_message": "🚀 GARAV HAI HUMKO APNI CODING PE! 🚀",
        "skills": ["Python", "Flask", "API Development", "GARAV Level: Expert"]
    })

# Special Garav endpoint
@app.route('/api/garav')
def garav_special():
    return jsonify({
        "message": "🚀 GARAV KI BAAT! 🚀",
        "description": "YEH API BANAYI HAI @oxmzoo NE - EK HI BANDAY NE BANA DIYA!",
        "credit": "SIRF EK BANDA - PAR KAM BOHOT BADA!",
        "garav_points": [
            "100% Self Made",
            "Zero External Help", 
            "Pure Desi Coding",
            "Apna Style, Apna Swag"
        ],
        "final_message": "GARAV HAI HUMKO APNE UPAR! 🔥"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
