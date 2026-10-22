import docx
import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('5topic.docx')

EMU_PER_PT = 12700

for p_idx in [5, 12, 19, 25, 33]:
    p = doc.paragraphs[p_idx]
    root = ET.fromstring(p._p.xml)
    print(f"\n================ Paragraph {p_idx} ================")
    
    # Get inline image size
    img_cx, img_cy = None, None
    for inline in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'):
        ext = inline.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')
        if ext is not None:
            img_cx = int(ext.attrib['cx'])
            img_cy = int(ext.attrib['cy'])
            print(f"Inline Image: cx={img_cx} ({img_cx/EMU_PER_PT:.1f}pt), cy={img_cy} ({img_cy/EMU_PER_PT:.1f}pt)")
            
    # Now get each anchor
    for i, anchor in enumerate(root.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}anchor')):
        ext = anchor.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')
        posH = anchor.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}positionH')
        posV = anchor.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}positionV')
        
        pos_offset_h = posH.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}posOffset') if posH is not None else None
        pos_offset_v = posV.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}posOffset') if posV is not None else None
        
        cx = int(ext.attrib['cx']) if ext is not None else 0
        cy = int(ext.attrib['cy']) if ext is not None else 0
        h_val = int(pos_offset_h.text) if pos_offset_h is not None and pos_offset_h.text else 0
        v_val = int(pos_offset_v.text) if pos_offset_v is not None and pos_offset_v.text else 0
        
        # Calculate percentage relative to image
        if img_cx and img_cy:
            pct_left = (h_val / img_cx) * 100
            pct_top = (v_val / img_cy) * 100
            pct_w = (cx / img_cx) * 100
            pct_h = (cy / img_cy) * 100
            print(f"  Anchor #{i}: x={h_val/EMU_PER_PT:.1f}pt, y={v_val/EMU_PER_PT:.1f}pt, w={cx/EMU_PER_PT:.1f}pt, h={cy/EMU_PER_PT:.1f}pt | rel: L={pct_left:.2f}%, T={pct_top:.2f}%, W={pct_w:.2f}%, H={pct_h:.2f}%")
        else:
            print(f"  Anchor #{i}: x={h_val/EMU_PER_PT:.1f}pt, y={v_val/EMU_PER_PT:.1f}pt, w={cx/EMU_PER_PT:.1f}pt, h={cy/EMU_PER_PT:.1f}pt")
