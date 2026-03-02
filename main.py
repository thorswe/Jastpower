import os

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from ai_service import analyze_fermentation

app = FastAPI()

class WineInput(BaseModel):
    og: float
    fg: float
    volume: float
    yeast: str

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/wine/analyze")
def analyze_wine(data: WineInput):
    abv = (data.og - data.fg) / 7.5

    prompt = f"""
    You are a fermentation analysis engine.
    All gravity values are in degrees Oechsle (°Oe).
    Do NOT convert units.

    Return ONLY valid JSON with:
    status, risk_level, reasoning, recommendation.

    OG: {data.og}
    FG: {data.fg}
    Volume: {data.volume}
    Yeast: {data.yeast}
    Estimated ABV: {abv:.2f}
    """

    ai_result = analyze_fermentation(prompt)

    # Fallback om AI misslyckas
    if not ai_result:
        return {
            "abv": round(abv, 2),
            "status": "unknown",
            "risk_level": "unknown",
            "recommendation": "AI service unavailable"
        }

    return {
        "abv": round(abv, 2),
        "ai_analysis": ai_result
    }
