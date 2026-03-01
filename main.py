from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WineInput(BaseModel):
    og: float
    fg: float
    volume: float
    yeast: str

@app.post("/wine/analyze")
def analyze_wine(data: WineInput):
    abv = (data.og - data.fg) / 7.5

    # Enkel logik
    if data.fg > 30:
        status = "active"
        risk = "low"
        recommendation = "Fermentation is still active. Let it continue."
    elif 5 < data.fg <= 30:
        status = "finishing"
        risk = "medium"
        recommendation = "Fermentation nearing completion. Monitor closely."
    else:
        status = "complete"
        risk = "low"
        recommendation = "Fermentation likely complete."

    return {
        "abv": round(abv, 2),
        "status": status,
        "risk_level": risk,
        "recommendation": recommendation
    }