import math
import os
import httpx

from dotenv import load_dotenv
from typing import Optional

load_dotenv()

API_KEY = os.getenv("YANDEX_API_KEY")
API_URL = lambda city: f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={city}&format=json"

async def get_coordinates(city: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL(city))
            response.raise_for_status()
            data = response.json()

            if data["response"]["GeoObjectCollection"]["featureMember"]:
                coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
                return {"lat": float(coordinates[1]), "lng": float(coordinates[0])}
            
            return None
        except (httpx.HTTPError, KeyError, IndexError):
            return None

def haversine_distance(coords1: dict, coords2: dict) -> float:
    def to_rad(value: float) -> float:
        return value * math.pi / 180
    
    R = 6371
    
    lat_diff = to_rad(coords2["lat"] - coords1["lat"])
    lng_diff = to_rad(coords2["lng"] - coords1["lng"])
    
    a = (math.sin(lat_diff / 2) ** 2 + 
        math.cos(to_rad(coords1["lat"])) * 
        math.cos(to_rad(coords2["lat"])) * 
        (math.sin(lng_diff / 2) ** 2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


async def calculate_distance(city1: str, city2: str):
    if not city1 or not city2:
        return {"error": "Please enter both city names."}
    
    try:
        coords1 = await get_coordinates(city1)
        coords2 = await get_coordinates(city2)
        
        if not coords1:
            return {"error": "Invalid name of the first city"}
        if not coords2:
            return {"error": "Invalid name of the second city"}
        
        distance = haversine_distance(coords1, coords2)
        return {"result": distance}
    except Exception as e:
        return {"error": str(e)}

    