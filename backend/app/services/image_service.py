from rembg import remove, new_session
from PIL import Image
import os
import uuid

UPLOAD_DIR = "app/uploads"
PROCESSED_DIR = "app/static/processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


# Initialize the lightweight model ONCE when the module loads
# This ensures we don't accidentally trigger the default 'u2net' download
u2netp_session = new_session("u2netp")

def process_image(file):
    file_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{file_id}.png"
    output_path = f"{PROCESSED_DIR}/{file_id}.png"

    # Save original
    with open(input_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Open image
    input_image = Image.open(input_path).convert("RGBA")

    # Remove background using the globally initialized lightweight model session
    output_image = remove(input_image, session=u2netp_session)

    # Resize
    output_image = output_image.resize((400, 400))

    # Clean semi-transparent edges
    pixels = output_image.getdata()
    new_pixels = []

    for item in pixels:
        if item[3] < 100:  # low alpha → make fully transparent
            new_pixels.append((0, 0, 0, 0))
        else:
            new_pixels.append(item)

    output_image.putdata(new_pixels)

    output_image.save(output_path)
    
    # Clean up the original uploaded image to save disk space
    if os.path.exists(input_path):
        os.remove(input_path)

    return output_path
