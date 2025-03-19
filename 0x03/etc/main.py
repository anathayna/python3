from PIL import Image, UnidentifiedImageError
import pytesseract
import os

def contains_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return len(text.strip()) > 0
    except UnidentifiedImageError:
        return False

image_dir = '/Users/ana.tc.franca/Downloads/img_resized'
output_dir = '/Users/ana.tc.franca/Downloads/filterimages'

os.makedirs(output_dir, exist_ok=True)

for image_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_name)
    if contains_text(image_path):
        output_path = os.path.join(output_dir, image_name)
        os.rename(image_path, output_path)

print('Done')