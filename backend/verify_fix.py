import requests

url = "http://127.0.0.1:8000/api/recommend"
payload = {'occasion': 'traditional', 'gender': 'female'}

try:
    response = requests.post(url, data=payload)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
