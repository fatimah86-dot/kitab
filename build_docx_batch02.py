#!/usr/bin/env python3
# Build DOCX for Batch02 V2 Hal09-13
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.dml.color import ColorFormat

SRC = Path("REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md")
OUT = Path("REVISI_BATCH_02_V2_9KETENTUAN_HAL09-13_FINAL.docx")

# Image paths
IMG_FINAL_10 = Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg")  # 59KB Hal10
IMG_FINAL_12 = Path("rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg")  # 80KB Hal12
FULL_SCANS = {
    9: Path("rajah_anwar_v2_300/hal09_300dpi.png"),
    10: Path("rajah_anwar_v2_300/hal10_300dpi.png"),
    11: Path("rajah_anwar_v2_300/hal11_300dpi.png"),
    12: Path("rajah_anwar_v2_300/hal12_300dpi.png"),
    13: Path("rajah_anwar_v2_300/hal13_300dpi.png"),
}

# Read markdown
md = SRC.read_text(encoding="utf-8")

doc = Document()

# -- Page setup A4, margins narrow for max image width, white background
for section in doc.sections:
    section.page_width = Inches(8.27)  # A4
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)

# -- Styles
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(9)
font.color.rgb = RGBColor(0x33,0x33,0x33)
pf = style.paragraph_format
pf.space_after = Pt(4)
pf.space_before = Pt(2)
pf.line_spacing = 1.12

# Heading styles
for name, size, color, bold in [
    ('Heading 1', 16, RGBColor(0x14,0x3D,0x6B), True),
    ('Heading 2', 12, RGBColor(0x1B,0x5E,0x20), True),
    ('Heading 3', 10, RGBColor(0x4E,0x34,0x2E), True),
]:
    s = doc.styles[name]
    s.font.name = 'Calibri'
    s.font.size = Pt(size)
    s.font.color.rgb = color
    s.font.bold = bold
    s.paragraph_format.space_before = Pt(8)
    s.paragraph_format.space_after = Pt(4)
    s.paragraph_format.keep_with_next = False

# Helper to add header/footer
def add_header_footer(doc):
    for section in doc.sections:
        header = section.header
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("ANWAR MUJAROBAT — Syeikh Basyir  •  REVISI BATCH 02 V2 Hal 09–13  •  9 Ketentuan  •  Sumber Tunggal rajah_anwar_FINAL_300DPI/ — JANGAN CROP ULANG")
        run.font.size = Pt(6.5)
        run.font.color.rgb = RGBColor(0x66,0x66,0x66)
        run.font.name = 'Calibri'
        run.italic = True
        # footer
        footer = section.footer
        pf = footer.paragraphs[0]
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        runf = pf.add_run()
        fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'),'begin')
        instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=" PAGE "
        fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'),'end')
        runf._r.append(fldChar1); runf._r.append(instr); runf._r.append(fldChar2)
        runf2 = pf.add_run("  •  Batch02 V2  •  300 DPI  •  Anwar Mujarobat Asli PDF 65 hal")
        runf2.font.size = Pt(6)
        runf2.font.color.rgb = RGBColor(0x88,0x88,0x88)

add_header_footer(doc)

def set_paragraph_shading(paragraph, bg_color_hex="FFF8E1"):
    """Light yellowish shading for Arabic blocks"""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), bg_color_hex)
    pPr.append(shd)

def add_arabic_block(doc, text, fill="FFF8E1"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT  # RTL simulation
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text.strip())
    run.font.name = 'Scheherazade New'  # fallback to Amiri
    # Use Traditional Arabic if available, else Amiri
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)
    # Ensure RTL via bidi
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'), '1')
    pPr.append(bidi)
    set_paragraph_shading(p, fill)
    # Border
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ['top','left','bottom','right']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:space'), '4')
        el.set(qn('w:color'), 'BDBDBD')
        pBdr.append(el)
    pPr.append(pBdr)
    return p

