#!/usr/bin/env python3
# REBUILD TOTAL FINAL SUPER BERSIH — 5 LAPIS — Hal01-13
import re, pathlib
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC_FILES = [
    "REVISI_BATCH_01_V2_9KETENTUAN__HAL01_SAMPUL.md",
    "REVISI_BATCH_01_V2_9KETENTUAN__HAL02-08.md",
    "REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md",
]
OUT_MD = pathlib.Path("/tmp/REVISI_FINAL_5_LAPIS_BERSIH_HAL01-13.md")
OUT_DOCX_TMP = pathlib.Path("/tmp/REVISI_FINAL_5_LAPIS_BERSIH_HAL01-13.docx")
OUT_DOCX_REPO = pathlib.Path("REVISI_FINAL_5_LAPIS_BERSIH_HAL01-13.docx")

# Images - sumber tunggal FINAL
CROP_MAP = {
    "08": [pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072327.jpg"),
           pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072355.jpg")],
    "10": [pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg")],
    "12": [pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg")],
    # Hal lain tidak ada wafaq → tidak pakai crop, hanya full scan tidak dimasukkan (sesuai aturan sortir)
}

# Load combined text
combined = ""
for f in SRC_FILES:
    combined += pathlib.Path(f).read_text(encoding="utf-8") + "\n\n"

def extract_hal_blocks():
    # Find all HALAMAN headers with their content until next HALAMAN or end
    pattern = re.compile(r"## HALAMAN (\d+).*?(?=\n## HALAMAN |\Z)", re.DOTALL)
    blocks = {}
    for m in pattern.finditer(combined):
        hal = m.group(1)
        content = m.group(0)
        blocks[hal] = content
    return blocks

blocks = extract_hal_blocks()
print(f"Found hals: {sorted(blocks.keys())}")

def get_arab(block):
    m = re.search(r"```arab(.*?)```", block, flags=re.DOTALL)
    return m.group(1).strip() if m else "[Arab belum tersedia]"

def get_latin_washal(block):
    # Try to find Washal bunyi line: after "Washal:" or "Washal bunyi:"
    # Look for italic wash* or plain
    # Extract the line that is after Latin section
    # Strategy: Find "### 4) Latin" then capture up to "### 5)"
    sec = re.search(r"### 4\).*?Latin.*?\n(.*?)(?=\n### 5\))", block, flags=re.DOTALL | re.IGNORECASE)
    if sec:
        txt = sec.group(1)
        # Find line with Washal: or inside *...*
        # Prefer italic line with *
        italics = re.findall(r"\*(.*?)\*", txt, flags=re.DOTALL)
        if italics:
            # Filter likely latins: contains Anwār or similar
            for it in italics:
                if any(k in it for k in ["Anwār","Anwar","Ihdā","Laqad","Fawā","Ṭarīqat","Anwāru"]):
                    return it.strip()
            return italics[-1].strip()
        # Fallback: find Washal:
        m = re.search(r"Washal[^\n]*:\s*\*?(.*?)(?:\n|$)", txt, flags=re.DOTALL)
        if m:
            return m.group(1).strip().strip("*")
        return txt.strip().split("\n")[0].strip()[:300]
    # Fallback search in whole block
    m2 = re.search(r"Washal bunyi.*?\n(.*)", block, flags=re.DOTALL)
    if m2:
        return m2.group(1).strip().split("\n")[0][:300]
    return "[Latin Washal belum tersedia]"

def get_terjemahan_puebi(block):
    m = re.search(r"### 5\) Terjemahan.*?\n(.*?)(?=\n### 6\)|\n---)", block, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        # Remove leading "> " and markdown
        t = re.sub(r"^>\s*", "", t, flags=re.MULTILINE)
        t = re.sub(r"\*\*", "", t)
        t = t.strip()
        # Remove lines that are sampah
        t = "\n".join([l for l in t.split("\n") if l.strip()])
        return t
    return ""

def get_syarah(block):
    m = re.search(r"### 6\) Syarah.*?\n(.*?)(?=\n### 7\))", block, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        # Clean sampah lines
        cleaned = []
        for line in t.split("\n"):
            if any(s in line for s in ["Pertahankan 300 DPI","Sumber:","Raw:","Full Scan Hal","[Gambar","[Full Scan","Arsip full","rajah_anwar_v2_300","rajah_anwar_FINAL"]):
                continue
            if line.strip().startswith(">"):
                continue
            cleaned.append(line)
        return "\n".join(cleaned).strip()
    return ""

def get_khususiyah(block):
    m = re.search(r"### 7\) Khususiyah.*?\n(.*?)(?=\n### 8\)|\n---)", block, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        cleaned = []
        for line in t.split("\n"):
            if any(s in line for s in ["Pertahankan 300 DPI","Sumber:","Raw:","Full Scan Hal","Arsip full","rajah_anwar_v2_300","rajah_anwar_FINAL","[Gambar","[Full Scan","Crop FINAL"]):
                continue
            cleaned.append(line)
        return "\n".join(cleaned).strip()
    return ""

# Build pesantren translation: transform PUEBI to pesantren style with Utawi, Adapun bermula, Puniko, Maka, Yakni
# We craft per hal manually with appropriate Javanese pesantren opening, but keep meaning accurate and without nahwu rule mention.

PESANTREN_TEMPLATES = {
    "01": "Utawi iki iku piro-piro cahayane Syeikh Basyir. Adapun bermula utawi Forum An-Anwar Al-Qadiriyah lan Arwah Ar-Rahmaniyah iku kang ngumpulake kitab iki. Maka utawi kitab iki den-arani Anwar amargo isine cahya ilmu kang madhangi ati.",
    "02": "Utawi iki iku hadiahe Syeikh Basyir. Puniko den-hadiahake marang junjungan Kanjeng Nabi Muhammad ﷺ lan keluargane kang suci pilihan, lan marang Syeikh Al-Faqir Al-Qadiri, lan Dr. Bihuni, saha marang sedoyo faqir. Adapun bermula faqir ing kene tegese wong kang butuh marang Gusti Allah.",
    "03": "Utawi iki iku ijazah umum saking Syeikh Basyir. Adapun bermula sopo wae kang tumeka kitab iki marang dheweke, puniko den-ijazahake umum kanti syarat rido Allah lan Rasul. Maka tatacarane moco sholawat kaping siji lan Fatihah kaping siji kang pahalane den-hadiahake marang Nabi, gurune Syeikh, lan Syeikh Faqir Qadiri. Puniko ijazah wus tumeka.",
    "04": "Utawi iki iku piro-piro faedah lan mujarobat kang wus den-cobo khasiate saking Syeikh Basyir. Adapun bermula iki dadi gapura pembuka kumpulan faedah, sawise mukadimah sampul lan ijazah.",
    "05": "Utawi iki iku daftar isine kitab mujarobat Syeikh Basyir. Puniko ono 13 faedah: (1) Dalane gampang narik rezeki (Maysarah), (2) Faedah ngobong lan ngusir jin lan maradah kanthi idine Allah, (3) Faedah medhot lara kesurupan, (4) Bentakan medhot kanggo njupuk janji khodam istinzal, (5) Ngusir 'Uthush ngrusak amal, (6) Mutiara cahya kanggo gangguan ruh, (7) Ngancurke wong dzalim, (8) Ngalahake qorin, (9) Pedang pamungkas nolak Maimun, (10) Mbaleake khodam, (11) Dongo wong wedi, (12) 10 ayat pembatal sihir, (13) Ngungkap lewat mimpi.",
    "06": "Utawi iki iku dalane gampang (Maysarah) kanggo narik rezeki lan nglariske dagang. Adapun bermula Syeikh ngendika: He sedulur-sedulurku krono Allah, puniko mutiara manfaati kang den-selehake ing ngarepmu. Maka contohe jeneng Murad bin Maryam: م ر ا د م ر ي م = 535. Puniko angkane den-waca huruf per huruf dadi خَمْسُ مِائَةٍ وَثَلَاثُونَ وَخَمْسُ مِائَةٍ, banjur den-buang huruf sing dobel lan huruf mad, kari م ر د ي = 4 huruf. Maka den-kurangi 9-4=5 — dadine wafaq 5×5.",
    "07": "Maka utawi carane njupuk jeneng ruhani, puniko di-jupuk saking baris kaping pindo kanthi mlumpat telu (tatslits) — [س م س] — dadine Samsail. Adapun bermula saking baris kaping telu kanthi mlumpat telu saking huruf pertama — [ن س ل م] — dadine Nasmahil. Puniko huruf amal lan huruf hakim rupane [ن ل م س ي ه و] — dadine Asma: La ilaha illa Allah Al-Muhaimin kang diwaca ing amal. Adapun bermula jam amale iku Zuhrah (sisa 6 saking 27 bagi 7).",
    "08": "Puniko wafaq gaweane (5×5) lan wafaq ruhani (4×4) kang wus den-turunake. Adapun bermula wafaq gaweane isine و ا هـ د ي kang diputer saben baris, den-kupengi ayat Qawluhu Al-Haqqu wa lahul-Mulku lan loro ayat Lathif lan Alladzina Yatlu. Maka wafaq ruhani isine م س ل ن kang diputer. Puniko bilangan wiride 196 ambalan kanthi tawajjuh marang Allah kanthi panyuwunanmu.",
    "09": "Utawi iki iku faedah kang ngobong lan ngusir jin lan maradah kanthi idine Allah. Adapun bermula tatacarane: dijupuk jenenge wong lan ibune, den-buang huruf sing kembar, banjur den-campur karo 7 huruf thabi'ah geni-hawa nurani [ا هـ ط م ك س ق] kanthi njogo huruf awal lan akhir. Maka baris campurane den-pecah nganti makhraj kanthi ninggal siji, banjur den-teliti cacah barise: yen genap dijupuk saking baris kapindo, yen ganjil saking baris katelu. Puniko digawe 3 lembar lan piring kang di-lebur banyu suci, den-obong menyan 7 godong bidara, 7 cengkeh, lan mustaka saben wengi.",
    "10": "Adapun bermula utawi contohe Hasan lan ibune Ruqayyah: den-jupuk huruf ruhani saking baris katelu [ن ح ق] cacahe 158 — den-waca Hinqayil. Puniko jenenge ruhani kang ditulis ing papat pojok jadwal lan den-kupengi qasam: Bismillah, sumpah marang Thaktsayil lan 'Awtsayil kanthi hakime Fahghayil, lan Ahya Syarahya, lan ayat In Kanat illa Shaihatan Wahidatan, lan Was-Sama'i Dzati Al-Buruj. Maka qasam diwaca ping 5 saben lembar.",
    "11": "Utawi iki iku faedah kang medhot kanggo nambani kesurupan (mass) lan mbatalake alangan bondo pendhem. Adapun bermula tatacarane: wafaq ditulis ing wadhah resik anyar nganggo banyu mawar, za'faran, lan misik, den-kupengi 5 ayat: Was-Syamsi, Al-Ikhlas, Allahu Nurus-Samawati, Wa Adzdzin fin-Nasi, lan Qul Uhiya. Maka tulisan di-lebur nganggo banyu udan luwih utama, yen ora nganggo banyu sumur kang ora kena srengenge lan rembulan, den-usap nganggo drijine tengen kaping 7.",
    "12": "Puniko wafaq kanggo nambani kesurupan. Adapun bermula angkane 3×3: 6000 | 1209 | 18 ing baris ndhuwur, 27 | 609 | 1191 ing tengah, 1200 | 9 | 618 ing ngisor — diwaca saking tengen mangiwo. Maka tulisan diwiwiti saking ndhuwur wafaq saking arah tengen mangiwo, mugi Gusti Allah paring pitulung.",
    "13": "Utawi iki iku bentakan kang medhot kanggo njupuk janji lan mitsaq saking khodam istinzal. Adapun bermula akeh kedadean wong ngangggo istinzal liwat bocah cilik (wasith) — khodame teko lan mangsuli pitakon, nanging akeh goroh. Maka yen khodame iku 'ulwi (luhur) ora gelem mudhun, diganti khodam suflî tukang goroh. Puniko faedah kanggo mbentak khodam supaya jujur: ojo di-kandhani bocah wasith arep diapakake, wacanen ayat Walau Aradul-Khuruja la-a'addu lahu 'uddatah kaping 7 karo nyekel bathuke, banjur kongkon syahadat, sholawat, lan sumpah ing ndhuwur mushaf Surah Al-Mujadalah.",
}

# Build MD
md_lines = []
md_lines.append("# REVISI FINAL SUPER BERSIH — 5 LAPIS — HAL 01-13")
md_lines.append("> Kitab Anwar Mujarobat Syeikh Basyir — 65 hal — Anwar Mujarobat Syeikh Basyir saja (bukan Abu Ma'syar) — Matan murni, tanpa Tanbih Syar'i — Gaya: Arab → Latin Wasal → Pesantren")
md_lines.append("> Format: 1) Arab Berharokat Full • 2) Latin Washal Bunyi • 3) Terjemahan Ala Pesantren (Utawi/Adapun bermula/Puniko/Maka/Yakni) • 4) Syarah dan Penjelasan • 5) Khususiyah dan Tatacara Praktik + Crop Wafaq (sumber tunggal rajah_anwar_FINAL_300DPI/)")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

for hal in ["01","02","03","04","05","06","07","08","09","10","11","12","13"]:
    block = blocks.get(hal, "")
    arab = get_arab(block)
    latin = get_latin_washal(block)
    # Clean latin: remove explanations like "Harfiah:" etc, keep only washal line
    # If latin still contains "Harfiah:" split, take after last "*"
    if "Harfiah:" in latin:
        # try to extract wash part
        m = re.search(r"Washal[^:]*:\s*\*?(.*?)(?:\*|$)", latin, flags=re.DOTALL)
        if m:
            latin = m.group(1).strip()
    latin = latin.strip().strip("*").strip()
    # Limit latin length
    if len(latin) > 800:
        latin = latin[:800] + "..."
    # Syarah and Khususiyah clean
    syarah = get_syarah(block)
    khusus = get_khususiyah(block)
    # Truncate overly long trash remnants already cleaned, but ensure not too long for MD readability
    # For pesantren terjemah, use template
    pesantren = PESANTREN_TEMPLATES.get(hal, "Utawi iki iku terjemah pesantren Hal "+hal)

    # Title per hal
    title_map = {
        "01": "HALAMAN 01 — SAMPUL — أَنْوَارُ الشَّيْخِ الْبَشِيرِ",
        "02": "HALAMAN 02 — IHDA' — إِهْدَاءُ الشَّيْخِ الْبَشِيرِ",
        "03": "HALAMAN 03 — IJAZAH 'AMMAH — إِجَازَةُ الشَّيْخِ الْبَشِيرِ",
        "04": "HALAMAN 04 — SAMPUL DALAM — فَوَائِدُ وَمُجَرَّبَاتُ الشَّيْخِ الْبَشِيرِ",
        "05": "HALAMAN 05 — FIHRIS — فِهْرِسُ مُجَرَّبَاتِ الشَّيْخِ الْبَشِيرِ",
        "06": "HALAMAN 06 — FAEDAH 01 (1/3) — طَرِيقَةُ الْمَيْسَرَةِ فِي جَلْبِ الْأَرْزَاقِ",
        "07": "HALAMAN 07 — FAEDAH 01 (2/3) — LANJUTAN MAYSARAH",
        "08": "HALAMAN 08 — FAEDAH 01 (3/3) — 2 WAFAQ (MUKHAMMAS 5×5 & MURABBA' 4×4)",
        "09": "HALAMAN 09 — FAEDAH MUHRIQAH 1/2 — فَائِدَةٌ مُحْرِقَةٌ طَارِدَةٌ لِلْجِنِّ",
        "10": "HALAMAN 10 — FAEDAH MUHRIQAH 2/2 — JADWAL & QASAM — حِنْقَايِيلُ",
        "11": "HALAMAN 11 — FAEDAH QATHI'AH 1/2 — فَائِدَةٌ قَاطِعَةٌ لِعِلَاجِ الْمَسِّ",
        "12": "HALAMAN 12 — FAEDAH QATHI'AH 2/2 — WAFAQ 3×3",
        "13": "HALAMAN 13 — ZAJR QATHI' 1/3 — الزَّجْرُ الْقَاطِعُ لِأَخْذِ الْعَهْدِ",
    }
    md_lines.append(f"## {title_map[hal]}")
    md_lines.append("")
    # 1 Arab
    md_lines.append("### 1. Arab Berharokat Full Halaman")
    md_lines.append("```arab")
    md_lines.append(arab)
    md_lines.append("```")
    md_lines.append("")
    # 2 Latin
    md_lines.append("### 2. Latin Washal Bunyi")
    md_lines.append(latin)
    md_lines.append("")
    # 3 Pesantren
    md_lines.append("### 3. Terjemahan Bahasa Indonesia Ala Pesantren")
    md_lines.append(pesantren)
    md_lines.append("")
    # 4 Syarah
    md_lines.append("### 4. Syarah dan Penjelasan")
    # Syarah: keep paragraphs, remove empty
    if syarah:
        # Split into paragraphs, keep up to 2 paragraphs to keep concise but informative
        paras = [p.strip() for p in syarah.split("\n\n") if p.strip()]
        for p in paras[:3]:
            # Remove markdown bold remaining and long sampah?
            p = re.sub(r"\*\*", "", p)
            # Trim
            if len(p) > 1200:
                p = p[:1200] + "..."
            md_lines.append(p)
            md_lines.append("")
    else:
        md_lines.append("_Syarah sesuai nash kitab._")
        md_lines.append("")
    # 5 Khususiyah + Crop
    md_lines.append("### 5. Khususiyah dan Tatacara Praktik")
    if khusus:
        paras = [p.strip() for p in khusus.split("\n\n") if p.strip()]
        for p in paras[:3]:
            p = re.sub(r"\*\*", "", p)
            # Clean bullet markers? Keep as text
            if len(p) > 1200:
                p = p[:1200] + "..."
            md_lines.append(p)
            md_lines.append("")
    else:
        # Provide minimal based on hal
        md_lines.append("_Khususiyah sesuai nash — lihat Syarah._")
        md_lines.append("")
    # Crop if exists - sorted automatically
    if hal in CROP_MAP:
        for img_path in CROP_MAP[hal]:
            md_lines.append(f"![Wafaq Hal {hal}]({img_path})")
            md_lines.append(f"[Gambar: Wafaq Hal {hal}]")
            md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

md_content = "\n".join(md_lines)
OUT_MD.write_text(md_content, encoding="utf-8")
print(f"MD saved {OUT_MD} {len(md_content)} chars")

# Build DOCX
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# Page setup A4
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)
    section.header_distance = Inches(0.28)
    section.footer_distance = Inches(0.28)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(9)
style.font.color.rgb = RGBColor(0x21,0x21,0x21)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.space_before = Pt(1)
style.paragraph_format.line_spacing = 1.08

for name, size, color in [('Heading 1', 18, RGBColor(0x14,0x3D,0x6B)), ('Heading 2', 13, RGBColor(0x1B,0x5E,0x20)), ('Heading 3', 10, RGBColor(0x4E,0x34,0x2E))]:
    s = doc.styles[name]
    s.font.name = 'Calibri'; s.font.size = Pt(size); s.font.color.rgb = color; s.font.bold = True
    s.paragraph_format.space_before = Pt(7); s.paragraph_format.space_after = Pt(3)

# Header/Footer
def add_header_footer(doc):
    for section in doc.sections:
        header = section.header
        p = header.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("ANWAR MUJAROBAT — Syeikh Basyir • 5 Lapis Bersih Hal01-13 • Arab • Latin • Pesantren • Syarah • Khususiyah + Wafaq")
        run.font.size = Pt(6.5); run.font.color.rgb = RGBColor(0x6D,0x4C,0x41); run.italic = True
        footer = section.footer
        p2 = footer.paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run()
        fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'),'begin')
        instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=' PAGE '
        fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'),'end')
        run2._r.append(fld1); run2._r.append(instr); run2._r.append(fld2)
        run3 = p2.add_run(" • Anwar Mujarobat Hal01-13 • 5 Lapis Bersih")
        run3.font.size = Pt(6); run3.font.color.rgb = RGBColor(0x75,0x75,0x75)
add_header_footer(doc)

def set_shading(paragraph, color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'), color)
    pPr.append(shd)

def add_bidi(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'),'1'); pPr.append(bidi)

def arab_block_doc(text, fill="FFF8E1"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text.strip())
    run.font.name = 'Scheherazade New'
    run.font.size = Pt(13.5)
    run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)
    add_bidi(p)
    set_shading(p, fill)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ['top','left','bottom','right']:
        el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'BDBDBD')
        pBdr.append(el)
    pPr.append(pBdr)
    return p

def body_doc(text, size=9, bold=False, italic=False, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(size); run.bold = bold; run.italic = italic; run.font.name='Calibri'
    if color: run.font.color.rgb = color
    return p

def caption_doc(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size = Pt(7.5); run.italic = True; run.font.color.rgb = RGBColor(0x42,0x42,0x42)
    return p

# Cover
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("REVISI FINAL SUPER BERSIH"); r.bold=True; r.font.size=Pt(9); r.font.color.rgb=RGBColor(0x6A,0x1B,0x9A)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("5 LAPIS HAL 01-13"); r.bold=True; r.font.size=Pt(22); r.font.color.rgb=RGBColor(0x14,0x3D,0x6B)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Arab Berharokat • Latin Washal • Terjemahan Pesantren (Utawi/Adapun/Puniko/Maka/Yakni) • Syarah • Khususiyah + Wafaq"); r.font.size=Pt(8); r.italic=True; r.font.color.rgb=RGBColor(0x55,0x55,0x55)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Anwar Mujarobat Syeikh Basyir — 65 hal — Edisi Pesantren"); r.font.size=Pt(7); r.font.color.rgb=RGBColor(0x75,0x75,0x75)

# Info box
p = doc.add_paragraph()
pPr = p._p.get_or_add_pPr()
shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'E8F5E9')
pPr.append(shd)
pBdr = OxmlElement('w:pBdr')
for edge in ['top','left','bottom','right']:
    el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'3'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'A5D6A7')
    pBdr.append(el)
pPr.append(pBdr)
run = p.add_run("Format Baru: 5 Lapis Bersih per halaman — hapus semua sampah Batch01/02 V2 lama")
run.bold=True; run.font.size=Pt(9); run.font.color.rgb=RGBColor(0x1B,0x5E,0x20)
for bullet in [
    "1) Arab Berharokat Full Halaman — dari anwar_mujarobat_asli.pdf Hal PDF 01-13/65 (harokat penuh)",
    "2) Latin Washal Bunyi — langsung latin sambung: Anwārush-Syaikhil-Basyīr",
    "3) Terjemahan Ala Pesantren — gaya Utawi / Adapun bermula / Puniko / Maka / Yakni",
    "4) Syarah dan Penjelasan — makna, asbab, dalil",
    "5) Khususiyah dan Tatacara Praktik + Crop Wafaq — sumber tunggal rajah_anwar_FINAL_300DPI/",
]:
    pb = doc.add_paragraph(style='List Bullet')
    run = pb.add_run(bullet); run.font.size=Pt(7.5)

# TOC
doc.add_heading("DAFTAR ISI — 5 Lapis Bersih Hal01-13", level=1)
toc = [
    "Hal 01 Sampul — Anwārush-Syaikhil-Basyīr ……………………………… 3",
    "Hal 02 Ihda' …………………………………………………………… 4",
    "Hal 03 Ijazah 'Ammah ……………………………………………… 5",
    "Hal 04 Sampul Dalam ……………………………………………… 6",
    "Hal 05 Fihris 13 Faedah …………………………………………… 7",
    "Hal 06 Faedah Maysarah 1/3 ……………………………………… 8",
    "Hal 07 Faedah Maysarah 2/3 ……………………………………… 10",
    "Hal 08 Faedah Maysarah 3/3 + 2 Wafaq ………………………… 12",
    "Hal 09 Muhriqah 1/2 ……………………………………………… 14",
    "Hal 10 Muhriqah 2/2 + Jadwal …………………………………… 16",
    "Hal 11 Qathi'ah 1/2 ……………………………………………… 18",
    "Hal 12 Qathi'ah 2/2 + Wafaq 3×3 ……………………………… 20",
    "Hal 13 Zajr Qathi' ………………………………………………… 22",
]
for it in toc:
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(it); run.font.size=Pt(8)

doc.add_page_break()

for hal in ["01","02","03","04","05","06","07","08","09","10","11","12","13"]:
    block = blocks.get(hal, "")
    if not block:
        continue
    title_map = {
        "01": "HALAMAN 01 — SAMPUL — أَنْوَارُ الشَّيْخِ الْبَشِيرِ",
        "02": "HALAMAN 02 — IHDA' — إِهْدَاءُ الشَّيْخِ الْبَشِيرِ",
        "03": "HALAMAN 03 — IJAZAH 'AMMAH — إِجَازَةُ الشَّيْخِ الْبَشِيرِ",
        "04": "HALAMAN 04 — SAMPUL DALAM — فَوَائِدُ وَمُجَرَّبَاتُ",
        "05": "HALAMAN 05 — FIHRIS — فِهْرِسُ مُجَرَّبَاتِ",
        "06": "HALAMAN 06 — FAEDAH MAYSARAH 1/3 — طَرِيقَةُ الْمَيْسَرَةِ",
        "07": "HALAMAN 07 — FAEDAH MAYSARAH 2/3 — LANJUTAN",
        "08": "HALAMAN 08 — FAEDAH MAYSARAH 3/3 — 2 WAFAQ",
        "09": "HALAMAN 09 — FAEDAH MUHRIQAH 1/2",
        "10": "HALAMAN 10 — FAEDAH MUHRIQAH 2/2 — JADWAL & QASAM",
        "11": "HALAMAN 11 — FAEDAH QATHI'AH 1/2",
        "12": "HALAMAN 12 — FAEDAH QATHI'AH 2/2 — WAFAQ 3×3",
        "13": "HALAMAN 13 — ZAJR QATHI' 1/3",
    }
    if hal != "01":
        doc.add_page_break()
    doc.add_heading(title_map[hal], level=1)
    arab = get_arab(block)
    latin = get_latin_washal(block)
    # Clean latin similarly
    if "Harfiah:" in latin:
        m = re.search(r"Washal[^:]*:\s*\*?(.*?)(?:\*|$)", latin, flags=re.DOTALL)
        if m:
            latin = m.group(1).strip()
    latin = latin.strip().strip("*").strip()
    if len(latin) > 900:
        latin = latin[:900]

    syarah = get_syarah(block)
    khusus = get_khususiyah(block)
    # Filter sampah already cleaned, but ensure no forbidden phrases remain
    for forbidden in ["Pertahankan 300 DPI","Sumber: rajah_anwar","Raw: https","Full Scan Hal","[Full Scan","Arsip full","Crop FINAL","rajah_anwar_v2_300","Struktur Kitab","ANDA DI SINI","Kaidah Nahwu","3 Hukum Washal","Transliterasi Kemenag","Ejaan Harfiah"]:
        syarah = syarah.replace(forbidden, "")
        khusus = khusus.replace(forbidden, "")

    pesantren = PESANTREN_TEMPLATES.get(hal, "")

    # 1 Arab
    doc.add_heading("1. Arab Berharokat Full Halaman", level=2)
    for para in arab.split("\n\n"):
        para = para.strip()
        if para:
            arab_block_doc(para, fill="FFF8E1")

    # 2 Latin
    doc.add_heading("2. Latin Washal Bunyi", level=2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(latin)
    run.font.size = Pt(9); run.italic = True; run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)

    # 3 Pesantren
    doc.add_heading("3. Terjemahan Bahasa Indonesia Ala Pesantren", level=2)
    p = doc.add_paragraph()
    # shading light blue for pesantren
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'E3F2FD')
    pPr.append(shd)
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left'); left.set(qn('w:val'),'single'); left.set(qn('w:sz'),'12'); left.set(qn('w:space'),'6'); left.set(qn('w:color'),'64B5F6')
    pBdr.append(left); pPr.append(pBdr)
    run = p.add_run(pesantren)
    run.font.size = Pt(9); run.font.color.rgb = RGBColor(0x0D,0x47,0xA1)

    # 4 Syarah
    doc.add_heading("4. Syarah dan Penjelasan", level=2)
    if syarah.strip():
        for para in [p.strip() for p in syarah.split("\n\n") if p.strip()][:3]:
            para = re.sub(r"\*\*", "", para)
            if len(para) > 1400:
                para = para[:1400]
            body_doc(para, size=8.5)
    else:
        body_doc("Syarah sesuai nash kitab.", size=8.5, italic=True)

    # 5 Khususiyah + Crop
    doc.add_heading("5. Khususiyah dan Tatacara Praktik", level=2)
    if khusus.strip():
        for para in [p.strip() for p in khusus.split("\n\n") if p.strip()][:3]:
            para = re.sub(r"\*\*", "", para)
            if len(para) > 1400:
                para = para[:1400]
            if para.startswith("- "):
                pb = doc.add_paragraph(style='List Bullet')
                run = pb.add_run(para[2:]); run.font.size = Pt(8)
            else:
                body_doc(para, size=8.5)
    else:
        body_doc("Khususiyah sesuai nash — amalkan dengan adab.", size=8.5, italic=True)

    # Crop wafaq if exists - sorted automatically
    if hal in CROP_MAP:
        for img_path in CROP_MAP[hal]:
            if img_path.exists():
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(str(img_path), width=Inches(4.8))
                caption_doc(f"[Gambar: Wafaq Hal {hal}]")

# Khatam
doc.add_page_break()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("KHATAM 5 LAPIS BERSIH — HAL 01-13"); r.bold=True; r.font.size=Pt(14); r.font.color.rgb=RGBColor(0x1B,0x5E,0x20)
body_doc("13 halaman — Sampul, Ihda', Ijazah, Sampul Dalam, Fihris, Maysarah 3 hal, Muhriqah 2 hal, Qathi'ah 2 hal, Zajr 1 hal — 5 lapis per halaman.", size=8, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x42,0x42,0x42))
body_doc("Gambar wafaq dari sumber tunggal rajah_anwar_FINAL_300DPI/ — ditampilkan langsung di halaman terkait.", size=7, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x75,0x75,0x75))

doc.core_properties.title = "Revisi Final 5 Lapis Bersih Hal01-13"
doc.core_properties.subject = "5 Lapis: Arab, Latin, Pesantren, Syarah, Khususiyah+Wafaq — super bersih"
doc.core_properties.author = "kitab — arena/7021a54a-kitab"

doc.save(OUT_DOCX_TMP)
import shutil, pathlib
shutil.copy(OUT_DOCX_TMP, OUT_DOCX_REPO)
print(f"MD saved {OUT_MD} chars={OUT_MD.stat().st_size}")
print(f"DOCX saved {OUT_DOCX_TMP} MB={OUT_DOCX_TMP.stat().st_size/1024/1024:.2f} -> repo {OUT_DOCX_REPO}")

