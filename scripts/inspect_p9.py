import json
data = json.load(open('data/ocr/page_009.json', encoding='utf-8'))
w, h = data['width'], data['height']
print(f"Page 9 items ({w}x{h}):")
for i, item in enumerate(data['items']):
    bbox = item['bbox']
    x0 = min(p[0] for p in bbox)
    x1 = max(p[0] for p in bbox)
    y0 = min(p[1] for p in bbox)
    y1 = max(p[1] for p in bbox)
    print(f"[{i:2d}] {item['text']:<35} left={x0/w*100:.2f}%, top={y0/h*100:.2f}%, w={(x1-x0)/w*100:.2f}%, h={(y1-y0)/h*100:.2f}%")