def add_body_text(doc, text, size=9, bold=False, italic=False, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = 'Calibri'
    if color:
        run.font.color.rgb = color
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.size = Pt(8)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x55,0x55,0x55)
    run.font.name = 'Calibri'
    return p

def add_image_with_caption(doc, img_path, caption_text, width_inches=5.5, dpi_note="300 DPI"):
    if not img_path.exists():
        add_body_text(doc, f"[MISSING IMAGE: {img_path}]", size=8, color=RGBColor(0xD3,0x2F,0x2F), bold=True)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    # Width constraint: keep 300 DPI logical size. Original FINAL crops are small (435x370 etc) — enlarge to readable 5.2" while preserving DPI metadata.
    # For full scans (3300×2550), limit to 6.2" width to fit A4.
    run.add_picture(str(img_path), width=Inches(width_inches))
    # Center the image via paragraph alignment already
    # Add caption
    add_caption(doc, caption_text)
    # Add source path small
    ps = doc.add_paragraph()
    ps.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps.paragraph_format.space_after = Pt(8)
    r = ps.add_run(f"Sumber: {img_path}  •  Pertahankan 300 DPI latar putih tanpa compress  •  Raw: https://raw.githubusercontent.com/fatimah86-dot/kitab/main/{img_path}")
    r.font.size = Pt(6)
    r.font.color.rgb = RGBColor(0x90,0x90,0x90)
    r.font.name = 'Calibri'

def add_info_box(doc, title, bullets):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'E8F5E9')
    pPr.append(shd)
    pBdr = OxmlElement('w:pBdr')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'3'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'A5D6A7')
        pBdr.append(el)
    pPr.append(pBdr)
    run = p.add_run(title)
    run.bold = True; run.font.size = Pt(9); run.font.color.rgb = RGBColor(0x1B,0x5E,0x20)
    for b in bullets:
        pb = doc.add_paragraph(style='List Bullet')
        pb.paragraph_format.left_indent = Inches(0.3)
        rn = pb.add_run(b)
        rn.font.size = Pt(8)
        rn.font.name = 'Calibri'

# ==================== COVER ====================
# Logo placeholder
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("REVISI ANWAR MUJAROBAT — Syeikh Basyir"); r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x6A,0x1B,0x9A); r.bold = True; r.font.name='Calibri'
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("BATCH 02 V2  —  HAL 09–13  —  9 KETENTUAN FINAL"); r.font.size = Pt(20); r.bold = True; r.font.color.rgb = RGBColor(0x14,0x3D,0x6B); r.font.name='Calibri'
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Faedah Muhriqah (2 hal) + Faedah Qathi'ah (2 hal) + Zajr Qathi' (1 hal)  •  2 Wafaq FINAL 300 DPI  •  Sumber Tunggal rajah_anwar_FINAL_300DPI/"); r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0x55,0x55,0x55); r.italic = True
# Divider
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("— — — — —"); r.font.color.rgb = RGBColor(0xBC,0xBC,0xBC)

# Meta table
table = doc.add_table(rows=1, cols=2)
table.style = 'Light Grid Accent 1'
table.autofit = True
hdr = table.rows[0].cells
hdr[0].text = "KETERANGAN"; hdr[1].text = "RINCIAN"
for cell in hdr: 
    for pr in cell.paragraphs: pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in cell.paragraphs[0].runs: run.bold = True; run.font.size = Pt(7)
