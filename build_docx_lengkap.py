#!/usr/bin/env python3
"""
REBUILD TOTAL DOCX Batch02 V2 Hal09-13 — 9 KETENTUAN LENGKAP
Template identik Batch01 V2 Hal01 Sampul (perfect PDF 8 hal)
Output: /tmp/REVISI_ANWAR_MUJAROBAT_BATCH02_V2_9KETENTUAN_HAL09-13_LENGKAP.docx
"""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC_MD = Path("REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md")
OUT_TMP = Path("/tmp/REVISI_ANWAR_MUJAROBAT_BATCH02_V2_9KETENTUAN_HAL09-13_LENGKAP.docx")
OUT_REPO = Path("REVISI_ANWAR_MUJAROBAT_BATCH02_V2_9KETENTUAN_HAL09-13_LENGKAP.docx")

FULL = {
    9:  Path("rajah_anwar_v2_300/hal09_300dpi.png"),
    10: Path("rajah_anwar_v2_300/hal10_300dpi.png"),
    11: Path("rajah_anwar_v2_300/hal11_300dpi.png"),
    12: Path("rajah_anwar_v2_300/hal12_300dpi.png"),
    13: Path("rajah_anwar_v2_300/hal13_300dpi.png"),
}
CROP10 = Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg")
CROP12 = Path("rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg")

md = SRC_MD.read_text(encoding="utf-8")

