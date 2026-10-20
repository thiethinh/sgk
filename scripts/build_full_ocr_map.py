import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ocr_dir = Path('data/ocr')

# Lesson pages definition:
# Page 8: Lam quen voi truong lop, ban be
# Page 9: Do dung hoc tap
# Pages 15-56: Lessons 1-21
lesson_pages = [8, 9] + list(range(15, 57))

for p in lesson_pages:
    json_path = ocr_dir / f"page_{p:03d}.json"
    if not json_path.exists():
        continue
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('items', [])
    filtered = []
    for item in items:
        t = item['text'].strip()
        # skip page numbers, "Bai X", "Nhan biet", "Doc", "To va viet", "Noi", single letters
        if re.match(r'^\d+$', t):
            continue
        if re.match(r'^(Bai|BAI)\s*\d*$', t, re.I):
            continue
        if re.match(r'^(Nhan biet|Doc|To va viet|Noi|Viet|Ke chuyen\*?)$', t, re.I):
            continue
        if len(t) <= 2 and not any(w in t.lower() for w in ['bo', 'ba', 'ca', 'be', 'co', 'de', 'do', 'he', 'ho', 'ga', 'go', 'me', 'no', 'ro', 'se']):
            continue
        filtered.append(t)
    print(f"P{p:02d}: {', '.join(filtered)}")