rows_data = [
    ("Sumber PDF", "anwar_mujarobat_asli.pdf 65 hal — Hal PDF 09–13/65"),
    ("Scan 300 DPI", "rajah_anwar_v2_300/hal09_300dpi.png (1.6M) • hal10 1.2M • hal11 840KB • hal12 687KB • hal13 780KB — 3300×2550, latar kuning krem"),
    ("Wafaq sumber tunggal", "rajah_anwar_FINAL_300DPI/ 15 file 1.2M total — Batch02 pakai 2 FINAL: IMG_20261025_072854.jpg (59KB, 435×370) & IMG_20261025_073117.jpg (80KB, 683×263) — 300 DPI, latar putih, tanpa compress, jangan crop ulang"),
    ("Template 9 Ketentuan", "(1) Arab Full Harokat (2) Nahwu-Sharaf (3) 3 Hukum Washal (4) Latin Kemenag (5) Terjemahan (6) Syarah (7) Khususiyah & Tata Cara (8) Struktur Kitab (9) Crop 300 DPI FINAL"),
    ("Tanggal / Cabang", "25 Okt 2026 — arena/4a8b9c56-kitab → PR #13 MERGED 428ff38 (main 2a0af22) — NEXT: arena/7021a54a-kitab DOCX preview"),
    ("File MD", "REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md — 55.099 bytes, 323 baris — Gaya: akademik harfiah (Arab → Latin Kemenag → baku), matan murni tanpa Tanbih Syar'i"),
]
for k,v in rows_data:
    cells = table.add_row().cells
    cells[0].text = k; cells[1].text = v
    for ci, cell in enumerate(cells):
        for pr in cell.paragraphs:
            for run in pr.runs: run.font.size = Pt(7); run.font.name='Calibri'
            if ci==0: 
                for run in pr.runs: run.bold = True; run.font.color.rgb = RGBColor(0x33,0x33,0x33)

doc.add_paragraph()  # spacer

add_info_box(doc, "RINGKASAN BATCH 02 V2 — 5 Halaman — 2 Wafaq FINAL", [
    "HAL 09: Faedah Muhriqah 1/2 — teori mazj (ا هـ ط م ك س ق) + taksir ilā al-makhraj ma'a tarkihi — genap→baris 2 / ganjil→baris 3 — 3 waraqāt + sidr/qaranful/mustakā — pintu Faedah 02.",
    "HAL 10: Faedah Muhriqah 2/2 — FINAL contoh Hasan bin Ruqayyah 158 → Hinqāyīl (ن ح ق) + Jadwal 5×15 (4 sudut حنقاييل merah) + Qasam Thaktsāyīl/'Awtsāyīl/Fahghāyīl + Āhyā Syarāhyā + Yasin 53 + Buruj — Gambar 2.1 FINAL 59KB 435×370.",
    "HAL 11: Faedah Qāthi'ah 1/2 — teori terapi Mass + Dafā'in — 5 ayat: Syams, Ikhlāsh, Nūr 35, Hajj 27, Jinn — bejana baru mawar/za'faran/misk — mahw hujan > sumur tersembunyi — Isya kecuali Rabu/Sabtu.",
    "HAL 12: Faedah Qāthi'ah 2/2 — FINAL Wafaq 3×3 angka (6000 |1209|18 /27|609|1191 /1200|9|618) kanan→kiri wāfaqakumullāh — wafaq 'adadi mu'addal khusus — Gambar 2.2 FINAL 80KB 683×263.",
    "HAL 13: Zajr Qāthi' 1/3 — 'ulwi vs suflī — 7 Mulūk tidak turun (nafsi rabbāni) — Taubah 46 7× pegang dahi nāzhir — syahadatain + Mushaf Mujādalah.",
    "Google Docs: 1IffC92Oc9hm4xBEAIGylAFzekJLQwvhkFFj3cFBrgqw end 282635 (+ test chunk) — MD repo lengkap, Docs chunked 6 segmen.",
    "PR #12 MERGED: https://github.com/fatimah86-dot/kitab/pull/12 (Wafaq FINAL inventory) — PR #13 MERGED: https://github.com/fatimah86-dot/kitab/pull/13 (Batch02 V2)",
])

