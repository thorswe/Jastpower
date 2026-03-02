import os
from openai import OpenAI

def analyze_fermentation(prompt: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.2
    )

    return response.output_text