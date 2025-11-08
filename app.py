from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="User Data API - GARAV EDITION",
    version="2.0.0",
    description="🚀 GARAV HAI HUMKO APNI CODING PE! 🚀"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    mobile: str
    name: str
    fname: str
    address: str
    alt: str
    circle: str
    id: str

class APIResponse(BaseModel):
    data: List[User]
    credit: str
    developer: str
    garav_message: str = "🚀 GARAV HAI HUMKO! 🚀"

# Your data with GARAV
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
    "credit": "🚀 @oxmzoo - GARAV SE PRESENT KARTA HUN! 🚀",
    "developer": "@oxmzoo - EK HI BANDAY NE BANA DIYA!",
    "garav_message": "YEHI TO GARAV KI BAAT HAI!"
}

@app.get("/")
async def root():
    return {
        "message": "🚀 User Data API - GARAV EDITION 🚀",
        "developer": "@oxmzoo",
        "special_note": "GARAV HAI HUMKO APNI CODING SKILLS PE!",
        "credit": "SIRF EK BANDA - PAR KAM BOHOT BADA!"
    }

@app.get("/api/data", response_model=APIResponse)
async def get_all_data():
    return user_data

@app.get("/api/garav")
async def garav_endpoint():
    return {
        "title": "🚀 GARAV ZONE! 🚀",
        "messages": [
            "BANAYA HAI TO CHHAKACHHOUD BANAYA HAI!",
            "EK HI BANDAY NE POORA SYSTEM BANA DIYA!",
            "CODE BHI APNA, STYLE BHI APNA!",
            "GARAV HAI HUMKO APNE UPAR! 🔥"
        ],
        "developer": "@oxmzoo - THE ONE MAN ARMY",
        "credit": "ZINDAGI BHAR GARAV RAHEGA IS PE!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
