import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_fermentation(prompt: str):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=250,
            temperature=0.2
        )
        return response.output_text
    except Exception as e:
        return None
