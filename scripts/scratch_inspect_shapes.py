import docx
import xml.etree.ElementTree as ET

doc = docx.Document('5topic.docx')
for p_idx in [5, 12, 19, 25, 33]:
    p = doc.paragraphs[p_idx]
    root = ET.fromstring(p._p.xml)
    print(f"=== Paragraph {p_idx} ===")
    tags = set(elem.tag.split('}')[-1] for elem in root.iter())
    print("Tags present:", tags)
    # Check if there are shape / drawing elements
    for shape in root.iter():
        tag = shape.tag.split('}')[-1]
        if tag in ['sp', 'shape', 'rect', 'textbox', 'txbx']:
            print(f"Found shape tag: {tag}, attribs: {shape.attrib}")
            text = "".join(shape.itertext())
            if text:
                print(f"   Shape text: {text}")
