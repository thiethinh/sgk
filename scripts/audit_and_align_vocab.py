import json
import os
from pathlib import Path

ocr_dir = Path('data/ocr')
entries_path = Path('src/data/entries.json')
overlays_path = Path('src/data/page_overlays.json')

with open(entries_path, encoding='utf-8') as f:
    entries = json.load(f)

print(f"Current entries count: {len(entries)}")

pages_info = {}
for p in range(1, 58):
    p_str = f"{p:03d}"
    json_file = ocr_dir / f"page_{p_str}.json"
    if json_file.exists():
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
            texts = [item['text'] for item in data.get('items', [])]
            pages_info[p] = {
                'width': data.get('width', 2280),
                'height': data.get('height', 3200),
                'items_count': len(data.get('items', [])),
                'texts': texts
            }
    else:
        pages_info[p] = None

# Print summary of pages with recognizable lesson content
for p in range(1, 58):
    info = pages_info[p]
    if not info:
        print(f"Page {p}: NO OCR")
        continue
    sample_text = " | ".join(info['texts'][:5])
    print(f"Page {p} ({info['items_count']} items): {sample_text[:80]}")
