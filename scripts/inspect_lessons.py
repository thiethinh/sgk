import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

lesson_pages = [
    (15, 16, "Bài 1: A a"),
    (17, 18, "Bài 2: B b"),
    (19, 20, "Bài 3: C c"),
    (21, 22, "Bài 4: E e, Ê ê"),
    (23, 24, "Bài 5: Ôn tập và kể chuyện"),
    (25, 26, "Bài 6: O o"),
    (27, 28, "Bài 7: Ô ô, Ơ ơ"),
    (29, 30, "Bài 8: D d, Đ đ"),
    (31, 32, "Bài 9: Ôn tập dấu hỏi, dấu nặng"),
    (33, 34, "Bài 10: Ôn tập và kể chuyện"),
    (35, 36, "Bài 11: I i, K k"),
    (37, 38, "Bài 12: H h, L l"),
    (39, 40, "Bài 13: U u, Ư ư"),
    (41, 42, "Bài 14: Ch ch, Kh kh"),
    (43, 44, "Bài 15: Ôn tập và kể chuyện"),
    (45, 46, "Bài 16: M m, N n"),
    (47, 48, "Bài 17: G g, Gi gi"),
    (49, 50, "Bài 18: Gh gh, Nh nh"),
    (51, 52, "Bài 19: Ng ng, Ngh ngh"),
    (53, 54, "Bài 20: Ôn tập và kể chuyện"),
    (55, 56, "Bài 21: R r, S s")
]

for p1, p2, title in lesson_pages:
    print(f"\n==================== {title} (Trang PDF {p1}-{p2}) ====================")
    for p in (p1, p2):
        with open(f"data/ocr/page_{p:03d}.json", encoding='utf-8') as f:
            d = json.load(f)
            items = [it['text'] for it in d['items']]
            print(f"--- Page {p} ---: " + " | ".join(items))
