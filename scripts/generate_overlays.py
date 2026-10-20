import json
import os

with open('src/data/entries.json', encoding='utf-8') as f:
    entries = json.load(f)

# Build a word to entryId lookup
word_lookup = {}
for entry_id, entry in entries.items():
    word_lookup[entry['wordVi'].lower()] = entry_id
    # Also individual words
    for w in entry['wordVi'].split():
        if len(w) > 1 and w.lower() not in word_lookup:
            word_lookup[w.lower()] = entry_id

page_overlays = {}

for p in range(1, 58):
    ocr_file = f'data/ocr/page_{p:03d}.json'
    overlays = []
    page_vocab_ids = set()

    if os.path.exists(ocr_file):
        with open(ocr_file, encoding='utf-8') as f:
            ocr_data = json.load(f)
            pw = ocr_data.get('width', 2280)
            ph = ocr_data.get('height', 3200)

            for idx, item in enumerate(ocr_data.get('items', [])):
                txt = item['text'].strip()
                bbox = item['bbox']
                xs = [pt[0] for pt in bbox]
                ys = [pt[1] for pt in bbox]
                left = round(min(xs) / pw * 100, 2)
                top = round(min(ys) / ph * 100, 2)
                width = round((max(xs) - min(xs)) / pw * 100, 2)
                height = round((max(ys) - min(ys)) / ph * 100, 2)

                # Check if this item or any substring matches an entry
                matched_entry_id = None
                clean_txt = txt.lower().replace('.', '').replace(',', '').replace('?', '').replace('!', '')
                
                # Direct match
                if clean_txt in word_lookup:
                    matched_entry_id = word_lookup[clean_txt]
                else:
                    # Substring match
                    for w, eid in word_lookup.items():
                        if w in clean_txt:
                            matched_entry_id = eid
                            break

                # Also match by page specific mappings for key sentences
                # If matched
                if matched_entry_id:
                    page_vocab_ids.add(matched_entry_id)
                    overlays.append({
                        "id": f"overlay_p{p}_{idx}",
                        "text": txt,
                        "entryId": matched_entry_id,
                        "left": left,
                        "top": top,
                        "width": width,
                        "height": height,
                        "isKeyVocab": True
                    })
                elif len(txt) >= 2 and not txt.isdigit() and "Trang" not in txt:
                    # Keep as general clickable reading overlay
                    overlays.append({
                        "id": f"overlay_p{p}_{idx}",
                        "text": txt,
                        "left": left,
                        "top": top,
                        "width": width,
                        "height": height,
                        "isKeyVocab": False
                    })

    # Ensure key vocabulary for this page is associated
    for entry_id, entry in entries.items():
        if p in entry.get('sourcePages', []):
            page_vocab_ids.add(entry_id)

    page_overlays[p] = {
        "pageNumber": p,
        "image": f"/pages/page_{p:03d}.jpg",
        "overlays": overlays,
        "vocabWordIds": list(page_vocab_ids)
    }

