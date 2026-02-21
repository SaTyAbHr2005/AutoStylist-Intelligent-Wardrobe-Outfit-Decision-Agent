import requests, os

BASE = 'http://localhost:8000'

def main():
    if not os.path.exists('tmp_token.txt'):
        print('tmp_token.txt missing')
        return
    token = open('tmp_token.txt').read().strip()
    img = 'tmp_test_image.png'
    if not os.path.exists(img):
        print('image not found:', img)
        return
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': (img, open(img,'rb'), 'image/png')}
    data = {'category':'bottom','style':'casual','gender':'male'}
    r = requests.post(f"{BASE}/api/upload", headers=headers, files=files, data=data)
    print('status', r.status_code, r.text)

if __name__ == '__main__':
    main()
