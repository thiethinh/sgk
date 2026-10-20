import sys
import json
import asyncio
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')

entries_file = Path('src/data/entries.json')
overlays_file = Path('src/data/page_overlays.json')
ocr_dir = Path('data/ocr')

# 1. Existing entries
with open(entries_file, encoding='utf-8') as f:
    entries = json.load(f)

# 2. Define all new vocabulary entries
new_entries = {
    "ba_ba": {
        "id": "ba_ba",
        "wordVi": "ba ba",
        "meaningsEn": [{"meaning": "softshell turtle", "ipa": "/ˈsɒft.ʃel ˈtɜː.tl/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Loài bò sát có mai mềm sống ở nước ngọt, bơi rất giỏi.",
        "exampleVi": "Bé nhìn thấy con ba ba bơi dưới nước.",
        "sourcePages": [17, 23],
        "audioVi": "/audio/vi/ba_ba.mp3",
        "audioEn": "/audio/en/us/ba_ba.mp3"
    },
    "ca_nuoc": {
        "id": "ca_nuoc",
        "wordVi": "ca",
        "meaningsEn": [{"meaning": "cup", "ipa": "/kʌp/"}, {"meaning": "mug", "ipa": "/mʌɡ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc ca nhỏ có quai cầm dùng để múc và uống nước.",
        "exampleVi": "Bé dùng ca sạch để uống nước.",
        "sourcePages": [19],
        "audioVi": "/audio/vi/ca_nuoc.mp3",
        "audioEn": "/audio/en/us/ca_nuoc.mp3"
    },
    "ca_tim": {
        "id": "ca_tim",
        "wordVi": "cà",
        "meaningsEn": [{"meaning": "eggplant", "ipa": "/ˈeɡ.plɑːnt/"}, {"meaning": "aubergine", "ipa": "/ˈoʊ.bɚ.ʒiːn/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Quả cà màu tím hoặc trắng dùng để nấu những món ăn ngon.",
        "exampleVi": "Mẹ đi chợ mua quả cà tím.",
        "sourcePages": [19],
        "audioVi": "/audio/vi/ca_tim.mp3",
        "audioEn": "/audio/en/us/ca_tim.mp3"
    },
    "con_be": {
        "id": "con_be",
        "wordVi": "bê",
        "meaningsEn": [{"meaning": "calf", "ipa": "/kæf/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Con bò con mới lớn, rất ngoan ngoãn và đáng yêu.",
        "exampleVi": "Chú bê con tung tăng theo mẹ trên đồng cỏ.",
        "sourcePages": [21],
        "audioVi": "/audio/vi/con_be.mp3",
        "audioEn": "/audio/en/us/con_be.mp3"
    },
    "be_ca": {
        "id": "be_ca",
        "wordVi": "bể cá",
        "meaningsEn": [{"meaning": "aquarium", "ipa": "/əˈkweə.ri.əm/"}, {"meaning": "fish tank", "ipa": "/ˈfɪʃ ˌtæŋk/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Bể kính trong suốt chứa nước để nuôi những chú cá cảnh xinh xắn.",
        "exampleVi": "Bé thích ngắm cá bơi lội trong bể cá.",
        "sourcePages": [23],
        "audioVi": "/audio/vi/be_ca.mp3",
        "audioEn": "/audio/en/us/be_ca.mp3"
    },
    "con_co": {
        "id": "con_co",
        "wordVi": "cò",
        "meaningsEn": [{"meaning": "stork", "ipa": "/stɔːrk/"}, {"meaning": "egret", "ipa": "/ˈiː.ɡrət/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Loài chim có bộ lông trắng tinh, chân dài và mỏ nhọn lội trên đồng cỏ.",
        "exampleVi": "Con cò trắng bay lả bay la trên cánh đồng.",
        "sourcePages": [25, 26],
        "audioVi": "/audio/vi/con_co.mp3",
        "audioEn": "/audio/en/us/con_co.mp3"
    },
    "bo_bien": {
        "id": "bo_bien",
        "wordVi": "bờ",
        "meaningsEn": [{"meaning": "shore", "ipa": "/ʃɔːr/"}, {"meaning": "bank", "ipa": "/bæŋk/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Phần đất ven mép nước như bờ sông, bờ hồ hoặc bờ biển.",
        "exampleVi": "Bé ngồi hóng gió mát bên bờ hồ.",
        "sourcePages": [27],
        "audioVi": "/audio/vi/bo_bien.mp3",
        "audioEn": "/audio/en/us/bo_bien.mp3"
    },
    "con_de": {
        "id": "con_de",
        "wordVi": "dê",
        "meaningsEn": [{"meaning": "goat", "ipa": "/ɡoʊt/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Con vật ăn cỏ có đôi tai vểnh, râu dài và đôi sừng cong xinh.",
        "exampleVi": "Chú dê con kêu be be trên sườn đồi.",
        "sourcePages": [29],
        "audioVi": "/audio/vi/con_de.mp3",
        "audioEn": "/audio/en/us/con_de.mp3"
    },
    "con_do": {
        "id": "con_do",
        "wordVi": "đò",
        "meaningsEn": [{"meaning": "boat", "ipa": "/boʊt/"}, {"meaning": "ferry", "ipa": "/ˈfer.i/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Thuyền chở người qua sông nhẹ nhàng trên dòng nước.",
        "exampleVi": "Bác lái đò chở khách sang sông.",
        "sourcePages": [29, 35],
        "audioVi": "/audio/vi/con_do.mp3",
        "audioEn": "/audio/en/us/con_do.mp3"
    },
    "bi_do": {
        "id": "bi_do",
        "wordVi": "bí đỏ",
        "meaningsEn": [{"meaning": "pumpkin", "ipa": "/ˈpʌmp.kɪn/"}, {"meaning": "squash", "ipa": "/skwɑːʃ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Quả bí ngô có ruột màu vàng đỏ ngọt bùi, nấu canh rất bổ dưỡng.",
        "exampleVi": "Mẹ nấu món canh bí đỏ thơm ngon cho cả nhà.",
        "sourcePages": [35],
        "audioVi": "/audio/vi/bi_do.mp3",
        "audioEn": "/audio/en/us/bi_do.mp3"
    },
    "ke_o": {
        "id": "ke_o",
        "wordVi": "kẻ ô",
        "meaningsEn": [{"meaning": "draw a grid", "ipa": "/drɔː ə ɡrɪd/"}],
        "partOfSpeech": "động từ",
        "definitionVi": "Dùng bút và thước kẻ những đường ô vuông thẳng tắp.",
        "exampleVi": "Bé tập kẻ ô vuông ngay ngắn trong vở.",
        "sourcePages": [35],
        "audioVi": "/audio/vi/ke_o.mp3",
        "audioEn": "/audio/en/us/ke_o.mp3"
    },
    "di_do": {
        "id": "di_do",
        "wordVi": "đi đò",
        "meaningsEn": [{"meaning": "ride a boat", "ipa": "/raɪd ə boʊt/"}],
        "partOfSpeech": "động từ",
        "definitionVi": "Ngồi trên con thuyền đò để sang bờ sông bên kia.",
        "exampleVi": "Bé được cùng mẹ đi đò ngắm cảnh quê hương.",
        "sourcePages": [35],
        "audioVi": "/audio/vi/di_do.mp3",
        "audioEn": "/audio/en/us/di_do.mp3"
    },
    "la_do": {
        "id": "la_do",
        "wordVi": "lá đỏ",
        "meaningsEn": [{"meaning": "red leaf", "ipa": "/red liːf/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc lá cây chuyển màu đỏ thắm tuyệt đẹp khi vào mùa thu.",
        "exampleVi": "Bé nhặt chiếc lá đỏ rơi trên sân trường.",
        "sourcePages": [37],
        "audioVi": "/audio/vi/la_do.mp3",
        "audioEn": "/audio/en/us/la_do.mp3"
    },
    "bo_ho": {
        "id": "bo_ho",
        "wordVi": "bờ hồ",
        "meaningsEn": [{"meaning": "lakeside", "ipa": "/ˈleɪk.saɪd/"}, {"meaning": "lakeshore", "ipa": "/ˈleɪk.ʃɔːr/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Dải đất ven hồ nước có cây xanh bóng mát.",
        "exampleVi": "Mọi người đi dạo thư thái quanh bờ hồ.",
        "sourcePages": [37, 43],
        "audioVi": "/audio/vi/bo_ho.mp3",
        "audioEn": "/audio/en/us/bo_ho.mp3"
    },
    "ho_du": {
        "id": "ho_du",
        "wordVi": "hổ dữ",
        "meaningsEn": [{"meaning": "ferocious tiger", "ipa": "/fəˈroʊ.ʃəs ˈtaɪ.ɡɚ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chú hổ to khỏe hung dữ được mệnh danh chúa sơn lâm.",
        "exampleVi": "Bé biết hổ dữ là loài thú săn mồi trong rừng.",
        "sourcePages": [39, 40],
        "audioVi": "/audio/vi/ho_du.mp3",
        "audioEn": "/audio/en/us/ho_du.mp3"
    },
    "la_kho": {
        "id": "la_kho",
        "wordVi": "lá khô",
        "meaningsEn": [{"meaning": "dry leaf", "ipa": "/draɪ liːf/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc lá úa vàng khô giòn rụng dưới gốc cây.",
        "exampleVi": "Gió thổi làm lá khô xào xạc trên mặt đất.",
        "sourcePages": [41, 43],
        "audioVi": "/audio/vi/la_kho.mp3",
        "audioEn": "/audio/en/us/la_kho.mp3"
    },
    "ca_me": {
        "id": "ca_me",
        "wordVi": "cá mè",
        "meaningsEn": [{"meaning": "silver carp", "ipa": "/ˈsɪl.vɚ kɑːrp/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Loài cá sống ở ao hồ, có vảy trắng sáng và bơi nhanh.",
        "exampleVi": "Bác nông dân thả đàn cá mè vào ao nhỏ.",
        "sourcePages": [45],
        "audioVi": "/audio/vi/ca_me.mp3",
        "audioEn": "/audio/en/us/ca_me.mp3"
    },
    "la_me": {
        "id": "la_me",
        "wordVi": "lá me",
        "meaningsEn": [{"meaning": "tamarind leaf", "ipa": "/ˈtæm.ə.rɪnd liːf/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc lá nhỏ li ti của cây me có vị chua thanh dịu mát.",
        "exampleVi": "Những chiếc lá me non xanh mướt đu đưa trong gió.",
        "sourcePages": [45],
        "audioVi": "/audio/vi/la_me.mp3",
        "audioEn": "/audio/en/us/la_me.mp3"
    },
    "ga_go": {
        "id": "ga_go",
        "wordVi": "gà gô",
        "meaningsEn": [{"meaning": "partridge", "ipa": "/ˈpɑːr.trɪdʒ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Loài gà rừng nhỏ có bộ lông lốm đốm màu xám nâu.",
        "exampleVi": "Chú gà gô kiếm ăn lặng lẽ trong lùm cây.",
        "sourcePages": [47],
        "audioVi": "/audio/vi/ga_go.mp3",
        "audioEn": "/audio/en/us/ga_go.mp3"
    },
    "do_go": {
        "id": "do_go",
        "wordVi": "đồ gỗ",
        "meaningsEn": [{"meaning": "wooden furniture", "ipa": "/ˈwʊd.ən ˈfɝː.nɪ.tʃɚ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Bàn ghế, tủ giường và các vật dụng làm bằng gỗ bền đẹp.",
        "exampleVi": "Nhà bé có nhiều món đồ gỗ sáng bóng.",
        "sourcePages": [47],
        "audioVi": "/audio/vi/do_go.mp3",
        "audioEn": "/audio/en/us/do_go.mp3"
    },
    "gia_do": {
        "id": "gia_do",
        "wordVi": "giá đỗ",
        "meaningsEn": [{"meaning": "bean sprouts", "ipa": "/ˈbiːn ˌspraʊts/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Mầm hạt đỗ xanh trắng mọng nước, dùng nấu canh hoặc xào rất mát.",
        "exampleVi": "Mẹ làm món rau xào giá đỗ giòn ngọt.",
        "sourcePages": [47, 53],
        "audioVi": "/audio/vi/gia_do.mp3",
        "audioEn": "/audio/en/us/gia_do.mp3"
    },
    "cu_gia": {
        "id": "cu_gia",
        "wordVi": "củ già",
        "meaningsEn": [{"meaning": "mature root", "ipa": "/məˈtʃʊr ruːt/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Củ cây thu hoạch khi đã già dặn, đậm đà hương vị.",
        "exampleVi": "Bà chọn củ gừng già thơm nồng để đun trà.",
        "sourcePages": [47],
        "audioVi": "/audio/vi/cu_gia.mp3",
        "audioEn": "/audio/en/us/cu_gia.mp3"
    },
    "ghe_da": {
        "id": "ghe_da",
        "wordVi": "ghế đá",
        "meaningsEn": [{"meaning": "stone bench", "ipa": "/stoʊn bentʃ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc ghế dài chắc chắn làm bằng đá đặt dưới bóng mát cây xanh.",
        "exampleVi": "Giờ ra chơi, bé ngồi nghỉ ngơi trên ghế đá.",
        "sourcePages": [49],
        "audioVi": "/audio/vi/ghe_da.mp3",
        "audioEn": "/audio/en/us/ghe_da.mp3"
    },
    "nha_go": {
        "id": "nha_go",
        "wordVi": "nhà gỗ",
        "meaningsEn": [{"meaning": "wooden house", "ipa": "/ˈwʊd.ən haʊs/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Ngôi nhà làm từ gỗ mát mẻ vào mùa hè và ấm áp vào mùa đông.",
        "exampleVi": "Quê nội có ngôi nhà gỗ cổ kính bên dòng suối.",
        "sourcePages": [49],
        "audioVi": "/audio/vi/nha_go.mp3",
        "audioEn": "/audio/en/us/nha_go.mp3"
    },
    "la_nho": {
        "id": "la_nho",
        "wordVi": "lá nho",
        "meaningsEn": [{"meaning": "grape leaf", "ipa": "/ɡreɪp liːf/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc lá xanh mướt của giàn nho sai trĩu quả.",
        "exampleVi": "Giàn lá nho xum xuê che mát một góc sân.",
        "sourcePages": [49],
        "audioVi": "/audio/vi/la_nho.mp3",
        "audioEn": "/audio/en/us/la_nho.mp3"
    },
    "nga_ba": {
        "id": "nga_ba",
        "wordVi": "ngã ba",
        "meaningsEn": [{"meaning": "three-way junction", "ipa": "/ˈθriː.weɪ ˈdʒʌŋk.ʃən/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Nơi con đường rẽ sang ba ngả khác nhau.",
        "exampleVi": "Đến ngã ba, bé chú ý quan sát trước khi rẽ.",
        "sourcePages": [51],
        "audioVi": "/audio/vi/nga_ba.mp3",
        "audioEn": "/audio/en/us/nga_ba.mp3"
    },
    "cu_nghe": {
        "id": "cu_nghe",
        "wordVi": "củ nghệ",
        "meaningsEn": [{"meaning": "turmeric", "ipa": "/ˈtɝː.mər.ɪk/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Loại củ có ruột vàng cam thơm lừng, dùng làm gia vị thơm ngon.",
        "exampleVi": "Củ nghệ giúp món cá kho có màu vàng óng.",
        "sourcePages": [51],
        "audioVi": "/audio/vi/cu_nghe.mp3",
        "audioEn": "/audio/en/us/cu_nghe.mp3"
    },
    "nghi_he": {
        "id": "nghi_he",
        "wordVi": "nghỉ hè",
        "meaningsEn": [{"meaning": "summer vacation", "ipa": "/ˈsʌm.ɚ veɪˈkeɪ.ʃən/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Kỳ nghỉ vui tươi sau một năm học chăm chỉ của các bạn học sinh.",
        "exampleVi": "Nghỉ hè, bé được về quê thăm ông bà.",
        "sourcePages": [51, 53],
        "audioVi": "/audio/vi/nghi_he.mp3",
        "audioEn": "/audio/en/us/nghi_he.mp3"
    },
    "nha_ga": {
        "id": "nha_ga",
        "wordVi": "nhà ga",
        "meaningsEn": [{"meaning": "train station", "ipa": "/ˈtreɪn ˌsteɪ.ʃən/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Nơi xe lửa dừng đón và trả hành khách đi xa.",
        "exampleVi": "Đoàn tàu hỏa rúc còi tiến vào nhà ga.",
        "sourcePages": [53],
        "audioVi": "/audio/vi/nha_ga.mp3",
        "audioEn": "/audio/en/us/nha_ga.mp3"
    },
    "bap_ngo": {
        "id": "bap_ngo",
        "wordVi": "bắp ngô",
        "meaningsEn": [{"meaning": "corn cob", "ipa": "/ˈkɔːrn ˌkɑːb/"}, {"meaning": "maize", "ipa": "/meɪz/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Bắp ngô vàng óng có hàng hạt đều tăm tắp, luộc ăn ngọt bùi.",
        "exampleVi": "Bé thích ăn bắp ngô luộc nóng hổi vào buổi sáng.",
        "sourcePages": [53],
        "audioVi": "/audio/vi/bap_ngo.mp3",
        "audioEn": "/audio/en/us/bap_ngo.mp3"
    },
    "chu_so": {
        "id": "chu_so",
        "wordVi": "chữ số",
        "meaningsEn": [{"meaning": "digit", "ipa": "/ˈdɪdʒ.ɪt/"}, {"meaning": "number", "ipa": "/ˈnʌm.bɚ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Ký hiệu các con số toán học giúp bé tập đếm.",
        "exampleVi": "Bé tập viết các chữ số từ một đến mười.",
        "sourcePages": [55],
        "audioVi": "/audio/vi/chu_so.mp3",
        "audioEn": "/audio/en/us/chu_so.mp3"
    },
    "ga_ri": {
        "id": "ga_ri",
        "wordVi": "gà ri",
        "meaningsEn": [{"meaning": "small native chicken", "ipa": "/smɔːl ˈneɪ.tɪv ˈtʃɪk.ɪn/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Giống gà ri nhỏ nhắn, mổ thóc lách cách quanh sân.",
        "exampleVi": "Đàn gà ri theo mẹ bới giun ngoài vườn.",
        "sourcePages": [56],
        "audioVi": "/audio/vi/ga_ri.mp3",
        "audioEn": "/audio/en/us/ga_ri.mp3"
    },
    "chu_he": {
        "id": "chu_he",
        "wordVi": "chú hề",
        "meaningsEn": [{"meaning": "clown", "ipa": "/klaʊn/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Người nghệ sĩ xiếc vui tính với chiếc mũi đỏ và bộ áo sặc sỡ.",
        "exampleVi": "Chú hề tung hứng bóng làm các bé cười thích thú.",
        "sourcePages": [43],
        "audioVi": "/audio/vi/chu_he.mp3",
        "audioEn": "/audio/en/us/chu_he.mp3"
    },
    "ca_co": {
        "id": "ca_co",
        "wordVi": "cá cờ",
        "meaningsEn": [{"meaning": "sailfish", "ipa": "/ˈseɪl.fɪʃ/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Loài cá biển nhanh nhẹn có vây lưng to cao như lá cờ.",
        "exampleVi": "Chú cá cờ bơi vút qua làn nước biển xanh.",
        "sourcePages": [31, 33, 43],
        "audioVi": "/audio/vi/ca_co.mp3",
        "audioEn": "/audio/en/us/ca_co.mp3"
    },
    "ghe_go": {
        "id": "ghe_go",
        "wordVi": "ghế gỗ",
        "meaningsEn": [{"meaning": "wooden chair", "ipa": "/ˈwʊd.ən tʃer/"}],
        "partOfSpeech": "danh từ",
        "definitionVi": "Chiếc ghế ngồi làm bằng gỗ chắc chắn và sạch sẽ.",
        "exampleVi": "Bé ngồi học bài ngay ngắn trên chiếc ghế gỗ.",
        "sourcePages": [49, 53],
        "audioVi": "/audio/vi/ghe_go.mp3",
        "audioEn": "/audio/en/us/ghe_go.mp3"
    }
}

for k, v in new_entries.items():
    entries[k] = v

with open(entries_file, 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"Updated entries.json: total {len(entries)} entries.")
