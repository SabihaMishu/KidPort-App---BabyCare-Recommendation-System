import json
import os


def get_kidmilestone(age_months: int):
    import json
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "updated_milestones.json")

    with open(file_path, "r", encoding="utf-8") as f:
        milestones = json.load(f)

    applicable = [
        m for m in milestones
        if m["min_age"] <= age_months <= m["max_age"]
    ]

    if not applicable:
        return {
            "age_range": "unknown",
            "description": "No milestone found"
        }

    return applicable[0]