from PIL import Image, ImageDraw

img = Image.open('public/pages/page_009.jpg')
w, h = img.size
draw = img.copy()
d = ImageDraw.Draw(draw)

p9_supplies = {
    "bút chì": [21.0, 16.5, 15.0, 11.0],
    "bảng con": [7.5, 27.5, 27.0, 14.5],
    "thước kẻ": [69.5, 13.0, 22.0, 8.5],
    "tẩy": [38.5, 35.5, 14.0, 6.5],
    "sách": [49.5, 21.0, 19.5, 20.5],
    "vở": [69.0, 21.0, 21.0, 20.5]
}

for name, (l, t, bw, bh) in p9_supplies.items():
    x0 = int(l / 100 * w)
    y0 = int(t / 100 * h)
    x1 = int((l + bw) / 100 * w)
    y1 = int((t + bh) / 100 * h)
    d.rectangle([x0, y0, x1, y1], outline="blue", width=6)

draw.save('scratch/verified_p9_supplies.jpg')
print("Saved scratch/verified_p9_supplies.jpg")
