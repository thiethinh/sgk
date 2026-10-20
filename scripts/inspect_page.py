import json
from pathlib import Path

data = json.load(open('data/ocr/page_017.json', encoding='utf-8'))
w = data['width']
h = data['height']
print(f"Page 17 (width={w}, height={h}):")
for item in data['items']:
    bbox = item['bbox']
    x0 = min(p[0] for p in bbox)
    x1 = max(p[0] for p in bbox)
    y0 = min(p[1] for p in bbox)
    y1 = max(p[1] for p in bbox)
    left_pct = round(x0 / w * 100, 2)
    top_pct = round(y0 / h * 100, 2)
    w_pct = round((x1 - x0) / w * 100, 2)
    h_pct = round((y1 - y0) / h * 100, 2)
    print(f"  '{item['text']}': left={left_pct}%, top={top_pct}%, width={w_pct}%, height={h_pct}%")
