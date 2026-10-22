import json
import cv2
import numpy as np

# Let's inspect the dimensions of the 5 images
imgs = {
    1: cv2.imread('extracted_docx_images/image1.png'),
    2: cv2.imread('extracted_docx_images/image2.png'),
    3: cv2.imread('extracted_docx_images/image3.jpeg'),
    4: cv2.imread('extracted_docx_images/image4.png'),
    5: cv2.imread('extracted_docx_images/image5.png'),
}

for idx, img in imgs.items():
    print(f"Topic {idx}: shape {img.shape} (h={img.shape[0]}, w={img.shape[1]})")
