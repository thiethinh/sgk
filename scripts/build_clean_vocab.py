import json
import os
import asyncio
import edge_tts

os.makedirs('src/data', exist_ok=True)
os.makedirs('public/audio/vi', exist_ok=True)
os.makedirs('public/audio/en/us', exist_ok=True)

# 1. Clean Dictionary of REAL meaningful words only (NO phonics, NO headings, NO names)
CLEAN_DICTIONARY = {
    "ca_hat": {
        "id": "ca_hat",
        "wordVi": "ca hát",
        "meaningVi": "Hát vang lên những giai điệu vui tươi, rộn ràng.",
        "meaningsEn": [{"meaning": "sing", "ipa": "/sɪŋ/", "partOfSpeech": "verb"}],
        "ipa": "/sɪŋ/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/ca_hat.mp3",
        "audioEn": "/audio/en/us/ca_hat.mp3",
        "sourcePages": [15]
    },
    "bo": {
        "id": "bo",
        "wordVi": "bố",
        "meaningVi": "Người đàn ông sinh thành, che chở và yêu thương con.",
        "meaningsEn": [
            {"meaning": "father", "ipa": "/ˈfɑːðər/", "partOfSpeech": "noun"},
            {"meaning": "dad", "ipa": "/dæd/", "partOfSpeech": "noun"}
        ],
        "ipa": "/ˈfɑːðər/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/bo.mp3",
        "audioEn": "/audio/en/us/bo.mp3",
        "sourcePages": [16, 18, 19, 27, 28, 32, 46]
    },
    "ba_noi": {
        "id": "ba_noi",
        "wordVi": "bà",
        "meaningVi": "Người phụ nữ lớn tuổi, là mẹ của bố hoặc mẹ, luôn thương yêu cháu.",
        "meaningsEn": [
            {"meaning": "grandmother", "ipa": "/ˈɡrænmʌðər/", "partOfSpeech": "noun"},
            {"meaning": "grandma", "ipa": "/ˈɡrænmɑː/", "partOfSpeech": "noun"}
        ],
        "ipa": "/ˈɡrænmʌðər/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ba_noi.mp3",
        "audioEn": "/audio/en/us/ba_noi.mp3",
        "sourcePages": [17, 22, 23, 33, 38, 48, 49, 53]
    },
    "be": {
        "id": "be",
        "wordVi": "bé",
        "meaningVi": "Em bé nhỏ tuổi, xinh xắn và đáng yêu.",
        "meaningsEn": [
            {"meaning": "baby", "ipa": "/ˈbeɪbi/", "partOfSpeech": "noun"},
            {"meaning": "little child", "ipa": "/ˈlɪtl tʃaɪld/", "partOfSpeech": "noun"}
        ],
        "ipa": "/ˈbeɪbi/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/be.mp3",
        "audioEn": "/audio/en/us/be.mp3",
        "sourcePages": [17, 21, 22, 26, 28, 30, 32, 38, 43]
    },
    "bup_be": {
        "id": "bup_be",
        "wordVi": "búp bê",
        "meaningVi": "Đồ chơi hình người nhỏ nhắn, xinh xắn của các bé.",
        "meaningsEn": [{"meaning": "doll", "ipa": "/dɑːl/", "partOfSpeech": "noun"}],
        "ipa": "/dɑːl/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/bup_be.mp3",
        "audioEn": "/audio/en/us/bup_be.mp3",
        "sourcePages": [17, 24]
    },
    "cau_ca": {
        "id": "cau_ca",
        "wordVi": "câu cá",
        "meaningVi": "Dùng cần câu có mồi để bắt cá dưới nước.",
        "meaningsEn": [{"meaning": "go fishing", "ipa": "/ɡoʊ ˈfɪʃɪŋ/", "partOfSpeech": "phrase"}],
        "ipa": "/ɡoʊ ˈfɪʃɪŋ/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/cau_ca.mp3",
        "audioEn": "/audio/en/us/cau_ca.mp3",
        "sourcePages": [19]
    },
    "ca": {
        "id": "ca",
        "wordVi": "cá",
        "meaningVi": "Con vật sống dưới nước, bơi bằng vây và thở bằng mang.",
        "meaningsEn": [{"meaning": "fish", "ipa": "/fɪʃ/", "partOfSpeech": "noun"}],
        "ipa": "/fɪʃ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ca.mp3",
        "audioEn": "/audio/en/us/ca.mp3",
        "sourcePages": [19, 20, 40, 42]
    },
    "co_do": {
        "id": "co_do",
        "wordVi": "cờ",
        "meaningVi": "Lá cờ đỏ sao vàng hoặc cờ hiệu tung bay trong gió.",
        "meaningsEn": [{"meaning": "flag", "ipa": "/flæɡ/", "partOfSpeech": "noun"}],
        "ipa": "/flæɡ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/co_do.mp3",
        "audioEn": "/audio/en/us/co_do.mp3",
        "sourcePages": [19, 27, 43]
    },
    "me": {
        "id": "me",
        "wordVi": "mẹ",
        "meaningVi": "Người phụ nữ sinh thành, chăm lo và nuôi nấng con.",
        "meaningsEn": [
            {"meaning": "mother", "ipa": "/ˈmʌðər/", "partOfSpeech": "noun"},
            {"meaning": "mom", "ipa": "/mɑːm/", "partOfSpeech": "noun"}
        ],
        "ipa": "/ˈmʌðər/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/me.mp3",
        "audioEn": "/audio/en/us/me.mp3",
        "sourcePages": [21, 45, 46, 50, 51, 53, 55]
    },
    "be_dong_tu": {
        "id": "be_dong_tu",
        "wordVi": "bế",
        "meaningVi": "Dùng hai tay ôm đỡ em bé vào lòng mình.",
        "meaningsEn": [{"meaning": "carry in arms", "ipa": "/ˈkæri ɪn ɑːrmz/", "partOfSpeech": "verb"}],
        "ipa": "/ˈkæri/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/be_dong_tu.mp3",
        "audioEn": "/audio/en/us/be_dong_tu.mp3",
        "sourcePages": [21, 22, 28]
    },
    "ban_be": {
        "id": "ban_be",
        "wordVi": "bạn bè",
        "meaningVi": "Những người bạn cùng học, cùng chơi thân thiết với nhau.",
        "meaningsEn": [{"meaning": "friends", "ipa": "/frendz/", "partOfSpeech": "noun"}],
        "ipa": "/frendz/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ban_be.mp3",
        "audioEn": "/audio/en/us/ban_be.mp3",
        "sourcePages": [8, 21, 29]
    },
    "de_men": {
        "id": "de_men",
        "wordVi": "dế mèn",
        "meaningVi": "Con côn trùng nhỏ màu nâu, gáy tiếng 'ri ri' vui tai.",
        "meaningsEn": [{"meaning": "cricket", "ipa": "/ˈkrɪkɪt/", "partOfSpeech": "noun"}],
        "ipa": "/ˈkrɪkɪt/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/de_men.mp3",
        "audioEn": "/audio/en/us/de_men.mp3",
        "sourcePages": [24, 33]
    },
    "con_bo": {
        "id": "con_bo",
        "wordVi": "bò",
        "meaningVi": "Loài vật nuôi bốn chân ăn cỏ, hiền lành và cho sữa.",
        "meaningsEn": [{"meaning": "cow", "ipa": "/kaʊ/", "partOfSpeech": "noun"}],
        "ipa": "/kaʊ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/con_bo.mp3",
        "audioEn": "/audio/en/us/con_bo.mp3",
        "sourcePages": [25]
    },
    "gam_co": {
        "id": "gam_co",
        "wordVi": "gặm cỏ",
        "meaningVi": "Động tác bò, dê dùng răng nhai cắn từng cụm cỏ non.",
        "meaningsEn": [{"meaning": "graze", "ipa": "/ɡreɪz/", "partOfSpeech": "verb"}],
        "ipa": "/ɡreɪz/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/gam_co.mp3",
        "audioEn": "/audio/en/us/gam_co.mp3",
        "sourcePages": [25]
    },
    "co": {
        "id": "co",
        "wordVi": "cỏ",
        "meaningVi": "Cây nhỏ thân mềm mọc thành thảm xanh trên mặt đất.",
        "meaningsEn": [{"meaning": "grass", "ipa": "/ɡræs/", "partOfSpeech": "noun"}],
        "ipa": "/ɡræs/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/co.mp3",
        "audioEn": "/audio/en/us/co.mp3",
        "sourcePages": [25, 26, 52]
    },
    "di_bo": {
        "id": "di_bo",
        "wordVi": "đi bộ",
        "meaningVi": "Di chuyển từng bước chân trên đường đi.",
        "meaningsEn": [{"meaning": "walk", "ipa": "/wɔːk/", "partOfSpeech": "verb"}],
        "ipa": "/wɔːk/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/di_bo.mp3",
        "audioEn": "/audio/en/us/di_bo.mp3",
        "sourcePages": [27]
    },
    "he_pho": {
        "id": "he_pho",
        "wordVi": "hè phố",
        "meaningVi": "Phần lề đường dành riêng cho người đi bộ trên phố.",
        "meaningsEn": [{"meaning": "sidewalk", "ipa": "/ˈsaɪdwɔːk/", "partOfSpeech": "noun"}],
        "ipa": "/ˈsaɪdwɔːk/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/he_pho.mp3",
        "audioEn": "/audio/en/us/he_pho.mp3",
        "sourcePages": [27]
    },
    "goc_da": {
        "id": "goc_da",
        "wordVi": "gốc đa",
        "meaningVi": "Phần dưới cùng của cây đa cổ thụ râm mát nơi đầu làng.",
        "meaningsEn": [{"meaning": "banyan tree base", "ipa": "/ˈbænjən triː beɪs/", "partOfSpeech": "noun"}],
        "ipa": "/ˈbænjən triː/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/goc_da.mp3",
        "audioEn": "/audio/en/us/goc_da.mp3",
        "sourcePages": [29]
    },
    "o_do": {
        "id": "o_do",
        "wordVi": "ô đỏ",
        "meaningVi": "Cái ô (dù) màu đỏ tươi dùng che mưa nắng.",
        "meaningsEn": [{"meaning": "red umbrella", "ipa": "/red ʌmˈbrelə/", "partOfSpeech": "noun phrase"}],
        "ipa": "/red ʌmˈbrelə/",
        "partOfSpeech": "cụm danh từ",
        "audioVi": "/audio/vi/o_do.mp3",
        "audioEn": "/audio/en/us/o_do.mp3",
        "sourcePages": [29, 30]
    },
    "tau_thuy": {
        "id": "tau_thuy",
        "wordVi": "tàu",
        "meaningVi": "Phương tiện giao thông to lớn chạy trên mặt nước.",
        "meaningsEn": [{"meaning": "ship", "ipa": "/ʃɪp/", "partOfSpeech": "noun"}],
        "ipa": "/ʃɪp/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/tau_thuy.mp3",
        "audioEn": "/audio/en/us/tau_thuy.mp3",
        "sourcePages": [31]
    },
    "cang_bien": {
        "id": "cang_bien",
        "wordVi": "cảng",
        "meaningVi": "Nơi tàu thuyền neo đậu để bốc dỡ hàng hóa.",
        "meaningsEn": [{"meaning": "port / harbor", "ipa": "/pɔːrt/", "partOfSpeech": "noun"}],
        "ipa": "/pɔːrt/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/cang_bien.mp3",
        "audioEn": "/audio/en/us/cang_bien.mp3",
        "sourcePages": [31]
    },
    "bo_de": {
        "id": "bo_de",
        "wordVi": "bờ đê",
        "meaningVi": "Dải đất cao ven sông để ngăn nước lũ tràn vào làng xóm.",
        "meaningsEn": [{"meaning": "dike embankment", "ipa": "/daɪk ɪmˈbæŋkmənt/", "partOfSpeech": "noun phrase"}],
        "ipa": "/daɪk/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/bo_de.mp3",
        "audioEn": "/audio/en/us/bo_de.mp3",
        "sourcePages": [31, 33, 52]
    },
    "do_be": {
        "id": "do_be",
        "wordVi": "đỡ bé",
        "meaningVi": "Dùng tay nâng hoặc giữ bé để bé không bị ngã.",
        "meaningsEn": [{"meaning": "support child", "ipa": "/səˈpɔːrt tʃaɪld/", "partOfSpeech": "verb phrase"}],
        "ipa": "/səˈpɔːrt/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/do_be.mp3",
        "audioEn": "/audio/en/us/do_be.mp3",
        "sourcePages": [31, 32]
    },
    "do_do": {
        "id": "do_do",
        "wordVi": "đỗ đỏ",
        "meaningVi": "Loại hạt đậu màu đỏ, dùng để nấu chè thơm ngon bổ dưỡng.",
        "meaningsEn": [{"meaning": "red beans", "ipa": "/red biːnz/", "partOfSpeech": "noun"}],
        "ipa": "/red biːnz/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/do_do.mp3",
        "audioEn": "/audio/en/us/do_do.mp3",
        "sourcePages": [33]
    },
    "dan_kien": {
        "id": "dan_kien",
        "wordVi": "đàn kiến",
        "meaningVi": "Nhiều con kiến nhỏ bé cùng làm việc chăm chỉ, đoàn kết.",
        "meaningsEn": [{"meaning": "colony of ants", "ipa": "/ˈkɑːləni əv ænts/", "partOfSpeech": "noun phrase"}],
        "ipa": "/ænts/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/dan_kien.mp3",
        "audioEn": "/audio/en/us/dan_kien.mp3",
        "sourcePages": [34]
    },
    "ki_da": {
        "id": "ki_da",
        "wordVi": "kì đà",
        "meaningVi": "Loài bò sát lớn có vảy giống thằn lằn, biết bơi và leo trèo.",
        "meaningsEn": [{"meaning": "monitor lizard", "ipa": "/ˈmɑːnɪtər ˈlɪzərd/", "partOfSpeech": "noun"}],
        "ipa": "/ˈmɑːnɪtər ˈlɪzərd/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ki_da.mp3",
        "audioEn": "/audio/en/us/ki_da.mp3",
        "sourcePages": [35, 36]
    },
    "ke_da": {
        "id": "ke_da",
        "wordVi": "kẽ đá",
        "meaningVi": "Khe hở hẹp ở giữa các tảng đá.",
        "meaningsEn": [{"meaning": "rock crevice", "ipa": "/rɑːk ˈkrevɪs/", "partOfSpeech": "noun"}],
        "ipa": "/ˈkrevɪs/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ke_da.mp3",
        "audioEn": "/audio/en/us/ke_da.mp3",
        "sourcePages": [36]
    },
    "le_le": {
        "id": "le_le",
        "wordVi": "le le",
        "meaningVi": "Loài vịt trời hoang dã nhỏ, bơi lội và lặn rất giỏi trên mặt nước.",
        "meaningsEn": [{"meaning": "whistling duck", "ipa": "/ˈwɪslɪŋ dʌk/", "partOfSpeech": "noun"}],
        "ipa": "/ˈwɪslɪŋ dʌk/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/le_le.mp3",
        "audioEn": "/audio/en/us/le_le.mp3",
        "sourcePages": [37]
    },
    "boi_loi": {
        "id": "boi_loi",
        "wordVi": "bơi",
        "meaningVi": "Di chuyển trên hoặc trong nước bằng vây hoặc chân tay.",
        "meaningsEn": [{"meaning": "swim", "ipa": "/swɪm/", "partOfSpeech": "verb"}],
        "ipa": "/swɪm/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/boi_loi.mp3",
        "audioEn": "/audio/en/us/boi_loi.mp3",
        "sourcePages": [37]
    },
    "mat_ho": {
        "id": "mat_ho",
        "wordVi": "hồ",
        "meaningVi": "Vùng nước ngọt rộng lớn và phẳng lặng.",
        "meaningsEn": [{"meaning": "lake", "ipa": "/leɪk/", "partOfSpeech": "noun"}],
        "ipa": "/leɪk/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/mat_ho.mp3",
        "audioEn": "/audio/en/us/mat_ho.mp3",
        "sourcePages": [37, 43]
    },
    "la_he": {
        "id": "la_he",
        "wordVi": "lá hẹ",
        "meaningVi": "Lá cây hẹ xanh, có vị thơm nồng, dùng chữa ho cho bé.",
        "meaningsEn": [{"meaning": "chive leaves", "ipa": "/tʃaɪv liːvz/", "partOfSpeech": "noun"}],
        "ipa": "/tʃaɪvz/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/la_he.mp3",
        "audioEn": "/audio/en/us/la_he.mp3",
        "sourcePages": [38, 43]
    },
    "du_du": {
        "id": "du_du",
        "wordVi": "đu đủ",
        "meaningVi": "Quả khi chín ruột màu vàng cam, ngọt mát và bổ dưỡng.",
        "meaningsEn": [{"meaning": "papaya", "ipa": "/pəˈpaɪə/", "partOfSpeech": "noun"}],
        "ipa": "/pəˈpaɪə/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/du_du.mp3",
        "audioEn": "/audio/en/us/du_du.mp3",
        "sourcePages": [39]
    },
    "ngot_lu": {
        "id": "ngot_lu",
        "wordVi": "ngọt lừ",
        "meaningVi": "Vị ngọt đậm đà, rất ngon lành.",
        "meaningsEn": [{"meaning": "very sweet", "ipa": "/ˈveri swiːt/", "partOfSpeech": "adjective"}],
        "ipa": "/swiːt/",
        "partOfSpeech": "tính từ",
        "audioVi": "/audio/vi/ngot_lu.mp3",
        "audioEn": "/audio/en/us/ngot_lu.mp3",
        "sourcePages": [39]
    },
    "ca_ho": {
        "id": "ca_ho",
        "wordVi": "cá hổ",
        "meaningVi": "Loài cá săn mồi có hàm răng sắc bén.",
        "meaningsEn": [{"meaning": "tigerfish", "ipa": "/ˈtaɪɡər fɪʃ/", "partOfSpeech": "noun"}],
        "ipa": "/ˈtaɪɡər fɪʃ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ca_ho.mp3",
        "audioEn": "/audio/en/us/ca_ho.mp3",
        "sourcePages": [40]
    },
    "hung_du": {
        "id": "hung_du",
        "wordVi": "dữ",
        "meaningVi": "Tính cách hung hăng, có thể cắn hay tấn công con vật khác.",
        "meaningsEn": [{"meaning": "fierce", "ipa": "/fɪrs/", "partOfSpeech": "adjective"}],
        "ipa": "/fɪrs/",
        "partOfSpeech": "tính từ",
        "audioVi": "/audio/vi/hung_du.mp3",
        "audioEn": "/audio/en/us/hung_du.mp3",
        "sourcePages": [40, 43]
    },
    "con_khi": {
        "id": "con_khi",
        "wordVi": "khỉ",
        "meaningVi": "Loài vật thông minh, leo trèo giỏi và thích ăn quả chuối.",
        "meaningsEn": [{"meaning": "monkey", "ipa": "/ˈmʌŋki/", "partOfSpeech": "noun"}],
        "ipa": "/ˈmʌŋki/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/con_khi.mp3",
        "audioEn": "/audio/en/us/con_khi.mp3",
        "sourcePages": [41]
    },
    "chuoi": {
        "id": "chuoi",
        "wordVi": "chuối",
        "meaningVi": "Quả dài cong cong, khi chín vỏ màu vàng thơm ngọt.",
        "meaningsEn": [{"meaning": "banana", "ipa": "/bəˈnænə/", "partOfSpeech": "noun"}],
        "ipa": "/bəˈnænə/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/chuoi.mp3",
        "audioEn": "/audio/en/us/chuoi.mp3",
        "sourcePages": [41]
    },
    "ca_kho": {
        "id": "ca_kho",
        "wordVi": "cá kho",
        "meaningVi": "Món ăn ngon từ cá nấu đậm vị thơm lừng.",
        "meaningsEn": [{"meaning": "braised fish", "ipa": "/breɪzd fɪʃ/", "partOfSpeech": "noun phrase"}],
        "ipa": "/breɪzd fɪʃ/",
        "partOfSpeech": "cụm danh từ",
        "audioVi": "/audio/vi/ca_kho.mp3",
        "audioEn": "/audio/en/us/ca_kho.mp3",
        "sourcePages": [42, 44]
    },
    "khe": {
        "id": "khe",
        "wordVi": "khế",
        "meaningVi": "Quả có 5 múi hình ngôi sao, vị chua thanh hoặc ngọt.",
        "meaningsEn": [{"meaning": "starfruit", "ipa": "/ˈstɑːrfruːt/", "partOfSpeech": "noun"}],
        "ipa": "/ˈstɑːrfruːt/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/khe.mp3",
        "audioEn": "/audio/en/us/khe.mp3",
        "sourcePages": [42, 44]
    },
    "con_qua": {
        "id": "con_qua",
        "wordVi": "con quạ",
        "meaningVi": "Loài chim có bộ lông đen tuyền, rất nhanh trí và thông minh.",
        "meaningsEn": [{"meaning": "crow", "ipa": "/kroʊ/", "partOfSpeech": "noun"}],
        "ipa": "/kroʊ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/con_qua.mp3",
        "audioEn": "/audio/en/us/con_qua.mp3",
        "sourcePages": [44]
    },
    "thong_minh": {
        "id": "thong_minh",
        "wordVi": "thông minh",
        "meaningVi": "Nhanh trí, khéo léo tìm ra cách giải quyết khó khăn.",
        "meaningsEn": [
            {"meaning": "smart", "ipa": "/smɑːrt/", "partOfSpeech": "adjective"},
            {"meaning": "clever", "ipa": "/ˈklevər/", "partOfSpeech": "adjective"}
        ],
        "ipa": "/smɑːrt/",
        "partOfSpeech": "tính từ",
        "audioVi": "/audio/vi/thong_minh.mp3",
        "audioEn": "/audio/en/us/thong_minh.mp3",
        "sourcePages": [44]
    },
    "no_do": {
        "id": "no_do",
        "wordVi": "nơ",
        "meaningVi": "Dải vải thắt hình cánh bướm cài lên tóc hoặc cổ áo xinh xắn.",
        "meaningsEn": [{"meaning": "ribbon bow", "ipa": "/ˈrɪbən boʊ/", "partOfSpeech": "noun"}],
        "ipa": "/boʊ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/no_do.mp3",
        "audioEn": "/audio/en/us/no_do.mp3",
        "sourcePages": [45]
    },
    "ca_no": {
        "id": "ca_no",
        "wordVi": "ca nô",
        "meaningVi": "Thuyền máy cỡ nhỏ lướt sóng nhanh trên sông, hồ.",
        "meaningsEn": [{"meaning": "motorboat / canoe", "ipa": "/ˈmoʊtərbəʊt/", "partOfSpeech": "noun"}],
        "ipa": "/ˈmoʊtərbəʊt/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ca_no.mp3",
        "audioEn": "/audio/en/us/ca_no.mp3",
        "sourcePages": [46]
    },
    "gio_trung": {
        "id": "gio_trung",
        "wordVi": "giỏ trứng",
        "meaningVi": "Cái giỏ nhỏ đan bằng tre dùng để đựng trứng gà.",
        "meaningsEn": [{"meaning": "egg basket", "ipa": "/eɡ ˈbæskɪt/", "partOfSpeech": "noun phrase"}],
        "ipa": "/ˈbæskɪt/",
        "partOfSpeech": "cụm danh từ",
        "audioVi": "/audio/vi/gio_trung.mp3",
        "audioEn": "/audio/en/us/gio_trung.mp3",
        "sourcePages": [47]
    },
    "con_ga": {
        "id": "con_ga",
        "wordVi": "gà",
        "meaningVi": "Loài gia cầm quen thuộc gáy te te báo trời sáng, gà mái đẻ trứng.",
        "meaningsEn": [{"meaning": "chicken", "ipa": "/ˈtʃɪkɪn/", "partOfSpeech": "noun"}],
        "ipa": "/ˈtʃɪkɪn/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/con_ga.mp3",
        "audioEn": "/audio/en/us/con_ga.mp3",
        "sourcePages": [47, 48, 56]
    },
    "che_gio": {
        "id": "che_gio",
        "wordVi": "che gió",
        "meaningVi": "Chắn bớt gió lạnh để giữ ấm cho người và con vật.",
        "meaningsEn": [{"meaning": "shield from wind", "ipa": "/ʃiːld frəm wɪnd/", "partOfSpeech": "verb phrase"}],
        "ipa": "/ʃiːld/",
        "partOfSpeech": "động từ",
        "audioVi": "/audio/vi/che_gio.mp3",
        "audioEn": "/audio/en/us/che_gio.mp3",
        "sourcePages": [48]
    },
    "nha_ba": {
        "id": "nha_ba",
        "wordVi": "nhà",
        "meaningVi": "Nơi chốn ấm áp để gia đình cùng chung sống.",
        "meaningsEn": [
            {"meaning": "house", "ipa": "/haʊs/", "partOfSpeech": "noun"},
            {"meaning": "home", "ipa": "/hoʊm/", "partOfSpeech": "noun"}
        ],
        "ipa": "/haʊs/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/nha_ba.mp3",
        "audioEn": "/audio/en/us/nha_ba.mp3",
        "sourcePages": [49, 53]
    },
    "ngo_nho": {
        "id": "ngo_nho",
        "wordVi": "ngõ nhỏ",
        "meaningVi": "Con đường nhỏ dẫn vào khu phố hoặc xóm làng.",
        "meaningsEn": [{"meaning": "small alley", "ipa": "/smɔːl ˈæli/", "partOfSpeech": "noun phrase"}],
        "ipa": "/ˈæli/",
        "partOfSpeech": "cụm danh từ",
        "audioVi": "/audio/vi/ngo_nho.mp3",
        "audioEn": "/audio/en/us/ngo_nho.mp3",
        "sourcePages": [49, 51, 53, 54]
    },
    "ghe_nho": {
        "id": "ghe_nho",
        "wordVi": "ghế",
        "meaningVi": "Đồ dùng bằng gỗ hoặc nhựa để bé ngồi học bài.",
        "meaningsEn": [{"meaning": "chair", "ipa": "/tʃer/", "partOfSpeech": "noun"}],
        "ipa": "/tʃer/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ghe_nho.mp3",
        "audioEn": "/audio/en/us/ghe_nho.mp3",
        "sourcePages": [49, 50, 53]
    },
    "con_nghe": {
        "id": "con_nghe",
        "wordVi": "nghé",
        "meaningVi": "Con trâu nhỏ mới sinh, rất dễ thương hay lon ton theo mẹ.",
        "meaningsEn": [
            {"meaning": "young buffalo", "ipa": "/jʌŋ ˈbʌfəloʊ/", "partOfSpeech": "noun phrase"},
            {"meaning": "calf", "ipa": "/kæf/", "partOfSpeech": "noun"}
        ],
        "ipa": "/kæf/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/con_nghe.mp3",
        "audioEn": "/audio/en/us/con_nghe.mp3",
        "sourcePages": [51, 52]
    },
    "chim_se": {
        "id": "chim_se",
        "wordVi": "sẻ",
        "meaningVi": "Loài chim nhỏ chuyền cành thoăn thoắt, hót líu lo bên mái hiên.",
        "meaningsEn": [{"meaning": "sparrow", "ipa": "/ˈspæroʊ/", "partOfSpeech": "noun"}],
        "ipa": "/ˈspæroʊ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/chim_se.mp3",
        "audioEn": "/audio/en/us/chim_se.mp3",
        "sourcePages": [55]
    },
    "riu_rit": {
        "id": "riu_rit",
        "wordVi": "ríu rít",
        "meaningVi": "Tiếng chim hót rộn ràng, vui vẻ bên nhau.",
        "meaningsEn": [{"meaning": "chirping happily", "ipa": "/tʃɜːrp ˈhæpɪli/", "partOfSpeech": "verb phrase"}],
        "ipa": "/tʃɜːrp/",
        "partOfSpeech": "từ tượng thanh",
        "audioVi": "/audio/vi/riu_rit.mp3",
        "audioEn": "/audio/en/us/riu_rit.mp3",
        "sourcePages": [55]
    },
    "cho_que": {
        "id": "cho_que",
        "wordVi": "chợ",
        "meaningVi": "Nơi họp mua bán thức ăn, hoa quả tươi ngon tấp nập.",
        "meaningsEn": [{"meaning": "market", "ipa": "/ˈmɑːrkɪt/", "partOfSpeech": "noun"}],
        "ipa": "/ˈmɑːrkɪt/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/cho_que.mp3",
        "audioEn": "/audio/en/us/cho_que.mp3",
        "sourcePages": [43, 56]
    },
    "ca_ro": {
        "id": "ca_ro",
        "wordVi": "cá rô",
        "meaningVi": "Loài cá nước ngọt vảy đen xám, thịt ngọt nấu canh rau cải rất ngon.",
        "meaningsEn": [{"meaning": "climbing perch", "ipa": "/ˈænəbæs/", "partOfSpeech": "noun"}],
        "ipa": "/ˈænəbæs/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ca_ro.mp3",
        "audioEn": "/audio/en/us/ca_ro.mp3",
        "sourcePages": [56]
    },
    "su_su": {
        "id": "su_su",
        "wordVi": "su su",
        "meaningVi": "Quả màu xanh mát, xào hoặc luộc chấm muối vừng.",
        "meaningsEn": [{"meaning": "chayote", "ipa": "/tʃaɪˈoʊti/", "partOfSpeech": "noun"}],
        "ipa": "/tʃaɪˈoʊti/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/su_su.mp3",
        "audioEn": "/audio/en/us/su_su.mp3",
        "sourcePages": [56]
    },
    "ro_ra": {
        "id": "ro_ra",
        "wordVi": "rổ rá",
        "meaningVi": "Đồ dùng đan bằng tre nứa để đựng rau quả hoặc đãi gạo.",
        "meaningsEn": [{"meaning": "woven baskets", "ipa": "/ˈwoʊvn ˈbæskɪts/", "partOfSpeech": "noun phrase"}],
        "ipa": "/ˈbæskɪts/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/ro_ra.mp3",
        "audioEn": "/audio/en/us/ro_ra.mp3",
        "sourcePages": [56]
    },
    "but_chi": {
        "id": "but_chi",
        "wordVi": "bút chì",
        "meaningVi": "Dụng cụ bằng gỗ có ruột chì để bé tập vẽ và viết chữ.",
        "meaningsEn": [{"meaning": "pencil", "ipa": "/ˈpensl/", "partOfSpeech": "noun"}],
        "ipa": "/ˈpensl/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/but_chi.mp3",
        "audioEn": "/audio/en/us/but_chi.mp3",
        "sourcePages": [9]
    },
    "thuoc_ke": {
        "id": "thuoc_ke",
        "wordVi": "thước kẻ",
        "meaningVi": "Cây thước thẳng có vạch số dùng kẻ những đường thẳng tắp.",
        "meaningsEn": [{"meaning": "ruler", "ipa": "/ˈruːlər/", "partOfSpeech": "noun"}],
        "ipa": "/ˈruːlər/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/thuoc_ke.mp3",
        "audioEn": "/audio/en/us/thuoc_ke.mp3",
        "sourcePages": [9]
    },
    "tay_gom": {
        "id": "tay_gom",
        "wordVi": "tẩy",
        "meaningVi": "Cục gôm cao su mềm dùng xóa sạch nét chì khi viết sai.",
        "meaningsEn": [{"meaning": "eraser", "ipa": "/ɪˈreɪsər/", "partOfSpeech": "noun"}],
        "ipa": "/ɪˈreɪsər/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/tay_gom.mp3",
        "audioEn": "/audio/en/us/tay_gom.mp3",
        "sourcePages": [9]
    },
    "vo_viet": {
        "id": "vo_viet",
        "wordVi": "vở",
        "meaningVi": "Tập giấy trắng đóng bìa đẹp để bé tập viết bài mỗi ngày.",
        "meaningsEn": [{"meaning": "notebook", "ipa": "/ˈnoʊtbʊk/", "partOfSpeech": "noun"}],
        "ipa": "/ˈnoʊtbʊk/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/vo_viet.mp3",
        "audioEn": "/audio/en/us/vo_viet.mp3",
        "sourcePages": [9]
    },
    "cap_sach": {
        "id": "cap_sach",
        "wordVi": "cặp sách",
        "meaningVi": "Túi đeo sau lưng để bé cất sách vở, đồ dùng đến trường.",
        "meaningsEn": [{"meaning": "schoolbag", "ipa": "/ˈskuːlbæɡ/", "partOfSpeech": "noun"}],
        "ipa": "/ˈskuːlbæɡ/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/cap_sach.mp3",
        "audioEn": "/audio/en/us/cap_sach.mp3",
        "sourcePages": [9]
    },
    "hop_but": {
        "id": "hop_but",
        "wordVi": "hộp bút",
        "meaningVi": "Chiếc hộp nhỏ xinh xắn để cất gọn bút, thước, tẩy.",
        "meaningsEn": [{"meaning": "pencil case", "ipa": "/ˈpensl keɪs/", "partOfSpeech": "noun"}],
        "ipa": "/ˈpensl keɪs/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/hop_but.mp3",
        "audioEn": "/audio/en/us/hop_but.mp3",
        "sourcePages": [9]
    },
    "bang_con": {
        "id": "bang_con",
        "wordVi": "bảng con",
        "meaningVi": "Tấm bảng nhỏ màu đen bé dùng phấn viết chữ trên lớp.",
        "meaningsEn": [{"meaning": "small chalkboard", "ipa": "/smɔːl ˈtʃɔːkbɔːrd/", "partOfSpeech": "noun"}],
        "ipa": "/ˈtʃɔːkbɔːrd/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/bang_con.mp3",
        "audioEn": "/audio/en/us/bang_con.mp3",
        "sourcePages": [9]
    },
    "truong_lop": {
        "id": "truong_lop",
        "wordVi": "trường lớp",
        "meaningVi": "Ngôi trường thân yêu nơi thầy cô dạy bé học bao điều mới.",
        "meaningsEn": [{"meaning": "school and class", "ipa": "/skuːl ənd klæs/", "partOfSpeech": "noun phrase"}],
        "ipa": "/skuːl/",
        "partOfSpeech": "danh từ",
        "audioVi": "/audio/vi/truong_lop.mp3",
        "audioEn": "/audio/en/us/truong_lop.mp3",
        "sourcePages": [8]
    }
}