# Preview total wafaq
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = p.add_run("Preview total wafaq & contoh Hal08 / Hal16 / Hal20 — "); r.bold=True; r.font.size=Pt(8); r.font.color.rgb=RGBColor(0x4E,0x34,0x2E)
add_body_text(doc, "Inventori rajah_anwar_FINAL_300DPI/ : 15 file JPG — 1.2 MB total — 300 DPI asli, latar putih tanpa compress. Contoh cross-ref: Hal08 (2 wafaq 4×4 ruhani + 5×5 mukhammas — FINAL crop_hal08_*.png di Batch01 V2 PR#12), Hal16 & Hal20 menunggu Batch03+ (akan pakai crop FINAL yang sama, markdown ![Wafaq Hal XX](rajah_anwar_FINAL_300DPI/...) + caption [Gambar X.X: ... — Crop Asli 300 DPI] + raw GitHub).", size=8)

# ==================== TOC manual ====================
doc.add_heading("DAFTAR ISI — Batch02 V2 Hal09-13", level=1)
toc_items = [
    "HAL 09 — Faedah Muhriqah Tharidah 1/2 — teori mazj-taksir ………………… 3",
    "HAL 10 — Faedah Muhriqah 2/2 — Jadwal & Qasam (Gambar 2.1 FINAL) … 7",
    "HAL 11 — Faedah Qathi'ah li 'Ilaj al-Mass 1/2 — 5 ayat ………………… 12",
    "HAL 12 — Faedah Qathi'ah 2/2 — Wafaq 3×3 (Gambar 2.2 FINAL) ……… 17",
    "HAL 13 — Zajr Qathi' li Akhdz al-'Ahd 1/3 — 'ulwi/suflī + Taubah46 … 20",
    "Lampiran — Full scan 300 DPI Hal09-13 + Manifest Wafaq FINAL ……… 24",
]
for it in toc_items:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(it); r.font.size = Pt(8)

doc.add_page_break()

# ======================================================
# Parse MD into structured sections — we will manually author per HAL to keep 9 ketentuan fidelity
# Instead of full markdown parser, we extract key Arabic blocks from file and rebuild with high-fidelity layout
# ======================================================

# Helper to extract arab lines quickly
def extract_arab_block(md_text, hal):
    # Simple: find HALAMAN XX section and grab arab code block
    import re
    pat = rf"## HALAMAN {hal:02d}.*?```arab(.*?)```"
    m = re.search(pat, md_text, re.DOTALL)
    if m: return m.group(1).strip()
    return ""

# Define content per HAL — we will load from markdown to ensure completeness, but for DOCX we build curated rich version
# We'll embed the full markdown text as well as images — to satisfy "ambil dari MD 55KB 323 baris"
# Approach: for each HAL, reproduce 9 ketentuan headings with content summarized from MD (already read).

# Load MD sections for verbatim inclusion in annex
# We'll also add a verbatim annex at end with monospaced MD

hals = [
    (9, "FAEDAH MUHRIQAH THARIDAH 1/2 — فَائِدَةٌ مُحْرِقَةٌ طَارِدَةٌ لِلْجِنِّ وَالْمَرَدَةِ بِإِذْنِ اللهِ", "Teori mazj-taksir — 7 huruf thabi'ah api-udara nurani", "tanpa wafaq — teks teori saja"),
    (10, "FAEDAH MUHRIQAH 2/2 — JADWAL & QASAM", "Contoh Hasan bin Ruqayyah 158 → Hinqayil — Jadwal 5×15 — Qasam Thaktsayil", "1 jadwal FINAL — Gambar 2.1"),
    (11, "FAEDAH QATHI'AH LI 'ILAJ AL-MASS 1/2", "Teori Mass + Dafā'in — 5 ayat Syams/Ikhlash/Nur/Hajj/Jinn — waktu Isya", "tanpa wafaq — daftar ayat"),
    (12, "FAEDAH QATHI'AH 2/2 — WAFAQ 3×3", "Wafaq angka mu'addal 6000/1209/18 — tulis kanan→kiri", "1 wafaq FINAL — Gambar 2.2"),
    (13, "ZAJR QATHI' LI AKHDZ AL-'AHD 1/3", "Etika istinzal — 'ulwi vs suflī — 7 Muluk — Taubah 46", "tanpa wafaq — teks merah/hitam"),
]

