import asyncio
import os
from pathlib import Path
import edge_tts

VI_VOICE = "vi-VN-HoaiMyNeural"
EN_VOICE = "en-US-JennyNeural"

vi_dir = Path("public/audio/vi")
en_dir = Path("public/audio/en/us")

vi_dir.mkdir(parents=True, exist_ok=True)
en_dir.mkdir(parents=True, exist_ok=True)

# Audio items: (entry_id, vi_text, en_text)
audio_items = [
    # TOPIC 1
    ("c", "cờ", "Letter C"),
    ("ca_nuoc", "ca", "cup"),
    ("ca_tim", "cà", "eggplant"),
    ("ca", "cá", "fish"),
    ("a_ca", "A, cá.", "Wow, fishes!"),
    ("b3_thoai_1", "Cháu chào bác ạ!", "Good morning"),
    ("b3_thoai_2", "Chào các bạn!", "Hi"),
    
    # TOPIC 2
    ("con_bo", "bò", "cow"),
    ("con_co", "cò", "egret"),
    ("co", "cỏ", "grass"),
    ("be_co_co", "Bê có cỏ.", "The calf has grass."),
    ("b6_thoai_1", "Con chào mẹ ạ!", "Hi, mom"),
    ("b6_thoai_2", "Cháu chào ông, cháu chào bà ạ!", "Good afternoon, Grandmother. Good afternoon, Grandfather."),
    
    # TOPIC 3
    ("dan_kien_title", "Đàn kiến con ngoan ngoãn", "The Well-Behaved Little Ants"),
    ("kien_tranh_1", "Bà kiến đã già, một mình ở trong cái tổ nhỏ chật hẹp, ẩm ướt. Mấy hôm nay, bà đau ốm cứ rên hừ hừ.", "Old mother ant lived alone in a small, damp nest. These days, she was sick and groaned in pain."),
    ("kien_tranh_2", "Đàn kiến con đi ngang qua, thấy vậy bèn giúp đỡ bà. Chúng tha về một chiếc lá đa vàng mới rụng, dìu bà ngồi trên đó, rồi lại cùng ghé vai khiêng chiếc lá đến chỗ đầy ánh nắng và thoáng mát.", "The little ants carried a yellow banyan leaf, helped her sit on it, and carried her to a sunny, breezy spot."),
    ("kien_tranh_3", "Rồi chúng chia nhau đi tìm nhà mới cho bà kiến. Cả đàn xúm vào khiêng chiếc lá, đưa bà kiến lên một ụ đất cao ráo.", "Then they searched for a new home and carried her up to a dry, sunny hillock."),
    ("kien_tranh_4", "Bà kiến được ở nhà mới sung sướng quá, nói với đàn kiến con: “Nhờ các cháu giúp đỡ, bà được đi tắm nắng lại được ở nhà mới cao ráo, đẹp đẽ. Bà thấy khỏe hơn nhiều lắm rồi. Các cháu ngoan lắm! Bà cảm ơn các cháu thật nhiều!”.", "Old mother ant rejoiced in her new home and said: “Thanks to your help, I can sunbathe and live in a high, dry, beautiful home. I feel much healthier now. You are very good children! Thank you so much!”"),
    ("bo_co", "bó cỏ", "bundle of grass"),
    ("ca_co", "cá cờ", "fighting fish"),
    ("bo_de", "bờ đê", "dike"),
    ("do_ba", "đỡ bà", "help grandmother"),
    ("co_do", "cờ đỏ", "red flag"),
    ("do_do", "đỗ đỏ", "red beans"),
    ("do_be", "đỡ bé", "support the baby"),
    ("cau_bo_de_co_de", "Bờ đê có dế.", "There are crickets on the dike."),
    ("cau_ba_co_do_do", "Bà có đỗ đỏ.", "Grandmother has red beans."),

    # TOPIC 4
    ("ca_me", "cá mè", "carp"),
    ("la_me", "lá me", "tamarind leaf"),
    ("no_do", "nơ đỏ", "red bow"),
    ("ca_no", "ca nô", "motorboat"),
    ("bo_me_cho_ha_di_ca_no", "Bố mẹ cho Hà đi ca nô.", "Parents let Ha ride the motorboat."),
    ("b16_thoai_gioi_thieu", "Cháu chào chú ạ! Cháu tên là Nam, học sinh lớp 1B8 trường Tiểu học Long Biên.", "Hello. My name is Nam, and I am a student in class 1B8 at Long Bien Primary School."),

    # TOPIC 5
    ("y_ta", "y tá", "nurse"),
    ("da_quy", "dã quỳ", "wild sunflower"),
    ("da_quy_gem", "đá quý", "gemstone"),
    ("cau_doc_p28", "Mẹ và Hà ghé nhà dì Kha. Dì kể cho Hà nghe về bà. Hà chú ý nghe dì kể.", "Mother and Ha stopped by aunt Kha's house. Aunt told Ha about grandmother. Ha listened attentively to her aunt."),
    ("b28_thoai_1", "Cảm ơn bạn nhé!", "Thank you"),
    ("b28_thoai_2", "Cháu cảm ơn ông bà rất nhiều ạ!", "Thank you so much, Grandmother and Grandfather"),
]

async def generate(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))
    print(f"  + Generated: {out_path.name}")

async def main():
    print(f"Total audio pairs to generate: {len(audio_items)}")
    for entry_id, vi_text, en_text in audio_items:
        vi_p = vi_dir / f"{entry_id}.mp3"
        en_p = en_dir / f"{entry_id}.mp3"
        
        # force generate to ensure top audio quality
        await generate(vi_text, VI_VOICE, vi_p)
        await generate(en_text, EN_VOICE, en_p)
        await asyncio.sleep(0.15)
        
    print("ALL AUDIOS SUCCESSFULLY GENERATED!")

if __name__ == '__main__':
    asyncio.run(main())
