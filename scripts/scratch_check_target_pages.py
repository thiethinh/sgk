import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('src/data/page_overlays.json', encoding='utf-8') as f:
    overlays = json.load(f)

for p in [18, 19, 20, 24, 25, 26, 32, 33, 34, 44, 45, 46]:
    data = overlays.get(str(p), {})
    print(f"=== Page {p} ===")
    print("Image:", data.get('image'))
    for ov in data.get('overlays', []):
        print(f"  Overlay: id={ov['id']}, text={ov['text']}, entryId={ov.get('entryId')}, L={ov['left']}%, T={ov['top']}%, W={ov['width']}%, H={ov['height']}%")
