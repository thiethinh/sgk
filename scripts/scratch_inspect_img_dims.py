import docx
import xml.etree.ElementTree as ET
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('5topic.docx')

for p_idx in [5, 12, 19, 25, 33]:
    p = doc.paragraphs[p_idx]
    root = ET.fromstring(p._p.xml)
    print(f"\n================ Paragraph {p_idx} ================")
    # Look for image / shape dimensions
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]
        if tag in ['shape', 'imagedata', 'extent', 'inline', 'anchor']:
            print(f"Tag: {tag}, attribs: {elem.attrib}")
