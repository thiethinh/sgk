import docx
import xml.etree.ElementTree as ET
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('5topic.docx')

for i, p in enumerate(doc.paragraphs):
    root = ET.fromstring(p._p.xml)
    # find all shapes/rects
    shapes = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]
        if tag in ['shape', 'rect']:
            style = elem.attrib.get('style', '')
            shape_id = elem.attrib.get('id', '')
            shapes.append((tag, shape_id, style))
    
    if shapes or p.text.strip():
        print(f"\n================ Paragraph {i} ================")
        if p.text.strip():
            print(f"Text: {p.text.strip()}")
        if shapes:
            print(f"Shapes ({len(shapes)}):")
            for tag, sid, style in shapes:
                # parse margin-left, margin-top, width, height
                ml = re.search(r'margin-left:([^;]+)', style)
                mt = re.search(r'margin-top:([^;]+)', style)
                w = re.search(r'width:([^;]+)', style)
                h = re.search(r'height:([^;]+)', style)
                pos = f"left={ml.group(1) if ml else '?'}, top={mt.group(1) if mt else '?'}, w={w.group(1) if w else '?'}, h={h.group(1) if h else '?'}"
                print(f"  [{tag} id={sid}] {pos}")
