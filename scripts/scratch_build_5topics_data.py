import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. BUILD ENTRIES
entries = {
    # === TOPIC 1: BÀI 3: C c ===
    "c": {
        "id": "c",
        "wordVi": "c",
        "meaningVi": "Chữ cái c, ghi âm cờ trong bảng chữ cái tiếng Việt.",
        "meaningsEn": [
            {
                "meaning": "Letter C / Phoneme /k/",
                "ipa": "/ˈletər siː/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kəː˧˧/",
        "partOfSpeech": "Chữ cái",
        "audioVi": "/audio/vi/c.mp3",
        "audioEn": "/audio/en/us/c.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },
    "ca_nuoc": {
        "id": "ca_nuoc",
        "wordVi": "ca",
        "meaningVi": "Cái ca (cốc) có quai cầm dùng để đựng nước, uống nước sạch hàng ngày.",
        "meaningsEn": [
            {
                "meaning": "mug / cup",
                "ipa": "/mʌɡ/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kaː˧˧/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/ca_nuoc.mp3",
        "audioEn": "/audio/en/us/ca_nuoc.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },
    "ca_tim": {
        "id": "ca_tim",
        "wordVi": "cà",
        "meaningVi": "Quả cà, một loại rau củ quen thuộc có màu tím hoặc xanh, dùng chế biến món ăn ngon.",
        "meaningsEn": [
            {
                "meaning": "eggplant / aubergine",
                "ipa": "/ˈeɡplænt/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kaː˨˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/ca_tim.mp3",
        "audioEn": "/audio/en/us/ca_tim.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },
    "ca": {
        "id": "ca",
        "wordVi": "cá",
        "meaningVi": "Con cá, loài động vật có vây, thở bằng mang, bơi lội dưới nước.",
        "meaningsEn": [
            {
                "meaning": "fish",
                "ipa": "/fɪʃ/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kaː˧˦/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/ca.mp3",
        "audioEn": "/audio/en/us/ca.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },
    "a_ca": {
        "id": "a_ca",
        "wordVi": "A, cá.",
        "meaningVi": "Tiếng reo vui tươi của bạn nhỏ khi bất ngờ phát hiện thấy đàn cá bơi lội dưới hồ nước.",
        "meaningsEn": [
            {
                "meaning": "Wow, fishes!",
                "ipa": "/waʊ ˈfɪʃɪz/",
                "partOfSpeech": "exclamation"
            }
        ],
        "ipa": "/aː˧˧ kaː˧˦/",
        "partOfSpeech": "Câu cảm thán",
        "audioVi": "/audio/vi/a_ca.mp3",
        "audioEn": "/audio/en/us/a_ca.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },
    "b3_thoai_1": {
        "id": "b3_thoai_1",
        "wordVi": "Cháu chào bác ạ! (Good morning)",
        "meaningVi": "Hội thoại chào hỏi lễ phép của bạn học sinh khi gặp bác bảo vệ ở cổng trường học.",
        "meaningsEn": [
            {
                "meaning": "Good morning (Greeting the school guard)",
                "ipa": "/ɡʊd ˈmɔːrnɪŋ/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/tɕaʊ˧˦ tɕaːw˨˩ ɓaːk˧˦ aː˧˨/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b3_thoai_1.mp3",
        "audioEn": "/audio/en/us/b3_thoai_1.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },
    "b3_thoai_2": {
        "id": "b3_thoai_2",
        "wordVi": "Chào các bạn! (Hi)",
        "meaningVi": "Lời chào tươi vui, thân thiện của bạn nhỏ khi bước vào lớp học gặp gỡ thầy cô và bạn bè.",
        "meaningsEn": [
            {
                "meaning": "Hi (Greeting classmates)",
                "ipa": "/haɪ/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/tɕaːw˨˩ kaːk˧˦ ɓaːn˧˨/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b3_thoai_2.mp3",
        "audioEn": "/audio/en/us/b3_thoai_2.mp3",
        "sourcePages": [1],
        "reviewStatus": "verified"
    },

    # === TOPIC 2: BÀI 6: O o ===
    "con_bo": {
        "id": "con_bo",
        "wordVi": "bò",
        "meaningVi": "Con bò, loài động vật bốn chân nuôi lấy sữa và kéo cày, thích ăn cỏ xanh non.",
        "meaningsEn": [
            {
                "meaning": "cow / ox",
                "ipa": "/kaʊ/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/ɓɔː˨˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/con_bo.mp3",
        "audioEn": "/audio/en/us/con_bo.mp3",
        "sourcePages": [2],
        "reviewStatus": "verified"
    },
    "con_co": {
        "id": "con_co",
        "wordVi": "cò",
        "meaningVi": "Con cò trắng có mỏ nhọn và chân dài, thường kiếm ăn ở đồng ruộng bờ ao thôn quê.",
        "meaningsEn": [
            {
                "meaning": "egret / stork",
                "ipa": "/ˈiːɡrət/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kɔː˨˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/con_co.mp3",
        "audioEn": "/audio/en/us/con_co.mp3",
        "sourcePages": [2],
        "reviewStatus": "verified"
    },
    "co": {
        "id": "co",
        "wordVi": "cỏ",
        "meaningVi": "Cỏ, loài thực vật thân mềm xanh tươi phủ trên mặt đất, thức ăn của bò và bê con.",
        "meaningsEn": [
            {
                "meaning": "grass",
                "ipa": "/ɡræs/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kɔː˧˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/co.mp3",
        "audioEn": "/audio/en/us/co.mp3",
        "sourcePages": [2],
        "reviewStatus": "verified"
    },
    "be_co_co": {
        "id": "be_co_co",
        "wordVi": "Bê có cỏ.",
        "meaningVi": "Chú bê con được nuôi trong chuồng và có cỏ tươi để ăn no.",
        "meaningsEn": [
            {
                "meaning": "The calf has grass.",
                "ipa": "/ðə kæf hæz ɡræs/",
                "partOfSpeech": "sentence"
            }
        ],
        "ipa": "/ɓeː˧˧ kɔː˧˦ kɔː˧˩/",
        "partOfSpeech": "Câu đọc",
        "audioVi": "/audio/vi/be_co_co.mp3",
        "audioEn": "/audio/en/us/be_co_co.mp3",
        "sourcePages": [2],
        "reviewStatus": "verified"
    },
    "b6_thoai_1": {
        "id": "b6_thoai_1",
        "wordVi": "Con chào mẹ ạ! (Hi, mom)",
        "meaningVi": "Lời chào đón đầy tình cảm của bạn nhỏ khi tan học về nhà gặp mẹ ở cửa.",
        "meaningsEn": [
            {
                "meaning": "Hi, mom (Greeting mom after school)",
                "ipa": "/haɪ mɑːm/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/kɔn˧˧ tɕaːw˨˩ mɛː˧˨ aː˧˨/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b6_thoai_1.mp3",
        "audioEn": "/audio/en/us/b6_thoai_1.mp3",
        "sourcePages": [2],
        "reviewStatus": "verified"
    },
    "b6_thoai_2": {
        "id": "b6_thoai_2",
        "wordVi": "Cháu chào ông, cháu chào bà ạ! (Good afternoon)",
        "meaningVi": "Bạn nhỏ khoanh tay lễ phép chào ông bà đang đọc báo và thư giãn trong phòng khách.",
        "meaningsEn": [
            {
                "meaning": "Good afternoon, Grandmother and Grandfather",
                "ipa": "/ɡʊd ˌæftərˈnuːn ˈɡrændˌmʌðər ænd ˈɡrændˌfɑːðər/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/tɕaʊ˧˦ tɕaːw˨˩ ăwŋ˧˧ tɕaʊ˧˦ tɕaːw˨˩ ɓaː˨˩ aː˧˨/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b6_thoai_2.mp3",
        "audioEn": "/audio/en/us/b6_thoai_2.mp3",
        "sourcePages": [2],
        "reviewStatus": "verified"
    },

    # === TOPIC 3: BÀI 10: ÔN TẬP VÀ KỂ CHUYỆN ===
    "dan_kien_title": {
        "id": "dan_kien_title",
        "wordVi": "Đàn kiến con ngoan ngoãn",
        "meaningVi": "Câu chuyện cảm động về đàn kiến con đoàn kết, hiếu thảo và biết tương trợ bà kiến già đau ốm.",
        "meaningsEn": [
            {
                "meaning": "The Well-Behaved Little Ants",
                "ipa": "/ðə wel bɪˈheɪvd ˈlɪtl ænts/",
                "partOfSpeech": "story title"
            }
        ],
        "ipa": "/ɗaːn˨˩ kiən˧˦ kɔn˧˧ nwaːn˧˧ nwaːn˧˦/",
        "partOfSpeech": "Tên câu chuyện",
        "audioVi": "/audio/vi/dan_kien_title.mp3",
        "audioEn": "/audio/en/us/dan_kien_title.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "kien_tranh_1": {
        "id": "kien_tranh_1",
        "wordVi": "Tranh 1: Tổ bà kiến chật hẹp, ẩm ướt",
        "meaningVi": "Bà kiến đã già, một mình ở trong cái tổ nhỏ chật hẹp, ẩm ướt. Mấy hôm nay, bà đau ốm cứ rên hừ hừ.",
        "meaningsEn": [
            {
                "meaning": "Old mother ant lived alone in a small, damp nest, groaning with illness.",
                "ipa": "/oʊld ˈmʌðər ænt lɪvd əˈloʊn ɪn ə smɔːl dæmp nest/",
                "partOfSpeech": "story section"
            }
        ],
        "ipa": "/ɓaː˨˩ kiən˧˦ ɗaː˧˦ zaː˨˩/",
        "partOfSpeech": "Kể chuyện (Tranh 1)",
        "audioVi": "/audio/vi/kien_tranh_1.mp3",
        "audioEn": "/audio/en/us/kien_tranh_1.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "kien_tranh_2": {
        "id": "kien_tranh_2",
        "wordVi": "Tranh 2: Đàn kiến tha chiếc lá đa vàng",
        "meaningVi": "Đàn kiến con đi ngang qua thấy vậy bèn giúp đỡ bà. Chúng tha về một chiếc lá đa vàng mới rụng, dìu bà ngồi trên đó rồi khiêng đi tắm nắng.",
        "meaningsEn": [
            {
                "meaning": "The little ants carried a yellow banyan leaf to help her sit and sunbathe.",
                "ipa": "/ðə ˈlɪtl ænts brɔːt ə ˈbænjən liːf/",
                "partOfSpeech": "story section"
            }
        ],
        "ipa": "/ɗaːn˨˩ kiən˧˦ kɔn˧˧ ɗiː˧˧ ŋaːŋ˧˧ kwaː˧˧/",
        "partOfSpeech": "Kể chuyện (Tranh 2)",
        "audioVi": "/audio/vi/kien_tranh_2.mp3",
        "audioEn": "/audio/en/us/kien_tranh_2.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "kien_tranh_3": {
        "id": "kien_tranh_3",
        "wordVi": "Tranh 3: Đưa bà kiến lên ụ đất cao ráo",
        "meaningVi": "Đàn kiến con chia nhau đi tìm nhà mới cho bà. Cả đàn xúm vào khiêng chiếc lá, đưa bà kiến lên một ụ đất cao ráo, thoáng mát.",
        "meaningsEn": [
            {
                "meaning": "The ants searched for a new home and carried her up to a dry, sunny hillock.",
                "ipa": "/ðə ænts ˈkærid hɜːr tuː ə braɪt ˈbriːzi maʊnd/",
                "partOfSpeech": "story section"
            }
        ],
        "ipa": "/tɕuŋ˧˦ tɕiə˧˧ ɲaʊ˧˧ ɗiː˧˧ tiəm˨˩ ɲaː˨˩ məːj˧˦/",
        "partOfSpeech": "Kể chuyện (Tranh 3)",
        "audioVi": "/audio/vi/kien_tranh_3.mp3",
        "audioEn": "/audio/en/us/kien_tranh_3.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "kien_tranh_4": {
        "id": "kien_tranh_4",
        "wordVi": "Tranh 4: Bà kiến sung sướng cảm ơn",
        "meaningVi": "Bà kiến được ở nhà mới vui sướng nói: “Nhờ các cháu giúp đỡ, bà được tắm nắng lại ở nhà mới cao ráo, đẹp đẽ. Bà cảm ơn các cháu thật nhiều!”.",
        "meaningsEn": [
            {
                "meaning": "Old mother ant happily thanked the kind little ants in her new sunny home.",
                "ipa": "/oʊld ˈmʌðər ænt ˈhæpɪli θæŋkt ðə kaɪnd ænts/",
                "partOfSpeech": "story section"
            }
        ],
        "ipa": "/ɓaː˨˩ kiən˧˦ ɗɨək˧˨ əː˧˩ ɲaː˨˩ məːj˧˦/",
        "partOfSpeech": "Kể chuyện (Tranh 4)",
        "audioVi": "/audio/vi/kien_tranh_4.mp3",
        "audioEn": "/audio/en/us/kien_tranh_4.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "bo_co": {
        "id": "bo_co",
        "wordVi": "bó cỏ",
        "meaningVi": "Một bó cỏ tươi được gom và buộc lại gọn gàng để cho gia súc ăn.",
        "meaningsEn": [
            {
                "meaning": "bundle of grass",
                "ipa": "/ˈbʌndl əv ɡræs/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/ɓɔː˧˦ kɔː˧˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/bo_co.mp3",
        "audioEn": "/audio/en/us/bo_co.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "ca_co": {
        "id": "ca_co",
        "wordVi": "cá cờ",
        "meaningVi": "Loài cá nhỏ bơi nhanh, có vây sặc sỡ giống ngọn cờ.",
        "meaningsEn": [
            {
                "meaning": "fighting fish / sailfish",
                "ipa": "/ˈfaɪtɪŋ fɪʃ/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kaː˧˦ kəː˨˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/ca_co.mp3",
        "audioEn": "/audio/en/us/ca_co.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "bo_de": {
        "id": "bo_de",
        "wordVi": "bờ đê",
        "meaningVi": "Đường bờ đê đắp bằng đất cao dọc theo dòng sông để ngăn nước lũ.",
        "meaningsEn": [
            {
                "meaning": "dike / embankment",
                "ipa": "/daɪk/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/ɓəː˨˩ ɗeː˧˧/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/bo_de.mp3",
        "audioEn": "/audio/en/us/bo_de.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "do_ba": {
        "id": "do_ba",
        "wordVi": "đỡ bà",
        "meaningVi": "Hành động lễ phép dìu đỡ bà bước đi vững vàng, an toàn.",
        "meaningsEn": [
            {
                "meaning": "help grandmother / support grandmother",
                "ipa": "/help ˈɡrændˌmʌðər/",
                "partOfSpeech": "verb phrase"
            }
        ],
        "ipa": "/ɗəː˧˦ ɓaː˨˩/",
        "partOfSpeech": "Cụm động từ",
        "audioVi": "/audio/vi/do_ba.mp3",
        "audioEn": "/audio/en/us/do_ba.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "co_do": {
        "id": "co_do",
        "wordVi": "cờ đỏ",
        "meaningVi": "Lá cờ đỏ thắm mang biểu tượng đất nước hoặc trường lớp rực rỡ.",
        "meaningsEn": [
            {
                "meaning": "red flag",
                "ipa": "/red flæɡ/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kəː˨˩ ɗɔː˧˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/co_do.mp3",
        "audioEn": "/audio/en/us/co_do.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "do_do": {
        "id": "do_do",
        "wordVi": "đỗ đỏ",
        "meaningVi": "Hạt đậu đỏ (đỗ đỏ) bổ dưỡng, dùng nấu xôi hoặc nấu chè thanh mát.",
        "meaningsEn": [
            {
                "meaning": "red beans / adzuki beans",
                "ipa": "/red biːnz/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/ɗoː˧˦ ɗɔː˧˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/do_do.mp3",
        "audioEn": "/audio/en/us/do_do.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "do_be": {
        "id": "do_be",
        "wordVi": "đỡ bé",
        "meaningVi": "Nâng đỡ và dìu dắt em bé chập chững những bước đi đầu đời.",
        "meaningsEn": [
            {
                "meaning": "support the baby",
                "ipa": "/səˈpɔːrt ðə ˈbeɪbi/",
                "partOfSpeech": "verb phrase"
            }
        ],
        "ipa": "/ɗəː˧˦ ɓɛː˧˦/",
        "partOfSpeech": "Cụm động từ",
        "audioVi": "/audio/vi/do_be.mp3",
        "audioEn": "/audio/en/us/do_be.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "cau_bo_de_co_de": {
        "id": "cau_bo_de_co_de",
        "wordVi": "Bờ đê có dế.",
        "meaningVi": "Trên dải cỏ triền đê có những chú dế mèn đào hang sinh sống.",
        "meaningsEn": [
            {
                "meaning": "There are crickets on the dike.",
                "ipa": "/ðer ɑːr ˈkrɪkɪts ɒn ðə daɪk/",
                "partOfSpeech": "sentence"
            }
        ],
        "ipa": "/ɓəː˨˩ ɗeː˧˧ kɔː˧˦ zeː˧˦/",
        "partOfSpeech": "Câu đọc",
        "audioVi": "/audio/vi/cau_bo_de_co_de.mp3",
        "audioEn": "/audio/en/us/cau_bo_de_co_de.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },
    "cau_ba_co_do_do": {
        "id": "cau_ba_co_do_do",
        "wordVi": "Bà có đỗ đỏ.",
        "meaningVi": "Bà có những hạt đỗ đỏ thơm ngon để chuẩn bị nấu chè cho cả nhà.",
        "meaningsEn": [
            {
                "meaning": "Grandmother has red beans.",
                "ipa": "/ˈɡrændˌmʌðər hæz red biːnz/",
                "partOfSpeech": "sentence"
            }
        ],
        "ipa": "/ɓaː˨˩ kɔː˧˦ ɗoː˧˦ ɗɔː˧˩/",
        "partOfSpeech": "Câu đọc",
        "audioVi": "/audio/vi/cau_ba_co_do_do.mp3",
        "audioEn": "/audio/en/us/cau_ba_co_do_do.mp3",
        "sourcePages": [3],
        "reviewStatus": "verified"
    },

    # === TOPIC 4: BÀI 16: M m, N n ===
    "ca_me": {
        "id": "ca_me",
        "wordVi": "cá mè",
        "meaningVi": "Loài cá nước ngọt vảy trắng óng ánh, sống ở ao hồ sông ngòi.",
        "meaningsEn": [
            {
                "meaning": "carp / silver carp",
                "ipa": "/kɑːrp/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kaː˧˦ mɛː˨˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/ca_me.mp3",
        "audioEn": "/audio/en/us/ca_me.mp3",
        "sourcePages": [4],
        "reviewStatus": "verified"
    },
    "la_me": {
        "id": "la_me",
        "wordVi": "lá me",
        "meaningVi": "Lá của cây me, những chiếc lá nhỏ xinh có vị chua thanh mát.",
        "meaningsEn": [
            {
                "meaning": "tamarind leaf",
                "ipa": "/ˈtæmərɪnd liːf/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/laː˧˦ mɛː˧˧/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/la_me.mp3",
        "audioEn": "/audio/en/us/la_me.mp3",
        "sourcePages": [4],
        "reviewStatus": "verified"
    },
    "no_do": {
        "id": "no_do",
        "wordVi": "nơ đỏ",
        "meaningVi": "Chiếc nơ màu đỏ thắm xinh xắn bé dùng để cài lên mái tóc.",
        "meaningsEn": [
            {
                "meaning": "red bow / red ribbon",
                "ipa": "/red boʊ/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/nəː˧˧ ɗɔː˧˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/no_do.mp3",
        "audioEn": "/audio/en/us/no_do.mp3",
        "sourcePages": [4],
        "reviewStatus": "verified"
    },
    "ca_no": {
        "id": "ca_no",
        "wordVi": "ca nô",
        "meaningVi": "Chiếc thuyền máy ca nô nhỏ chạy bằng động cơ lướt nhanh trên mặt nước.",
        "meaningsEn": [
            {
                "meaning": "motorboat / canoe",
                "ipa": "/ˈmoʊtərbəʊt/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/kaː˧˧ noː˧˧/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/ca_no.mp3",
        "audioEn": "/audio/en/us/ca_no.mp3",
        "sourcePages": [4],
        "reviewStatus": "verified"
    },
    "bo_me_cho_ha_di_ca_no": {
        "id": "bo_me_cho_ha_di_ca_no",
        "wordVi": "Bố mẹ cho Hà đi ca nô.",
        "meaningVi": "Bé Hà được bố và mẹ dắt đi trải nghiệm ngồi xuồng ca nô lướt sóng vui vẻ.",
        "meaningsEn": [
            {
                "meaning": "Parents let Ha ride the motorboat.",
                "ipa": "/ˈperənts let hɑː raɪd ðə ˈmoʊtərbəʊt/",
                "partOfSpeech": "sentence"
            }
        ],
        "ipa": "/ɓoː˧˦ mɛː˧˨ tɕɔː˧˧ haː˨˩ ɗiː˧˧ kaː˧˧ noː˧˧/",
        "partOfSpeech": "Câu đọc",
        "audioVi": "/audio/vi/bo_me_cho_ha_di_ca_no.mp3",
        "audioEn": "/audio/en/us/bo_me_cho_ha_di_ca_no.mp3",
        "sourcePages": [4],
        "reviewStatus": "verified"
    },
    "b16_thoai_gioi_thieu": {
        "id": "b16_thoai_gioi_thieu",
        "wordVi": "Giới thiệu bản thân (Hello. My name is Nam...)",
        "meaningVi": "Cháu chào chú công an ạ! Cháu tên là Nam, học sinh lớp 1B8 trường Tiểu học Long Biên.",
        "meaningsEn": [
            {
                "meaning": "Hello. My name is Nam, and I am a student in class 1B8 at Long Bien Primary School.",
                "ipa": "/həˈloʊ maɪ neɪm ɪz næm ænd aɪ æm ə ˈstuːdənt ɪn klæs wʌn biː eɪt/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/tɕaʊ˧˦ tɕaːw˨˩ tɕuː˧˦ kəwŋ͡m˧˧ aːn˧˧ aː˧˨/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b16_thoai_gioi_thieu.mp3",
        "audioEn": "/audio/en/us/b16_thoai_gioi_thieu.mp3",
        "sourcePages": [4],
        "reviewStatus": "verified"
    },

    # === TOPIC 5: BÀI 28: Y y ===
    "y_ta": {
        "id": "y_ta",
        "wordVi": "y tá",
        "meaningVi": "Cô y tá mặc áo trắng tận tụy chăm sóc bệnh nhân và người già tại cơ sở y tế.",
        "meaningsEn": [
            {
                "meaning": "nurse",
                "ipa": "/nɜːrs/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/iː˧˧ taː˧˦/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/y_ta.mp3",
        "audioEn": "/audio/en/us/y_ta.mp3",
        "sourcePages": [5],
        "reviewStatus": "verified"
    },
    "da_quy": {
        "id": "da_quy",
        "wordVi": "dã quỳ",
        "meaningVi": "Hoa dã quỳ, loài hoa dại cánh vàng rực rỡ nở bừng trên các triền đồi núi cao.",
        "meaningsEn": [
            {
                "meaning": "wild sunflower",
                "ipa": "/waɪld ˈsʌnˌflaʊər/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/zaː˧˦ kwiː˨˩/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/da_quy.mp3",
        "audioEn": "/audio/en/us/da_quy.mp3",
        "sourcePages": [5],
        "reviewStatus": "verified"
    },
    "da_quy_gem": {
        "id": "da_quy_gem",
        "wordVi": "đá quý",
        "meaningVi": "Những viên đá quý lấp lánh sắc màu rực rỡ và vô cùng quý giá trong thiên nhiên.",
        "meaningsEn": [
            {
                "meaning": "gemstone / precious stone",
                "ipa": "/ˈdʒemstoʊn/",
                "partOfSpeech": "noun"
            }
        ],
        "ipa": "/ɗaː˧˦ kwiː˧˦/",
        "partOfSpeech": "Danh từ",
        "audioVi": "/audio/vi/da_quy_gem.mp3",
        "audioEn": "/audio/en/us/da_quy_gem.mp3",
        "sourcePages": [5],
        "reviewStatus": "verified"
    },
    "cau_doc_p28": {
        "id": "cau_doc_p28",
        "wordVi": "Mẹ và Hà ghé nhà dì Kha. Dì kể cho Hà nghe về bà. Hà chú ý nghe dì kể.",
        "meaningVi": "Đoạn văn ấm áp kể về chuyến thăm dì Kha của hai mẹ con bé Hà và câu chuyện về người bà thân yêu.",
        "meaningsEn": [
            {
                "meaning": "Mother and Ha stopped by aunt Kha's house. Aunt told Ha about grandmother. Ha listened attentively.",
                "ipa": "/ˈmʌðər ænd hɑː stɑːpt baɪ ænt kɑːz haʊs/",
                "partOfSpeech": "reading text"
            }
        ],
        "ipa": "/mɛː˧˨ vaː˨˩ haː˨˩ ɣɛː˧˦ ɲaː˨˩ ziː˨˩ kʰaː˧˧/",
        "partOfSpeech": "Đoạn đọc",
        "audioVi": "/audio/vi/cau_doc_p28.mp3",
        "audioEn": "/audio/en/us/cau_doc_p28.mp3",
        "sourcePages": [5],
        "reviewStatus": "verified"
    },
    "b28_thoai_1": {
        "id": "b28_thoai_1",
        "wordVi": "Cảm ơn bạn nhé! (Thank you)",
        "meaningVi": "Lời cảm ơn chân thành của bạn nhỏ khi được bạn che ô đi cùng dưới trời mưa tan trường.",
        "meaningsEn": [
            {
                "meaning": "Thank you (Sharing umbrella under rain)",
                "ipa": "/ˈθæŋk juː/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/kaːm˧˩ əːn˧˧ ɓaːn˧˨ ɲɛː˧˦/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b28_thoai_1.mp3",
        "audioEn": "/audio/en/us/b28_thoai_1.mp3",
        "sourcePages": [5],
        "reviewStatus": "verified"
    },
    "b28_thoai_2": {
        "id": "b28_thoai_2",
        "wordVi": "Cháu cảm ơn ông bà rất nhiều ạ! (Thank you so much)",
        "meaningVi": "Bạn nhỏ khoanh hai tay lễ phép nói lời cảm ơn ông bà khi được ông bà chúc mừng và trao quà.",
        "meaningsEn": [
            {
                "meaning": "Thank you so much, Grandmother and Grandfather",
                "ipa": "/ˈθæŋk juː soʊ mʌtʃ ˈɡrændˌmʌðər ænd ˈɡrændˌfɑːðər/",
                "partOfSpeech": "dialogue"
            }
        ],
        "ipa": "/tɕaʊ˧˦ kaːm˧˩ əːn˧˧ ăwŋ˧˧ ɓaː˨˩ zət˧˦ ɲiəw˨˩ aː˧˨/",
        "partOfSpeech": "Hội thoại",
        "audioVi": "/audio/vi/b28_thoai_2.mp3",
        "audioEn": "/audio/en/us/b28_thoai_2.mp3",
        "sourcePages": [5],
        "reviewStatus": "verified"
    }
}

# 2. BUILD PAGE OVERLAYS FOR THE 5 TOPICS
page_overlays = {
    "1": {
        "pageNumber": 1,
        "image": "/pages/topic_1.png",
        "overlays": [
            {"id": "ov_t1_c", "text": "c", "entryId": "c", "left": 24.8, "top": 44.8, "width": 3.2, "height": 4.8, "isKeyVocab": True},
            {"id": "ov_t1_ca_nuoc", "text": "ca", "entryId": "ca_nuoc", "left": 10.4, "top": 72.2, "width": 5.5, "height": 4.8, "isKeyVocab": True},
            {"id": "ov_t1_ca_tim", "text": "cà", "entryId": "ca_tim", "left": 22.8, "top": 72.2, "width": 5.5, "height": 4.8, "isKeyVocab": True},
            {"id": "ov_t1_ca", "text": "cá", "entryId": "ca", "left": 35.4, "top": 72.2, "width": 5.5, "height": 4.8, "isKeyVocab": True},
            {"id": "ov_t1_a_ca", "text": "A, cá.", "entryId": "a_ca", "left": 63.8, "top": 19.8, "width": 8.8, "height": 5.5, "isKeyVocab": True},
            {"id": "ov_t1_thoai_1", "text": "Tranh 1: Cháu chào bác ạ! (Good morning)", "entryId": "b3_thoai_1", "left": 56.4, "top": 57.8, "width": 18.6, "height": 37.0},
            {"id": "ov_t1_thoai_2", "text": "Tranh 2: Chào các bạn! (Hi)", "entryId": "b3_thoai_2", "left": 75.7, "top": 57.8, "width": 18.6, "height": 37.0}
        ],
        "vocabWordIds": ["ca_nuoc", "ca_tim", "ca", "c", "a_ca", "b3_thoai_1", "b3_thoai_2"]
    },
    "2": {
        "pageNumber": 2,
        "image": "/pages/topic_2.png",
        "overlays": [
            {"id": "ov_t2_bo", "text": "bò", "entryId": "con_bo", "left": 11.9, "top": 72.4, "width": 5.8, "height": 5.0, "isKeyVocab": True},
            {"id": "ov_t2_co_egret", "text": "cò", "entryId": "con_co", "left": 24.1, "top": 72.4, "width": 5.8, "height": 5.0, "isKeyVocab": True},
            {"id": "ov_t2_co_grass", "text": "cỏ", "entryId": "co", "left": 35.7, "top": 72.4, "width": 5.8, "height": 5.0, "isKeyVocab": True},
            {"id": "ov_t2_be_co_co", "text": "Bê có cỏ.", "entryId": "be_co_co", "left": 69.4, "top": 42.3, "width": 12.2, "height": 5.2, "isKeyVocab": True},
            {"id": "ov_t2_thoai_1", "text": "Tranh 1: Con chào mẹ ạ! (Hi, mom)", "entryId": "b6_thoai_1", "left": 56.1, "top": 58.8, "width": 18.9, "height": 36.8},
            {"id": "ov_t2_thoai_2", "text": "Tranh 2: Cháu chào ông bà ạ! (Good afternoon)", "entryId": "b6_thoai_2", "left": 75.7, "top": 58.8, "width": 18.9, "height": 36.8}
        ],
        "vocabWordIds": ["con_bo", "con_co", "co", "be_co_co", "b6_thoai_1", "b6_thoai_2"]
    },
    "3": {
        "pageNumber": 3,
        "image": "/pages/topic_3.png",
        "overlays": [
            {"id": "ov_t3_title", "text": "Đàn kiến con ngoan ngoãn", "entryId": "dan_kien_title", "left": 62.4, "top": 22.3, "width": 23.8, "height": 4.8, "isKeyVocab": True},
            {"id": "ov_t3_tranh_1", "text": "Tranh 1: Bà kiến sống ở đâu?", "entryId": "kien_tranh_1", "left": 54.4, "top": 27.8, "width": 19.7, "height": 29.4},
            {"id": "ov_t3_tranh_2", "text": "Tranh 2: Khiêng bà kiến bằng chiếc lá đa", "entryId": "kien_tranh_2", "left": 74.9, "top": 27.8, "width": 19.7, "height": 29.4},
            {"id": "ov_t3_tranh_3", "text": "Tranh 3: Đưa bà kiến đến nơi thoáng mát", "entryId": "kien_tranh_3", "left": 54.4, "top": 60.8, "width": 19.7, "height": 29.4},
            {"id": "ov_t3_tranh_4", "text": "Tranh 4: Được ở nhà mới, bà kiến cảm ơn", "entryId": "kien_tranh_4", "left": 74.9, "top": 60.8, "width": 19.7, "height": 29.4},
            {"id": "ov_t3_bo_co", "text": "bó cỏ", "entryId": "bo_co", "left": 19.4, "top": 44.8, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_ca_co", "text": "cá cờ", "entryId": "ca_co", "left": 4.9, "top": 51.3, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_bo_de", "text": "bờ đê", "entryId": "bo_de", "left": 25.4, "top": 55.3, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_do_ba", "text": "đỡ bà", "entryId": "do_ba", "left": 36.4, "top": 51.3, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_co_do", "text": "cờ đỏ", "entryId": "co_do", "left": 12.4, "top": 62.3, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_do_do", "text": "đỗ đỏ", "entryId": "do_do", "left": 30.4, "top": 67.8, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_do_be", "text": "đỡ bé", "entryId": "do_be", "left": 14.4, "top": 73.8, "width": 6.7, "height": 4.0, "isKeyVocab": True},
            {"id": "ov_t3_cau_1", "text": "Bờ đê có dế.", "entryId": "cau_bo_de_co_de", "left": 7.9, "top": 82.3, "width": 13.2, "height": 4.7, "isKeyVocab": True},
            {"id": "ov_t3_cau_2", "text": "Bà có đỗ đỏ.", "entryId": "cau_ba_co_do_do", "left": 23.4, "top": 82.3, "width": 13.2, "height": 4.7, "isKeyVocab": True}
        ],
        "vocabWordIds": [
            "dan_kien_title", "kien_tranh_1", "kien_tranh_2", "kien_tranh_3", "kien_tranh_4",
            "bo_co", "ca_co", "bo_de", "do_ba", "co_do", "do_do", "do_be",
            "cau_bo_de_co_de", "cau_ba_co_do_do"
        ]
    },
    "4": {
        "pageNumber": 4,
        "image": "/pages/topic_4.png",
        "overlays": [
            {"id": "ov_t4_ca_me", "text": "cá mè", "entryId": "ca_me", "left": 7.9, "top": 72.6, "width": 7.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t4_la_me", "text": "lá me", "entryId": "la_me", "left": 16.9, "top": 72.6, "width": 7.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t4_no_do", "text": "nơ đỏ", "entryId": "no_do", "left": 25.9, "top": 72.6, "width": 7.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t4_ca_no", "text": "ca nô", "entryId": "ca_no", "left": 35.9, "top": 72.6, "width": 7.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t4_bo_me", "text": "Bố mẹ cho Hà đi ca nô.", "entryId": "bo_me_cho_ha_di_ca_no", "left": 64.4, "top": 35.8, "width": 19.7, "height": 5.0, "isKeyVocab": True},
            {"id": "ov_t4_thoai_gioi_thieu", "text": "Giới thiệu bản thân (Hello. My name is Nam...)", "entryId": "b16_thoai_gioi_thieu", "left": 53.4, "top": 51.2, "width": 41.8, "height": 41.8}
        ],
        "vocabWordIds": ["ca_me", "la_me", "no_do", "ca_no", "bo_me_cho_ha_di_ca_no", "b16_thoai_gioi_thieu"]
    },
    "5": {
        "pageNumber": 5,
        "image": "/pages/topic_5.png",
        "overlays": [
            {"id": "ov_t5_y_ta", "text": "y tá", "entryId": "y_ta", "left": 11.4, "top": 71.8, "width": 6.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t5_da_quy", "text": "dã quỳ", "entryId": "da_quy", "left": 23.9, "top": 71.8, "width": 7.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t5_da_quy_gem", "text": "đá quý", "entryId": "da_quy_gem", "left": 35.7, "top": 71.8, "width": 7.7, "height": 4.4, "isKeyVocab": True},
            {"id": "ov_t5_cau_doc", "text": "Mẹ và Hà ghé nhà dì Kha. Dì kể cho Hà nghe về bà. Hà chú ý nghe dì kể.", "entryId": "cau_doc_p28", "left": 56.4, "top": 39.8, "width": 40.7, "height": 7.8, "isKeyVocab": True},
            {"id": "ov_t5_thoai_1", "text": "Tranh 1: Cảm ơn bạn nhé! (Thank you)", "entryId": "b28_thoai_1", "left": 57.4, "top": 58.8, "width": 18.9, "height": 36.8},
            {"id": "ov_t5_thoai_2", "text": "Tranh 2: Cháu cảm ơn ông bà rất nhiều ạ!", "entryId": "b28_thoai_2", "left": 76.9, "top": 58.8, "width": 18.9, "height": 36.8}
        ],
        "vocabWordIds": ["y_ta", "da_quy", "da_quy_gem", "cau_doc_p28", "b28_thoai_1", "b28_thoai_2"]
    }
}

with open('src/data/entries.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)
print(f"Wrote {len(entries)} entries to src/data/entries.json")

with open('src/data/page_overlays.json', 'w', encoding='utf-8') as f:
    json.dump(page_overlays, f, ensure_ascii=False, indent=2)
print(f"Wrote {len(page_overlays)} topic pages to src/data/page_overlays.json")
