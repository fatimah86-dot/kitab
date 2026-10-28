#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Publication-Grade REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.docx
from upgraded REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md + 16 300-DPI Wafaq images.
"""

import re
import io, struct, zlib
from pathlib import Path
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md"
OUT_DOCX = ROOT / "REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.docx"
DPI_DIR = ROOT / "rajah_anwar_FINAL_300DPI"

# Visually verified 1-to-1 mapping: (page_number, table_index_in_page) -> (filename, caption, max_width_in)
WAFAQ_MAP = {
    (8, 0):  ("IMG_20261025_072355.jpg", "Wafaq Asli 300 DPI — Hal. 08 (1): Wafaq Mukhammas 5×5 Huruf 'Amal", 3.1),
    (8, 1):  ("IMG_20261025_072327.jpg", "Wafaq Asli 300 DPI — Hal. 08 (2): Wafaq Murabba' 4×4 Rūḥānī Ḥākim", 3.0),
    (10, 0): ("IMG_20261025_072854.jpg", "Jadwal Asli 300 DPI — Hal. 10: Jadwal Taksīr 5×15 Khadim Ḥanaqāyīl", 4.8),
    (12, 0): ("IMG_20261025_073117.jpg", "Wafaq Asli 300 DPI — Hal. 12: Wafaq Musallas 3×3 'Ilājul-Mass (Konstanta 1827)", 3.2),
    (16, 0): ("IMG_20261025_092532.jpg", "Wafaq Asli 300 DPI — Hal. 16: Wafaq Musallas 3×3 Thard 'Athlūsy (Konstanta 1115)", 3.2),
    (18, 0): ("IMG_20261025_094727.jpg", "Wafaq Asli 300 DPI — Hal. 18: Wafaq Murabba' 4×4 Ad-Durratun-Nūrāniyyah (Konstanta 1198)", 3.3),
    (20, 0): ("IMG_20261025_094859.jpg", "Wafaq Asli 300 DPI — Hal. 20: Wafaq Musallas Khālil-Qalb Tadmīrizh-Zhālim (Konstanta 1896)", 3.3),
    (24, 0): ("IMG_20261025_101416.jpg", "Wafaq Asli 300 DPI — Hal. 24: Wafaq Musallas 3×3 As-Saiful-Battār (Konstanta 582)", 3.3),
    (28, 0): ("IMG_20261025_233529.png", "Wafaq Asli 300 DPI — Hal. 28: Wafaq Musallas 3×3 Al-Āyātul-'Asyr (Konstanta 2190)", 3.3),
    (30, 0): ("IMG_20261025_102900.jpg", "Wafaq Asli 300 DPI — Hal. 30: Wafaq Mukhammas 5×5 Al-Kasyful-Manāmī (Konstanta 3266)", 3.6),
    (46, 0): ("IMG_20261025_110522.jpg", "Wafaq Asli 300 DPI — Hal. 46: Wafaq Al-Mutsallatsuth-Thabī'ī 3×3 (Konstanta 15)", 3.2),
    (48, 0): ("IMG_20261025_110735.jpg", "Rajah Asli 300 DPI — Hal. 48: Pemetaan Kamar Huruf Nūrāniyyah (اجهزط)", 3.1),
    (49, 0): ("IMG_20261025_153252.jpg", "Rajah Asli 300 DPI — Hal. 49: Pemetaan Kamar Huruf Zhulmāniyyah (بدوح)", 3.1),
    (57, 0): ("IMG_20261025_153335.jpg", "Wafaq Asli 300 DPI — Hal. 57: Wafaq Musallas Hurufī 3×3 Asrārur-Rijāl", 3.2),
    (58, 0): ("IMG_20261025_153402.jpg", "Wafaq Asli 300 DPI — Hal. 58: Wafaq Murabba' 'Adadī 4×4 Metode Azlan", 3.4),
    (59, 0): ("IMG_20261025_153434.jpg", "Wafaq Asli 300 DPI — Hal. 59: Wafaq at-Tashrīf Hurufī 4×4 Asrārur-Rijāl", 3.5),
}

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+")

# Colors
C_EMERALD_DARK = RGBColor(0x06, 0x4E, 0x3B)
C_EMERALD_MID  = RGBColor(0x04, 0x78, 0x57)
C_NAVY         = RGBColor(0x1E, 0x3A, 0x8A)
C_SLATE_DARK   = RGBColor(0x1F, 0x29, 0x37)
C_SLATE_MUTED  = RGBColor(0x4B, 0x55, 0x63)
C_GOLD_DARK    = RGBColor(0x92, 0x40, 0x0E)

def has_arabic(s: str) -> bool:
    return bool(ARABIC_RE.search(s))

def strip_dir_marks(s: str) -> str:
    return s.replace("\u200e", "").replace("\u200f", "")

def set_p_bidi(p, is_rtl: bool):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:bidi")):
        pPr.remove(old)
    bidi = OxmlElement("w:bidi")
    bidi.set(qn("w:val"), "1" if is_rtl else "0")
    pPr.append(bidi)

def set_p_shading(p, fill_hex: str):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:shd")):
        pPr.remove(old)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>')
    pPr.append(shd)

def set_p_bottom_border(p, color_hex: str = "065F46", sz: str = "12"):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:pBdr")):
        pPr.remove(old)
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="4" w:color="{color_hex}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

def format_run_fonts(run, font_latin="Calibri", font_arabic="Traditional Arabic",
                     size_pt=11, size_cs_pt=None, bold=False, italic=False,
                     color: RGBColor = None, is_rtl=False):
    run.bold = bold
    run.italic = italic
    run.font.name = font_latin
    run.font.size = Pt(size_pt)
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), font_latin)
    rFonts.set(qn("w:hAnsi"), font_latin)
    rFonts.set(qn("w:cs"), font_arabic)
    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = OxmlElement("w:szCs")
        rPr.append(szCs)
    szCs.set(qn("w:val"), str(int((size_cs_pt or size_pt) * 2)))
    if bold:
        if rPr.find(qn("w:bCs")) is None:
            rPr.append(OxmlElement("w:bCs"))
    if is_rtl:
        if rPr.find(qn("w:rtl")) is None:
            rPr.append(OxmlElement("w:rtl"))

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+")

def emit_text_segments_with_arabic_detection(p, text_str: str, bold=False, italic=False, is_code=False,
                                             base_size=11, base_color=C_SLATE_DARK):
    if not text_str:
        return
    pos = 0
    for m in ARABIC_RE.finditer(text_str):
        if m.start() > pos:
            lat_part = text_str[pos:m.start()]
            r = p.add_run(lat_part)
            c = C_NAVY if is_code else base_color
            f_lat = "Cambria" if is_code else "Calibri"
            sz = base_size - 0.5 if is_code else base_size
            format_run_fonts(r, font_latin=f_lat, size_pt=sz, bold=bold, italic=italic, color=c, is_rtl=False)
        arb_part = m.group(0)
        r_ar = p.add_run(arb_part)
        format_run_fonts(
            r_ar,
            font_latin="Traditional Arabic",
            font_arabic="Traditional Arabic",
            size_pt=base_size + 2.5,
            size_cs_pt=base_size + 3.0,
            bold=True if (bold or is_code) else False,
            italic=False,
            color=C_EMERALD_DARK if is_code else base_color,
            is_rtl=True,
        )
        pos = m.end()
    if pos < len(text_str):
        lat_part = text_str[pos:]
        r = p.add_run(lat_part)
        c = C_NAVY if is_code else base_color
        f_lat = "Cambria" if is_code else "Calibri"
        sz = base_size - 0.5 if is_code else base_size
        format_run_fonts(r, font_latin=f_lat, size_pt=sz, bold=bold, italic=italic, color=c, is_rtl=False)

# State-machine rich inline parser supporting **bold**, *italic*, ***bold-italic***, and `code/arabic` with ZERO leftover markers!
def parse_inline_rich(p, s: str, bold=False, italic=False, base_size=11, base_color=C_SLATE_DARK):
    b_state = bold
    i_state = italic
    c_state = False
    buf = []

    def flush():
        if buf:
            txt = "".join(buf)
            buf.clear()
            emit_text_segments_with_arabic_detection(
                p, txt, bold=b_state, italic=i_state, is_code=c_state,
                base_size=base_size, base_color=base_color
            )

    idx = 0
    n = len(s)
    while idx < n:
        if c_state:
            if s[idx] == "`":
                flush()
                c_state = False
                idx += 1
            else:
                buf.append(s[idx])
                idx += 1
            continue

        if s[idx] == "`":
            flush()
            c_state = True
            idx += 1
        elif s.startswith("***", idx):
            flush()
            b_state = not b_state
            i_state = not i_state
            idx += 3
        elif s.startswith("**", idx):
            flush()
            b_state = not b_state
            idx += 2
        elif s[idx] == "*":
            flush()
            i_state = not i_state
            idx += 1
        else:
            buf.append(s[idx])
            idx += 1
    flush()

def style_rtl_wafaq_table(table, ncols: int):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    # Ensure single clean w:bidiVisual so column 0 is on the RIGHT (authentic Arabic RTL grid!)
    for old in tblPr.findall(qn("w:bidiVisual")):
        tblPr.remove(old)
    tblPr.append(OxmlElement("w:bidiVisual"))

    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="10" w:space="0" w:color="065F46"/>'
        f'  <w:left w:val="single" w:sz="10" w:space="0" w:color="065F46"/>'
        f'  <w:bottom w:val="single" w:sz="10" w:space="0" w:color="065F46"/>'
        f'  <w:right w:val="single" w:sz="10" w:space="0" w:color="065F46"/>'
        f'  <w:insideH w:val="single" w:sz="8" w:space="0" w:color="065F46"/>'
        f'  <w:insideV w:val="single" w:sz="8" w:space="0" w:color="065F46"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # Cell padding & sizing
    cell_w_in = 0.37 if ncols >= 12 else (0.72 if ncols == 5 else (0.85 if ncols == 4 else 1.0))
    font_sz = 12 if ncols >= 12 else 16

    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        fill_hex = "ECFDF5" if r_idx % 2 == 0 else "FFFFFF"
        for cell in row.cells:
            cell.width = Inches(cell_w_in)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>'))
            tcPr.append(parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'  <w:top w:w="80" w:type="dxa"/>'
                f'  <w:bottom w:w="80" w:type="dxa"/>'
                f'  <w:left w:w="80" w:type="dxa"/>'
                f'  <w:right w:w="80" w:type="dxa"/>'
                f'</w:tcMar>'
            ))
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                set_p_bidi(p, True)
                for r in p.runs:
                    format_run_fonts(
                        r,
                        font_latin="Traditional Arabic",
                        font_arabic="Traditional Arabic",
                        size_pt=font_sz,
                        size_cs_pt=font_sz + 1,
                        bold=True,
                        color=C_EMERALD_DARK,
                        is_rtl=True,
                    )

def add_wafaq_image(doc: Document, page_num: int, tbl_idx: int):
    key = (page_num, tbl_idx)
    assert key in WAFAQ_MAP, f"Unmapped wafaq table at {key}!"
    fname, caption, max_w = WAFAQ_MAP[key]
    img_path = DPI_DIR / fname
    assert img_path.exists(), f"Missing 300 DPI image: {img_path}"

    image_bytes = img_path.read_bytes()
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        # Repair invalid ancillary CRCs without re-encoding or altering pixels.
        fixed = bytearray(image_bytes[:8]); pos = 8
        while pos < len(image_bytes):
            length = struct.unpack(">I", image_bytes[pos:pos+4])[0]
            payload = image_bytes[pos+4:pos+8+length]
            fixed += struct.pack(">I", length) + payload + struct.pack(">I", zlib.crc32(payload) & 0xffffffff)
            pos += length + 12
        image_bytes = bytes(fixed)
    with Image.open(io.BytesIO(image_bytes)) as im:
        w_px, h_px = im.size
    aspect = h_px / float(w_px)
    disp_w = min(max_w, 5.2)
    if disp_w * aspect > 4.2:
        disp_w = 4.2 / aspect

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(2)
    set_p_bidi(p_img, False)
    run_img = p_img.add_run()
    run_img.add_picture(io.BytesIO(image_bytes), width=Inches(disp_w))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    set_p_bidi(p_cap, False)
    r_cap = p_cap.add_run(caption)
    format_run_fonts(r_cap, font_latin="Calibri", size_pt=9.5, italic=True, color=C_SLATE_MUTED, is_rtl=False)

def build_docx():
    md_text = MD_PATH.read_text(encoding="utf-8")
    blocks = [b for b in re.split(r"(?=^## HALAMAN )", md_text, flags=re.M) if b.strip()]
    assert len(blocks) == 65, f"Expected 65 blocks, got {len(blocks)}"

    # Pre-parse page metadata for Daftar Isi
    toc_items = []
    for b in blocks:
        hdr_line = strip_dir_marks(b.splitlines()[0]).lstrip("# ").strip()
        m_hdr = re.match(r"HALAMAN (\d{2})\s*—\s*(.+)", hdr_line)
        assert m_hdr, f"Bad header: {hdr_line}"
        pnum = int(m_hdr.group(1))
        ar_title = m_hdr.group(2).strip()
        # Get first line of Terjemahan as concise Indonesian title
        m_terj = re.search(r"^### Terjemahan\n(.*?)(?=^### )", b, flags=re.M | re.S)
        first_terj = [strip_dir_marks(ln).strip() for ln in m_terj.group(1).splitlines() if strip_dir_marks(ln).strip()][0]
        if len(first_terj) > 85:
            first_terj = first_terj[:82] + "..."
        toc_items.append((pnum, ar_title, first_terj))

    doc = Document()

    # Configure A4 page setup & clean margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

        # Running header & footer
        hdr_p = section.header.paragraphs[0]
        hdr_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_p_bidi(hdr_p, False)
        r_hdr = hdr_p.add_run("Anwārusy-Syaikhil-Basyīr — Edisi Lengkap 5 Lapis Bersih (Halaman 01–65)")
        format_run_fonts(r_hdr, size_pt=8.5, italic=True, color=C_SLATE_MUTED)

    # -----------------------------------------------------------------------
    # COVER & COMPLETE 65-PAGE DAFTAR ISI
    # -----------------------------------------------------------------------
    p_cov_ar = doc.add_paragraph()
    p_cov_ar.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_ar.paragraph_format.space_before = Pt(18)
    p_cov_ar.paragraph_format.space_after = Pt(4)
    set_p_bidi(p_cov_ar, True)
    r1 = p_cov_ar.add_run("أَنْوَارُ الشَّيْخِ الْبَشِيرِ")
    format_run_fonts(r1, font_latin="Traditional Arabic", font_arabic="Traditional Arabic",
                     size_pt=26, size_cs_pt=28, bold=True, color=C_EMERALD_DARK, is_rtl=True)

    p_cov_ar2 = doc.add_paragraph()
    p_cov_ar2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_ar2.paragraph_format.space_before = Pt(0)
    p_cov_ar2.paragraph_format.space_after = Pt(12)
    set_p_bidi(p_cov_ar2, True)
    r2 = p_cov_ar2.add_run("مُنْتَدَيَاتُ الْأَنْوَارِ الْقَادِرِيَّةِ وَالْأَرْوَاحِ الرَّحْمَانِيَّةِ")
    format_run_fonts(r2, font_latin="Traditional Arabic", font_arabic="Traditional Arabic",
                     size_pt=16, size_cs_pt=17, bold=True, color=C_EMERALD_MID, is_rtl=True)

    p_cov_id = doc.add_paragraph()
    p_cov_id.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_id.paragraph_format.space_before = Pt(4)
    p_cov_id.paragraph_format.space_after = Pt(4)
    set_p_bidi(p_cov_id, False)
    set_p_bottom_border(p_cov_id, "065F46", "12")
    r3 = p_cov_id.add_run("TERJEMAH & SYARAH LENGKAP KITAB ANWĀRUSY-SYAIKH AL-BASYĪR\nEDISI FINAL 5 LAPIS BERSIH (65 HALAMAN LENGKAP — KHATAM)")
    format_run_fonts(r3, font_latin="Calibri", size_pt=13.5, bold=True, color=C_NAVY, is_rtl=False)

    p_cov_sub = doc.add_paragraph()
    p_cov_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_sub.paragraph_format.space_before = Pt(6)
    p_cov_sub.paragraph_format.space_after = Pt(16)
    set_p_bidi(p_cov_sub, False)
    r4 = p_cov_sub.add_run(
        "1. Matan Arab Berharakat Lengkap (RTL)  •  2. Transliterasi Latin  •  3. Terjemahan Bahasa Indonesia\n"
        "4. Syarah Nahwu-Shorof & Penjelasan Hisab Wafaq  •  5. Khususiyah & Tatacara Praktik  •  16 Wafaq Asli 300 DPI"
    )
    format_run_fonts(r4, font_latin="Calibri", size_pt=9.5, italic=True, color=C_SLATE_MUTED, is_rtl=False)

    # Heading 1: DAFTAR ISI LENGKAP (HALAMAN 01–65)
    p_toc_h = doc.add_paragraph(style="Heading 1")
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_toc_h.paragraph_format.space_before = Pt(8)
    p_toc_h.paragraph_format.space_after = Pt(6)
    set_p_bidi(p_toc_h, False)
    for r in list(p_toc_h.runs):
        p_toc_h._p.remove(r._r)
    r_th = p_toc_h.add_run("DAFTAR ISI LENGKAP — HALAMAN 01 s.d. HALAMAN 65")
    format_run_fonts(r_th, font_latin="Calibri", size_pt=13, bold=True, color=C_EMERALD_DARK)

    toc_tbl = doc.add_table(rows=1, cols=3)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = toc_tbl._tbl.tblPr
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'  <w:left w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'  <w:right w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'</w:tblBorders>'
    ))
    hdr_cells = toc_tbl.rows[0].cells
    col_widths = [Inches(0.65), Inches(3.25), Inches(2.65)]
    headers_txt = ["Hal.", "Pokok Bahasan (Terjemahan)", "Judul Bab (Matan Arab)"]
    for idx, c in enumerate(hdr_cells):
        c.width = col_widths[idx]
        c._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="064E3B"/>'))
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else (WD_ALIGN_PARAGRAPH.RIGHT if idx == 2 else WD_ALIGN_PARAGRAPH.LEFT)
        set_p_bidi(p, False)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(headers_txt[idx])
        format_run_fonts(r, size_pt=9.5, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))

    for pnum, ar_t, id_t in toc_items:
        row = toc_tbl.add_row()
        cells = row.cells
        bg = "F8FAFC" if pnum % 2 == 0 else "FFFFFF"
        if pnum in (1, 4, 31, 43, 65):
            bg = "ECFDF5"
        for idx, c in enumerate(cells):
            c.width = col_widths[idx]
            c._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{bg}"/>'))
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            if idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_p_bidi(p, False)
                r = p.add_run(f"{pnum:02d}")
                format_run_fonts(r, size_pt=9, bold=True, color=C_EMERALD_DARK)
            elif idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                set_p_bidi(p, False)
                r = p.add_run(id_t)
                format_run_fonts(r, size_pt=9, bold=(pnum in (1, 4, 31, 43, 65)), color=C_SLATE_DARK)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                set_p_bidi(p, True)
                r = p.add_run(ar_t)
                format_run_fonts(r, font_latin="Traditional Arabic", font_arabic="Traditional Arabic",
                                 size_pt=11.5, size_cs_pt=12, bold=True, color=C_EMERALD_DARK, is_rtl=True)

    doc.add_page_break()

    # -----------------------------------------------------------------------
    # RENDER ALL 65 PAGES (5 LAPIS BERSIH + 16 ORIGINAL 300 DPI WAFAQS)
    # -----------------------------------------------------------------------
    LAYER_STYLES = {
        "arab": (True, WD_ALIGN_PARAGRAPH.RIGHT, C_EMERALD_DARK, "ECFDF5"),
        "latin": (False, WD_ALIGN_PARAGRAPH.LEFT, C_NAVY, "EFF6FF"),
        "Terjemahan": (False, WD_ALIGN_PARAGRAPH.LEFT, C_EMERALD_MID, "F0FDF4"),
        "Syarah dan Penjelasan": (False, WD_ALIGN_PARAGRAPH.LEFT, C_GOLD_DARK, "FFFBEB"),
        "Khususiyah dan Tatacara Praktik": (False, WD_ALIGN_PARAGRAPH.LEFT, C_NAVY, "F8FAFC"),
    }

    embedded_wafaq_count = 0

    for b_idx, block in enumerate(blocks):
        if b_idx > 0:
            doc.add_page_break()

        lines = block.splitlines()
        hdr_raw = strip_dir_marks(lines[0]).lstrip("# ").strip()
        m_hdr = re.match(r"HALAMAN (\d{2})\s*—\s*(.+)", hdr_raw)
        page_num = int(m_hdr.group(1))
        ar_title = m_hdr.group(2).strip()

        # Heading 2 Banner for Page
        p_h2 = doc.add_paragraph(style="Heading 2")
        p_h2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_h2.paragraph_format.space_before = Pt(4)
        p_h2.paragraph_format.space_after = Pt(8)
        set_p_bidi(p_h2, False)
        set_p_shading(p_h2, "ECFDF5")
        set_p_bottom_border(p_h2, "065F46", "10")
        r_pnum = p_h2.add_run(f"HALAMAN {page_num:02d} — ")
        format_run_fonts(r_pnum, font_latin="Calibri", size_pt=13.5, bold=True, color=C_EMERALD_DARK)
        emit_text_segments_with_arabic_detection(p_h2, ar_title, bold=True, base_size=13.5, base_color=C_EMERALD_DARK)

        # Split into 5 layers
        sec_matches = list(re.finditer(r"^### (arab|latin|Terjemahan|Syarah dan Penjelasan|Khususiyah dan Tatacara Praktik)\n(.*?)(?=^### |\Z)", block, flags=re.M | re.S))
        assert len(sec_matches) == 5, f"Page {page_num} has {len(sec_matches)} sections!"

        page_tbl_idx = 0

        for sm in sec_matches:
            sec_name = sm.group(1)
            sec_body = sm.group(2).strip()
            is_ar_sec, sec_align, sec_color, sec_bg = LAYER_STYLES[sec_name]

            # Heading 3 Layer Label
            p_h3 = doc.add_paragraph(style="Heading 3")
            p_h3.alignment = sec_align
            p_h3.paragraph_format.space_before = Pt(8)
            p_h3.paragraph_format.space_after = Pt(4)
            set_p_bidi(p_h3, False)
            set_p_shading(p_h3, sec_bg)
            r_h3 = p_h3.add_run(sec_name)
            format_run_fonts(r_h3, font_latin="Calibri", size_pt=11, bold=True, color=sec_color)

            # Parse lines & Markdown tables inside sec_body
            raw_lines = sec_body.splitlines()
            i = 0
            while i < len(raw_lines):
                ln_clean = strip_dir_marks(raw_lines[i]).rstrip()
                if not ln_clean.strip():
                    i += 1
                    continue

                # Check Markdown table start
                if ln_clean.lstrip().startswith("|") and ln_clean.endswith("|"):
                    tbl_rows = []
                    while i < len(raw_lines):
                        tln = strip_dir_marks(raw_lines[i]).strip()
                        if tln.startswith("|") and tln.endswith("|"):
                            if not re.match(r"^\|[-:| ]+\|$", tln):
                                cells = [c.strip() for c in tln.strip("|").split("|")]
                                tbl_rows.append(cells)
                            i += 1
                        else:
                            break
                    if tbl_rows:
                        ncols = max(len(r) for r in tbl_rows)
                        t = doc.add_table(rows=len(tbl_rows), cols=ncols)
                        for r_i, r_cells in enumerate(tbl_rows):
                            for c_i, val in enumerate(r_cells):
                                t.cell(r_i, c_i).paragraphs[0].text = val
                        style_rtl_wafaq_table(t, ncols)
                        # Embed authentic 300 DPI wafaq image right below its Arabic wafaq table!
                        if is_ar_sec:
                            add_wafaq_image(doc, page_num, page_tbl_idx)
                            page_tbl_idx += 1
                            embedded_wafaq_count += 1
                    continue

                # Regular / list paragraph
                if is_ar_sec:
                    p = doc.add_paragraph()
                    # Check if purely Latin URL line inside arab (e.g. Hal 65 http://www.alanwaralqadria.com)
                    if ln_clean.strip().startswith("http://") or ln_clean.strip().startswith("https://"):
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        set_p_bidi(p, False)
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(4)
                        r_url = p.add_run(ln_clean.strip())
                        format_run_fonts(r_url, font_latin="Calibri", size_pt=11, color=C_NAVY, is_rtl=False)
                    else:
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        set_p_bidi(p, True)
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(5)
                        p.paragraph_format.line_spacing = 1.45
                        r_ar = p.add_run(ln_clean.strip())
                        format_run_fonts(
                            r_ar,
                            font_latin="Traditional Arabic",
                            font_arabic="Traditional Arabic",
                            size_pt=16,
                            size_cs_pt=16.5,
                            bold=False,
                            color=RGBColor(0x11, 0x18, 0x27),
                            is_rtl=True,
                        )
                else:
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    set_p_bidi(p, False)
                    p.paragraph_format.line_spacing = 1.25
                    p.paragraph_format.space_before = Pt(1.5)
                    p.paragraph_format.space_after = Pt(3.5)

                    # Detect indentation / list hierarchy cleanly
                    leading_spaces = len(ln_clean) - len(ln_clean.lstrip(" "))
                    stripped = ln_clean.lstrip(" ")

                    if stripped.startswith("- "):
                        # Bullet item: render clean "• " with hanging indent (zero raw "-" markdown marker!)
                        lvl = 1 if leading_spaces <= 4 else (2 if leading_spaces <= 6 else 3)
                        p.paragraph_format.left_indent = Inches(0.22 * lvl + 0.12)
                        p.paragraph_format.first_line_indent = Inches(-0.14)
                        r_bul = p.add_run("•  ")
                        format_run_fonts(r_bul, size_pt=10.5, bold=True, color=C_EMERALD_MID)
                        parse_inline_rich(p, stripped[2:], base_size=10.5 if sec_name.startswith(("Syarah", "Khususiyah")) else 11)
                    elif re.match(r"^\d+[\.)]\s+", stripped):
                        m_num = re.match(r"^(\d+[\.)]\s+)(.*)", stripped)
                        lvl = 0 if leading_spaces == 0 else (1 if leading_spaces <= 5 else 2)
                        p.paragraph_format.left_indent = Inches(0.22 * lvl + 0.22)
                        p.paragraph_format.first_line_indent = Inches(-0.22)
                        r_num = p.add_run(m_num.group(1))
                        format_run_fonts(r_num, size_pt=11, bold=(lvl == 0 and sec_name.startswith(("Syarah", "Khususiyah"))), color=C_EMERALD_DARK if lvl == 0 else C_SLATE_DARK)
                        parse_inline_rich(p, m_num.group(2), base_size=10.5 if sec_name.startswith(("Syarah", "Khususiyah")) else 11)
                    else:
                        if leading_spaces >= 2:
                            p.paragraph_format.left_indent = Inches(0.25)
                        is_ital_sec = (sec_name == "latin")
                        parse_inline_rich(
                            p,
                            stripped,
                            italic=is_ital_sec and not stripped.startswith("["),
                            base_size=10.5 if sec_name.startswith(("Syarah", "Khususiyah")) else 11,
                            base_color=C_SLATE_MUTED if stripped.startswith("[Wafaq") or stripped.startswith("[Jadwal") else C_SLATE_DARK,
                        )
                i += 1

    assert embedded_wafaq_count == 16, f"Expected 16 embedded wafaqs, got {embedded_wafaq_count}"
    doc.save(str(OUT_DOCX))
    print(f"Successfully generated {OUT_DOCX} ({OUT_DOCX.stat().st_size:,} bytes) with {embedded_wafaq_count}/16 300-DPI wafaqs!")

if __name__ == "__main__":
    build_docx()
