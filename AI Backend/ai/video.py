import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def video_to_text(video_path: str):
    """
    Analyzes a video and returns a text description.
    Note: Real video analysis would require frame extraction or a multimodal model that supports video.
    For now, this is a placeholder that returns a supportive message.
    """
    if not client:
        return "Video analysis unavailable: No OpenAI API key found."

    # Placeholder logic
    return "The video shows the child engaged in active play, demonstrating good motor coordination and curiosity. (Video analysis is in placeholder mode)."
