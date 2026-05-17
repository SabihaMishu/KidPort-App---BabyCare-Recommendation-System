import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"DEBUG: Using OpenAI Key (Rec): {api_key[:8]}...{api_key[-4:]}")
client = OpenAI(api_key=api_key) if api_key else None


def generate_recommendation(child_name: str, age_months: int, milestone: dict, pattern: str):
    if not client:
        return f"At {age_months} months, {child_name} is expected to reach the {milestone.get('name')} milestone. Based on current observations, keep providing a supportive environment."

    try:
        prompt = f"""
                Baby Name: {child_name}
                Child Age: {age_months} months

                Expected Age Range:
                {milestone.get("min_age")}–{milestone.get("max_age")} months

                Expected Behavior:
                {milestone.get("description")}

                Detected Pattern:
                {pattern}

                Give a gentle parent-friendly recommendation in 2-3 sentences.
                Start by mentioning {child_name} and something positive about the pattern.
                Do not diagnose.
                """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a child development assistant. Do not diagnose. Give gentle supportive guidance."
                },
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Recommendation engine encountered an error: {str(e)}"
