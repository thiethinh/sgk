import cv2
import json

def draw_test_boxes(img_path, boxes, out_path):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    for b in boxes:
        x = int(b['left'] * w / 100)
        y = int(b['top'] * h / 100)
        bw = int(b['width'] * w / 100)
        bh = int(b['height'] * h / 100)
        cv2.rectangle(img, (x, y), (x + bw, y + bh), (0, 0, 255), 2)
        cv2.putText(img, b['id'], (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    cv2.imwrite(out_path, img)

# Topic 1 proposed boxes:
topic1_boxes = [
    {"id": "c", "text": "c", "left": 25.0, "top": 45.0, "width": 3.0, "height": 4.5},
    {"id": "ca_nuoc", "text": "ca", "left": 10.5, "top": 72.5, "width": 5.2, "height": 4.5},
    {"id": "ca_tim", "text": "cà", "left": 23.0, "top": 72.5, "width": 5.2, "height": 4.5},
    {"id": "ca", "text": "cá", "left": 35.5, "top": 72.5, "width": 5.2, "height": 4.5},
    {"id": "a_ca", "text": "A, cá.", "left": 64.0, "top": 20.0, "width": 8.5, "height": 5.2},
    {"id": "hoi_thoai_1", "text": "Good morning", "left": 56.5, "top": 58.0, "width": 18.5, "height": 37.0},
    {"id": "hoi_thoai_2", "text": "Hi", "left": 75.8, "top": 58.0, "width": 18.5, "height": 37.0},
]
draw_test_boxes('public/pages/topic_1.png', topic1_boxes, 'scratch_test_topic1.png')

# Topic 2 proposed boxes:
# Width=1204, Height=835
# Left: bò, cò, cỏ. Right: Bê có cỏ. Tranh 1: Hi, mom. Tranh 2: Good afternoon...
topic2_boxes = [
    {"id": "con_bo", "text": "bò", "left": 12.0, "top": 72.5, "width": 5.5, "height": 4.8},
    {"id": "con_co", "text": "cò", "left": 24.2, "top": 72.5, "width": 5.5, "height": 4.8},
    {"id": "co", "text": "cỏ", "left": 35.8, "top": 72.5, "width": 5.5, "height": 4.8},
    {"id": "be_co_co", "text": "Bê có cỏ.", "left": 69.5, "top": 42.5, "width": 12.0, "height": 5.0},
    {"id": "hoi_thoai_1", "text": "Hi, mom", "left": 56.2, "top": 59.0, "width": 18.8, "height": 36.5},
    {"id": "hoi_thoai_2", "text": "Good afternoon, Grandmother / Grandfather", "left": 75.8, "top": 59.0, "width": 18.8, "height": 36.5},
]
draw_test_boxes('public/pages/topic_2.png', topic2_boxes, 'scratch_test_topic2.png')

# Topic 3 proposed boxes (Bài 10):
# Width=1389, Height=963
# Left: bó cỏ, cá cờ, bờ đê, đỡ bà, cờ đỏ, đỗ đỏ, đỡ bé, Bờ đê có dế., Bà có đỗ đỏ.
# Right: Đàn kiến con ngoan ngoãn. 4 pictures (1), (2), (3), (4)
topic3_boxes = [
    {"id": "dan_kien_title", "text": "Đàn kiến con ngoan ngoãn", "left": 62.5, "top": 22.5, "width": 23.5, "height": 4.5},
    {"id": "tranh_1", "text": "Bà kiến sống ở đâu?", "left": 54.5, "top": 28.0, "width": 19.5, "height": 29.0},
    {"id": "tranh_2", "text": "Đàn kiến con dùng vật gì để khiêng bà kiến?", "left": 75.0, "top": 28.0, "width": 19.5, "height": 29.0},
    {"id": "tranh_3", "text": "Đàn kiến con đưa bà kiến đến đâu?", "left": 54.5, "top": 61.0, "width": 19.5, "height": 29.0},
    {"id": "tranh_4", "text": "Được ở nhà mới, bà kiến nói gì với đàn kiến con?", "left": 75.0, "top": 61.0, "width": 19.5, "height": 29.0},
    # Left page vocabulary
    {"id": "ca_co", "text": "cá cờ", "left": 5.0, "top": 51.5, "width": 6.5, "height": 3.8},
    {"id": "bo_co", "text": "bó cỏ", "left": 19.5, "top": 45.0, "width": 6.5, "height": 3.8},
    {"id": "bo_de", "text": "bờ đê", "left": 25.5, "top": 55.5, "width": 6.5, "height": 3.8},
    {"id": "do_ba", "text": "đỡ bà", "left": 36.5, "top": 51.5, "width": 6.5, "height": 3.8},
    {"id": "co_do", "text": "cờ đỏ", "left": 12.5, "top": 62.5, "width": 6.5, "height": 3.8},
    {"id": "do_be", "text": "đỡ bé", "left": 14.5, "top": 74.0, "width": 6.5, "height": 3.8},
    {"id": "do_do", "text": "đỗ đỏ", "left": 30.5, "top": 68.0, "width": 6.5, "height": 3.8},
    {"id": "cau_1", "text": "Bờ đê có dế.", "left": 8.0, "top": 82.5, "width": 13.0, "height": 4.5},
    {"id": "cau_2", "text": "Bà có đỗ đỏ.", "left": 23.5, "top": 82.5, "width": 13.0, "height": 4.5},
]
draw_test_boxes('public/pages/topic_3.png', topic3_boxes, 'scratch_test_topic3.png')

# Topic 4 proposed boxes (Bài 16):
# Width=1376, Height=954
# Left: cá mè, lá me, nơ đỏ, ca nô. Right: Bố mẹ cho Hà đi ca nô. Tranh Nói: Giới thiệu
topic4_boxes = [
    {"id": "ca_me", "text": "cá mè", "left": 8.0, "top": 72.8, "width": 7.5, "height": 4.2},
    {"id": "la_me", "text": "lá me", "left": 17.0, "top": 72.8, "width": 7.5, "height": 4.2},
    {"id": "no_do", "text": "nơ đỏ", "left": 26.0, "top": 72.8, "width": 7.5, "height": 4.2},
    {"id": "ca_no", "text": "ca nô", "left": 36.0, "top": 72.8, "width": 7.5, "height": 4.2},
    {"id": "bo_me_cho_ha_di_ca_no", "text": "Bố mẹ cho Hà đi ca nô.", "left": 64.5, "top": 36.0, "width": 19.5, "height": 4.8},
    {"id": "hoi_thoai_gioi_thieu", "text": "Giới thiệu bản thân", "left": 53.5, "top": 51.5, "width": 41.5, "height": 41.5},
]
draw_test_boxes('public/pages/topic_4.png', topic4_boxes, 'scratch_test_topic4.png')

# Topic 5 proposed boxes (Bài 28):
# Width=1305, Height=905
# Left: y tá, dã quỳ, đá quý. Right: Mẹ và Hà ghé nhà dì Kha... Tranh 1: Cảm ơn (che ô). Tranh 2: Cảm ơn ông bà.
topic5_boxes = [
    {"id": "y_ta", "text": "y tá", "left": 11.5, "top": 72.0, "width": 6.5, "height": 4.2},
    {"id": "da_quy", "text": "dã quỳ", "left": 24.0, "top": 72.0, "width": 7.5, "height": 4.2},
    {"id": "da_quy_gem", "text": "đá quý", "left": 35.8, "top": 72.0, "width": 7.5, "height": 4.2},
    {"id": "cau_doc_p28", "text": "Mẹ và Hà ghé nhà dì Kha. Dì kể cho Hà nghe về bà. Hà chú ý nghe dì kể.", "left": 56.5, "top": 40.0, "width": 40.5, "height": 7.5},
    {"id": "hoi_thoai_1", "text": "Thank you", "left": 57.5, "top": 59.0, "width": 18.8, "height": 36.5},
    {"id": "hoi_thoai_2", "text": "Thank you so much, Grandmother and Grandfather", "left": 77.0, "top": 59.0, "width": 18.8, "height": 36.5},
]
draw_test_boxes('public/pages/topic_5.png', topic5_boxes, 'scratch_test_topic5.png')
print("All test box images generated successfully!")
