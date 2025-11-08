from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# External API URL template
EXTERNAL_API_URL = "https://seller-ki-mkc.taitanx.workers.dev/?mobile={mobile_number}"

# Cache to store previous searches (optional)
search_cache = {}

@app.route('/')
def home():
    return jsonify({
        "message": "🚀 Mobile Data Search API - GARAV EDITION 🚀",
        "developer": "@oxmzoo",
        "external_api": "https://seller-ki-mkc.taitanx.workers.dev/",
        "garav": "YEHI TO GARAV KI BAAT HAI!",
        "endpoints": {
            "search_mobile": "/api/search/<mobile_number>",
            "bulk_search": "/api/bulk-search?mobiles=number1,number2,number3",
            "cache_status": "/api/cache",
            "developer_info": "/api/developer",
            "health": "/health"
        },
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Search any mobile number using external API
@app.route('/api/search/<mobile>')
def search_by_mobile(mobile):
    try:
        # Check cache first
        if mobile in search_cache:
            return jsonify({
                "search_query": mobile,
                "source": "cache",
                "data": search_cache[mobile],
                "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
            })
        
        # Call external API
        api_url = EXTERNAL_API_URL.format(mobile_number=mobile)
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Store in cache
            search_cache[mobile] = data
            
            return jsonify({
                "search_query": mobile,
                "source": "external_api",
                "api_used": EXTERNAL_API_URL,
                "data": data,
                "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀",
                "message": "DATA MIL GAYA! GARAV HAI HUMKO! 🚀"
            })
        else:
            return jsonify({
                "error": "External API error",
                "status_code": response.status_code,
                "search_query": mobile
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "External API timeout",
            "search_query": mobile,
            "message": "API response nahi de rahi, thoda time lagega!"
        }), 504
    except Exception as e:
        return jsonify({
            "error": str(e),
            "search_query": mobile,
            "message": "Kuch toh gadbad hai!"
        }), 500

# Bulk search multiple mobile numbers
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
            api_url = EXTERNAL_API_URL.format(mobile_number=mobile)
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                results[mobile] = response.json()
                # Cache the result
                search_cache[mobile] = response.json()
            else:
                results[mobile] = {"error": f"API returned {response.status_code}"}
                
        except Exception as e:
            results[mobile] = {"error": str(e)}
    
    return jsonify({
        "bulk_search_results": results,
        "total_searched": len(mobiles),
        "successful": len([r for r in results.values() if "error" not in r]),
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Get cache status
@app.route('/api/cache')
def cache_status():
    return jsonify({
        "cached_numbers": list(search_cache.keys()),
        "cache_size": len(search_cache),
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Clear cache (optional)
@app.route('/api/clear-cache')
def clear_cache():
    cache_size = len(search_cache)
    search_cache.clear()
    return jsonify({
        "message": "Cache cleared successfully!",
        "cleared_entries": cache_size,
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀"
    })

# Health check
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "mobile-search-api", 
        "external_api": "ACTIVE ✅",
        "cache_system": "WORKING ✅",
        "garav_level": "100% 🚀",
        "message": "SAB KUCCH GARAV SE CHAL RAHA HAI!"
    })

# Developer info
@app.route('/api/developer')
def developer_info():
    return jsonify({
        "developer": "@oxmzoo",
        "credit": "🚀 @oxmzoo - GARAV HAI HUMKO 🚀", 
        "features": [
            "Any Mobile Number Search",
            "External API Integration",
            "Bulk Search Support",
            "Caching System",
            "Fast Response"
        ],
        "special_message": "AB KISI BHI MOBILE KA DATA SEARCH KARO! 🔥"
    })

# Special Garav endpoint
@app.route('/api/garav')
def garav_special():
    return jsonify({
        "message": "🚀 GARAV KI BAAT! 🚀", 
        "description": "EXTERNAL API INTEGRATION BHI @oxmzoo NE HI KIYA!",
        "capabilities": [
            "Koi bhi mobile number search karo",
            "Bulk search support",
            "Smart caching system", 
            "Fast response time"
        ],
        "final_message": "GARAV HAI HUMKO APNI TECH SKILLS PE! 🔥"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