# --- helpers ---
def set_cell_shading(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'), color)
    tcPr.append(shd)

def set_paragraph_shading(paragraph, color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'), color)
    pPr.append(shd)

def add_bidi(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'),'1'); pPr.append(bidi)

def add_page_number_footer(doc):
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'),'begin')
        instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=' PAGE '
        fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'),'separate')
        fldChar3 = OxmlElement('w:fldChar'); fldChar3.set(qn('w:fldCharType'),'end')
        run._r.append(fldChar1); run._r.append(instr); run._r.append(fldChar2); run._r.append(fldChar3)
        run2 = p.add_run("  •  Anwar Mujarobat Batch02 V2 Hal09-13  •  300 DPI  •  Sumber tunggal rajah_anwar_FINAL_300DPI/ — Jangan crop ulang")
        run2.font.size = Pt(6); run2.font.color.rgb = RGBColor(0x75,0x75,0x75); run2.font.name='Calibri'

def add_header(doc):
    for section in doc.sections:
        header = section.header
        header.is_linked_to_previous = False
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("ANWAR MUJAROBAT — Syeikh al-Basyir  •  BATCH 02 V2 Hal 09–13  •  9 Ketentuan Lengkap  •  rajah_anwar_FINAL_300DPI/ — Jangan crop ulang  •  300 DPI")
        run.font.size = Pt(6.5); run.font.color.rgb = RGBColor(0x6D,0x4C,0x41); run.italic = True; run.font.name='Calibri'

def style_document(doc):
    # page setup A4
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
        section.header_distance = Inches(0.28)
        section.footer_distance = Inches(0.28
        )
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(9)
    style.font.color.rgb = RGBColor(0x21,0x21,0x21)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.space_before = Pt(1)
    style.paragraph_format.line_spacing = 1.08
    for name, size, color in [('Heading 1', 17, RGBColor(0x14,0x3D,0x6B)), ('Heading 2', 12, RGBColor(0x1B,0x5E,0x20)), ('Heading 3', 10, RGBColor(0x4E,0x34,0x2E))]:
        s = doc.styles[name]
        s.font.name = 'Calibri'; s.font.size = Pt(size); s.font.color.rgb = color; s.font.bold = True
        s.paragraph_format.space_before = Pt(7); s.paragraph_format.space_after = Pt(3)
    add_header(doc)
    add_page_number_footer(doc)

def arab_block(doc, text, fill="FFF8E1"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text.strip())
    run.font.name = 'Scheherazade New'
    run.font.size = Pt(13.5)
    run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)
    add_bidi(p)
    set_paragraph_shading(p, fill)
    # border
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ['top','left','bottom','right']:
        el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'BDBDBD')
        pBdr.append(el)
    pPr.append(pBdr)
    return p

def body(doc, text, size=9, bold=False, italic=False, color=None, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(4)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = space_after
    run = p.add_run(text)
    run.font.size = Pt(size); run.bold = bold; run.italic = italic; run.font.name='Calibri'
    if color: run.font.color.rgb = color
    return p

def caption_para(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.size = Pt(7.5); run.italic = True; run.font.color.rgb = RGBColor(0x42,0x42,0x42); run.font.name='Calibri'
    return p

def small_meta(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.size = Pt(6); run.font.color.rgb = RGBColor(0x8D,0x8D,0x8D); run.font.name='Calibri'
    return p

def add_image(doc, path, width, caption, raw_link=None):
    if not path.exists():
        body(doc, f"[GAMBAR HILANG: {path}]", size=8, color=RGBColor(0xC6,0x28,0x28), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        return
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(1)
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width))
    caption_para(doc, caption)
    if raw_link:
        small_meta(doc, f"Sumber: {path}  •  Pertahankan 300 DPI latar putih tanpa compress  •  Raw: {raw_link}")

def table_3col(doc, rows, header_color="1B5E20", header_text_color="FFFFFF"):
    if not rows: return None
    t = doc.add_table(rows=1, cols=3)
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    headers = ["Kata", "I'rab & Kedudukan", "Wazan Sharaf & Asal"]
    for i, h in enumerate(headers):
        hdr[i].text = h
        for par in hdr[i].paragraphs:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in par.runs:
                run.bold = True; run.font.size = Pt(7.5); run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF); run.font.name='Calibri'
        set_cell_shading(hdr[i], header_color)
        hdr[i].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
    for kata, irab, wazan in rows:
        cells = t.add_row().cells
        cells[0].text = kata; cells[1].text = irab; cells[2].text = wazan
        for ci, cell in enumerate(cells):
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(7.5); run.font.name = 'Calibri'
                    if ci==0:
                        run.bold = True; run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)
                par.paragraph_format.space_before = Pt(1); par.paragraph_format.space_after = Pt(1)
            if ci==0:
                set_cell_shading(cell, "FFF8E1")
    return t

# ---- Parse helpers for 9 ketentuan per HAL ----
def extract_hal_block(md, hal):
    pat = rf"## HALAMAN {hal:02d}.*?(?=\n## HALAMAN \d{{2}}|\n---\n\n> \*\*KHATAM|\Z)"
    m = re.search(pat, md, re.DOTALL)
    return m.group(0) if m else ""

def extract_arab(md_hal):
    m = re.search(r"```arab(.*?)```", md_hal, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_section(md_hal, heading_keyword):
    # heading like "### 2) Kaidah" -> next heading "### 3)"
    pat = rf"### \d\) {heading_keyword}.*?\n(.*?)(?=\n### \d\)|\n---|\n## HALAMAN|\Z)"
    m = re.search(pat, md_hal, re.DOTALL)
    return m.group(1).strip() if m else ""

def parse_nahwu_to_rows(nahwu_text):
    rows=[]
    # Each line: - **WORD** = ... wazan **...** etc.
    lines = [l.strip() for l in nahwu_text.split("\n") if l.strip().startswith("- **")]
    for line in lines:
        # extract **WORD**
        m = re.search(r"\*\*(.+?)\*\*", line)
        if not m: continue
        kata = m.group(1).strip().strip('`')
        # remainder after =
        parts = line.split("=",1)
        remainder = parts[1].strip() if len(parts)>1 else ""
        # Try to split i'rab vs wazan: look for wazan keyword
        # wazan may be like wazan **...** or wazan ...
        # We'll split at "wazan" or "Wazan" or "—"
        # Heuristic: irab is before "wazan", wazan is after
        irab = remainder
        wazan = ""
        # find wazan marker
        low = remainder.lower()
        idx = low.find("wazan")
        if idx!=-1:
            irab = remainder[:idx].strip(" ,—-")
            wazan = remainder[idx:].strip()
            # clean wazan: keep up to next period
        else:
            # alternative: look for "dari" as wazan start
            pass
        # clean markdown ** -> remove
        irab = re.sub(r"\*\*", "", irab)
        wazan = re.sub(r"\*\*", "", wazan)
        # truncate long cells
        if len(irab) > 280: irab = irab[:277] + "..."
        if len(wazan) > 220: wazan = wazan[:217] + "..."
        rows.append((kata, irab, wazan))
    return rows

def extract_3wasal(md_hal):
    sec = extract_section(md_hal, "3 Hukum Washal")
    # Split into A/B/C
    # Patterns: **A. Washal:** etc
    a = re.search(r"\*\*A\. Washal:\*\*(.*?)(?=\*\*B\. Waqf|\Z)", sec, re.DOTALL)
    b = re.search(r"\*\*B\. Waqf:\*\*(.*?)(?=\*\*C\. Ibtida|\Z)", sec, re.DOTALL)
    c = re.search(r"\*\*C\. Ibtida.*?(\*\*C\. Ibtida[^\:]*:\*\*)?(.*)", sec, re.DOTALL)
    # fallback: use whole sec if not found
    return (a.group(1).strip() if a else sec[:600],
            b.group(1).strip() if b else "",
            c.group(2).strip() if c and c.group(2) else "")

def extract_latin(md_hal):
    sec = extract_section(md_hal, "Latin Washal Bunyi")
    return sec

def extract_terjemah(md_hal):
    m = re.search(r"### 5\) Terjemahan\n(.*?)(?=\n### 6\)|\n---|\Z)", md_hal, re.DOTALL)
    if m:
        t = m.group(1).strip()
        # remove leading "> " markers
        t = re.sub(r"^> ", "", t, flags=re.MULTILINE)
        t = re.sub(r"^\> ", "", t, flags=re.MULTILINE)
        return t
    return ""

def extract_syarah(md_hal):
    sec = extract_section(md_hal, "Syarah")
    return sec

def extract_khususiyah(md_hal):
    sec = extract_section(md_hal, "Khususiyah")
    return sec

def extract_struktur(md_hal):
    sec = extract_section(md_hal, "Struktur Kitab")
    return sec

def extract_crop_sec(md_hal):
    sec = extract_section(md_hal, "Crop 300 DPI")
    return sec

# ============ Build DOC ============
doc = Document()
style_document(doc)

# COVER
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("REVISI ANWAR MUJAROBAT — SYEIKH AL-BASYIR"); r.font.size=Pt(9); r.font.color.rgb=RGBColor(0x6A,0x1B,0x9A); r.bold=True
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("BATCH 02 V2 — HAL 09–13 — 9 KETENTUAN LENGKAP"); r.font.size=Pt(20); r.bold=True; r.font.color.rgb=RGBColor(0x14,0x3D,0x6B)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Rebuild Total — Bukan Ringkasan — 5 Halaman × 9 Lapis Identik Batch 01 V2 Hal 01 Sampul"); r.font.size=Pt(8.5); r.italic=True; r.font.color.rgb=RGBColor(0x55,0x55,0x55)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Faedah Muhriqah (2 hal) + Faedah Qathi'ah (2 hal) + Zajr Qathi' 1/3  •  2 Wafaq FINAL 300 DPI  •  Sumber tunggal rajah_anwar_FINAL_300DPI/"); r.font.size=Pt(8); r.font.color.rgb=RGBColor(0x33,0x33,0x33)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("— — — — —"); r.font.color.rgb=RGBColor(0xBC,0xBC,0xBC)

# Meta table
t = doc.add_table(rows=1, cols=2); t.style='Light Grid Accent 1'
hdr = t.rows[0].cells
hdr[0].text="KETERANGAN"; hdr[1].text="RINCIAN"
for cell in hdr:
    for par in cell.paragraphs: par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    for run in cell.paragraphs[0].runs: run.bold=True; run.font.size=Pt(7)
    set_cell_shading(cell, "1B5E20")
    for run in cell.paragraphs[0].runs: run.font.color.rgb=RGBColor(0xFF,0xFF,0xFF)

meta_rows=[
    ("Sumber PDF", "anwar_mujarobat_asli.pdf 65 hal — Hal PDF 09–13/65 — Scan 300 DPI hal09 (1.6M) • hal10 1.2M • hal11 840KB • hal12 687KB • hal13 780KB — 3300×2550"),
    ("Scan 300 DPI", "rajah_anwar_v2_300/hal09_300dpi.png s/d hal13_300dpi.png — latar kuning krem, 300 DPI asli tanpa compress"),
    ("Wafaq sumber tunggal", "rajah_anwar_FINAL_300DPI/ — 15 JPG 1.2M total — Batch02 pakai 2 FINAL: Hal10 IMG_20261025_072854.jpg 435×370 59KB [Gambar 2.1] & Hal12 IMG_20261025_073117.jpg 683×263 80KB [Gambar 2.2] — Hal09/11/13 tanpa wafaq hanya full scan"),
    ("Template 9 Ketentuan", "(1) Arab Full Harokat (2) Kaidah Nahwu-Sharaf — tabel kata|I'rab|Wazan (3) 3 Hukum Washal A/B/C (4) Latin Kemenag Bunyi (5) Terjemahan PUEBI (6) Syarah (7) Khususiyah & Tata Cara (8) Struktur Kitab (9) Crop FINAL 300 DPI"),
    ("Bacaan akademik", "Arab → transliterasi Kemenag RI (Anwārush-Syaikhil-Basyīr style) → terjemahan baku — matan murni tanpa Tanbih Syar'i"),
    ("PR & Google Docs", "PR #13 MERGED 428ff38 (e12bf57)  •  Google Docs 1IffC92Oc9hm4xBEAIGylAFzekJLQwvhkFFj3cFBrgqw end 282635  •  Branch arena/7021a54a-kitab — rebuild lengkap"),
    ("File lama dibuang", "REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md 55KB 323 baris (ringkasan) — DIGANTI file lengkap ini"),
]
for k,v in meta_rows:
    cells=t.add_row().cells
    cells[0].text=k; cells[1].text=v
    for ci, cell in enumerate(cells):
        for par in cell.paragraphs:
            for run in par.runs: run.font.size=Pt(7)
            if ci==0:
                for run in par.runs: run.bold=True
                set_cell_shading(cell, "F1F8E9")

body(doc, "Kitab fokus: Anwar Mujarobat Syeikh al-Basyir saja (65 hal) — bukan revisi Abu Ma'syar — Kitab ini riyadhah modern forum Qadiriyah, bukan falak klasik.", size=7, italic=True, color=RGBColor(0x4E,0x34,0x2E), align=WD_ALIGN_PARAGRAPH.CENTER)

# Ringkasan 9 lapis info
body(doc, "Setiap halaman kini disajikan dalam 9 lapis (identik Hal01 Sampul perfect): Arab Full Harokat → Kaidah Nahwu-Sharaf (tabel) → 3 Hukum Washal (A Washal Idgham, B Waqf sukun, C Ibtida' hamzah) → Latin Washal Bunyi (Kemenag RI) → Terjemahan PUEBI → Syarah → Khususiyah & Tata Cara → Struktur Kitab → Crop Wafaq FINAL 300 DPI.", size=8, color=RGBColor(0x33,0x33,0x33))

# TOC
doc.add_heading("DAFTAR ISI — Batch02 V2 Hal09–13 LENGKAP", level=1)
toc=[
    "HAL 09 — Faedah Muhriqah Tharidah 1/2 — teori mazj-taksir (ا هـ ط م ك س ق) …………… 4",
    "HAL 10 — Faedah Muhriqah 2/2 — Jadwal & Qasam — Hinqayil 158 + Gambar 2.1 FINAL …… 10",
    "HAL 11 — Faedah Qathi'ah li 'Ilaj al-Mass 1/2 — 5 ayat (Syams/Ikhlash/Nur/Hajj/Jinn) … 16",
    "HAL 12 — Faedah Qathi'ah 2/2 — Wafaq 3×3 — 6000/1209/18 + Gambar 2.2 FINAL ………… 22",
    "HAL 13 — Zajr Qathi' li Akhdz al-'Ahd 1/3 — 'ulwi vs suflī + Taubah 46 ………………… 28",
    "LAMPIRAN — 5 Full Scan 300 DPI + 2 Crop FINAL + Manifest ……………………… 34",
]
for it in toc:
    p=doc.add_paragraph(style='List Bullet')
    run=p.add_run(it); run.font.size=Pt(8)

doc.add_page_break()

# ===== HAL 09-13 loops =====
HAL_TITLES = {
    9:  ("HALAMAN 09 — FAEDAH MUHRIQAH THARIDAH 1/2", "فَائِدَةٌ مُحْرِقَةٌ طَارِدَةٌ لِلْجِنِّ وَالْمَرَدَةِ بِإِذْنِ اللهِ", "Teori mazj (ا هـ ط م ك س ق) + taksir ilā al-makhraj ma'a tarkihi — 3 waraqāt + sidr/qaranful/mustakā — tanpa wafaq"),
    10: ("HALAMAN 10 — FAEDAH MUHRIQAH 2/2 — JADWAL & QASAM", "أَخَذْنَا حُرُوفَ الرُّوحَانِيِّ مِنَ السَّطْرِ الثَّالِثِ [ن ح ق] = 158 → حِنْقَايِيلُ", "Contoh Hasan bin Ruqayyah — Jadwal 5×15 — Qasam Thaktsayil/'Awtsayil/Fahghayil — Gambar 2.1 FINAL"),
    11: ("HALAMAN 11 — FAEDAH QATHI'AH LI 'ILAJ AL-MASS 1/2", "فَائِدَةٌ قَاطِعَةٌ لِعِلَاجِ الْمَسِّ — 5 ayat", "Teori Mass + Dafā'in — Syams/Ikhlash/Nur/Hajj/Jinn — Isya kecuali Rabu/Sabtu — tanpa wafaq"),
    12: ("HALAMAN 12 — FAEDAH QATHI'AH 2/2 — WAFAQ 3×3", "وَفْقٌ لِعِلَاجِ الْمَسِّ — مُنْتَدَى الْأَنْوَارِ", "Wafaq angka mu'addal 6000 |1209|18 — kanan→kiri — Gambar 2.2 FINAL"),
    13: ("HALAMAN 13 — ZAJR QATHI' LI AKHDZ AL-'AHD 1/3", "الزَّجْرُ الْقَاطِعُ لِأَخْذِ الْعَهْدِ عَلَى خَادِمِ الِاسْتِنْزَالِ", "'ulwi vs suflī — 7 Mulūk — Taubah 46 7× — tanpa wafaq"),
}

hal_struct_map = {
    9: "[HAL06-08] Faedah01 Maysarah → [HAL09] Faedah02 1/2 (mazj-taksir) → [HAL10] Contoh 158 Hinqayil → [HAL11-12] Qathi'ah → [HAL13] Zajr  — pintu Faedah02",
    10: "[HAL09] Teori mazj → [HAL10] Contoh 158 Hinqayil + Jadwal + Qasam ← ANDA DI SINI → [HAL11] Qathi'ah 1/2 → [HAL12] Wafaq 3×3 → [HAL13] Zajr",
    11: "[HAL10] Jadwal Muhriqah → [HAL11] Faedah03 1/2 (5 ayat) ← ANDA DI SINI → [HAL12] Wafaq 3×3 → [HAL13] Zajr Qathi'",
    12: "[HAL11] Teori 5 ayat → [HAL12] Wafaq 3×3 ← ANDA DI SINI → [HAL13] Zajr 1/3 → [HAL14] Wafaq hijau 8-bagian",
    13: "[HAL12] Wafaq Mass → [HAL13] Zajr Qathi' 1/3 ← ANDA DI SINI → [HAL14] Zajr lanjutan (wafaq hijau 8-bagian) — muqaddimah istinzal",
}

for hal in [9,10,11,12,13]:
    title, arab_short, subtitle = HAL_TITLES[hal]
    # Header per HAL
    if hal != 9:
        doc.add_page_break()
    h = doc.add_heading(title, level=1)
    # subtitle line
    body(doc, arab_short, size=9, italic=True, color=RGBColor(0x1B,0x5E,0x20), align=WD_ALIGN_PARAGRAPH.RIGHT)
    body(doc, subtitle, size=8, color=RGBColor(0x6D,0x4C,0x41), italic=True)
    # Struktur breadcrumb
    body(doc, hal_struct_map[hal], size=6.5, bold=True, color=RGBColor(0x0D,0x47,0xA1), align=WD_ALIGN_PARAGRAPH.CENTER)

    # --- Extract хал block ---
    hal_block = extract_hal_block(md, hal)
    if not hal_block:
        body(doc, f"[HAL {hal} block not found — fallback]", color=RGBColor(0xC6,0x28,0x28))
        continue

    # Full scan image top (required: 5 full scans)
    body(doc, f"Full scan 300 DPI — {FULL[hal].name} — {FULL[hal].stat().st_size/1024:.0f} KB — 3300×2550 — pertahankan 300 DPI tanpa crop ulang:", size=7, bold=True, color=RGBColor(0x4E,0x34,0x2E))
    add_image(doc, FULL[hal], width=6.0 if hal!=10 else 5.8,
              caption=f"[Full Scan Hal {hal:02d}: anwar_mujarobat_asli.pdf Hal PDF {hal:02d}/65 — 300 DPI — rajah_anwar_v2_300/{FULL[hal].name}]",
              raw_link=f"https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_v2_300/{FULL[hal].name}")

    # 1) Arab Full Harokat
    doc.add_heading("1) Arab Full Harokat", level=2)
    arab = extract_arab(hal_block)
    if arab:
        # split into paragraphs by double newline
        paras = [p.strip() for p in arab.split("\n\n") if p.strip()]
        for para in paras:
            # For jadwal lines in hal10, handle separately
            if hal==10 and "ا ح د" in para or "ا ا د" in para:
                # This is jadwal - will be handled after
                continue
            arab_block(doc, para, fill="FFF8E1")
        # For Hal10 jadwal special
        if hal==10:
            jadwal = re.search(r"```\n(ا ح د.*?ا د و ط.*?)\n```", hal_block, re.DOTALL)
            if jadwal:
                body(doc, "Jadwal (5 baris × 15 kolom, dibaca kanan→kiri — 4 penjuru حِنْقَايِيلُ):", size=8, bold=True, color=RGBColor(0x1B,0x5E,0x20))
                jt = jadwal.group(1)
                for line in jt.split("\n"):
                    if line.strip():
                        arab_block(doc, line.strip(), fill="E8F5E9")
                body(doc, "Empat penjuru jadwal tertulis diagonal: حِنْقَايِيلُ (4 sudut merah) — lihat Crop FINAL Gambar 2.1 di bawah.", size=7, italic=True)
        # For Hal12 wafaq numbers
        if hal==12:
            wafaq_nums = re.search(r"```\n(٦٠٠٠.*?٦١٨)\n```", hal_block, re.DOTALL)
            if wafaq_nums:
                body(doc, "Wafaq 3×3 angka (dibaca kanan→kiri per baris):", size=8, bold=True)
                for line in wafaq_nums.group(1).split("\n"):
                    if line.strip():
                        arab_block(doc, line.strip(), fill="FCE4EC")
    else:
        body(doc, "[Arab block missing]", color=RGBColor(0xC6,0x28,0x28))

    # 2) Kaidah Nahwu-Sharaf — TABLE
    doc.add_heading("2) Kaidah Nahwu–Sharaf", level=2)
    nahwu_raw = extract_section(hal_block, "Kaidah Nahwu")
    rows = parse_nahwu_to_rows(nahwu_raw)
    if rows:
        body(doc, "Tabel i'rab & wazan sharaf per kata (seperti Hal01 Sampul — format 3 kolom):", size=7, italic=True, color=RGBColor(0x55,0x55,0x55))
        table_3col(doc, rows)
        # If there are leftover notes beyond bullets, add as paragraph
        # Extract non-bullet lines (e.g., idhafah bertingkat)
        remaining = "\n".join([l for l in nahwu_raw.split("\n") if not l.strip().startswith("- **") and l.strip()])
        if remaining.strip():
            for line in remaining.split("\n"):
                if line.strip() and not line.strip().startswith("|"):
                    body(doc, line.strip(), size=7.5, color=RGBColor(0x42,0x42,0x42))
    else:
        # fallback: dump raw as bullets
        for line in nahwu_raw.split("\n"):
            if line.strip().startswith("- "):
                body(doc, line.strip()[2:], size=8)

    # 3) 3 Hukum Washal
    doc.add_heading("3) 3 Hukum Washal", level=2)
    a,b,c = extract_3wasal(hal_block)
    for label, content, color in [("Hukum A — Washal (Menyambung + Idgham)", a, "E8F5E9"), ("Hukum B — Waqf (Berhenti dengan sukun & qalqalah)", b, "FFF3E0"), ("Hukum C — Ibtida' (Memulai — hamzah qath'/washal)", c, "E3F2FD")]:
        doc.add_heading(label, level=3)
        if content:
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'), color); pPr.append(shd)
            run = p.add_run(content.strip())
            run.font.size = Pt(8); run.font.name='Calibri'
        else:
            body(doc, "[konten washal kosong — lihat nash Hal01 untuk kaidah umum]", size=7, italic=True)

    # 4) Latin Washal Bunyi
    doc.add_heading("4) Latin Washal Bunyi", level=2)
    latin = extract_latin(hal_block)
    if latin:
        body(doc, "Transliterasi Kemenag RI — Ejaan Harfiah (qathi') vs Bunyi Washal (sambung):", size=7, bold=True, color=RGBColor(0x0D,0x47,0xA1))
        # Split Harfiah vs Washal bunyi
        # Find blocks Harfiah: and Washal / Washal bunyi:
        harfiah = re.search(r"\*\*Harfiah:\*\*(.*?)(?=\*\*Washal|\n>|\Z)", latin, re.DOTALL)
        washal = re.search(r"\*\*Washal bunyi:\*\*(.*?)(?=\n###|\Z)", latin, re.DOTALL)
        if harfiah:
            p = doc.add_paragraph()
            set_paragraph_shading(p, "FFF8E1")
            run = p.add_run("Harfiah (qathi'): " + harfiah.group(1).strip())
            run.font.size = Pt(8); run.font.name='Calibri'
        if washal:
            p = doc.add_paragraph()
            set_paragraph_shading(p, "E8F5E9")
            run = p.add_run("Washal bunyi (sambung — dipakai ijazah/tilawah): " + washal.group(1).strip())
            run.italic = True; run.font.size = Pt(8); run.font.name='Calibri'
        # fallback dump remainder
        if not harfiah and not washal:
            for line in latin.split("\n"):
                if line.strip():
                    body(doc, line.strip(), size=8, italic=True)
    else:
        body(doc, "[Latin belum terisi — lihat contoh Hal10: Hinqāyīl, Thaktsāyīl, 'Awtsāyīl, Fahghāyīl]", size=8, italic=True)

    # 5) Terjemahan
    doc.add_heading("5) Terjemahan Indonesia Baku (PUEBI)", level=2)
    terjemah = extract_terjemah(hal_block)
    if terjemah:
        p = doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'E3F2FD')
        pPr.append(shd)
        pBdr = OxmlElement('w:pBdr')
        left = OxmlElement('w:left'); left.set(qn('w:val'),'single'); left.set(qn('w:sz'),'12'); left.set(qn('w:space'),'6'); left.set(qn('w:color'),'64B5F6')
        pBdr.append(left); pPr.append(pBdr)
        # handle bold via ** split
        parts = re.split(r"(\*\*.*?\*\*)", terjemah)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                run = p.add_run(part[2:-2]); run.bold=True; run.font.size=Pt(9)
            elif part.strip():
                run = p.add_run(part); run.font.size=Pt(9)
    else:
        body(doc, "[Terjemahan belum terisi]", size=8)

    # 6) Syarah
    doc.add_heading("6) Syarah", level=2)
    syarah = extract_syarah(hal_block)
    if syarah:
        for line in syarah.split("\n"):
            line=line.strip()
            if not line: continue
            if line.startswith("> "):  # quote skipped (translation)
                continue
            if line.startswith("- "):
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(line[2:]); run.font.size=Pt(8)
            else:
                # Handle bold
                p = doc.add_paragraph()
                parts = re.split(r"(\*\*.*?\*\*)", line)
                for part in parts:
                    if part.startswith("**") and part.endswith("**"):
                        run = p.add_run(part[2:-2]); run.bold=True; run.font.size=Pt(8.5)
                    elif part:
                        run = p.add_run(part); run.font.size=Pt(8.5)
    else:
        body(doc, "[Syarah belum terisi]", size=8)

    # 7) Khususiyah & Tata Cara
    doc.add_heading("7) Khususiyah & Tata Cara", level=2)
    khusus = extract_khususiyah(hal_block)
    if khusus:
        # Parse bullets with bold categories
        for line in khusus.split("\n"):
            line=line.strip()
            if not line: continue
            if line.startswith("**Khasiat:**") or line.startswith("**Tata cara") or line.startswith("**Pantangan") or line.startswith("- **"):
                # Use bold handling
                p = doc.add_paragraph()
                parts = re.split(r"(\*\*.*?\*\*)", line)
                for part in parts:
                    if part.startswith("**") and part.endswith("**"):
                        run = p.add_run(part[2:-2]); run.bold=True; run.font.size=Pt(8.5)
                    elif part:
                        run = p.add_run(part); run.font.size=Pt(8.5)
            elif line.startswith("- "):
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(line[2:]); run.font.size=Pt(8)
            else:
                body(doc, line, size=8)
        # Add highlight box for bilangan/waktu/media per instruction
        if hal in [9,10]:
            p = doc.add_paragraph()
            set_paragraph_shading(p, "FFF8E1")
            pPr = p._p.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            for edge in ['top','left','bottom','right']:
                el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'3'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'FFB74D')
                pBdr.append(el)
            pPr.append(pBdr)
            run = p.add_run("Bilangan: 7 huruf thabi'ah [ا هـ ط م ك س ق] • 3 waraqāt (sidr/qaranful/mustakā) • Taksir genap→baris2 / ganjil→baris3 • 158 → Hinqayil (ن ح ق) — lihat Gambar 2.1")
            run.bold=True; run.font.size=Pt(8)
        if hal in [11,12]:
            p = doc.add_paragraph()
            set_paragraph_shading(p, "E8F5E9")
            pPr = p._p.get_or_add_pPr()
            pBdr = OxmlElement('w:pBdr')
            for edge in ['top','left','bottom','right']:
                el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'3'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'81C784')
                pBdr.append(el)
            pPr.append(pBdr)
            run = p.add_run("Waktu: setelah Isya kecuali Rabu & Sabtu (hari nahas falak Jafari) • Media: bejana baru mawar/za'faran/misk • Mahw air hujan > sumur tak kena matahari/bulan • Telunjuk kanan 7×")
            run.bold=True; run.font.size=Pt(8)
    else:
        body(doc, "[Khususiyah belum terisi]", size=8)

    # 8) Struktur Kitab
    doc.add_heading("8) Struktur Kitab", level=2)
    struktur = extract_struktur(hal_block)
    if struktur:
        # Usually first line is bracket map
        for line in struktur.split("\n"):
            line=line.strip()
            if not line: continue
            if line.startswith("[HAL"):
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(line); run.bold=True; run.font.size=Pt(7); run.font.color.rgb=RGBColor(0x1B,0x5E,0x20); run.font.name='Calibri'
            else:
                body(doc, line, size=7.5, color=RGBColor(0x42,0x42,0x42))
    else:
        body(doc, hal_struct_map.get(hal,""), size=7, bold=True, color=RGBColor(0x1B,0x5E,0x20), align=WD_ALIGN_PARAGRAPH.CENTER)

    # 9) Crop Wafaq FINAL
    doc.add_heading("9) Crop Wafaq FINAL 300 DPI — Sumber Tunggal", level=2)
    if hal == 10:
        body(doc, "DENGAN WAFAQ (1 jadwal) — Sumber tunggal — jangan crop ulang:", size=8, bold=True, color=RGBColor(0x1B,0x5E,0x20))
        add_image(doc, CROP10, width=5.0,
                  caption="[Gambar 2.1: Jadwal Taksir Muhriqah 5×15 — حنقاييل di 4 sudut — Crop Asli 300 DPI]",
                  raw_link="https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg")
        body(doc, "Deskripsi: Tabel 5 baris huruf campuran (ا ح د س ط ن …), 4 diagonal merah Ḥinqāyīl (حنقاييل) — 435×370 px, 59 KB — pertahankan 300 DPI latar putih tanpa compress. Link raw: https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg — Jangan pakai rajah_anwar/rajah_p10_jadwal_muhriqah.png lama (200 DPI).", size=7, color=RGBColor(0x55,0x55,0x55))
        body(doc, "Untuk Hal10, markdown: ![Wafaq Hal 10](rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg)", size=6, color=RGBColor(0x8D,0x8D,0x8D))
    elif hal == 12:
        body(doc, "DENGAN WAFAQ (1) — 3×3 angka — kanan→kiri — Sumber tunggal:", size=8, bold=True, color=RGBColor(0x1B,0x5E,0x20))
        add_image(doc, CROP12, width=5.0,
                  caption="[Gambar 2.2: Wafaq Qathi'ah li 'Ilaj al-Mass 3×3 Angka — 6000/1209/18 — Crop Asli 300 DPI]",
                  raw_link="https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg")
        body(doc, "Deskripsi: Wafaq 3×3 angka — baris1: 6000 |1209|18 — baris2: 27|609|1191 — baris3: 1200|9|618 — garis merah 2pt, angka hitam, latar putih — 683×263 px, 80 KB — tulis mulai dari atas kanan ke kiri • waffaqakumullāh. Link raw: https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg", size=7, color=RGBColor(0x55,0x55,0x55))
        body(doc, "Markdown: ![Wafaq Hal 12](rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg)", size=6, color=RGBColor(0x8D,0x8D,0x8D))
    else:
        # Hal without wafaq
        msg = {9: "Tanpa wafaq di Hal09 (teks teori saja) — jadwal baru di Hal10 — Arsip full: rajah_anwar_v2_300/hal09_300dpi.png (3300×2550, 1.6 MB, kuning krem) — jangan crop baru, pertahankan 300 DPI.",
               11: "Tanpa wafaq di Hal11 (teks + daftar 5 ayat) — wafaq baru di Hal12 — Arsip full: rajah_anwar_v2_300/hal11_300dpi.png (3300×2550, 840KB)",
               13: "Tanpa wafaq di Hal13 (teks hitam-merah) — wafaq hijau 8-bagian menyusul Hal14 — Arsip full: rajah_anwar_v2_300/hal13_300dpi.png (3300×2550, 780KB) — teks hitam-merah"}
        body(doc, msg.get(hal, "Tanpa wafaq — hanya full scan"), size=7.5, italic=True, color=RGBColor(0x6D,0x4C,0x41))
        # Also show small note about source
        small_meta(doc, f"Full scan arsip — jangan crop ulang — hanya halaman dengan wafaq yang pakai rajah_anwar_FINAL_300DPI/ — Hal lain cukup full scan.")

