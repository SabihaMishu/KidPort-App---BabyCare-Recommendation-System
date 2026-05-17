import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def image_to_text(image_path: str):
    """
    Analyzes an image and returns a text description of child behavior/milestones.
    """
    if not client:
        return "Image analysis unavailable: No OpenAI API key found."

    try:
        base64_image = encode_image(image_path)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe what the child is doing in this image in terms of developmental milestones (e.g., sitting, crawling, playing with toys). Keep it short and supportive."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