for hal_num, title, subtitle, wafaq_note in hals:
    # Page break before each HAL except first after TOC already did
    if hal_num != 9:
        doc.add_page_break()
    # HAL header
    h = doc.add_heading(f"HALAMAN {hal_num:02d} — {title}", level=1)
    # Subtitle
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(subtitle + f"  •  {wafaq_note}"); r.font.size=Pt(8); r.font.color.rgb=RGBColor(0x66,0x66,0x66); r.italic=True
    # Structure breadcrumb
    bread = {
        9: "[HAL06-08] Faedah01 Maysarah → [HAL09] Faedah02 1/2 (mazj-taksir) → [HAL10] Contoh Hinqayil → [HAL11-12] Qathi'ah → [HAL13] Zajr",
        10: "[HAL09] Teori mazj → [HAL10] Contoh 158 Hinqayil + Jadwal + Qasam → [HAL11] Qathi'ah → [HAL12] Wafaq 3×3",
        11: "[HAL10] Jadwal Muhriqah → [HAL11] Faedah03 1/2 (5 ayat) → [HAL12] Wafaq 3×3 → [HAL13] Zajr",
        12: "[HAL11] Teori 5 ayat → [HAL12] Wafaq 3×3 FAEDAH03 → [HAL13] Zajr Qathi'",
        13: "[HAL12] Wafaq Mass → [HAL13] Zajr 1/3 ('ulwi/suflī, Taubah46) → [HAL14] Zajr lanjutan (wafaq hijau 8-bagian)",
    }
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run(bread[hal_num]); r2.font.size=Pt(6.5); r2.font.color.rgb=RGBColor(0x18,0x5E,0x4B); r2.bold=True
    # Full scan first (keep 300 DPI)
    add_body_text(doc, f"Full scan 300 DPI — {FULL_SCANS[hal_num].name} (3300×2550, {FULL_SCANS[hal_num].stat().st_size/1024/1024:.2f} MB, kuning krem) — arsip 300 DPI tanpa compress:", size=7, color=RGBColor(0x6D,0x4C,0x41), bold=True)
    add_image_with_caption(doc, FULL_SCANS[hal_num], f"[Full Scan Hal {hal_num:02d}: anwar_mujarobat_asli.pdf Hal PDF {hal_num:02d}/65 — 300 DPI — rajah_anwar_v2_300/{FULL_SCANS[hal_num].name}]", width_inches=6.1 if hal_num!=10 else 5.8)
    # Now inject the 9 ketentuan content from MD — we will parse the MD section for this HAL
    # Extract the HAL chunk from md
    import re
    hal_pat = rf"## HALAMAN {hal_num:02d}.*?(?=\\n## HALAMAN|\\n---\\n\\n> \\*\\*KHATAM|\\Z)"
    m = re.search(hal_pat, md, re.DOTALL)
    hal_text = m.group(0) if m else ""
    # For each ketentuan 1-9, extract heading if present
    # We'll render them as Heading2 with bullet content — simplified but faithful
    # Replace the ```arab blocks with styled Arabic
    arab_blocks = re.findall(r"```arab(.*?)```", hal_text, re.DOTALL)
    for ab in arab_blocks:
        # Clean, keep original harokat
        ab_clean = ab.strip()
        # Add heading for Arabic Full Harokat
        doc.add_heading("1) Arab Full Harokat (matan — harokat penuh)", level=3)
        # Split into paragraphs (double newline)
        paras = [p.strip() for p in ab_clean.split("\n\n") if p.strip()]
        for para in paras[:6]:  # limit to avoid overflow but keep core
            # For long jadwal-like lines, keep mono
            if len(para) < 300:
                add_arabic_block(doc, para, fill="FFF8E1")
            else:
                add_arabic_block(doc, para[:800], fill="FFF8E1")
        # Add note for جدول if hal10
        if hal_num==10 and "ح" in ab_clean:
            add_body_text(doc, "Jadwal 5 baris × 15 kolom (dibaca kanan→kiri) — 4 penjuru diagonal حِنْقَايِيلُ — lihat crop FINAL Gambar 2.1 di bawah.", size=8, italic=True, color=RGBColor(0x6A,0x1B,0x9A))
        break  # only first arab block as main; other arab handled separately if waqf table

    # Ketentuan 2-8 — we take raw markdown lines after headings and convert to paragraphs/bullets
    # For fidelity, we'll dump the remaining markdown for this HAL as formatted paragraphs in DOCX (preserving bullet structure)
    # Clean: remove the arab code fences already handled, then convert ### headings to Heading3, bullets to List Bullet
    remaining = hal_text
    # Remove arab fences
    remaining = re.sub(r"```arab.*?```", "", remaining, flags=re.DOTALL)
    # Remove the HAL title heading itself
    remaining = re.sub(r"^## HALAMAN.*\n", "", remaining)
    # Split into lines
    lines = remaining.split("\n")
    for line in lines:
        line_strip = line.strip()
        if not line_strip: 
            continue
        if line_strip.startswith("### "):
            title = line_strip[4:].strip()
            # Map to 9 ketentuan
            doc.add_heading(title, level=2)
        elif line_strip.startswith("- **") or line_strip.startswith("- "):
            # Bullet
            p = doc.add_paragraph(style='List Bullet')
            # Keep bold via runs: split **bold**
            # Simplify: add as text with bold detection
            parts = re.split(r"(\*\*.*?\*\*)", line_strip[2:])
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    run = p.add_run(part[2:-2])
                    run.bold = True; run.font.size = Pt(8)
                else:
                    run = p.add_run(part)
                    run.font.size = Pt(8)
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(2)
        elif line_strip.startswith("> "):
            # Quote / Terjemahan
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'E3F2FD')
            pPr.append(shd)
            pBdr = OxmlElement('w:pBdr')
            left = OxmlElement('w:left'); left.set(qn('w:val'),'single'); left.set(qn('w:sz'),'12'); left.set(qn('w:space'),'6'); left.set(qn('w:color'),'64B5F6')
            pBdr.append(left); pPr.append(pBdr)
            run = p.add_run(line_strip[2:])
            run.font.size = Pt(8.5); run.italic = True; run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)
        elif line_strip.startswith("```"):
            # skip code fences for non-arab (keep nội)
            continue
        elif line_strip.startswith("**Wafaq") or line_strip.startswith("*Di naskah") or line_strip.startswith("Harfiah:") or line_strip.startswith("Washal:"):
            p = doc.add_paragraph()
            run = p.add_run(line_strip)
            run.font.size = Pt(8)
            run.font.name = 'Calibri'
        elif line_strip.startswith("---"):
            # Divider
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run("— — —"); r.font.color.rgb = RGBColor(0xBC,0xBC,0xBC)
        else:
            # Regular paragraph (handle bold markers)
            if len(line_strip) < 3: continue
            # Skip duplicate sumber lines already in cover
            if "Crop FINAL" in line_strip and hal_num in [10,12]:
                continue  # will be handled via image caption below
            p = doc.add_paragraph()
            # Handle **bold** inline
            parts = re.split(r"(\*\*.*?\*\*)", line_strip)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    run = p.add_run(part[2:-2]); run.bold = True; run.font.size = Pt(8.5)
                elif part.startswith("*") and part.endswith("*") and len(part)>2:
                    run = p.add_run(part[1:-1]); run.italic = True; run.font.size = Pt(8.5)
                else:
                    if part.strip():
                        run = p.add_run(part); run.font.size = Pt(8.5)

    # Insert FINAL wafaq images for Hal10 and Hal12 with required captions
    if hal_num == 10:
        doc.add_heading("Crop 300 DPI — Sumber Tunggal FINAL — Gambar 2.1", level=3)
        add_image_with_caption(doc, IMG_FINAL_10, "[Gambar 2.1: Jadwal Taksir Muhriqah 5×15 — حنقاييل di 4 sudut — Crop Asli 300 DPI]", width_inches=5.2)
        add_body_text(doc, "Deskripsi: Tabel 5 baris huruf campuran (ا ح د س ط ن …), 4 diagonal merah Ḥinqāyīl (حنقاييل) — 435×370 px, 59 KB — pertahankan 300 DPI latar putih tanpa compress. Link raw: https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg — Jangan pakai rajah_anwar/rajah_p10_jadwal_muhriqah.png lama (200 DPI).", size=7, color=RGBColor(0x55,0x55,0x55))
    if hal_num == 12:
        doc.add_heading("Crop 300 DPI — Sumber Tunggal FINAL — Gambar 2.2", level=3)
        add_image_with_caption(doc, IMG_FINAL_12, "[Gambar 2.2: Wafaq Qathi'ah li 'Ilaj al-Mass 3×3 Angka — 6000/1209/18 — Crop Asli 300 DPI]", width_inches=5.2)
        add_body_text(doc, "Deskripsi: Wafaq 3×3 angka — baris1: 6000 |1209|18 — baris2: 27|609|1191 — baris3: 1200|9|618 — garis merah 2pt, angka hitam, latar putih — 683×263 px, 80 KB — tulis dari atas kanan→kiri. Link raw: https://raw.githubusercontent.com/fatimah86-dot/kitab/main/rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg — Konstanta wafaq 'adadi mu'addal khusus (lihat Syarah).", size=7, color=RGBColor(0x55,0x55,0x55))
    if hal_num in [9,11,13]:
        add_body_text(doc, f"Catatan Hal {hal_num:02d}: Tanpa wafaq — teks teori saja. Arsip full: rajah_anwar_v2_300/hal{hal_num:02d}_300dpi.png — wafaq baru di Hal {'10' if hal_num==9 else '12' if hal_num==11 else '14 (Batch03)'} — jangan crop ulang, pertahankan 300 DPI.", size=7, italic=True, color=RGBColor(0x6D,0x4C,0x41))

