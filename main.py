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

    return {
        "abv": round(abv, 2),
        "message": "Jästpower MVP kör!"
    }