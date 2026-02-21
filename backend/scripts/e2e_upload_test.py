import requests
from PIL import Image, ImageDraw
import io

BASE = 'http://localhost:8000'

def create_test_image(path):
    img = Image.new('RGBA', (500,500), (255,0,0,255))
    d = ImageDraw.Draw(img)
    d.ellipse((100,100,400,400), fill=(0,255,0,255))
    img.save(path, format='PNG')

def upload(token, image_path):
    url = f"{BASE}/api/upload"
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': ('tmp_test_image.png', open(image_path, 'rb'), 'image/png')}
    data = {'category':'top', 'style':'casual', 'gender':'male'}
    r = requests.post(url, headers=headers, files=files, data=data)
    return r

def main():
    # read token from tmp file if created by e2e_test
    import os
    token_file = 'tmp_token.txt'
    if not os.path.exists(token_file):
        print('token file not found; run e2e_test first to obtain token')
        return
    token = open(token_file).read().strip()
    image_path = 'tmp_test_image.png'
    create_test_image(image_path)
    print('Uploading image...')
    r = upload(token, image_path)
    print('Upload status:', r.status_code, r.text)

if __name__ == '__main__':
    main()