# Specific high precision overlays for key lesson pages to ensure perfect word-level clickability
MANUAL_KEY_OVERLAYS = {
    15: [
        {"id": "ov_p15_nam", "text": "Nam", "entryId": "nam", "left": 37.4, "top": 60.0, "width": 6.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p15_ha", "text": "Hà", "entryId": "ha", "left": 48.0, "top": 60.0, "width": 4.8, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p15_cahat", "text": "ca hát", "entryId": "ca_hat", "left": 53.5, "top": 60.0, "width": 11.2, "height": 2.6, "isKeyVocab": True},
    ],
    16: [
        {"id": "ov_p16_ba", "text": "ba", "entryId": "bo", "left": 15.0, "top": 55.0, "width": 8.0, "height": 3.0, "isKeyVocab": True}
    ],
    17: [
        {"id": "ov_p17_ba", "text": "Bà", "entryId": "ba_noi", "left": 36.5, "top": 59.8, "width": 5.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p17_be", "text": "bé", "entryId": "be", "left": 47.0, "top": 59.8, "width": 5.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p17_bupbe", "text": "búp bê", "entryId": "bup_be", "left": 53.0, "top": 59.8, "width": 12.0, "height": 2.6, "isKeyVocab": True},
    ],
    18: [
        {"id": "ov_p18_ba", "text": "ba", "entryId": "bo", "left": 15.0, "top": 55.0, "width": 8.0, "height": 3.0, "isKeyVocab": True}
    ],
    19: [
        {"id": "ov_p19_nam", "text": "Nam", "entryId": "nam", "left": 35.0, "top": 59.8, "width": 6.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p19_bo", "text": "bố", "entryId": "bo", "left": 46.5, "top": 59.8, "width": 5.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p19_cauca", "text": "câu cá", "entryId": "cau_ca", "left": 52.5, "top": 59.8, "width": 11.0, "height": 2.6, "isKeyVocab": True},
    ],
    20: [
        {"id": "ov_p20_ca", "text": "cá", "entryId": "ca", "left": 18.0, "top": 55.0, "width": 8.0, "height": 3.0, "isKeyVocab": True}
    ],
    21: [
        {"id": "ov_p21_be", "text": "Bé", "entryId": "be", "left": 28.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p21_me", "text": "mẹ", "entryId": "me", "left": 41.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p21_banbe", "text": "bạn bè", "entryId": "ban_be", "left": 60.0, "top": 59.8, "width": 11.5, "height": 2.6, "isKeyVocab": True},
    ],
    22: [
        {"id": "ov_p22_ba", "text": "Bà", "entryId": "ba_noi", "left": 14.5, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p22_bedt", "text": "bế", "entryId": "be_dong_tu", "left": 21.5, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p22_be", "text": "bé", "entryId": "be", "left": 28.0, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
    ],
    25: [
        {"id": "ov_p25_bo", "text": "bò", "entryId": "con_bo", "left": 44.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p25_gamco", "text": "gặm cỏ", "entryId": "gam_co", "left": 51.0, "top": 59.8, "width": 12.0, "height": 2.6, "isKeyVocab": True},
    ],
    26: [
        {"id": "ov_p26_be", "text": "Bé", "entryId": "be", "left": 14.5, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p26_co", "text": "cỏ", "entryId": "co", "left": 28.0, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
    ],
    27: [
        {"id": "ov_p27_bo", "text": "Bố", "entryId": "bo", "left": 26.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p27_ha", "text": "Hà", "entryId": "ha", "left": 37.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p27_dibo", "text": "đi bộ", "entryId": "di_bo", "left": 43.5, "top": 59.8, "width": 8.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p27_hepho", "text": "hè phố", "entryId": "he_pho", "left": 58.0, "top": 59.8, "width": 11.0, "height": 2.6, "isKeyVocab": True},
    ],
    29: [
        {"id": "ov_p29_banbe", "text": "bạn", "entryId": "ban_be", "left": 47.0, "top": 59.8, "width": 6.0, "height": 2.6, "isKeyVocab": True},
    ],
    30: [
        {"id": "ov_p30_be", "text": "Bé", "entryId": "be", "left": 14.5, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p30_odo", "text": "ô đỏ", "entryId": "o_do", "left": 27.0, "top": 55.0, "width": 9.0, "height": 2.8, "isKeyVocab": True},
    ],
    31: [
        {"id": "ov_p31_dobe", "text": "đỡ bé", "entryId": "do_be", "left": 52.0, "top": 76.0, "width": 10.0, "height": 2.8, "isKeyVocab": True},
    ],
    32: [
        {"id": "ov_p32_bo", "text": "Bố", "entryId": "bo", "left": 14.5, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p32_dobe", "text": "đỡ bé", "entryId": "do_be", "left": 21.0, "top": 55.0, "width": 11.0, "height": 2.8, "isKeyVocab": True},
    ],
    35: [
        {"id": "ov_p35_nam", "text": "Nam", "entryId": "nam", "left": 38.0, "top": 59.8, "width": 6.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p35_kida", "text": "kì đà", "entryId": "ki_da", "left": 51.0, "top": 59.8, "width": 9.5, "height": 2.6, "isKeyVocab": True},
    ],
    36: [
        {"id": "ov_p36_kida", "text": "Kì đà", "entryId": "ki_da", "left": 14.5, "top": 55.0, "width": 10.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p36_keda", "text": "kẽ đá", "entryId": "ke_da", "left": 35.0, "top": 55.0, "width": 9.0, "height": 2.8, "isKeyVocab": True},
    ],
    37: [
        {"id": "ov_p37_lele", "text": "Le le", "entryId": "le_le", "left": 36.0, "top": 59.8, "width": 9.0, "height": 2.6, "isKeyVocab": True},
    ],
    38: [
        {"id": "ov_p38_be", "text": "Bé", "entryId": "be", "left": 14.5, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p38_ba", "text": "Bà", "entryId": "ba_noi", "left": 32.0, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p38_lahe", "text": "lá hẹ", "entryId": "la_he", "left": 48.0, "top": 55.0, "width": 9.0, "height": 2.8, "isKeyVocab": True},
    ],
    39: [
        {"id": "ov_p39_dudu", "text": "Đu đủ", "entryId": "du_du", "left": 34.0, "top": 59.8, "width": 9.5, "height": 2.6, "isKeyVocab": True},
    ],
    40: [
        {"id": "ov_p40_caho", "text": "Cá hổ", "entryId": "ca_ho", "left": 14.5, "top": 55.0, "width": 9.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p40_cadu", "text": "cá dữ", "entryId": "hung_du", "left": 32.0, "top": 55.0, "width": 9.0, "height": 2.8, "isKeyVocab": True},
    ],
    41: [
        {"id": "ov_p41_khi", "text": "khỉ", "entryId": "con_khi", "left": 46.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p41_chuoi", "text": "chuối", "entryId": "chuoi", "left": 58.0, "top": 59.8, "width": 9.0, "height": 2.6, "isKeyVocab": True},
    ],
    42: [
        {"id": "ov_p42_cakho", "text": "cá kho", "entryId": "ca_kho", "left": 28.0, "top": 55.0, "width": 10.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p42_khe", "text": "khế", "entryId": "khe", "left": 39.5, "top": 55.0, "width": 6.5, "height": 2.8, "isKeyVocab": True},
    ],
    45: [
        {"id": "ov_p45_me", "text": "Mẹ", "entryId": "me", "left": 36.0, "top": 59.8, "width": 6.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p45_no", "text": "nơ", "entryId": "no_do", "left": 49.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p45_ha", "text": "Hà", "entryId": "ha", "left": 61.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
    ],
    46: [
        {"id": "ov_p46_bome", "text": "Bố", "entryId": "bo", "left": 14.5, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p46_me", "text": "mẹ", "entryId": "me", "left": 20.5, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p46_ha", "text": "Hà", "entryId": "ha", "left": 33.0, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p46_cano", "text": "ca nô", "entryId": "ca_no", "left": 43.0, "top": 55.0, "width": 9.5, "height": 2.8, "isKeyVocab": True},
    ],
    47: [
        {"id": "ov_p47_ha", "text": "Hà", "entryId": "ha", "left": 36.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p47_giotrung", "text": "giỏ trứng", "entryId": "gio_trung", "left": 47.0, "top": 59.8, "width": 14.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p47_ga", "text": "gà", "entryId": "con_ga", "left": 62.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
    ],
    48: [
        {"id": "ov_p48_ba", "text": "Bà", "entryId": "ba_noi", "left": 14.5, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p48_chegio", "text": "che gió", "entryId": "che_gio", "left": 21.0, "top": 55.0, "width": 11.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p48_ga", "text": "gà", "entryId": "con_ga", "left": 50.0, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
    ],
    49: [
        {"id": "ov_p49_ha", "text": "Hà", "entryId": "ha", "left": 26.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p49_nhaba", "text": "nhà", "entryId": "nha_ba", "left": 38.0, "top": 59.8, "width": 6.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p49_ba", "text": "bà", "entryId": "ba_noi", "left": 45.0, "top": 59.8, "width": 5.5, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p49_ngonho", "text": "ngõ nhỏ", "entryId": "ngo_nho", "left": 65.0, "top": 59.8, "width": 12.0, "height": 2.6, "isKeyVocab": True},
    ],
    50: [
        {"id": "ov_p50_me", "text": "Mẹ", "entryId": "me", "left": 14.5, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p50_ha", "text": "Hà", "entryId": "ha", "left": 28.0, "top": 55.0, "width": 6.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p50_ghenho", "text": "ghế", "entryId": "ghe_nho", "left": 39.0, "top": 55.0, "width": 6.5, "height": 2.8, "isKeyVocab": True},
    ],
    51: [
        {"id": "ov_p51_nghe", "text": "Nghé", "entryId": "con_nghe", "left": 34.0, "top": 59.8, "width": 9.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p51_me", "text": "mẹ", "entryId": "me", "left": 51.0, "top": 59.8, "width": 6.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p51_ngo", "text": "ngõ", "entryId": "ngo_nho", "left": 63.0, "top": 59.8, "width": 6.0, "height": 2.6, "isKeyVocab": True},
    ],
    52: [
        {"id": "ov_p52_nghe1", "text": "Nghé", "entryId": "con_nghe", "left": 14.5, "top": 55.0, "width": 8.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p52_co", "text": "cỏ", "entryId": "co", "left": 30.5, "top": 55.0, "width": 5.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p52_nghe2", "text": "Nghé", "entryId": "con_nghe", "left": 38.0, "top": 55.0, "width": 8.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p52_bode", "text": "bờ đê", "entryId": "bo_de", "left": 55.0, "top": 55.0, "width": 9.5, "height": 2.8, "isKeyVocab": True},
    ],
    55: [
        {"id": "ov_p55_se", "text": "sẻ", "entryId": "chim_se", "left": 41.0, "top": 59.8, "width": 5.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p55_riurit", "text": "ríu ra ríu rít", "entryId": "riu_rit", "left": 52.0, "top": 59.8, "width": 16.0, "height": 2.6, "isKeyVocab": True},
        {"id": "ov_p55_me", "text": "mẹ", "entryId": "me", "left": 74.0, "top": 59.8, "width": 6.0, "height": 2.6, "isKeyVocab": True},
    ],
    56: [
        {"id": "ov_p56_cho1", "text": "Chợ", "entryId": "cho_que", "left": 14.5, "top": 55.0, "width": 6.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p56_ga", "text": "gà", "entryId": "con_ga", "left": 26.5, "top": 55.0, "width": 5.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p56_caro", "text": "cá rô", "entryId": "ca_ro", "left": 37.0, "top": 55.0, "width": 8.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p56_susu", "text": "su su", "entryId": "su_su", "left": 48.0, "top": 55.0, "width": 8.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p56_cho2", "text": "Chợ", "entryId": "cho_que", "left": 58.5, "top": 55.0, "width": 6.5, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p56_rora", "text": "rổ rá", "entryId": "ro_ra", "left": 72.0, "top": 55.0, "width": 8.5, "height": 2.8, "isKeyVocab": True},
    ]
}

# Merge manual key overlays
for p, manual_list in MANUAL_KEY_OVERLAYS.items():
    if p in page_overlays:
        # Prepend manual key overlays
        existing = page_overlays[p]['overlays']
        # remove overlaps or duplicates
        page_overlays[p]['overlays'] = manual_list + existing
        for item in manual_list:
            if item.get('entryId'):
                page_overlays[p]['vocabWordIds'].append(item['entryId'])
        page_overlays[p]['vocabWordIds'] = list(set(page_overlays[p]['vocabWordIds']))

with open('src/data/page_overlays.json', 'w', encoding='utf-8') as f:
    json.dump(page_overlays, f, ensure_ascii=False, indent=2)

print('Generated src/data/page_overlays.json for all 57 pages.')
