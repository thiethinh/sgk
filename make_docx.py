import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def create_callout(doc, text_list, title=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=220, right=180)
    
    # Left thick border
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1A365D"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_after = Pt(4)
    if title:
        run_title = p.add_run(f"★ {title}\n")
        run_title.font.name = "Times New Roman"
        run_title.font.size = Pt(12)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        
    for i, t in enumerate(text_list):
        if i > 0 or title:
            p2 = cell.add_paragraph()
        else:
            p2 = p
        p2.paragraph_format.line_spacing = 1.2
        p2.paragraph_format.space_after = Pt(3)
        run = p2.add_run(t)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(6)

def build_document():
    doc = docx.Document()
    
    # Thiết lập lề trang giấy chuẩn (Lề trái 2.5cm, phải 2cm, trên 2cm, dưới 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)     # ~2.0 cm
        section.bottom_margin = Inches(0.8)  # ~2.0 cm
        section.left_margin = Inches(1.0)    # ~2.5 cm
        section.right_margin = Inches(0.8)   # ~2.0 cm

    # Màu sắc chủ đạo: Xanh đậm trang trọng
    COLOR_PRIMARY = RGBColor(0x1A, 0x36, 0x5D)     # Deep Navy
    COLOR_SECONDARY = RGBColor(0x2B, 0x6C, 0xB0)   # Slate Blue
    COLOR_DARK = RGBColor(0x2D, 0x37, 0x48)        # Charcoal Text
    
    # ------------------ TIÊU ĐỀ BÁO CÁO ------------------
    p_org = doc.add_paragraph()
    p_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_org = p_org.add_run("BÁO CÁO SÁNG KIẾN & GIẢI PHÁP ỨNG DỤNG HỌC LIỆU SỐ TIỂU HỌC")
    r_org.font.name = "Times New Roman"
    r_org.font.size = Pt(11)
    r_org.font.bold = True
    r_org.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    p_org.paragraph_format.space_after = Pt(6)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÉ TẬP ĐỌC LỚP 1\nSÁCH GIÁO KHOA ĐIỆN TỬ TƯƠNG TÁC TÍCH HỢP TỪ ĐIỂN SONG NGỮ")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY
    p_title.paragraph_format.line_spacing = 1.2
    p_title.paragraph_format.space_after = Pt(4)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("(Giải pháp hỗ trợ học sinh học vần, mở rộng vốn từ và làm quen ngôn ngữ tự nhiên)")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    p_sub.paragraph_format.space_after = Pt(16)

    # Đường kẻ ngăn cách trang nhã
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("―" * 32)
    r_line.font.name = "Times New Roman"
    r_line.font.size = Pt(10)
    r_line.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE0)
    p_line.paragraph_format.space_after = Pt(14)

    # Hàm trợ giúp thêm Heading 1
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    # Hàm trợ giúp thêm Heading 2
    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return p

    # Hàm trợ giúp thêm đoạn văn
    def add_body(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Times New Roman"
            rb.font.size = Pt(12)
            rb.font.bold = True
            rb.font.color.rgb = COLOR_DARK
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.italic = italic
        r.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Times New Roman"
            rb.font.size = Pt(12)
            rb.font.bold = True
            rb.font.color.rgb = COLOR_DARK
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.color.rgb = COLOR_DARK
        return p

    # ------------------ PHẦN I: Ý TƯỞNG VÀ BỐI CẢNH ------------------
    add_h1("I. BỐI CẢNH THỰC TẾ VÀ Ý TƯỞNG CỐT LÕI")

    add_h2("1. Những trăn trở từ thực tế dạy và học lớp 1")
    add_body("Giai đoạn bước vào lớp 1 (6 tuổi) là bước ngoặt tâm sinh lý vô cùng lớn đối với các em học sinh. Các em vừa rời khỏi môi trường mầm non với tinh thần 'chơi là chính' để bước sang một môi trường học tập nề nếp, có kỷ luật và đòi hỏi khả năng tập trung cao hơn.")
    add_body("Trong quá trình đồng hành cùng học sinh lớp 1, thực tế giảng dạy và chăm sóc cho thấy ba khó khăn phổ biến:")
    add_bullet(" Sách giáo khoa giấy truyền thống (bộ sách 'Kết nối tri thức với cuộc sống') được biên soạn với hình ảnh rất đẹp mắt, nhưng là học liệu tĩnh. Sách không thể tự phát âm, không tương tác được. Khi gặp các vần khó hoặc từ mới, trẻ dễ nản lòng và giảm hứng thú nếu không có người kèm cặp liên tục.", "Sách giáo khoa giấy thiếu âm thanh sống động:")
    add_bullet(" Nhiều phụ huynh rất mong muốn hướng dẫn con học bài nhưng lại bận rộn công việc, hoặc lo lắng mình phát âm tiếng Việt chưa chuẩn mẫu, hay ngập ngừng khi gặp từ ngữ tiếng Anh, không tự tin hướng dẫn con đọc đúng.", "Phụ huynh gặp khó khăn khi kèm con tại nhà:")
    add_bullet(" Xu hướng cho trẻ làm quen với tiếng Anh từ lớp 1 ngày càng được chú trọng. Tuy nhiên, cách dạy tiếng Anh tách rời hiện nay thường khiến trẻ phải học thuộc lòng máy móc, không tạo được mối liên hệ tự nhiên giữa từ ngữ mẹ đẻ và từ ngữ tiếng Anh trong các hoạt động đời thường.", "Việc học ngôn ngữ còn rời rạc, thiếu ngữ cảnh:")

    add_h2("2. Ý tưởng giải pháp: Cuốn sách giáo khoa 'biết nói và biết giải nghĩa'")
    add_body("Xuất phát từ tình yêu trẻ thơ và mong muốn tạo ra một công cụ học tập gần gũi, dự án đã ấp ủ ý tưởng biến cuốn sách giáo khoa quen thuộc hằng ngày thành một ")
    p_last = doc.paragraphs[-1]
    r_em = p_last.add_run("không gian đọc sách tương tác đa giác quan: Nhìn tranh - Chạm vào chữ - Nghe phát âm chuẩn - Hiểu nghĩa từ ngữ.")
    r_em.font.name = "Times New Roman"
    r_em.font.size = Pt(12)
    r_em.font.bold = True
    r_em.font.color.rgb = COLOR_PRIMARY

    add_body("Thay vì tạo ra một ứng dụng hoạt hình hoàn toàn mới lạ khiến trẻ xa rời trang sách thật, giải pháp giữ trọn vẹn 100% hình ảnh nguyên bản của cuốn sách giáo khoa trên lớp. Trên mỗi trang sách, từng chữ cái, từ vựng và hình minh họa đều được thổi hồn để các em chạm vào là có tiếng đọc mẫu vang lên và có khung giải nghĩa hiện ra ngay bên cạnh.")

    create_callout(
        doc,
        [
            "Ý tưởng xuyên suốt: Giữ trọn sự thân thuộc của cuốn sách giáo khoa trên lớp, nhưng mang lại trải nghiệm kỳ diệu như một cuốn sách thần kỳ – 'Chạm vào đâu, hiểu sâu và đọc chuẩn ở đó'."
        ],
        title="Thông điệp sư phạm của dự án"
    )

    # ------------------ PHẦN II: HIỆN THỰC HÓA ------------------
    add_h1("II. SẢN PHẨM ĐÃ HIỆN THỰC HÓA TRÊN THỰC TẾ")
    add_body("Dự án không dừng lại ở mức mô hình phác thảo mà đã được xây dựng hoàn thiện thành một cuốn sách điện tử hoàn chỉnh, có thể mở lên và sử dụng ngay lập tức trên máy tính bàn, máy tính xách tay, tivi thông minh hoặc màn hình tương tác tại lớp học.")

    add_h2("1. Bố cục hai phần thông minh – Vừa đọc sách, vừa tra cứu liền mạch")
    add_body("Màn hình được chia làm hai khu vực làm việc song song, giúp mắt của trẻ không phải đảo qua đảo lại giữa nhiều cửa sổ rắc rối:")
    add_bullet(" Tái hiện trọn vẹn 57 trang sách bài học của cuốn Sách giáo khoa Tiếng Việt 1 (Tập 1 - Bộ Kết nối tri thức với cuộc sống). Trang sách được căn chỉnh với tỷ lệ vừa vặn tầm mắt của học sinh, màu sắc sáng rõ và giữ nguyên vẹn từng nét vẽ, bài thơ, đoạn văn của bộ sách.", "Khu vực bên trái (Trang sách nguyên bản):")
    add_bullet(" Mỗi từ ngữ quan trọng trên trang sách đều được phủ một vùng nhận diện thông minh. Khi bé dùng chuột nhấp vào (hoặc chạm tay trên màn hình cảm ứng), từ đó sẽ nổi bật lên và phát ra giọng đọc mẫu ngay tức thì.", "Vùng tương tác trực tiếp trên trang sách:")
    add_bullet(" Mỗi khi bé chạm vào một từ trong bài, khung bên phải sẽ mở ngay thẻ giải nghĩa của từ đó, bao gồm: giải nghĩa bằng tiếng Việt dễ hiểu, từ tiếng Anh tương đương, phiên âm quốc tế và các nút bấm nghe lại giọng đọc.", "Khu vực bên phải (Thẻ từ điển đồng hành):")

    add_h2("2. Kho giọng đọc mẫu chuẩn mực – Âm thanh trong trẻo, tự nhiên")
    add_body("Để trẻ tiếp thu chuẩn xác ngay từ những ngày đầu tập đọc, ứng dụng đã chuẩn bị sẵn kho âm thanh phong phú với hơn 200 bản thu âm chất lượng cao, bao gồm:")
    add_bullet(" Giọng đọc truyền cảm, ấm áp, ngắt nghỉ tròn vành rõ chữ theo đúng chuẩn phát âm tiếng Việt giáo khoa, giúp các em bắt chước đọc theo dễ dàng.", "Giọng đọc tiếng Việt mẫu:")
    add_bullet(" Giọng phát âm chuẩn xác của người bản ngữ, giúp trẻ cảm nhận đúng ngữ điệu và phát âm quốc tế ngay khi mới 6 tuổi.", "Giọng đọc tiếng Anh đối chiếu:")
    add_bullet(" Khi bé bấm vào từ trên trang sách, máy sẽ tự động phát âm ngay lập tức mà không có độ trễ, kích thích thính giác và sự tò mò của trẻ.", "Cơ chế phát âm tức thì:")

    add_h2("3. Lời giải nghĩa viết riêng cho tâm hồn trẻ thơ 6 tuổi")
    add_body("Khác với các từ điển người lớn thường dùng ngôn ngữ hàn lâm, phức tạp, toàn bộ các lời giải thích trong ứng dụng đều được biên soạn tỉ mỉ theo đúng tâm lý và lứa tuổi học sinh lớp 1. Lời giải nghĩa giàu hình ảnh, gắn liền với tình cảm gia đình, trường lớp và cuộc sống xung quanh:")
    
    # Bảng ví dụ giải nghĩa
    tbl_vn = doc.add_table(rows=4, cols=3)
    tbl_vn.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_vn)
    
    headers = ["Từ trong bài", "Lời giải nghĩa dành cho bé lớp 1", "Từ tiếng Anh tương ứng"]
    col_widths = [Inches(1.3), Inches(3.6), Inches(1.5)]
    
    # Header row
    hdr_cells = tbl_vn.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "2B6CB0")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    data_rows = [
        ("Bà", "Người phụ nữ lớn tuổi, là mẹ của bố hoặc mẹ, luôn thương yêu, chăm sóc và vỗ về cháu.", "Grandmother"),
        ("Gia đình", "Tổ ấm thân thương gồm có ông bà, cha mẹ và con cái cùng sống gắn bó, yêu thương nhau.", "Family"),
        ("Búp bê", "Đồ chơi mô phỏng hình em bé hoặc bạn nhỏ xinh xắn, đáng yêu mà các bạn nhỏ rất thích chơi.", "Doll")
    ]
    
    for row_idx, data in enumerate(data_rows, start=1):
        row_cells = tbl_vn.rows[row_idx].cells
        bg_col = "FFFFFF" if row_idx % 2 == 1 else "F7FAFC"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].width = col_widths[col_idx]
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(text)
                r.font.bold = True
            elif col_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(text)
                r.font.italic = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.color.rgb = COLOR_DARK
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(6)

    add_h2("4. Các tính năng trợ giúp học tập thân thiện và tiện dụng")
    add_bullet(" Ở góc trang sách luôn có một mảnh giấy màu vàng nhạt ghim nhẹ nhàng với biểu tượng dễ hiểu: 'Chạm vào từ để nghe đọc' và 'Lướt chuột để lật trang'. Trẻ chỉ cần nhìn một lần là hiểu cách dùng mà không cần người lớn giải thích dài dòng.", "Mảnh ghi nhớ hướng dẫn bé:")
    add_bullet(" Mỗi khi khám phá được một từ thú vị hoặc một từ mình hay quên, các em có thể nhấn nút 'Thả tim / Lưu từ này'. Ứng dụng sẽ gom các từ đó vào một cuốn sổ tay nhỏ để các em mở ra ôn lại bất cứ lúc nào, tạo niềm say mê sưu tập từ vựng.", "Cuốn sổ tay từ vựng của bé:")
    add_bullet(" Thao tác lật trang sách được thiết kế êm ái, người dùng chỉ cần cuộn nhẹ bi lăn của chuột là sách chuyển trang từ tốn như ta đang lật từng tờ giấy thật, không gây mỏi mắt hay giật hình.", "Lật sách mượt mà, tự nhiên:")
    add_bullet(" Toàn bộ màn hình chỉ tập trung vào việc đọc sách. Các chi tiết rườm rà, các thanh điều khiển phức tạp đều được lược bỏ để giúp học sinh hoàn toàn tập trung vào nội dung bài học.", "Giao diện gọn gàng, không gây xao nhãng:")

    # ------------------ PHẦN III: LỢI ÍCH MANG LẠI ------------------
    add_h1("III. LỢI ÍCH TO LỚN ĐỐI VỚI GIÁO DỤC TIỂU HỌC")
    add_body("Ứng dụng mang lại những giá trị thiết thực và trực tiếp cho cả ba chủ thể trung tâm của giáo dục: Học sinh, Giáo viên và Phụ huynh học sinh.")

    add_h2("1. Lợi ích đối với học sinh lớp 1")
    add_bullet(" Ở lứa tuổi này, các em đang trong giai đoạn làm quen mặt chữ và ghép vần. Khi gặp các từ khó, từ tượng thanh tượng hình (như 'líu lo', 'ngọt lừ', 'ba ba'), việc được nghe máy phát âm ngay giúp các em vượt qua rào cản sợ đọc sai, từ đó tự tin hơn rất nhiều khi đứng lên đọc to trước lớp.", "Khắc phục triệt để nỗi sợ đọc sai, tăng sự tự tin:")
    add_bullet(" Việc được tự tay chạm vào trang sách và nhận lại âm thanh tức thì tạo cảm giác như một trò chơi khám phá tri thức. Trẻ không còn cảm giác bị 'bắt buộc phải ngồi vào bàn học', mà chủ động tìm kiếm các từ mới trong từng trang sách.", "Hình thành thói quen tự giác và hứng thú học tập:")
    add_bullet(" Thay vì bắt các em học những danh sách từ vựng tiếng Anh xa lạ, việc học từ tiếng Anh gắn liền với bài học tiếng Việt trên lớp giúp các em ghi nhớ tự nhiên. Ví dụ: khi học bài về lớp học, các em vừa đọc chữ 'cây bút', 'thước kẻ' trong tiếng Việt vừa biết thêm từ tương ứng trong tiếng Anh. Điều này gieo mầm tư duy song ngữ từ sớm một cách nhẹ nhàng.", "Phát triển tư duy ngôn ngữ song song:")

    add_h2("2. Lợi ích đối với Giáo viên trong công tác giảng dạy")
    add_bullet(" Giáo viên có thể trình chiếu trực tiếp ứng dụng lên bảng tương tác thông minh hoặc tivi của lớp học. Trong tiết học vần hay tập đọc, cô giáo có thể mời học sinh lên chạm vào từ trên bảng để cả lớp cùng nghe và đồng thanh đọc theo, tạo nên một không khí học tập vô cùng sôi nổi và cuốn hút.", "Giáo cụ trực quan hiện đại trong giờ lên lớp:")
    add_bullet(" Trong các tiết học dạy phát âm, giáo viên không cần phải đọc lặp đi lặp lại một từ nhiều lần làm mất sức. Giọng đọc mẫu chuẩn mực trong ứng dụng sẽ là người trợ giảng đắc lực hỗ trợ cô giáo phát âm mẫu chuẩn xác.", "Giảm tải áp lực phát âm mẫu liên tục cho cô giáo:")
    add_bullet(" Ứng dụng bám sát 100% từng trang sách giáo khoa chính khóa của Bộ Giáo dục & Đào tạo, do đó giáo viên không cần phải soạn lại giáo án hay thay đổi tiến trình bài dạy, có thể sử dụng được ngay trong các tiết dạy thông thường lẫn các tiết hội giảng, chuyên đề.", "Đồng bộ tuyệt đối với chương trình hiện hành:")

    add_h2("3. Lợi ích đối với Phụ huynh học sinh")
    add_bullet(" Phụ huynh không còn phải băn khoăn hay e ngại việc mình phát âm chưa chuẩn để dạy con. Giọng đọc chuẩn mực tích hợp sẵn trong sách sẽ thay phụ huynh hướng dẫn bé đọc đúng từng âm, từng từ.", "Đồng hành cùng con tại nhà dù không rành ngoại ngữ:")
    add_bullet(" Với thiết kế trực quan, dễ dùng, chỉ sau 1 đến 2 lần hướng dẫn đầu tiên, các bé 6 tuổi đã có thể tự mở sách và tự học bài tại nhà, giúp cha mẹ an tâm làm việc mà con vẫn có những giờ tự học bổ ích, lành mạnh.", "Giải phóng thời gian kèm cặp cho cha mẹ:")

    # Bảng tổng hợp giá trị
    tbl_val = doc.add_table(rows=4, cols=3)
    tbl_val.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_val)
    
    h_val = ["Đối tượng", "Khó khăn trước đây", "Giá trị ứng dụng đem lại"]
    w_val = [Inches(1.4), Inches(2.4), Inches(2.6)]
    
    for i, title_txt in enumerate(h_val):
        cell = tbl_val.rows[0].cells[i]
        cell.width = w_val[i]
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    rows_content = [
        ("Học sinh lớp 1", "Dễ nản khi gặp từ khó; sợ đọc sai; mau chán vì sách giấy không có tiếng.", "Tự tin bấm nghe đọc mẫu; hào hứng khám phá trang sách; vừa đọc thạo vừa biết thêm tiếng Anh."),
        ("Giáo viên", "Mất sức đọc mẫu nhiều lần; khó duy trì sự tập trung của cả lớp suốt tiết học.", "Có giáo cụ sinh động trên bảng lớp; tiết học cuốn hút; đồng bộ hoàn toàn với sách giấy trên tay trò."),
        ("Phụ huynh", "Bận rộn; không tự tin về phát âm tiếng Anh; khó kèm con học đều đặn mỗi tối.", "An tâm cho con tự học bài; máy tự đọc mẫu chuẩn xác; hình thành nếp tự giác cho con.")
    ]
    
    for row_idx, r_data in enumerate(rows_content, start=1):
        row_cells = tbl_val.rows[row_idx].cells
        bg_col = "FFFFFF" if row_idx % 2 == 1 else "F7FAFC"
        for col_idx, text in enumerate(r_data):
            row_cells[col_idx].width = w_val[col_idx]
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(text)
                r.font.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.color.rgb = COLOR_DARK
            
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(6)

    # ------------------ PHẦN IV: ĐIỂM NỔI BẬT VỀ MẶT SƯ PHẠM ------------------
    add_h1("IV. NHỮNG ĐIỂM SÁNG VÀ TÂM HUYẾT SƯ PHẠM TRONG DỰ ÁN")

    add_h2("1. Tôn trọng tuyệt đối tính quy chuẩn của Sách Giáo Khoa")
    add_body("Dự án kiên định với định hướng: ")
    p_last = doc.paragraphs[-1]
    r_em2 = p_last.add_run("không thay đổi bất kỳ hình ảnh, trật tự hay câu từ nào trong sách giáo khoa của Bộ Giáo dục & Đào tạo.")
    r_em2.font.bold = True
    add_body("Nhiều ứng dụng hiện nay tự vẽ lại hình hoạt họa hoặc biên soạn lại nội dung, vô tình khiến học sinh bị 'lệch' so với cuốn sách các em cầm ở lớp. Với giải pháp này, hình ảnh trên máy tính giống hệt 100% trang sách trên bàn học, giúp các em củng cố sự thân thuộc và tin cậy tuyệt đối.")

    add_h2("2. Phương pháp tiếp cận 'Học tiếng Anh trong ngữ cảnh tiếng Việt'")
    add_body("Đây là điểm sáng tạo nổi bật nhất của đề tài. Trẻ không học những từ ngữ tiếng Anh xa xôi, trừu tượng, mà học ngay những từ ngữ xuất hiện trong bài tập đọc tiếng Việt:")
    add_bullet(" Khi bài tập đọc nói về 'Gia đình', bé được học các từ: Ông bà, cha mẹ, anh em và đối chiếu ngay với từ tiếng Anh tương ứng.", "Ngữ cảnh gần gũi:")
    add_bullet(" Khi đọc bài 'Đồ dùng học tập', bé được nghe đọc: cây bút, quyển vở, thước kẻ, cục tẩy bằng cả hai ngôn ngữ.", "Vốn từ thiết thực:")
    add_body("Cách tiếp cận này giúp ngôn ngữ thứ hai được neo chặt vào ngôn ngữ mẹ đẻ, giúp trẻ hiểu bản chất sự vật chứ không học vẹt.")

    add_h2("3. Thiết kế tối giản, bảo vệ thị lực và sự tập trung của trẻ")
    add_body("Khác với các phần mềm giải trí thường có nhiều màu sắc lòe loẹt hoặc quảng cáo gây xao nhãng, ứng dụng được thiết kế trang nhã với tông màu dịu mắt. Kích thước trang sách được tính toán cố định vừa khít màn hình máy tính, giúp các em ngồi học với khoảng cách mắt hợp lý, không bị mỏi mắt hay phân tâm bởi các nút bấm kỹ thuật không cần thiết.")

    # ------------------ PHẦN V: ĐỊNH HƯỚNG PHÁT TRIỂN ------------------
    add_h1("V. ĐỊNH HƯỚNG PHÁT TRIỂN VÀ NHÂN RỘNG")
    add_body("Trên nền tảng những kết quả vững chắc đã đạt được, dự án đã vạch ra lộ trình nâng cấp nhằm phục vụ tốt hơn nữa cho học sinh và nhà trường:")
    add_bullet(" Ứng dụng sẽ tích hợp tính năng cho phép bé tự đọc to vào máy, sau đó máy sẽ phân tích và động viên: 'Bé đọc rất hay!' hoặc 'Bé phát âm vần này rõ hơn một chút nhé'. Điều này sẽ kích thích các em luyện đọc nhiều hơn nữa.", "Thêm tính năng chấm điểm giọng đọc của bé:")
    add_bullet(" Bổ sung các hoạt động ghép chữ với tranh minh họa, chọn từ đúng để nhận các bông hoa điểm 10 sau mỗi bài học, giúp giờ ôn tập thêm phần hào hứng.", "Xây dựng các trò chơi ôn tập nhẹ nhàng:")
    add_bullet(" Tiếp tục triển khai cho Tập 2 của Tiếng Việt lớp 1 và từng bước nhân rộng sang các khối lớp 2, 3, 4, 5, tạo thành một hệ thống học liệu số hoàn chỉnh cho bậc tiểu học.", "Mở rộng sang các cuốn sách và khối lớp tiếp theo:")

    # ------------------ PHẦN VI: KẾT LUẬN ------------------
    add_h1("VI. KẾT LUẬN")
    add_body("Dự án ")
    p_last = doc.paragraphs[-1]
    r_bold_prj = p_last.add_run("Bé Tập Đọc Lớp 1 – Sách Giáo Khoa Điện Tử Tương Tác Tích Hợp Từ Điển Song Ngữ")
    r_bold_prj.font.bold = True
    r_bold_prj.font.color.rgb = COLOR_PRIMARY
    p_last.add_run(" không chỉ đơn thuần là việc đưa một cuốn sách giấy lên màn hình vi tính, mà là một ")
    p_last.add_run("sáng kiến giáo dục mang tính ứng dụng thực tiễn cao").bold = True
    p_last.add_run(". Giải pháp đã giải quyết được trúng và đúng những khó khăn của học sinh lớp 1 trong giai đoạn đầu đời tiếp cận chữ viết và ngôn ngữ.")

    add_body("Với sự kết hợp hài hòa giữa ")
    p_last2 = doc.paragraphs[-1]
    p_last2.add_run("tính quy chuẩn sư phạm").bold = True
    p_last2.add_run(", ")
    p_last2.add_run("tâm lý học lứa tuổi mầm non - tiểu học").bold = True
    p_last2.add_run(" và ")
    p_last2.add_run("sự tiện ích, dễ dùng của công nghệ").bold = True
    p_last2.add_run(", dự án hứa hẹn sẽ là người bạn đồng hành tin cậy của các thầy cô giáo trên bục giảng, của các bậc phụ huynh trong mỗi gia đình, và đặc biệt là món quà học tập thú vị, bổ ích cho các em học sinh thân yêu.")

    # Phần chữ ký/thông tin cuối văn bản
    p_foot_space = doc.add_paragraph()
    p_foot_space.paragraph_format.space_before = Pt(20)

    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sign.autofit = False
    
    cell_l = tbl_sign.cell(0, 0)
    cell_l.width = Inches(3.2)
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    
    cell_r = tbl_sign.cell(0, 1)
    cell_r.width = Inches(3.2)
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    
    r_date = p_r.add_run("Hà Nội, ngày 21 tháng 10 năm 2026\n")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(11)
    r_date.font.italic = True
    
    r_author = p_r.add_run("NGƯỜI LẬP BÁO CÁO\n\n\n\n")
    r_author.font.name = "Times New Roman"
    r_author.font.size = Pt(11.5)
    r_author.font.bold = True
    
    r_name = p_r.add_run("Ban Dự Án Bé Tập Đọc Lớp 1")
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(11.5)
    r_name.font.bold = True
    r_name.font.italic = True

    output_path = r"c:\Users\HINH\Downloads\sgk1\BAO_CAO_DU_AN.docx"
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    build_document()
