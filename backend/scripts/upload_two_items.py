import requests
from PIL import Image, ImageDraw
import os

BASE = 'http://localhost:8000'

def create_image(path, color):
    img = Image.new('RGBA', (500,500), color)
    d = ImageDraw.Draw(img)
    d.rectangle((50,50,450,450), outline=(0,0,0))
    img.save(path, format='PNG')

def upload(token, path, category):
    url = f"{BASE}/api/upload"
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': (os.path.basename(path), open(path,'rb'), 'image/png')}
    data = {'category':category, 'style':'casual', 'gender':'male'}
    r = requests.post(url, headers=headers, files=files, data=data)
    return r

def main():
    if not os.path.exists('tmp_token.txt'):
        print('tmp_token.txt missing; run e2e_test first')
        return
    token = open('tmp_token.txt').read().strip()
    t1 = 'tmp_top.png'
    t2 = 'tmp_bottom.png'
    create_image(t1, (200,50,50,255))
    create_image(t2, (50,50,200,255))
    print('Uploading top...')
    print(upload(token, t1, 'top').status_code)
    print('Uploading bottom...')
    print(upload(token, t2, 'bottom').status_code)

if __name__ == '__main__':
    main()