# ==================== LAMPIRAN ====================
doc.add_page_break()
doc.add_heading("LAMPIRAN — Manifest & Full Scan 300 DPI Hal09-13", level=1)
add_body_text(doc, "Manifest wafaq crop saya — sumber tunggal — 15 file JPG 1.2M — Batch02 V2 pakai 2 FINAL (Hal10 + Hal12) — semua 300 DPI latar putih tanpa compress — halaman tanpa wafaq cukup full scan:", size=8, bold=True, color=RGBColor(0x1B,0x5E,0x20))

# Manifest table
manifest = [
    ("Hal", "Nama File FINAL", "Ukuran", "Wafaq Apa"),
    ("Hal10", "IMG_20261025_072854.jpg", "435×370 • 59 KB", "Jadwal Taksir Muhriqah 5×15 — حنقاييل di 4 sudut [Gambar 2.1]"),
    ("Hal12", "IMG_20261025_073117.jpg", "683×263 • 80 KB", "Wafaq Qathi'ah 3×3 Angka — 6000/1209/18 [Gambar 2.2]"),
    ("—", "13 file lain di rajah_anwar_FINAL_300DPI/", "1.06 MB", "Hal08 (2), Hal14-65 (wafaq hijau 8-bagian dll) — dipakai Batch03+"),
]
t = doc.add_table(rows=1, cols=4); t.style='Light Grid Accent 1'
hdr = t.rows[0].cells
for i, h in enumerate(manifest[0]): 
    hdr[i].text = h
    for pr in hdr[i].paragraphs: 
        for run in pr.runs: run.bold=True; run.font.size=Pt(7)
