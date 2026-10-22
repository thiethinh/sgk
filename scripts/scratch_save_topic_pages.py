import cv2
import os

os.makedirs('public/pages', exist_ok=True)

image_mapping = [
    ('extracted_docx_images/image1.png', 'public/pages/topic_1.png'),
    ('extracted_docx_images/image2.png', 'public/pages/topic_2.png'),
    ('extracted_docx_images/image3.jpeg', 'public/pages/topic_3.png'),
    ('extracted_docx_images/image4.png', 'public/pages/topic_4.png'),
    ('extracted_docx_images/image5.png', 'public/pages/topic_5.png'),
]

for src, dst in image_mapping:
    img = cv2.imread(src)
    # Save as high-quality PNG
    cv2.imwrite(dst, img)
    print(f"Saved {dst}: {img.shape[1]}x{img.shape[0]}")