# ===== LAMPIRAN =====
doc.add_page_break()
doc.add_heading("LAMPIRAN — 5 Full Scan 300 DPI + 2 Crop FINAL + Manifest", level=1)
body(doc, "Sumber tunggal rajah_anwar_FINAL_300DPI/ — 15 JPG 1.2M — pertahankan 300 DPI latar putih tanpa compress — Halaman tanpa wafaq (Hal09/11/13) cukup full scan, jangan crop baru:", size=8, bold=True, color=RGBColor(0x1B,0x5E,0x20))

# Manifest table
headers = ["Hal", "Nama File FINAL", "Ukuran", "Wafaq Apa — Caption"]
table = doc.add_table(rows=1, cols=4); table.style='Light Grid Accent 1'
hdr = table.rows[0].cells
for i, h in enumerate(headers):
    hdr[i].text = h
    for par in hdr[i].paragraphs:
        for run in par.runs: run.bold=True; run.font.size=Pt(7); run.font.color.rgb=RGBColor(0xFF,0xFF,0xFF)
        par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    set_cell_shading(hdr[i], "1B5E20")

manifest_rows = [
    ("Hal10", "IMG_20261025_072854.jpg", "435×370 • 59 KB", "[Gambar 2.1: Jadwal Taksir 5×15 — حنقاييل — Crop Asli 300 DPI]"),
    ("Hal12", "IMG_20261025_073117.jpg", "683×263 • 80 KB", "[Gambar 2.2: Wafaq 3×3 6000/1209/18 — Crop Asli 300 DPI]"),
    ("—", "13 file lain di rajah_anwar_FINAL_300DPI/", "1.06 MB", "Hal08 (2) 4×4 & 5×5 mukhammas • Hal14-65 wafaq hijau 8-bagian etc. — Batch03+"),
    ("—", "5 Full scan Hal09-13", "1.6/1.2/840K/687K/780K", "hal09_300dpi.png s/d hal13_300dpi.png — 3300×2550 — kuning krem — arsip 300 DPI"),
]
for r in manifest_rows:
    cells = table.add_row().cells
    for i, val in enumerate(r):
        cells[i].text = val
        for par in cells[i].paragraphs:
            for run in par.runs: run.font.size=Pt(7)

