from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

app.openapi_tags = [
    {"name": "Search", "description": "Local bizneslarni qidirish bo'yicha yo'nalishlar"}
]

RAPIDAPI_HOST = "local-business-data.p.rapidapi.com"

@app.get("/search", response_class=JSONResponse, tags=["Search"])
async def search_hotels(query: str, rapidapi_key: str, limit: int = 20, lat: float = 37.359428, lng: float = -121.925337, zoom: int = 13, language: str = "en", region: str = "us"):
    url = f"https://{RAPIDAPI_HOST}/search-nearby"
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    querystring = {
        "query": query,
        "limit": limit,
        "lat": lat,
        "lng": lng,
        "zoom": zoom,
        "language": language,
        "region": region
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
