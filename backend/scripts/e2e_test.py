import requests
import sys

BASE = 'http://localhost:8000'

def register(email, full_name, password):
    url = f"{BASE}/api/auth/register"
    payload = {"full_name": full_name, "email": email, "password": password}
    r = requests.post(url, json=payload)
    return r

def login(email, password):
    url = f"{BASE}/api/auth/login"
    data = {'username': email, 'password': password}
    r = requests.post(url, data=data)
    return r

def me(token):
    url = f"{BASE}/api/auth/me"
    headers = {'Authorization': f'Bearer {token}'}
    return requests.get(url, headers=headers)

def recommend(token, occasion='casual'):
    url = f"{BASE}/api/recommend"
    headers = {'Authorization': f'Bearer {token}'}
    data = {'occasion': occasion}
    return requests.post(url, headers=headers, data=data)

def main():
    email = 'satya69+autotest@gmail.com'
    password = '12345678'
    full_name = 'Satya Autotest'

    print('Registering user...')
    r = register(email, full_name, password)
    print('Register status:', r.status_code, r.text)

    print('Logging in...')
    r = login(email, password)
    print('Login status:', r.status_code, r.text)
    if r.status_code != 200:
        print('Login failed; aborting e2e run')
        sys.exit(1)

    token = r.json().get('access_token')
    if not token:
        print('No token returned; aborting')
        sys.exit(1)

    # Save token for other scripts
    with open('tmp_token.txt','w') as f:
        f.write(token)

    print('Calling /api/auth/me')
    r = me(token)
    print('/me status:', r.status_code, r.text)

    print('Calling /api/recommend (may return error if no wardrobe items)')
    r = recommend(token, 'casual')
    print('/recommend status:', r.status_code, r.text)

if __name__ == '__main__':
    main()
