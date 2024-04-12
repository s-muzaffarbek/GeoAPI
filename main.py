from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()

app.openapi_tags = [
    {"name": "Search", "description": "Local bizneslarni qidirish bo'yicha yo'nalishlar"},
    {"name": "ChatGPT4", "description": "ChatGPT4"},
    {"name": "Video", "description": "Video Yuklovchi API"}
]

RAPIDAPI_HOST = "local-business-data.p.rapidapi.com"
RAPIDAPI_HOST1 = "https://chatgpt-42.p.rapidapi.com/conversationgpt4"
RAPIDAPI_HOST2 = "auto-download-all-in-one.p.rapidapi.com"

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

@app.get("/chat", response_class=JSONResponse, tags=["ChatGPT4"])
async def search_hotels(query: str, key: str):
    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0301",
        # model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": query
            },
        ],
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content


class VideoUrl(BaseModel):
    url: str

@app.post("/video_url")
async def get_video_info(video_url: VideoUrl, rapidapi_key: str):
    url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "auto-download-all-in-one.p.rapidapi.com"
    }
    payload = { "url": video_url.url }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))