from PIL import Image
import numpy as np

img = Image.open('public/pages/page_009.jpg')
arr = np.array(img)
w, h = img.size

# Let's inspect rows from y=450 to y=2200
# Let's find connected components or bright colored regions
# Or save an annotated image with rectangles so we can inspect and tune!
draw = img.copy()
from PIL import ImageDraw

d = ImageDraw.Draw(draw)

# Let's test candidate boxes in %
test_boxes = {
    # Row 1 (top):
    "cặp sách": [10.5, 17.5, 24.5, 24.0],  # backpack on left
    "hộp bút": [37.5, 17.5, 23.0, 16.5],   # pencil case in middle top
    "bảng con": [63.0, 17.5, 27.0, 24.0],  # chalkboard on right top
    # Row 2 (middle):
    "bút chì": [10.5, 43.5, 18.0, 21.0],   # pencil
    "thước kẻ": [30.5, 43.5, 23.0, 21.0],  # ruler
    "tẩy": [56.0, 43.5, 15.0, 21.0],       # eraser
    "vở": [73.0, 43.5, 18.0, 21.0]         # notebook
}

for name, (l, t, bw, bh) in test_boxes.items():
    x0 = int(l / 100 * w)
    y0 = int(t / 100 * h)
    x1 = int((l + bw) / 100 * w)
    y1 = int((t + bh) / 100 * h)
    d.rectangle([x0, y0, x1, y1], outline="red", width=8)

draw.save('scratch/annotated_p9.jpg')
print("Saved scratch/annotated_p9.jpg")
