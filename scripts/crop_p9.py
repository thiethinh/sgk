from PIL import Image

img = Image.open('public/pages/page_009.jpg')
w, h = img.size
print(f"Image size: {w}x{h}")

# The school supplies are arranged in the middle illustration.
# Let's crop vertical slices or find where the items are located:
# Part a: "Goi ten do dung hoc tap" is at top=10.69% to top=69.41%
# Let's save a preview with grid or inspect the items
# In page 9:
# There are 7 items:
# 1. Cặp sách (backpack)
# 2. Hộp bút (pencil case)
# 3. Bảng con (chalkboard)
# 4. Bút chì (pencil)
# 5. Thước kẻ (ruler)
# 6. Tẩy (eraser)
# 7. Vở (notebook / book)

# Let's find their exact bounding boxes by cropping and checking:
crops = {
    "cap_sach": (int(w * 0.10), int(h * 0.18), int(w * 0.35), int(h * 0.42)),
    "hop_but": (int(w * 0.36), int(h * 0.18), int(w * 0.60), int(h * 0.36)),
    "bang_con": (int(w * 0.61), int(h * 0.18), int(w * 0.90), int(h * 0.42)),
    "but_chi": (int(w * 0.10), int(h * 0.43), int(w * 0.30), int(h * 0.65)),
    "thuoc_ke": (int(w * 0.31), int(h * 0.43), int(w * 0.55), int(h * 0.65)),
    "tay": (int(w * 0.56), int(h * 0.43), int(w * 0.72), int(h * 0.65)),
    "vo": (int(w * 0.73), int(h * 0.43), int(w * 0.92), int(h * 0.65))
}

for name, box in crops.items():
    cropped = img.crop(box)
    cropped.save(f"scratch/p9_{name}.jpg")
    print(f"Saved {name}: box={box}")
