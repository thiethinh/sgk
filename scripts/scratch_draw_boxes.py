import cv2
import docx
import xml.etree.ElementTree as ET
import os

os.makedirs('annotated_docx_images', exist_ok=True)
doc = docx.Document('5topic.docx')

EMU_PER_PT = 12700

items = [
    (5, 'image1.png', 'annotated_1.png'),
    (12, 'image2.png', 'annotated_2.png'),
    (19, 'image3.jpeg', 'annotated_3.png'),
    (25, 'image4.png', 'annotated_4.png'),
    (33, 'image5.png', 'annotated_5.png'),
]

for p_idx, in_name, out_name in items:
    img = cv2.imread(f'extracted_docx_images/{in_name}')
    h_img, w_img, _ = img.shape
    
    p = doc.paragraphs[p_idx]
    root = ET.fromstring(p._p.xml)
    
    # Get inline image size
    img_cx, img_cy = None, None
    for inline in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'):
        ext = inline.find('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')
        if ext is not None:
            img_cx = int(ext.attrib['cx'])
            img_cy = int(ext.attrib['cy'])
            
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
        
        rel_x = h_val / img_cx
        rel_y = v_val / img_cy
        rel_w = cx / img_cx
        rel_h = cy / img_cy
        
        px = int(rel_x * w_img)
        py = int(rel_y * h_img)
        pw = int(rel_w * w_img)
        ph = int(rel_h * h_img)
        
        cv2.rectangle(img, (px, py), (px + pw, py + ph), (0, 0, 255), 3)
        cv2.putText(img, str(i), (px, max(20, py - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # also crop and save
        crop = img[max(0, py):min(h_img, py+ph), max(0, px):min(w_img, px+pw)]
        if crop.size > 0:
            cv2.imwrite(f'annotated_docx_images/crop_p{p_idx}_{i}.png', crop)

    cv2.imwrite(f'annotated_docx_images/{out_name}', img)
    print(f"Saved annotated_docx_images/{out_name}")
