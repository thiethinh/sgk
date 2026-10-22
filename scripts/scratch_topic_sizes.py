import cv2
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# The 5 spread images from docx
image_files = {
    1: 'image1.png',
    2: 'image2.png',
    3: 'image3.jpeg',
    4: 'image4.png',
    5: 'image5.png',
}

# Let's inspect image dimensions
for t, fname in image_files.items():
    img = cv2.imread(f'extracted_docx_images/{fname}')
    print(f"Topic {t} ({fname}): width={img.shape[1]}, height={img.shape[0]}")