body(doc, "7 Gambar WAJIB — 5 full scan + 2 crop FINAL — semua 300 DPI (1.5/1.2/840/687/780 KB + 59/80 KB):", size=8, bold=True)
for hal in [9,10,11,12,13]:
    body(doc, f"Full Scan Hal{hal:02d} — {FULL[hal].name} — {FULL[hal].stat().st_size/1024:.0f} KB — 300 DPI", size=7, bold=True)
    add_image(doc, FULL[hal], width=5.3,
              caption=f"[Full Scan Hal {hal:02d}: {FULL[hal].name} — 3300×2550 — 300 DPI — rajah_anwar_v2_300/{FULL[hal].name}]",
              raw_link=f"https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_v2_300/{FULL[hal].name}")

# Show FINAL crops again in lampiran as proof
body(doc, "Bukti Crop FINAL 300 DPI — Sumber tunggal — Pertahankan 300 DPI:", size=8, bold=True, color=RGBColor(0xAD,0x14,0x57))
add_image(doc, CROP10, width=4.8, caption="[Gambar 2.1: Jadwal Taksir Muhriqah 5×15 — حنقاييل di 4 sudut — Crop Asli 300 DPI]", raw_link="https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg")
add_image(doc, CROP12, width=4.8, caption="[Gambar 2.2: Wafaq Qathi'ah li 'Ilaj al-Mass 3×3 Angka — 6000/1209/18 — Crop Asli 300 DPI]", raw_link="https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg")