for row in manifest[1:]:
    cells = t.add_row().cells
    for i, val in enumerate(row):
        cells[i].text = val
        for pr in cells[i].paragraphs:
            for run in pr.runs: run.font.size=Pt(7)

# Full scan gallery (thumbnails)
add_body_text(doc, "Galeri Full Scan 300 DPI — Hal09-13 (3300×2550) — pertahankan 300 DPI, jangan crop ulang untuk hal tanpa wafaq:", size=8, bold=True)
for hal in [9,10,11,12,13]:
    add_body_text(doc, f"Hal {hal:02d} — {FULL_SCANS[hal].name} — {FULL_SCANS[hal].stat().st_size//1024} KB", size=7, bold=True, color=RGBColor(0x3E,0x27,0x23))
    add_image_with_caption(doc, FULL_SCANS[hal], f"[Full Scan Hal {hal:02d}: {FULL_SCANS[hal].name} — 3300×2550 — 300 DPI — Crop ulang DILARANG untuk hal tanpa wafaq]", width_inches=5.0)

# Annex verbatim MD
doc.add_page_break()
doc.add_heading("ANNEX — Verbatim Markdown 55KB 323 baris (sumber tunggal)", level=1)
add_body_text(doc, "Berikut teks verbatim REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md (55.099 bytes, 323 baris) untuk audit harokat & transliterasi — preserve sebagai arsip:", size=7, italic=True, color=RGBColor(0x55,0x55,0x55))
# Monospaced annex — use small font, preserve line breaks
# Split MD into chunks to avoid huge single paragraph (Word limit ~50k chars per paragraph, so chunk)
chunk_size = 3000
for idx in range(0, len(md), chunk_size):
    chunk = md[idx:idx+chunk_size]
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'F5F5F5')
    pPr.append(shd)
    run = p.add_run(chunk)
    run.font.name = 'Consolas'
    run.font.size = Pt(6)
    run.font.color.rgb = RGBColor(0x33,0x33,0x33)

