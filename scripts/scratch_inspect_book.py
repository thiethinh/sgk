import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('src/data/book.json', encoding='utf-8') as f:
    book = json.load(f)

print(f"Total lessons: {len(book.get('lessons', []))}")
for l in book.get('lessons', []):
    print(f"ID: {l.get('id')}, LessonNum: {l.get('lessonNumber')}, Title: {l.get('title')}, pagePdf: {l.get('pagePdf')}, pageBook: {l.get('pageBook')}")

with open('src/data/page_overlays.json', encoding='utf-8') as f:
    overlays = json.load(f)

print(f"\nTotal overlay pages: {len(overlays)}")
for p, data in sorted(overlays.items(), key=lambda x: int(x[0])):
    print(f"Page {p}: {len(data.get('overlays', []))} overlays, vocabWordIds: {data.get('vocabWordIds', [])}")
