import docx
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('5topic.docx')

for i, p in enumerate(doc.paragraphs):
    has_img = any('drawing' in r._r.xml for r in p.runs)
    t = p.text.strip()
    if t or has_img:
        print(f"P{i} (img={has_img}): {t}")
