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

    if not ai_result:
        return {
            "abv": round(abv, 2),
            "status": "unknown",
            "risk_level": "unknown",
            "recommendation": "AI service unavailable"
        }

    try:
        parsed = json.loads(ai_result)
    except Exception as e:
        print("JSON parse error:", e)
        print("AI raw result:", ai_result)
        return {
            "abv": round(abv, 2),
            "status": "error",
            "risk_level": "unknown",
            "recommendation": "AI returned invalid JSON",
            "raw": ai_result
        }

    return {
        "abv": round(abv, 2),
        **parsed
    }