import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"DEBUG: Using OpenAI Key: {api_key[:8]}...{api_key[-4:]}")
client = OpenAI(api_key=api_key) if api_key else None


def analyze_input(content: str):
    if not client:
        return {
            "language": 0.5,
            "motor": 0.5,
            "social": 0.5,
            "cognitive": 0.5,
            "mood": "normal",
            "note": f"AI not active. .env checked at: {ENV_PATH}"
        }

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """
You are a child development expert.

Analyze the parent's note and return ONLY JSON.

Format:
{
  "language": number (0 to 1),
  "motor": number (0 to 1),
  "social": number (0 to 1),
  "cognitive": number (0 to 1),
  "mood": "low" or "normal" or "good"
}

Rules:
- Estimate scores based on behavior
- If not mentioned → give 0.5
- Keep it simple
- DO NOT return text, only JSON
"""
                },
                {"role": "user", "content": content}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        text = content.lower()

        return {
            "language": 0.8 if "babbling" in text or "sound" in text else 0.5,
            "motor": 0.8 if "sitting" in text or "reaching" in text or "crawling" in text else 0.5,
            "social": 0.8 if "smiling" in text or "eye contact" in text else 0.5,
            "cognitive": 0.7 if "reaching" in text or "toy" in text or "toys" in text else 0.5,
            "mood": "good" if "smiling" in text else "normal",
            "ai_error": str(e)
        }