# Khatam
doc.add_heading("KHATAM BATCH 02 V2 — 5 Halaman × 9 Ketentuan LENGKAP", level=1)
p = doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("5 halaman (Muhriqah 2 hal + Qathi'ah 2 hal + Zajr 1 hal) — 7 gambar — 2 Wafaq FINAL 300 DPI — 9 lapis per hal identik Hal01 Sampul Perfect — Rebuild Total."); run.bold=True; run.font.size=Pt(11); run.font.color.rgb=RGBColor(0x1B,0x5E,0x20)
body(doc, "File lama REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md 55KB 323 baris (ringkasan) DIBUANG — digantikan file lengkap ini yang memuat Arab Full Harokat lengkap + tabel Nahwu-Sharaf 3 kolom + 3 Hukum Washal A/B/C + Latin Kemenag bunyi washal (Hinqayil, Thaktsayil, 'Awtsayil, Fahghayil) + Terjemahan PUEBI + Syarah + Khususiyah (7 huruf, 3 waraqāt, jam Isya kecuali Rabu/Sabtu, bejana mawar/za'faran/misk) + Struktur Kitab + Crop FINAL.", size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
body(doc, "PR #13 MERGED 428ff38 (e12bf57) — Google Docs end 282635 — update append lengkap 9 ketentuan (bukan ringkasan) — Branch arena/7021a54a-kitab — Anwar Mujarobat Syeikh al-Basyir — 65 hal.", size=7, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x75,0x75,0x75))

# core props
doc.core_properties.title = "Revisi Anwar Mujarobat Batch02 V2 Hal09-13 LENGKAP — 9 Ketentuan"
doc.core_properties.subject = "Batch02 V2 5 Halaman × 9 Lapis — Arab Harokat, Nahwu-Sharaf tabel, 3 Washal, Latin Kemenag, Terjemahan, Syarah, Khususiyah, Struktur, Crop FINAL 300 DPI"
doc.core_properties.author = "fatimah86-dot/kitab — arena/7021a54a-kitab"
doc.core_properties.keywords = "Anwar Mujarobat, Syeikh Basyir, 9 Ketentuan, 300 DPI, Wafaq FINAL, Hinqayil, Hal09-13"
doc.core_properties.comments = "Rebuild total bukan ringkasan — 7 gambar — 5 full scan + 2 FINAL — pertahankan 300 DPI latar putih tanpa compress — PR #13 e12bf57"

doc.save(OUT_TMP)
# also copy to repo for git if needed
import shutil
shutil.copy(OUT_TMP, OUT_REPO)
print(f"Saved {OUT_TMP} — {OUT_TMP.stat().st_size/1024/1024:.2f} MB")
print(f"Also copied to {OUT_REPO}")
