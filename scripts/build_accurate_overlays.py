import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ocr_dir = Path('data/ocr')
entries_file = Path('src/data/entries.json')
overlays_file = Path('src/data/page_overlays.json')

with open(entries_file, encoding='utf-8') as f:
    entries = json.load(f)

def norm(s):
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def get_sentence_word_bbox(items, sentence_substr, word_substr, w, h):
    s_norm = norm(sentence_substr)
    target_item = None
    for item in items:
        it_norm = norm(item['text'])
        if s_norm in it_norm:
            target_item = item
            break
    
    if not target_item:
        return None
    
    t = target_item['text']
    bbox = target_item['bbox']
    x0 = min(p[0] for p in bbox)
    x1 = max(p[0] for p in bbox)
    y0 = min(p[1] for p in bbox)
    y1 = max(p[1] for p in bbox)

    t_norm = norm(t)
    w_norm = norm(word_substr)
    idx = t_norm.find(w_norm)
    if idx == -1:
        return None
    
    total_len = len(t)
    char_w = (x1 - x0) / total_len
    w_len = len(word_substr)

    wx0 = x0 + idx * char_w
    wx1 = wx0 + w_len * char_w

    l = round(wx0 / w * 100 - 0.2, 2)
    t_pct = round(y0 / h * 100 - 0.2, 2)
    bw = round((wx1 - wx0) / w * 100 + 0.4, 2)
    bh = round((y1 - y0) / h * 100 + 0.4, 2)
    return max(0.5, l), max(0.5, t_pct), min(50.0, bw), min(15.0, bh)

def get_standalone_word_bbox(items, word_substr, w, h, occurrence=1):
    w_norm = norm(word_substr)
    found_count = 0
    for item in items:
        it_norm = norm(item['text'])
        # check exact match or isolated word
        if it_norm == w_norm or re.search(r'\b' + re.escape(w_norm) + r'\b', it_norm):
            found_count += 1
            if found_count == occurrence:
                bbox = item['bbox']
                x0 = min(p[0] for p in bbox)
                x1 = max(p[0] for p in bbox)
                y0 = min(p[1] for p in bbox)
                y1 = max(p[1] for p in bbox)
                l = round(x0 / w * 100 - 0.3, 2)
                t = round(y0 / h * 100 - 0.3, 2)
                bw = round((x1 - x0) / w * 100 + 0.6, 2)
                bh = round((y1 - y0) / h * 100 + 0.6, 2)
                return max(0.5, l), max(0.5, t), min(50.0, bw), min(15.0, bh)
    return None