# Final footer note
doc.add_page_break()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("KHATAM BATCH 02 V2 (Hal 09-13) — 5 Halaman — 9 Ketentuan — 2 Wafaq FINAL 300 DPI — Anwar Mujarobat Syeikh Basyir"); r.bold=True; r.font.size=Pt(10); r.font.color.rgb=RGBColor(0x1B,0x5E,0x20)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("GitHub: REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md + 5 PNG rajah_anwar_v2_300/hal09-13_300dpi.png + 2 JPG FINAL  •  PR #13 MERGED 428ff38  •  Google Docs: 1IffC92Oc9hm4xBEAIGylAFzekJLQwvhkFFj3cFBrgqw  •  Preview total wafaq 15 file/1.2M + 3 contoh Hal08(2)/Hal16/Hal20"); r.font.size=Pt(7); r.font.color.rgb=RGBColor(0x66,0x66,0x66)

# Set document core properties
doc.core_properties.title = "Revisi Batch02 V2 Hal09-13 — 9 Ketentuan — Anwar Mujarobat"
doc.core_properties.subject = "Anwar Mujarobat Syeikh Basyir — Muhriqah + Qathi'ah + Zajr — 300 DPI"
doc.core_properties.author = "fatimah86-dot/kitab"
doc.core_properties.keywords = "Anwar Mujarobat, 9 Ketentuan, 300 DPI, Wafaq FINAL, Hal09-13"
doc.core_properties.comments = "Sumber tunggal rajah_anwar_FINAL_300DPI/ — jangan crop ulang — Gambar 2.1/2.2 Crop Asli 300 DPI"

doc.save(OUT)
print(f"Saved {OUT} — {OUT.stat().st_size/1024/1024:.2f} MB")
print("Done")
