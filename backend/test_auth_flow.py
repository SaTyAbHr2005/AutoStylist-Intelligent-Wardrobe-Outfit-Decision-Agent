import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api"

# 1. Register a test user
unique_id = str(uuid.uuid4())[:8]
email = f"testuser_{unique_id}@example.com"
password = "testpassword123"

def test_auth_flow():
    print(f"Registering user: {email}...")
    register_data = {
        "full_name": "Test User",
        "email": email,
        "password": password
    }
    
    register_res = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if register_res.status_code != 201:
        print(f"FAILED to register: {register_res.text}")
        return None
        
    print(f"Successfully registered: {register_res.json()}")
    
    # 2. Login
    print("\nLogging in...")
    login_data = {
        "email": email,
        "password": password
    }
    
    login_res = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if login_res.status_code != 200:
        print(f"FAILED to login: {login_res.text}")
        return None
        
    token_data = login_res.json()
    token = token_data.get("access_token")
    print(f"Successfully logged in. Token: {token[:20]}...")
    
    # 3. Test Protected Route (/auth/me)
    print("\nTesting /auth/me with token...")
    headers = {"Authorization": f"Bearer {token}"}
    me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if me_res.status_code != 200:
         print(f"FAILED to access protected route /me: {me_res.text}")
         return None
         
    print(f"Successfully fetched me: {me_res.json()}")

    # 4. Try querying recommend with no items in DB for this user
    print("\nTesting /recommend (should return error 'Not enough wardrobe items')...")
    rec_data = {"occasion": "casual", "gender": "male"}
    rec_res = requests.post(f"{BASE_URL}/recommend", data=rec_data, headers=headers)
    print(f"Recommend Response: {rec_res.json()}")

    # 5. Logout
    print("\nTesting Logout...")
    logout_res = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    if logout_res.status_code != 200:
         print(f"FAILED to logout: {logout_res.text}")
         return None
         
    print("Logged out successfully.")
    
    # 6. Test blocklisted token
    print("\nTesting /auth/me with blocklisted token (should fail)...")
    me_res_blocked = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Response (should be 401): {me_res_blocked.status_code} - {me_res_blocked.text}")

if __name__ == "__main__":
    try:
        # Check if server is running
        res = requests.get("http://localhost:8000/")
        if res.status_code == 200:
            test_auth_flow()
        else:
            print("Server is not running correctly.")
    except requests.exceptions.ConnectionError:
        print("Server is NOT running at http://localhost:8000. Start it with: uvicorn app.main:app --reload")