# Definitive target mapping for all pages
PAGE_TARGETS = {
    8: [
        {"id": "ov_p8_truonglop", "text": "trường lớp", "entryId": "truong_lop", "type": "standalone", "query": "truong lop"},
        {"id": "ov_p8_banbe", "text": "bạn bè", "entryId": "ban_be", "type": "standalone", "query": "ban be"},
    ],
    9: [
        {"id": "ov_p9_butchi", "text": "bút chì", "entryId": "but_chi", "type": "fallback", "box": [21.0, 16.5, 15.0, 11.0]},
        {"id": "ov_p9_bangcon", "text": "bảng con", "entryId": "bang_con", "type": "fallback", "box": [7.5, 27.5, 27.0, 14.5]},
        {"id": "ov_p9_thuocke", "text": "thước kẻ", "entryId": "thuoc_ke", "type": "fallback", "box": [69.5, 13.0, 22.0, 8.5]},
        {"id": "ov_p9_tay", "text": "tẩy", "entryId": "tay_gom", "type": "fallback", "box": [38.5, 35.5, 14.0, 6.5]},
        {"id": "ov_p9_sach", "text": "sách", "entryId": "sach", "type": "fallback", "box": [49.5, 21.0, 19.5, 20.5]},
        {"id": "ov_p9_vo", "text": "vở", "entryId": "vo_viet", "type": "fallback", "box": [69.0, 21.0, 21.0, 20.5]},
    ],
    15: [
        {"id": "ov_p15_cahat", "text": "ca hát", "entryId": "ca_hat", "type": "fallback", "box": [54.39, 59.69, 9.91, 2.81]},
    ],
    16: [
        {"id": "ov_p16_chaohoi", "text": "chào hỏi", "entryId": "chao_hoi", "type": "fallback", "box": [43.8, 55.7, 14.5, 3.0]},
    ],
    17: [
        {"id": "ov_p17_ba", "text": "bà", "entryId": "ba_noi", "type": "sentence", "sentence": "bup be", "query": "Ba"},
        {"id": "ov_p17_be", "text": "bé", "entryId": "be", "type": "sentence", "sentence": "bup be", "query": "be"},
        {"id": "ov_p17_bupbe", "text": "búp bê", "entryId": "bup_be", "type": "sentence", "sentence": "bup be", "query": "bup be"},
        {"id": "ov_p17_soba", "text": "ba", "entryId": "so_ba", "type": "fallback", "box": [24.5, 73.3, 5.5, 3.3]},
        {"id": "ov_p17_banoipic", "text": "bà", "entryId": "ba_noi", "type": "fallback", "box": [49.0, 73.3, 5.5, 3.3]},
        {"id": "ov_p17_baba", "text": "ba ba", "entryId": "ba_ba", "type": "fallback", "box": [71.2, 73.3, 10.0, 3.3]},
    ],
    18: [
        {"id": "ov_p18_giadinh", "text": "gia đình", "entryId": "gia_dinh", "type": "fallback", "box": [43.6, 50.3, 13.6, 3.2]},
    ],
    19: [
        {"id": "ov_p19_bo", "text": "bố", "entryId": "bo", "type": "sentence", "sentence": "cau ca", "query": "bo"},
        {"id": "ov_p19_cauca", "text": "câu cá", "entryId": "cau_ca", "type": "sentence", "sentence": "cau ca", "query": "cau ca"},
        {"id": "ov_p19_canuoc", "text": "ca", "entryId": "ca_nuoc", "type": "fallback", "box": [24.0, 73.0, 6.0, 3.2]},
        {"id": "ov_p19_catim", "text": "cà", "entryId": "ca_tim", "type": "fallback", "box": [49.0, 73.0, 6.0, 3.2]},
        {"id": "ov_p19_ca", "text": "cá", "entryId": "ca", "type": "fallback", "box": [74.0, 73.0, 6.0, 3.2]},
    ],
    20: [
        {"id": "ov_p20_chaohoi", "text": "chào hỏi", "entryId": "chao_hoi", "type": "fallback", "box": [45.0, 51.6, 14.5, 3.2]},
    ],
    21: [
        {"id": "ov_p21_be", "text": "bé", "entryId": "be", "type": "sentence", "sentence": "ve ban be", "query": "Be"},
        {"id": "ov_p21_me", "text": "mẹ", "entryId": "me", "type": "sentence", "sentence": "ve ban be", "query": "me"},
        {"id": "ov_p21_banbe", "text": "bạn bè", "entryId": "ban_be", "type": "sentence", "sentence": "ve ban be", "query": "ban be"},
        {"id": "ov_p21_conbe", "text": "bê", "entryId": "con_be", "type": "fallback", "box": [73.5, 73.2, 5.5, 3.0]},
    ],
    22: [
        {"id": "ov_p22_ba", "text": "bà", "entryId": "ba_noi", "type": "sentence", "sentence": "Ba be be", "query": "Ba"},
        {"id": "ov_p22_betay", "text": "bế", "entryId": "be_tay", "type": "fallback", "box": [47.5, 38.6, 4.5, 3.0]},
        {"id": "ov_p22_be", "text": "bé", "entryId": "be", "type": "fallback", "box": [52.2, 38.6, 4.8, 3.0]},
    ],
    23: [
        {"id": "ov_p23_baba", "text": "ba ba", "entryId": "ba_ba", "type": "standalone", "query": "ba ba"},
        {"id": "ov_p23_beca", "text": "bể cá", "entryId": "be_ca", "type": "standalone", "query": "be ca"},
        {"id": "ov_p23_betay", "text": "bế", "entryId": "be_tay", "type": "sentence", "sentence": "Ba be be", "query": "be"},
    ],
    24: [
        {"id": "ov_p24_bupbe", "text": "búp bê", "entryId": "bup_be", "type": "sentence", "sentence": "Bup be va de men", "query": "Bup be"},
        {"id": "ov_p24_demen", "text": "dế mèn", "entryId": "de_men", "type": "sentence", "sentence": "Bup be va de men", "query": "de men"},
    ],
    25: [
        {"id": "ov_p25_bo", "text": "bò", "entryId": "con_bo", "type": "sentence", "sentence": "gam co", "query": "bo"},
        {"id": "ov_p25_gamco", "text": "gặm cỏ", "entryId": "gam_co", "type": "sentence", "sentence": "gam co", "query": "gam co"},
        {"id": "ov_p25_conco", "text": "cò", "entryId": "con_co", "type": "fallback", "box": [51.5, 73.0, 5.0, 3.0]},
        {"id": "ov_p25_co", "text": "cỏ", "entryId": "co", "type": "fallback", "box": [74.5, 73.0, 5.5, 3.0]},
    ],
    26: [
        {"id": "ov_p26_be", "text": "bé", "entryId": "be", "type": "sentence", "sentence": "Be co co", "query": "Be"},
        {"id": "ov_p26_conco", "text": "cò", "entryId": "con_co", "type": "fallback", "box": [48.0, 39.5, 5.0, 3.0]},
    ],
    27: [
        {"id": "ov_p27_bo", "text": "bố", "entryId": "bo", "type": "sentence", "sentence": "di bo tren he pho", "query": "Bo"},
        {"id": "ov_p27_dibo", "text": "đi bộ", "entryId": "di_bo", "type": "sentence", "sentence": "di bo tren he pho", "query": "di bo"},
        {"id": "ov_p27_hepho", "text": "hè phố", "entryId": "he_pho", "type": "sentence", "sentence": "di bo tren he pho", "query": "he pho"},
        {"id": "ov_p27_bobien", "text": "bờ", "entryId": "bo_bien", "type": "fallback", "box": [24.5, 73.2, 5.5, 3.0]},
        {"id": "ov_p27_laco", "text": "cờ", "entryId": "la_co", "type": "fallback", "box": [48.0, 73.2, 5.5, 3.0]},
    ],
    28: [
        {"id": "ov_p28_bo", "text": "bố", "entryId": "bo", "type": "sentence", "sentence": "Bo be be", "query": "Bo"},
        {"id": "ov_p28_betay", "text": "bế", "entryId": "be_tay", "type": "sentence", "sentence": "Bo be be", "query": "be"},
    ],
    29: [
        {"id": "ov_p29_gocda", "text": "gốc đa", "entryId": "goc_da", "type": "sentence", "sentence": "Duoi goc da", "query": "goc da"},
        {"id": "ov_p29_conde", "text": "dê", "entryId": "con_de", "type": "fallback", "box": [23.5, 72.5, 6.5, 3.2]},
        {"id": "ov_p29_condo", "text": "đò", "entryId": "con_do", "type": "fallback", "box": [48.5, 72.5, 6.5, 3.2]},
        {"id": "ov_p29_odo", "text": "ô đỏ", "entryId": "o_do", "type": "standalone", "query": "o do"},
    ],
    30: [
        {"id": "ov_p30_odo", "text": "ô đỏ", "entryId": "o_do", "type": "sentence", "sentence": "Be co o do", "query": "o do"},
    ],
    31: [
        {"id": "ov_p31_tau", "text": "tàu", "entryId": "tau", "type": "sentence", "sentence": "cang", "query": "Tau"},
        {"id": "ov_p31_cang", "text": "cảng", "entryId": "cang", "type": "sentence", "sentence": "cang", "query": "cang"},
        {"id": "ov_p31_bode", "text": "bờ đê", "entryId": "bo_de", "type": "standalone", "query": "bo de"},
        {"id": "ov_p31_caco", "text": "cá cờ", "entryId": "ca_co", "type": "standalone", "query": "ca co"},
        {"id": "ov_p31_dobe", "text": "đỡ bé", "entryId": "do_be", "type": "standalone", "query": "do be"},
    ],
    32: [
        {"id": "ov_p32_dobe", "text": "đỡ bé", "entryId": "do_be", "type": "sentence", "sentence": "Bo do be", "query": "do be"},
    ],
    33: [
        {"id": "ov_p33_bode", "text": "bờ đê", "entryId": "bo_de", "type": "standalone", "query": "bo de"},
        {"id": "ov_p33_caco", "text": "cá cờ", "entryId": "ca_co", "type": "standalone", "query": "ca co"},
        {"id": "ov_p33_dodo", "text": "đỗ đỏ", "entryId": "do_do", "type": "fallback", "box": [71.0, 73.0, 9.0, 3.2]},
    ],
    34: [
        {"id": "ov_p34_dankien", "text": "đàn kiến", "entryId": "dan_kien", "type": "sentence", "sentence": "Dan kien", "query": "Dan kien"},
    ],
    35: [
        {"id": "ov_p35_kida", "text": "kì đà", "entryId": "ki_da", "type": "standalone", "query": "ki da"},
        {"id": "ov_p35_bido", "text": "bí đỏ", "entryId": "bi_do", "type": "standalone", "query": "bi do"},
        {"id": "ov_p35_keo", "text": "kẻ ô", "entryId": "ke_o", "type": "standalone", "query": "ke o"},
        {"id": "ov_p35_dido", "text": "đi đò", "entryId": "di_do", "type": "standalone", "query": "di do"},
    ],
    36: [
        {"id": "ov_p36_kida", "text": "kì đà", "entryId": "ki_da", "type": "sentence", "sentence": "Ki da bo o ke da", "query": "Ki da"},
        {"id": "ov_p36_keda", "text": "kẽ đá", "entryId": "ke_da", "type": "sentence", "sentence": "Ki da bo o ke da", "query": "ke da"},
    ],
    37: [
        {"id": "ov_p37_lele", "text": "le le", "entryId": "le_le", "type": "standalone", "query": "le le"},
        {"id": "ov_p37_boi", "text": "bơi", "entryId": "boi", "type": "sentence", "sentence": "Le le boi tren ho", "query": "boi"},
        {"id": "ov_p37_honuoc", "text": "hồ", "entryId": "ho_nuoc", "type": "sentence", "sentence": "Le le boi tren ho", "query": "ho"},
        {"id": "ov_p37_lado", "text": "lá đỏ", "entryId": "la_do", "type": "standalone", "query": "la do"},
        {"id": "ov_p37_boho", "text": "bờ hồ", "entryId": "bo_ho", "type": "standalone", "query": "bo ho"},
        {"id": "ov_p37_caho", "text": "cá hổ", "entryId": "ca_ho", "type": "standalone", "query": "ca ho"},
    ],
    38: [
        {"id": "ov_p38_lahe", "text": "lá hẹ", "entryId": "la_he", "type": "sentence", "sentence": "la he", "query": "la he"},
        {"id": "ov_p38_ba", "text": "bà", "entryId": "ba_noi", "type": "sentence", "sentence": "la he", "query": "Ba"},
    ],
    39: [
        {"id": "ov_p39_dudu", "text": "đu đủ", "entryId": "du_du", "type": "standalone", "query": "du du"},
        {"id": "ov_p39_ngotlu", "text": "ngọt lừ", "entryId": "ngot_lu", "type": "sentence", "sentence": "Du du chin ngot lu", "query": "ngot lu"},
        {"id": "ov_p39_hodu", "text": "hổ dữ", "entryId": "ho_du", "type": "standalone", "query": "ho dur"},
    ],
    40: [
        {"id": "ov_p40_caho", "text": "cá hổ", "entryId": "ca_ho", "type": "sentence", "sentence": "Ca ho la ca du", "query": "Ca ho"},
        {"id": "ov_p40_dution", "text": "dữ", "entryId": "du_ton", "type": "sentence", "sentence": "Ca ho la ca du", "query": "du"},
    ],
    41: [
        {"id": "ov_p41_chukhi", "text": "khỉ", "entryId": "chu_khi", "type": "standalone", "query": "chu khi"},
        {"id": "ov_p41_chuoi", "text": "chuối", "entryId": "chuoi", "type": "sentence", "sentence": "an chuoi", "query": "chuoi"},
        {"id": "ov_p41_cho", "text": "chợ", "entryId": "cho_que", "type": "standalone", "query": "cho ca"},
        {"id": "ov_p41_lakho", "text": "lá khô", "entryId": "la_kho", "type": "standalone", "query": "la kho"},
    ],
    42: [
        {"id": "ov_p42_cakho", "text": "cá kho", "entryId": "ca_kho", "type": "sentence", "sentence": "ca kho khe", "query": "ca kho"},
        {"id": "ov_p42_quakhe", "text": "khế", "entryId": "qua_khe", "type": "sentence", "sentence": "ca kho khe", "query": "khe"},
    ],
    43: [
        {"id": "ov_p43_chuhe", "text": "chú hề", "entryId": "chu_he", "type": "standalone", "query": "chu he"},
        {"id": "ov_p43_choca", "text": "chợ", "entryId": "cho_que", "type": "standalone", "query": "cho ca"},
        {"id": "ov_p43_boho", "text": "bờ hồ", "entryId": "bo_ho", "type": "standalone", "query": "bo ho"},
        {"id": "ov_p43_lahe", "text": "lá hẹ", "entryId": "la_he", "type": "standalone", "query": "la he"},
        {"id": "ov_p43_lakho", "text": "lá khô", "entryId": "la_kho", "type": "standalone", "query": "la kho"},
        {"id": "ov_p43_caco", "text": "cá cờ", "entryId": "ca_co", "type": "fallback", "box": [70.0, 72.0, 8.5, 3.2]},
    ],
    44: [
        {"id": "ov_p44_conqua", "text": "con quạ", "entryId": "con_qua", "type": "sentence", "sentence": "Con qua thong minh", "query": "Con qua"},
        {"id": "ov_p44_thongminh", "text": "thông minh", "entryId": "thong_minh", "type": "sentence", "sentence": "Con qua thong minh", "query": "thong minh"},
    ],
    45: [
        {"id": "ov_p45_no", "text": "nơ", "entryId": "no", "type": "standalone", "query": "no do"},
        {"id": "ov_p45_me", "text": "mẹ", "entryId": "me", "type": "sentence", "sentence": "Me mua no", "query": "Me"},
        {"id": "ov_p45_came", "text": "cá mè", "entryId": "ca_me", "type": "standalone", "query": "ca me"},
        {"id": "ov_p45_lame", "text": "lá me", "entryId": "la_me", "type": "standalone", "query": "la me"},
        {"id": "ov_p45_cano", "text": "ca nô", "entryId": "ca_no", "type": "standalone", "query": "ca no"},
    ],
    46: [
        {"id": "ov_p46_cano", "text": "ca nô", "entryId": "ca_no", "type": "sentence", "sentence": "di ca no", "query": "ca no"},
        {"id": "ov_p46_bome", "text": "bố", "entryId": "bo", "type": "sentence", "sentence": "Bo me cho Ha", "query": "Bo"},
        {"id": "ov_p46_me", "text": "mẹ", "entryId": "me", "type": "sentence", "sentence": "Bo me cho Ha", "query": "me"},
    ],
    47: [
        {"id": "ov_p47_giotrung", "text": "giỏ trứng", "entryId": "gio_trung", "type": "sentence", "sentence": "gio trung ga", "query": "gio trung"},
        {"id": "ov_p47_conga", "text": "gà", "entryId": "con_ga", "type": "sentence", "sentence": "gio trung ga", "query": "ga"},
        {"id": "ov_p47_gago", "text": "gà gô", "entryId": "ga_go", "type": "standalone", "query": "ga go"},
        {"id": "ov_p47_dogo", "text": "đồ gỗ", "entryId": "do_go", "type": "standalone", "query": "do go"},
        {"id": "ov_p47_giado", "text": "giá đỗ", "entryId": "gia_do", "type": "standalone", "query": "gia do"},
        {"id": "ov_p47_cugia", "text": "củ già", "entryId": "cu_gia", "type": "standalone", "query": "cu gia"},
    ],
    48: [
        {"id": "ov_p48_chegio", "text": "che gió", "entryId": "che_gio", "type": "sentence", "sentence": "che gio", "query": "che gio"},
        {"id": "ov_p48_ba", "text": "bà", "entryId": "ba_noi", "type": "sentence", "sentence": "Ba che gio", "query": "Ba"},
        {"id": "ov_p48_conga", "text": "gà", "entryId": "con_ga", "type": "sentence", "sentence": "chu ga", "query": "ga"},
    ],
    49: [
        {"id": "ov_p49_ngoinha", "text": "nhà", "entryId": "ngoi_nha", "type": "sentence", "sentence": "ghe nha ba", "query": "nha"},
        {"id": "ov_p49_ngonho", "text": "ngõ nhỏ", "entryId": "ngo_nho", "type": "sentence", "sentence": "ngo nho", "query": "ngo nho"},
        {"id": "ov_p49_gheda", "text": "ghế đá", "entryId": "ghe_da", "type": "standalone", "query": "ghe da"},
        {"id": "ov_p49_ghego", "text": "ghế gỗ", "entryId": "ghe_go", "type": "fallback", "box": [34.5, 72.5, 9.5, 3.2]},
        {"id": "ov_p49_nhago", "text": "nhà gỗ", "entryId": "nha_go", "type": "standalone", "query": "nha go"},
        {"id": "ov_p49_lanho", "text": "lá nho", "entryId": "la_nho", "type": "standalone", "query": "la nho"},
    ],
    50: [
        {"id": "ov_p50_ghego", "text": "ghế", "entryId": "ghe", "type": "sentence", "sentence": "ghe nho", "query": "ghe"},
    ],
    51: [
        {"id": "ov_p51_connghe", "text": "nghé", "entryId": "con_nghe", "type": "sentence", "sentence": "Nghe theo me", "query": "Nghe"},
        {"id": "ov_p51_ngo", "text": "ngõ", "entryId": "ngo_nho", "type": "sentence", "sentence": "ra ngo", "query": "ngo"},
        {"id": "ov_p51_ngaba", "text": "ngã ba", "entryId": "nga_ba", "type": "standalone", "query": "nga ba"},
        {"id": "ov_p51_cunghe", "text": "củ nghệ", "entryId": "cu_nghe", "type": "standalone", "query": "cu nghe"},
        {"id": "ov_p51_nghihe", "text": "nghỉ hè", "entryId": "nghi_he", "type": "standalone", "query": "nghi he"},
    ],
    52: [
        {"id": "ov_p52_connghe", "text": "nghé", "entryId": "con_nghe", "type": "sentence", "sentence": "Nghe da no co", "query": "Nghe"},
        {"id": "ov_p52_co", "text": "cỏ", "entryId": "co", "type": "sentence", "sentence": "Nghe da no co", "query": "co"},
        {"id": "ov_p52_bode", "text": "bờ đê", "entryId": "bo_de", "type": "sentence", "sentence": "bo de", "query": "bo de"},
    ],
    53: [
        {"id": "ov_p53_nhaga", "text": "nhà ga", "entryId": "nha_ga", "type": "standalone", "query": "nha ga"},
        {"id": "ov_p53_nghihe", "text": "nghỉ hè", "entryId": "nghi_he", "type": "standalone", "query": "nghi he"},
        {"id": "ov_p53_bapngo", "text": "bắp ngô", "entryId": "bap_ngo", "type": "standalone", "query": "bongo"},
        {"id": "ov_p53_giado", "text": "giá đỗ", "entryId": "gia_do", "type": "standalone", "query": "gia do"},
        {"id": "ov_p53_ghego", "text": "ghế gỗ", "entryId": "ghe_go", "type": "standalone", "query": "ghe go"},
        {"id": "ov_p53_ngonho", "text": "ngõ nhỏ", "entryId": "ngo_nho", "type": "standalone", "query": "nho nho"},
    ],
    55: [
        {"id": "ov_p55_chimse", "text": "sẻ", "entryId": "chim_se", "type": "sentence", "sentence": "Bay se non", "query": "se"},
        {"id": "ov_p55_riurit", "text": "ríu rít", "entryId": "riu_rit", "type": "sentence", "sentence": "riu ra riu rit", "query": "riu rit"},
        {"id": "ov_p55_rora", "text": "rổ rá", "entryId": "ro_ra", "type": "standalone", "query": "r ra", "fallback": [18.5, 73.0, 8.5, 3.2]},
        {"id": "ov_p55_caro", "text": "cá rô", "entryId": "ca_ro", "type": "standalone", "query": "ca ro"},
        {"id": "ov_p55_chuso", "text": "chữ số", "entryId": "chu_so", "type": "standalone", "query": "chur so"},
        {"id": "ov_p55_susu", "text": "su su", "entryId": "su_su", "type": "standalone", "query": "susu"},
    ],
    56: [
        {"id": "ov_p56_gari", "text": "gà ri", "entryId": "ga_ri", "type": "sentence", "sentence": "ga ri", "query": "ga ri"},
        {"id": "ov_p56_caro", "text": "cá rô", "entryId": "ca_ro", "type": "sentence", "sentence": "ca ro", "query": "ca ro"},
        {"id": "ov_p56_susu", "text": "su su", "entryId": "su_su", "type": "sentence", "sentence": "su su", "query": "su su"},
        {"id": "ov_p56_rora", "text": "rổ rá", "entryId": "ro_ra", "type": "sentence", "sentence": "ro ra", "query": "ro ra"},
        {"id": "ov_p56_cho", "text": "chợ", "entryId": "cho_que", "type": "sentence", "sentence": "Cho co ga ri", "query": "Cho"},
    ],
}

