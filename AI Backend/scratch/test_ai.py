import sys
from ai.structuring import analyze_input
from ai.recommendation import generate_recommendation

print("Testing AI structuring...")
try:
    res = analyze_input("My baby started sitting up today without support! She is also babbling a lot and smiling at us")
    print("Result:", res)
except Exception as e:
    print("Error in structuring:", e)
    import traceback
    traceback.print_exc()

print("\nTesting AI recommendation...")
try:
    milestone = {"name": "Sitting without support", "description": "Rolls over in both directions. Begins to sit without support."}
    res = generate_recommendation(6, milestone, "language strong, motor strong")
    print("Result:", res)
except Exception as e:
    print("Error in recommendation:", e)
    import traceback
    traceback.print_exc()
