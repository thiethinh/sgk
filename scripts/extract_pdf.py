import fitz
import os
import json
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
import time

def process_pdf(pdf_path='sgk1_t1.pdf'):
    os.makedirs('data/source', exist_ok=True)
    os.makedirs('data/extracted/pages', exist_ok=True)
    os.makedirs('data/ocr', exist_ok=True)
    os.makedirs('data/reports', exist_ok=True)
    os.makedirs('data/markdown', exist_ok=True)
    os.makedirs('data/review', exist_ok=True)

    source_meta = {
        "file": pdf_path,
        "title": "Tiếng Việt 1 - Tập Một (Kết nối tri thức với cuộc sống)",
        "publisher": "Nhà xuất bản Giáo dục Việt Nam",
        "authors": [
            "Bùi Mạnh Hùng (Tổng Chủ biên kiêm Chủ biên)",
            "Lê Thị Lan Anh",
            "Nguyễn Thị Ngân Hoa",
            "Vũ Thị Thanh Hương",
            "Vũ Thị Lan"
        ],
        "total_pages": 0,
        "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    source_meta["total_pages"] = total_pages

    with open('data/source/metadata.json', 'w', encoding='utf-8') as f:
        json.dump(source_meta, f, ensure_ascii=False, indent=2)

    print(f"Loaded {pdf_path}: {total_pages} pages")
    engine = RapidOCR()

    page_reports = []

    for i in range(total_pages):
        page_num = i + 1
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img_path = f"data/extracted/pages/page_{page_num:03d}.png"
        pix.save(img_path)

        # Convert to numpy array for OCR
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_result, elapse = engine(np.array(img))

        extracted_items = []
        full_text_lines = []
        if ocr_result:
            for item in ocr_result:
                bbox, text, score = item
                extracted_items.append({
                    "bbox": [[float(c) for c in pt] for pt in bbox],
                    "text": text,
                    "score": float(score)
                })
                full_text_lines.append(text)

        # Save OCR JSON
        ocr_json_path = f"data/ocr/page_{page_num:03d}.json"
        with open(ocr_json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "page": page_num,
                "width": pix.width,
                "height": pix.height,
                "items": extracted_items
            }, f, ensure_ascii=False, indent=2)

        # Save Raw Text
        txt_path = f"data/extracted/page_{page_num:03d}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(full_text_lines))

        page_reports.append({
            "page": page_num,
            "width": pix.width,
            "height": pix.height,
            "items_count": len(extracted_items),
            "char_count": sum(len(x) for x in full_text_lines),
            "preview": " | ".join(full_text_lines[:4]) if full_text_lines else "(No text detected)"
        })

        if page_num % 10 == 0 or page_num == total_pages:
            print(f"Processed page {page_num}/{total_pages} (lines: {len(extracted_items)})")

    # Generate Extraction Report
    report_md = [
        "# Báo Cáo Trích Xuất và Phân Loại Toàn Bộ PDF (sgk1_t1.pdf)",
        "",
        f"- **Tập tin:** `{pdf_path}`",
        f"- **Tổng số trang:** {total_pages}",
        f"- **Thời gian xử lý:** {source_meta['processed_at']}",
        "- **Phân loại định dạng PDF:** 100% Scanned / Raster image (Không có text stream vector, mỗi trang là 1 ảnh DeviceRGB độ phân giải cao).",
        "",
        "## Bảng tổng hợp từng trang",
        "",
        "| Trang PDF | Kích thước (px) | Số block OCR | Số ký tự | Phân loại | Trích yếu nội dung ban đầu |",
        "|---|---|---|---|---|---|"
    ]

    for p in page_reports:
        classification = "Scanned Image / Mixed"
        preview_clean = p['preview'].replace("|", "/").replace("\n", " ")
        report_md.append(f"| Trang {p['page']:02d} | {p['width']}x{p['height']} | {p['items_count']} | {p['char_count']} | {classification} | {preview_clean[:60]} |")

    report_path = "data/reports/extraction-report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_md))

    manifest_path = "data/reports/page_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(page_reports, f, ensure_ascii=False, indent=2)

    print(f"Report written to {report_path}")

if __name__ == "__main__":
    process_pdf()