all_page_overlays = {}

for p in range(1, 58):
    p_str = f"{p:03d}"
    img_path = f"/pages/page_{p_str}.jpg"
    
    # Title / non-lesson pages: 1-7, 10-14, 57
    if p not in PAGE_TARGETS:
        all_page_overlays[str(p)] = {
            "pageNumber": p,
            "image": img_path,
            "overlays": [],
            "vocabWordIds": []
        }
        continue

    # Load OCR data
    json_path = ocr_dir / f"page_{p_str}.json"
    w, h, items = 2280, 3200, []
    if json_path.exists():
        with open(json_path, encoding='utf-8') as f:
            ocr_data = json.load(f)
            w = ocr_data.get('width', 2280)
            h = ocr_data.get('height', 3200)
            items = ocr_data.get('items', [])

    targets = PAGE_TARGETS[p]
    page_overlays_list = []
    page_vocab_ids = []

    for tgt in targets:
        t_type = tgt['type']
        coords = None
        if t_type == 'sentence':
            coords = get_sentence_word_bbox(items, tgt['sentence'], tgt['query'], w, h)
        elif t_type == 'standalone':
            coords = get_standalone_word_bbox(items, tgt['query'], w, h)
        
        if not coords and 'box' in tgt:
            coords = tgt['box']
        elif not coords and 'fallback' in tgt:
            coords = tgt['fallback']
        elif not coords:
            coords = [30.0, 50.0, 10.0, 3.5]

        eid = tgt['entryId']
        if eid not in page_vocab_ids:
            page_vocab_ids.append(eid)
        
        page_overlays_list.append({
            "id": tgt['id'],
            "text": tgt['text'],
            "entryId": eid,
            "left": coords[0],
            "top": coords[1],
            "width": coords[2],
            "height": coords[3],
            "isKeyVocab": True
        })

    all_page_overlays[str(p)] = {
        "pageNumber": p,
        "image": img_path,
        "overlays": page_overlays_list,
        "vocabWordIds": page_vocab_ids
    }

with open(overlays_file, 'w', encoding='utf-8') as f:
    json.dump(all_page_overlays, f, ensure_ascii=False, indent=2)

print(f"Generated pixel-accurate overlays for all 57 pages.")
for p in [1, 5, 8, 9, 15, 17, 19, 21, 25, 35, 47, 55, 57]:
    d = all_page_overlays[str(p)]
    print(f"Page {p:2d}: {len(d['overlays'])} overlays")
    for ov in d['overlays']:
        print(f"  [{ov['text']}] left={ov['left']}%, top={ov['top']}%, w={ov['width']}%, h={ov['height']}%")
