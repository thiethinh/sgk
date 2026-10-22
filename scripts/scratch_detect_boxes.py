import cv2
import numpy as np
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['image1.png', 'image2.png', 'image3.jpeg', 'image4.png', 'image5.png']:
    img = cv2.imread(f'extracted_docx_images/{fname}')
    h, w, c = img.shape
    print(f"=== {fname} ({w}x{h}) ===")
    
    # Check for prominent red/colored rectangular contours
    # In HSV: Red is around H: 0-10, 170-180, S > 100, V > 100
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2
    
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for cnt in contours:
        x, y, rw, rh = cv2.boundingRect(cnt)
        if rw > 15 and rh > 15: # filter small noise
            rects.append((x, y, rw, rh, rw * rh))
            
    rects.sort(key=lambda r: (r[1], r[0]))
    print(f"Found {len(rects)} red boxes:")
    for r in rects:
        # relative percent
        rx = round(r[0] / w * 100, 2)
        ry = round(r[1] / h * 100, 2)
        rw_pct = round(r[2] / w * 100, 2)
        rh_pct = round(r[3] / h * 100, 2)
        print(f"  Box: x={r[0]}, y={r[1]}, w={r[2]}, h={r[3]} ({rw_pct}% left, {ry}% top, {rw_pct}% width, {rh_pct}% height) area={r[4]}")
