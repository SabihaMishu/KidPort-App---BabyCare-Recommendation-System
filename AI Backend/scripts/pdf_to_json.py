import json
import re
from pathlib import Path
from PyPDF2 import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "data" / "cdc.pdf"
OUTPUT_PATH = BASE_DIR / "data" / "milestones.json"

CATEGORY_MAP = {
    "Social/Emotional Milestones": "social",
    "Language/Communication Milestones": "language",
    "Cognitive Milestones": "cognitive",
    "Movement/Physical Development": "motor",
    "Movement/Physical Development Milestones": "motor",
}

AGE_MAP = {
    "2 months": 2,
    "4 months": 4,
    "6 months": 6,
    "9 months": 9,
    "12 months": 12,
    "15 months": 15,
    "18 months": 18,
    "2 years": 24,
    "30 months": 30,
    "3 years": 36,
    "4 years": 48,
    "5 years": 60,
}


def extract_text():
    reader = PdfReader(str(PDF_PATH))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def detect_age(line: str):
    clean = line.lower().replace("*", "")
    for label, months in AGE_MAP.items():
        if label in clean:
            return months
    return None


def clean_item(text: str):
    text = text.replace("◦", "").strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -•")


def parse_pdf_text(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    milestones = []
    current_age = None
    current_category = None

    skip_phrases = [
        "What most",
        "Other important",
        "Milestones matter",
        "You know",
        "Don’t wait",
        "Acting early",
        "Baby’s Name",
        "Child’s Name",
        "It’s time",
        "Help your",
        "Learn the Signs",
        "This milestone checklist",
        "www.cdc.gov",
        "To see more tips",
    ]

    for line in lines:
        age = detect_age(line)
        if age:
            current_age = age
            current_category = None
            continue

        for heading, category in CATEGORY_MAP.items():
            if heading.lower() in line.lower():
                current_category = category
                break

        if any(p.lower() in line.lower() for p in skip_phrases):
            continue

        if current_age and current_category and line.startswith("◦"):
            desc = clean_item(line)
            if desc:
                milestones.append({
                    "age_months": current_age,
                    "category": current_category,
                    "description": desc
                })

    return milestones


def remove_duplicates(data):
    seen = set()
    cleaned = []

    for item in data:
        key = (
            item["age_months"],
            item["category"],
            item["description"].lower()
        )

        if key not in seen:
            seen.add(key)
            cleaned.append(item)

    return cleaned


def save_json(data):
    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    text = extract_text()
    data = parse_pdf_text(text)
    data = remove_duplicates(data)
    save_json(data)

    print(f"✅ Generated {len(data)} milestones")
    print(f"📁 Saved to: {OUTPUT_PATH}")