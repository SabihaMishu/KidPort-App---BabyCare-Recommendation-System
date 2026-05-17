import json
import os

# Define file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data", "milestones.json")
output_path = os.path.join(base_dir, "data", "updated_milestones.json")

# Load the existing milestones.json file
with open(file_path, "r", encoding="utf-8") as f:
    milestones = json.load(f)

# List to store updated milestones
updated_milestones = []

# Loop through each milestone and update age to range
for milestone in milestones:
    age = milestone["age_months"]

    # Define the range based on the age_months value (can modify based on your range)
    if age == 0:
        min_age = 0
        max_age = 2
    elif age == 2:
        min_age = 2
        max_age = 4
    elif age == 4:
        min_age = 4
        max_age = 6
    elif age == 6:
        min_age = 6
        max_age = 9
    elif age == 9:
        min_age = 9
        max_age = 12
    elif age == 12:
        min_age = 12
        max_age = 15
    elif age == 15:
        min_age = 15
        max_age = 18
    elif age == 18:
        min_age = 18
        max_age = 24
    elif age == 24:
        min_age = 24
        max_age = 30
    elif age == 30:
        min_age = 30
        max_age = 36
    elif age == 36:
        min_age = 36
        max_age = 48
    elif age == 48:
        min_age = 48
        max_age = 60
    else:
        min_age = age
        max_age = age + 1  # Default range if no specific range is defined

    # Create a new milestone dict with min_age and max_age
    updated_milestone = {
        "min_age": min_age,
        "max_age": max_age,
        "category": milestone["category"],
        "description": milestone["description"]
    }

    # Append the updated milestone to the list
    updated_milestones.append(updated_milestone)

# Save the updated data into a new JSON file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(updated_milestones, f, indent=4)

print("✅ Milestones updated successfully and saved to updated_milestones.json")