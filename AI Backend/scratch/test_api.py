import requests
import json

def test_analyze():
    url = "http://127.0.0.1:8000/analyze"
    payload = {
        "child_id": "child_123",
        "age_months": 6,
        "content": "My baby started sitting up today without support! She is also babbling a lot and smiling at us."
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_analyze()
