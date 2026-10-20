import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ocr_dir = Path('data/ocr')

def get_sentence_word_bbox(items, sentence_substring, word_substring, w, h):
    # Find item that contains the sentence
    target_item = None
    for item in items:
        t = item['text']
        if sentence_substring.lower() in t.lower():
            target_item = item
            break
    
    if not target_item:
        return None
    
    t = target_item['text']
    bbox = target_item['bbox']
    x0 = min(p[0] for p in bbox)
    x1 = max(p[0] for p in bbox)
    y0 = min(p[1] for p in bbox)
    y1 = max(p[1] for p in bbox)

    idx = t.lower().find(word_substring.lower())
    if idx == -1:
        return None
    
    total_len = len(t)
    char_w = (x1 - x0) / total_len
    w_len = len(word_substring)

    wx0 = x0 + idx * char_w
    wx1 = wx0 + w_len * char_w

    l = round(wx0 / w * 100 - 0.2, 2)
    t_pct = round(y0 / h * 100 - 0.2, 2)
    bw = round((wx1 - wx0) / w * 100 + 0.4, 2)
    bh = round((y1 - y0) / h * 100 + 0.4, 2)
    return l, t_pct, bw, bh

for p in [15, 17, 19]:
    with open(ocr_dir / f"page_{p:03d}.json", encoding='utf-8') as f:
        data = json.load(f)
    w, h, items = data['width'], data['height'], data['items']
    print(f"\n--- Page {p} ---")
    if p == 15:
        print("ca hat:", get_sentence_word_bbox(items, "ca hat", "ca hat", w, h))
    elif p == 17:
        print("Ba:", get_sentence_word_bbox(items, "bup be", "Ba", w, h))
        print("be:", get_sentence_word_bbox(items, "bup be", "be", w, h))
        print("bup be:", get_sentence_word_bbox(items, "bup be", "bup be", w, h))
    elif p == 19:
        print("bo:", get_sentence_word_bbox(items, "cau ca", "bo", w, h))
        print("cau ca:", get_sentence_word_bbox(items, "cau ca", "cau ca", w, h))
