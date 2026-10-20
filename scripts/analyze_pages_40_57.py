import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ocr_dir = Path('data/ocr')

def analyze_page(page_num):
    json_path = ocr_dir / f"page_{page_num:03d}.json"
    if not json_path.exists():
        return
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    w = data['width']
    h = data['height']
    items = data.get('items', [])
    print(f"\n================ PAGE {page_num} ({w}x{h}, {len(items)} items) ================")
    for idx, item in enumerate(items):
        bbox = item['bbox']
        x0 = min(p[0] for p in bbox)
        x1 = max(p[0] for p in bbox)
        y0 = min(p[1] for p in bbox)
        y1 = max(p[1] for p in bbox)
        l = round(x0 / w * 100, 2)
        t = round(y0 / h * 100, 2)
        bw = round((x1 - x0) / w * 100, 2)
        bh = round((y1 - y0) / h * 100, 2)
        text = item['text']
        print(f"[{idx:2d}] {text:<30} left={l:5.2f}% top={t:5.2f}% w={bw:5.2f}% h={bh:5.2f}%")

for p in range(40, 58):
    analyze_page(p)