# 2. Precise Page Overlays containing ONLY real vocabulary words (NO letters, NO section numbers)
PAGE_VOCAB_OVERLAYS = {
    8: [
        {"id": "ov_p8_truonglop", "text": "trường lớp", "entryId": "truong_lop", "left": 18.0, "top": 11.5, "width": 14.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p8_banbe", "text": "bạn bè", "entryId": "ban_be", "left": 18.0, "top": 15.0, "width": 10.0, "height": 3.0, "isKeyVocab": True}
    ],
    9: [
        {"id": "ov_p9_capsach", "text": "cặp sách", "entryId": "cap_sach", "left": 15.0, "top": 28.0, "width": 12.0, "height": 3.5, "isKeyVocab": True},
        {"id": "ov_p9_hopbut", "text": "hộp bút", "entryId": "hop_but", "left": 40.0, "top": 28.0, "width": 11.5, "height": 3.5, "isKeyVocab": True},
        {"id": "ov_p9_bangcon", "text": "bảng con", "entryId": "bang_con", "left": 65.0, "top": 28.0, "width": 12.5, "height": 3.5, "isKeyVocab": True},
        {"id": "ov_p9_butchi", "text": "bút chì", "entryId": "but_chi", "left": 15.0, "top": 55.0, "width": 11.0, "height": 3.5, "isKeyVocab": True},
        {"id": "ov_p9_thuocke", "text": "thước kẻ", "entryId": "thuoc_ke", "left": 40.0, "top": 55.0, "width": 12.0, "height": 3.5, "isKeyVocab": True},
        {"id": "ov_p9_taygom", "text": "tẩy", "entryId": "tay_gom", "left": 65.0, "top": 55.0, "width": 8.0, "height": 3.5, "isKeyVocab": True},
        {"id": "ov_p9_voviet", "text": "vở", "entryId": "vo_viet", "left": 40.0, "top": 80.0, "width": 8.0, "height": 3.5, "isKeyVocab": True}
    ],
    15: [
        {"id": "ov_p15_cahat", "text": "ca hát", "entryId": "ca_hat", "left": 53.0, "top": 60.0, "width": 11.8, "height": 2.7, "isKeyVocab": True}
    ],
    16: [
        {"id": "ov_p16_bo", "text": "ba", "entryId": "bo", "left": 14.5, "top": 54.8, "width": 8.5, "height": 3.2, "isKeyVocab": True}
    ],
    17: [
        {"id": "ov_p17_ba", "text": "Bà", "entryId": "ba_noi", "left": 36.5, "top": 59.8, "width": 5.2, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p17_be", "text": "bé", "entryId": "be", "left": 47.0, "top": 59.8, "width": 5.0, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p17_bupbe", "text": "búp bê", "entryId": "bup_be", "left": 53.0, "top": 59.8, "width": 12.2, "height": 2.7, "isKeyVocab": True}
    ],
    18: [
        {"id": "ov_p18_bo", "text": "ba", "entryId": "bo", "left": 14.5, "top": 54.8, "width": 8.5, "height": 3.2, "isKeyVocab": True}
    ],
    19: [
        {"id": "ov_p19_bo", "text": "bố", "entryId": "bo", "left": 46.5, "top": 59.8, "width": 5.0, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p19_cauca", "text": "câu cá", "entryId": "cau_ca", "left": 52.5, "top": 59.8, "width": 11.2, "height": 2.7, "isKeyVocab": True}
    ],
    20: [
        {"id": "ov_p20_ca", "text": "cá", "entryId": "ca", "left": 17.5, "top": 54.8, "width": 8.5, "height": 3.2, "isKeyVocab": True}
    ],
    21: [
        {"id": "ov_p21_be", "text": "Bé", "entryId": "be", "left": 27.8, "top": 59.8, "width": 5.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p21_me", "text": "mẹ", "entryId": "me", "left": 41.0, "top": 59.8, "width": 5.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p21_banbe", "text": "bạn bè", "entryId": "ban_be", "left": 59.8, "top": 59.8, "width": 11.8, "height": 2.7, "isKeyVocab": True}
    ],
    22: [
        {"id": "ov_p22_ba", "text": "Bà", "entryId": "ba_noi", "left": 14.2, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p22_bedt", "text": "bế", "entryId": "be_dong_tu", "left": 21.5, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p22_be", "text": "bé", "entryId": "be", "left": 28.0, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True}
    ],
    24: [
        {"id": "ov_p24_bupbe", "text": "Búp bê", "entryId": "bup_be", "left": 35.0, "top": 45.0, "width": 12.0, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p24_demen", "text": "dế mèn", "entryId": "de_men", "left": 53.0, "top": 45.0, "width": 12.0, "height": 3.0, "isKeyVocab": True}
    ],
    25: [
        {"id": "ov_p25_bo", "text": "bò", "entryId": "con_bo", "left": 44.0, "top": 59.8, "width": 5.8, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p25_gamco", "text": "gặm cỏ", "entryId": "gam_co", "left": 50.8, "top": 59.8, "width": 12.5, "height": 2.7, "isKeyVocab": True}
    ],
    26: [
        {"id": "ov_p26_be", "text": "Bé", "entryId": "be", "left": 14.2, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p26_co", "text": "cỏ", "entryId": "co", "left": 28.0, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True}
    ],
    27: [
        {"id": "ov_p27_bo", "text": "Bố", "entryId": "bo", "left": 25.8, "top": 59.8, "width": 5.8, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p27_dibo", "text": "đi bộ", "entryId": "di_bo", "left": 43.2, "top": 59.8, "width": 8.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p27_hepho", "text": "hè phố", "entryId": "he_pho", "left": 57.8, "top": 59.8, "width": 11.5, "height": 2.7, "isKeyVocab": True}
    ],
    28: [
        {"id": "ov_p28_bo", "text": "Bố", "entryId": "bo", "left": 14.2, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p28_bedt", "text": "bế", "entryId": "be_dong_tu", "left": 21.5, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p28_be", "text": "bé", "entryId": "be", "left": 28.0, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True}
    ],
    29: [
        {"id": "ov_p29_gocda", "text": "gốc đa", "entryId": "goc_da", "left": 24.0, "top": 59.8, "width": 10.0, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p29_banbe", "text": "bạn", "entryId": "ban_be", "left": 46.8, "top": 59.8, "width": 6.2, "height": 2.7, "isKeyVocab": True}
    ],
    30: [
        {"id": "ov_p30_be", "text": "Bé", "entryId": "be", "left": 14.2, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p30_odo", "text": "ô đỏ", "entryId": "o_do", "left": 26.8, "top": 54.8, "width": 9.5, "height": 3.0, "isKeyVocab": True}
    ],
    31: [
        {"id": "ov_p31_tauthuy", "text": "Tàu", "entryId": "tau_thuy", "left": 32.0, "top": 59.8, "width": 6.8, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p31_cangbien", "text": "cảng", "entryId": "cang_bien", "left": 63.0, "top": 59.8, "width": 8.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p31_bode", "text": "bờ đê", "entryId": "bo_de", "left": 15.0, "top": 76.0, "width": 10.0, "height": 2.8, "isKeyVocab": True},
        {"id": "ov_p31_dobe", "text": "đỡ bé", "entryId": "do_be", "left": 51.8, "top": 76.0, "width": 10.5, "height": 2.8, "isKeyVocab": True}
    ],
    32: [
        {"id": "ov_p32_bo", "text": "Bố", "entryId": "bo", "left": 14.2, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p32_dobe", "text": "đỡ bé", "entryId": "do_be", "left": 20.8, "top": 54.8, "width": 11.5, "height": 3.0, "isKeyVocab": True}
    ],
    33: [
        {"id": "ov_p33_bode", "text": "Bờ đê", "entryId": "bo_de", "left": 14.2, "top": 85.0, "width": 10.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p33_demen", "text": "dế", "entryId": "de_men", "left": 31.0, "top": 85.0, "width": 5.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p33_ba", "text": "Bà", "entryId": "ba_noi", "left": 40.0, "top": 85.0, "width": 5.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p33_dodo", "text": "đỗ đỏ", "entryId": "do_do", "left": 52.0, "top": 85.0, "width": 9.5, "height": 3.0, "isKeyVocab": True}
    ],
    34: [
        {"id": "ov_p34_dankien", "text": "Đàn kiến", "entryId": "dan_kien", "left": 25.0, "top": 45.0, "width": 14.0, "height": 3.0, "isKeyVocab": True}
    ],
    35: [
        {"id": "ov_p35_kida", "text": "kì đà", "entryId": "ki_da", "left": 50.8, "top": 59.8, "width": 10.0, "height": 2.7, "isKeyVocab": True}
    ],
    36: [
        {"id": "ov_p36_kida", "text": "Kì đà", "entryId": "ki_da", "left": 14.2, "top": 54.8, "width": 10.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p36_keda", "text": "kẽ đá", "entryId": "ke_da", "left": 34.8, "top": 54.8, "width": 9.5, "height": 3.0, "isKeyVocab": True}
    ],
    37: [
        {"id": "ov_p37_lele", "text": "Le le", "entryId": "le_le", "left": 35.8, "top": 59.8, "width": 9.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p37_boiloi", "text": "bơi", "entryId": "boi_loi", "left": 49.0, "top": 59.8, "width": 6.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p37_matho", "text": "hồ", "entryId": "mat_ho", "left": 65.0, "top": 59.8, "width": 6.0, "height": 2.7, "isKeyVocab": True}
    ],
    38: [
        {"id": "ov_p38_be", "text": "Bé", "entryId": "be", "left": 14.2, "top": 54.8, "width": 6.0, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p38_ba", "text": "Bà", "entryId": "ba_noi", "left": 31.8, "top": 54.8, "width": 6.0, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p38_lahe", "text": "lá hẹ", "entryId": "la_he", "left": 47.8, "top": 54.8, "width": 9.5, "height": 3.0, "isKeyVocab": True}
    ],
    39: [
        {"id": "ov_p39_dudu", "text": "Đu đủ", "entryId": "du_du", "left": 33.8, "top": 59.8, "width": 10.0, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p39_ngotlu", "text": "ngọt lừ", "entryId": "ngot_lu", "left": 60.0, "top": 59.8, "width": 11.5, "height": 2.7, "isKeyVocab": True}
    ],
    40: [
        {"id": "ov_p40_caho", "text": "Cá hổ", "entryId": "ca_ho", "left": 14.2, "top": 54.8, "width": 9.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p40_cadu", "text": "cá dữ", "entryId": "hung_du", "left": 31.8, "top": 54.8, "width": 9.5, "height": 3.0, "isKeyVocab": True}
    ],
    41: [
        {"id": "ov_p41_khi", "text": "khỉ", "entryId": "con_khi", "left": 45.8, "top": 59.8, "width": 6.0, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p41_chuoi", "text": "chuối", "entryId": "chuoi", "left": 57.8, "top": 59.8, "width": 9.5, "height": 2.7, "isKeyVocab": True}
    ],
    42: [
        {"id": "ov_p42_cakho", "text": "cá kho", "entryId": "ca_kho", "left": 27.8, "top": 54.8, "width": 10.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p42_khe", "text": "khế", "entryId": "khe", "left": 39.2, "top": 54.8, "width": 7.0, "height": 3.0, "isKeyVocab": True}
    ],
    44: [
        {"id": "ov_p44_conqua", "text": "Con quạ", "entryId": "con_qua", "left": 28.0, "top": 45.0, "width": 14.0, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p44_thongminh", "text": "thông minh", "entryId": "thong_minh", "left": 45.0, "top": 45.0, "width": 18.0, "height": 3.0, "isKeyVocab": True}
    ],
    45: [
        {"id": "ov_p45_me", "text": "Mẹ", "entryId": "me", "left": 35.8, "top": 59.8, "width": 6.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p45_nodo", "text": "nơ", "entryId": "no_do", "left": 48.8, "top": 59.8, "width": 6.0, "height": 2.7, "isKeyVocab": True}
    ],
    46: [
        {"id": "ov_p46_bo", "text": "Bố", "entryId": "bo", "left": 14.2, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p46_me", "text": "mẹ", "entryId": "me", "left": 20.2, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p46_cano", "text": "ca nô", "entryId": "ca_no", "left": 42.8, "top": 54.8, "width": 10.0, "height": 3.0, "isKeyVocab": True}
    ],
    47: [
        {"id": "ov_p47_giotrung", "text": "giỏ trứng", "entryId": "gio_trung", "left": 46.8, "top": 59.8, "width": 14.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p47_ga", "text": "gà", "entryId": "con_ga", "left": 61.8, "top": 59.8, "width": 6.0, "height": 2.7, "isKeyVocab": True}
    ],
    48: [
        {"id": "ov_p48_ba", "text": "Bà", "entryId": "ba_noi", "left": 14.2, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p48_chegio", "text": "che gió", "entryId": "che_gio", "left": 20.8, "top": 54.8, "width": 11.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p48_ga", "text": "gà", "entryId": "con_ga", "left": 49.8, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True}
    ],
    49: [
        {"id": "ov_p49_nhaba", "text": "nhà", "entryId": "nha_ba", "left": 37.8, "top": 59.8, "width": 6.8, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p49_ba", "text": "bà", "entryId": "ba_noi", "left": 44.8, "top": 59.8, "width": 5.8, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p49_ngonho", "text": "ngõ nhỏ", "entryId": "ngo_nho", "left": 64.8, "top": 59.8, "width": 12.5, "height": 2.7, "isKeyVocab": True}
    ],
    50: [
        {"id": "ov_p50_me", "text": "Mẹ", "entryId": "me", "left": 14.2, "top": 54.8, "width": 6.2, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p50_ghenho", "text": "ghế", "entryId": "ghe_nho", "left": 38.8, "top": 54.8, "width": 7.0, "height": 3.0, "isKeyVocab": True}
    ],
    51: [
        {"id": "ov_p51_nghe", "text": "Nghé", "entryId": "con_nghe", "left": 33.8, "top": 59.8, "width": 9.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p51_me", "text": "mẹ", "entryId": "me", "left": 50.8, "top": 59.8, "width": 6.2, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p51_ngo", "text": "ngõ", "entryId": "ngo_nho", "left": 62.8, "top": 59.8, "width": 6.2, "height": 2.7, "isKeyVocab": True}
    ],
    52: [
        {"id": "ov_p52_nghe1", "text": "Nghé", "entryId": "con_nghe", "left": 14.2, "top": 54.8, "width": 8.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p52_co", "text": "cỏ", "entryId": "co", "left": 30.2, "top": 54.8, "width": 5.8, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p52_nghe2", "text": "Nghé", "entryId": "con_nghe", "left": 37.8, "top": 54.8, "width": 8.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p52_bode", "text": "bờ đê", "entryId": "bo_de", "left": 54.8, "top": 54.8, "width": 10.0, "height": 3.0, "isKeyVocab": True}
    ],
    55: [
        {"id": "ov_p55_se", "text": "sẻ", "entryId": "chim_se", "left": 40.8, "top": 59.8, "width": 5.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p55_riurit", "text": "ríu ra ríu rít", "entryId": "riu_rit", "left": 51.8, "top": 59.8, "width": 16.5, "height": 2.7, "isKeyVocab": True},
        {"id": "ov_p55_me", "text": "mẹ", "entryId": "me", "left": 73.8, "top": 59.8, "width": 6.2, "height": 2.7, "isKeyVocab": True}
    ],
    56: [
        {"id": "ov_p56_cho1", "text": "Chợ", "entryId": "cho_que", "left": 14.2, "top": 54.8, "width": 7.0, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p56_ga", "text": "gà", "entryId": "con_ga", "left": 26.2, "top": 54.8, "width": 5.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p56_caro", "text": "cá rô", "entryId": "ca_ro", "left": 36.8, "top": 54.8, "width": 8.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p56_susu", "text": "su su", "entryId": "su_su", "left": 47.8, "top": 54.8, "width": 8.5, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p56_cho2", "text": "Chợ", "entryId": "cho_que", "left": 58.2, "top": 54.8, "width": 7.0, "height": 3.0, "isKeyVocab": True},
        {"id": "ov_p56_rora", "text": "rổ rá", "entryId": "ro_ra", "left": 71.8, "top": 54.8, "width": 9.0, "height": 3.0, "isKeyVocab": True}
    ]
}

async def generate_missing_audio():
    print(f"Generating audio for {len(CLEAN_DICTIONARY)} clean meaningful entries...")
    for entry_id, entry in CLEAN_DICTIONARY.items():
        vi_path = f"public{entry['audioVi']}"
        en_path = f"public{entry['audioEn']}"

        if not os.path.exists(vi_path):
            try:
                tts_vi = edge_tts.Communicate(entry['wordVi'], 'vi-VN-HoaiMyNeural')
                await tts_vi.save(vi_path)
            except Exception as e:
                print(f"Error VI {entry_id}: {e}")

        if not os.path.exists(en_path):
            try:
                en_word = entry['meaningsEn'][0]['meaning'].split(' (')[0].split(' /')[0]
                tts_en = edge_tts.Communicate(en_word, 'en-US-AnaNeural')
                await tts_en.save(en_path)
            except Exception as e:
                print(f"Error EN {entry_id}: {e}")

# Save clean entries.json
with open('src/data/entries.json', 'w', encoding='utf-8') as f:
    json.dump(CLEAN_DICTIONARY, f, ensure_ascii=False, indent=2)

# Save page_overlays.json for all 57 pages
all_page_overlays = {}
for p in range(1, 58):
    overlays = PAGE_VOCAB_OVERLAYS.get(p, [])
    # Find all vocab IDs for this page
    vocab_ids = [it['entryId'] for it in overlays if it.get('entryId')]
    # Also check if any entry has this sourcePage
    for eid, entry in CLEAN_DICTIONARY.items():
        if p in entry.get('sourcePages', []) and eid not in vocab_ids:
            vocab_ids.append(eid)

    all_page_overlays[p] = {
        "pageNumber": p,
        "image": f"/pages/page_{p:03d}.jpg",
        "overlays": overlays,
        "vocabWordIds": vocab_ids
    }

with open('src/data/page_overlays.json', 'w', encoding='utf-8') as f:
    json.dump(all_page_overlays, f, ensure_ascii=False, indent=2)

print(f"Saved clean entries.json ({len(CLEAN_DICTIONARY)} words) and page_overlays.json (57 pages).")

if __name__ == '__main__':
    asyncio.run(generate_missing_audio())
