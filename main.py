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

Return ONLY valid JSON.
No markdown.
No explanation outside JSON.

Format exactly like this:

{{
  "status": "active | finishing | complete | stuck",
  "risk_level": "low | medium | high",
  "reasoning": "short technical explanation",
  "recommendation": "clear action advice"
}}

All gravity values are in degrees Oechsle (°Oe).
Do NOT convert units.

OG: {data.og}
FG: {data.fg}
Volume: {data.volume}
Yeast: {data.yeast}
Estimated ABV: {abv:.2f}
"""

    ai_result = analyze_fermentation(prompt)

    if not ai_result:
        return {
            "abv": round(abv, 2),
            "ai_analysis": "AI service unavailable"
        }

cleaned = ai_result.replace("```json", "").replace("```", "").strip()

try:
    parsed = json.loads(cleaned)
except Exception as e:
    print("JSON parse error:", e)
    return {
        "abv": round(abv, 2),
        "status": "error",
        "risk_level": "unknown",
        "reasoning": "AI returned invalid JSON",
        "recommendation": "Check backend logs"
    }

return {
    "abv": round(abv, 2),
    **parsed
}