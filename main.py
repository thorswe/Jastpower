import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

class WineInput(BaseModel):
    og: float
    fg: float
    volume: float
    yeast: str

@app.post("/wine/analyze")
def analyze_wine(data: WineInput):
    abv = (data.og - data.fg) / 7.5

    prompt = f"""
    Analyze this wine fermentation:
    OG: {data.og}
    FG: {data.fg}
    Volume: {data.volume} L
    Yeast: {data.yeast}
    Estimated ABV: {abv:.2f}%

    Provide:
    - status
    - risk level
    - recommendation
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=200
    )

    return {
        "abv": round(abv, 2),
        "ai_analysis": response.output_text
    }