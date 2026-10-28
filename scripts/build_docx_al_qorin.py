#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an Al-Qorin DOCX from the locked 5-layer Markdown.

Compliance points implemented here (see STANDAR_MUTLAK_AL_QORIN_123.md):
- Arabic layer: w:bidi=1 and w:jc="start" (visual right in an RTL paragraph);
  every Arabic-layer run also carries w:rtl so neutral punctuation and
  mirrored brackets stay on the correct sides of Arabic phrases
- Latin/other prose: w:bidi=0 and w:jc="left"
- wafaq crop paragraphs and transcription-table cells: w:jc="center"
- Amiri Regular/Bold/Italic/BoldItalic embedded as obfuscated OpenType parts
  (word/fonts/*.odttf) with fontTable relationships and embedTrueTypeFonts.
The builder does not compose or alter source sentences; it only renders the MD.
"""
import argparse, io, re, uuid, zipfile
from pathlib import Path
from lxml import etree
from PIL import Image
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "al_qorin/REVISI_AL_QORIN_PILOT.md"
DEFAULT_OUT = ROOT / "al_qorin/AL_QORIN_PILOT_5_LAPIS.docx"
FONT_DIR = ROOT / "fonts"
AR_RE = re.compile(r"([\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+)")
FONT = "Amiri"
INK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x4B, 0x55, 0x63)

# ----------------------------------------------------------------- XML helpers
def set_jc(p, val):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:jc")):
        pPr.remove(old)
    jc = OxmlElement("w:jc"); jc.set(qn("w:val"), val); pPr.append(jc)

def set_bidi(p, rtl):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:bidi")):
        pPr.remove(old)
    b = OxmlElement("w:bidi"); b.set(qn("w:val"), "1" if rtl else "0"); pPr.append(b)

def format_run(run, size=12, cs_size=None, bold=False, italic=False, rtl=False, color=INK):
    run.bold = bold; run.italic = italic
    run.font.name = FONT; run.font.size = Pt(size); run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts"); rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT)
    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = OxmlElement("w:szCs"); rPr.append(szCs)
    szCs.set(qn("w:val"), str(int((cs_size or size) * 2)))
    if bold and rPr.find(qn("w:bCs")) is None: rPr.append(OxmlElement("w:bCs"))
    if italic and rPr.find(qn("w:iCs")) is None: rPr.append(OxmlElement("w:iCs"))
    if rtl and rPr.find(qn("w:rtl")) is None: rPr.append(OxmlElement("w:rtl"))

# --------------------------------------------------------------- inline parser
def emit_segments(p, text, *, size, cs_extra=2, bold=False, italic=False, color=INK, force_rtl=False):
    for seg in AR_RE.split(text):
        if not seg:
            continue
        is_ar = bool(AR_RE.fullmatch(seg))
        r = p.add_run(seg)
        format_run(r, size=size + (2 if is_ar else 0), cs_size=size + cs_extra + (2 if is_ar else 0),
                   bold=bold, italic=(italic and not is_ar), rtl=(is_ar or force_rtl), color=color)

def parse_inline(p, s, *, size=12, color=INK, bold=False, italic=False, force_rtl=False):
    b, i, code, buf = bold, italic, False, []
    def flush():
        if buf:
            emit_segments(p, "".join(buf), size=size, bold=b, italic=i, color=color, force_rtl=force_rtl)
            buf.clear()
    idx = 0
    while idx < len(s):
        if code:
            if s[idx] == "`": flush(); code = False; idx += 1
            else: buf.append(s[idx]); idx += 1
            continue
        if s[idx] == "`": flush(); code = True; idx += 1
        elif s.startswith("\\*", idx): buf.append("*"); idx += 2
        elif s.startswith("***", idx): flush(); b = not b; i = not i; idx += 3
        elif s.startswith("**", idx): flush(); b = not b; idx += 2
        elif s[idx] == "*": flush(); i = not i; idx += 1
        elif s.startswith("\\|", idx): buf.append("|"); idx += 2
        else: buf.append(s[idx]); idx += 1
    flush()

# ---------------------------------------------------------------- MD parsing
IMG_RE = re.compile(r"^!\[[^\]]*\]\(([^)]+)\)\s*$")
def split_table_line(line):
    s = line.strip()
    if s.startswith("|"): s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"): s = s[:-1]
    cells = re.split(r"(?<!\\)\|", s)
    return [c.strip().replace("\\|", "|") for c in cells]

def is_separator(cells):
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c or "---") for c in cells)

def parse_md(path: Path, only_units=None):
    lines = path.read_text(encoding="utf-8").splitlines()
    units, front = [], []
    cur = None
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            heading = m.group(1).strip()
            uid = "SAMPUL" if heading == "SAMPUL" else heading.split()[0]
            cur = {"unit_id": uid, "heading": heading, "events": []}
            if only_units is None or uid in only_units:
                units.append(cur)
            else:
                cur = {"unit_id": uid, "heading": heading, "events": [], "_skip": True}
            continue
        if cur is None:
            front.append(line)
        elif not cur.get("_skip"):
            cur["events"].append(line)
    # front matter -> simple events
    fevents = []
    for line in front:
        s = line.strip()
        if s.startswith("# "): fevents.append(("title", s[2:].strip()))
        elif s.startswith(">"): fevents.append(("quote", s.lstrip("> ").strip()))
        elif s and not s.startswith("<!--"): fevents.append(("para", s))
    for u in units:
        events, buf, ctx = [], [], "front"
        ctx_before_image = ctx
        def flush():
            nonlocal ctx
            if buf:
                text = " ".join(buf).strip()
                event_ctx = ctx
                if ctx == "caption" and not text.startswith("[Crop halaman"):
                    event_ctx = ctx_before_image
                events.append(("para", event_ctx, text)); buf.clear()
                if ctx == "caption":
                    ctx = ctx_before_image
        for raw in u.pop("events"):
            s = raw.rstrip()
            st = s.strip()
            m3 = re.match(r"^###\s+(.+)$", st); m4 = re.match(r"^####\s+(.+)$", st)
            mi = IMG_RE.match(st)
            if m4:
                flush(); h = m4.group(1).strip(); events.append(("h3", h))
                ctx = "metode" if h.startswith("1.") else ("jam" if h.startswith("2.") else "catatan")
            elif m3:
                flush(); h = m3.group(1).strip(); events.append(("h2", h))
                ctx = ("Arab" if h.startswith("1.") else "latin" if h.startswith("2.") else
                       "terjemahan" if h.startswith("3.") else "layer4" if h.startswith("4.") else "khususiyah")
            elif mi:
                flush(); events.append(("image", mi.group(1).strip()))
                ctx_before_image = ctx; ctx = "caption"
            elif st.startswith("|"):
                flush(); cells = split_table_line(st)
                if not is_separator(cells): events.append(("trow", cells))
            elif not st or st.startswith("<!--") or st == "---":
                flush()
            else:
                buf.append(st)
        flush()
        # group table rows
        grouped, rows = [], []
        for ev in events:
            if ev[0] == "trow": rows.append(ev[1])
            else:
                if rows: grouped.append(("table", rows)); rows = []
                grouped.append(ev)
        if rows: grouped.append(("table", rows))
        u["events"] = grouped
    return fevents, units

# ------------------------------------------------------------------ rendering
def style_document(doc, clean=False):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.0)
    sec.left_margin = sec.right_margin = Cm(2.0)
    for name, size, bold in (("Normal", 12, False), ("Title", 26, True),
                             ("Heading 1", 18, True), ("Heading 2", 15, True), ("Heading 3", 13, True)):
        st = doc.styles[name]
        st.font.name = FONT; st.font.size = Pt(size); st.font.bold = bold
        rPr = st.element.get_or_add_rPr(); rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None: rFonts = OxmlElement("w:rFonts"); rPr.insert(0, rFonts)
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rFonts.set(qn(attr), FONT)
    hdr = sec.header.paragraphs[0]
    set_bidi(hdr, False); set_jc(hdr, "left")
    if not clean:
        format_run(hdr.add_run("Al-Qorin war Riyadhah — revisi dokumenter"), size=9, italic=True, color=MUTED)
    ftr = sec.footer.paragraphs[0]
    set_bidi(ftr, False); set_jc(ftr, "center")
    if not clean:
        format_run(ftr.add_run("Teks dinisbatkan kepada penulis kitab; bukan anjuran atau jaminan hasil.  "), size=9, italic=True, color=MUTED)
    # Proper PAGE field: begin / instruction / separate / cached result / end.
    def field_run(child=None, text=None):
        r = ftr.add_run(text or "")
        format_run(r, size=9, italic=True, color=MUTED)
        if child is not None:
            r._r.append(child)
        return r
    begin = OxmlElement("w:fldChar"); begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = " PAGE "
    separate = OxmlElement("w:fldChar"); separate.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end")
    field_run(begin); field_run(instr); field_run(separate); field_run(text="1"); field_run(end)

def heading(doc, text, lvl):
    p = doc.add_heading(level=lvl)
    set_bidi(p, False); set_jc(p, "left")
    p.paragraph_format.space_before = Pt(12 if lvl < 3 else 8); p.paragraph_format.space_after = Pt(5)
    parse_inline(p, text, size=(18 if lvl == 1 else 15 if lvl == 2 else 13), bold=True)
    return p

def body(doc_or_cell, text, ctx, *, first_para=None):
    p = first_para if first_para is not None else doc_or_cell.add_paragraph()
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.12
    if ctx == "Arab":
        set_bidi(p, True); set_jc(p, "start")  # start = right in RTL, per locked standard
        # Brackets and other neutral punctuation are separate non-Arabic
        # segments during inline rendering.  Forcing w:rtl on those segments
        # prevents Word from placing/mirroring them as LTR text inside an
        # otherwise RTL Arabic paragraph.
        parse_inline(p, text, size=19, force_rtl=True)
    elif ctx == "caption" and text.strip().startswith("[Crop halaman"):
        set_bidi(p, False); set_jc(p, "center")
        parse_inline(p, text, size=10, italic=True, color=MUTED)
    elif ctx == "latin":
        set_bidi(p, False); set_jc(p, "left")
        parse_inline(p, text, size=13)
    else:
        set_bidi(p, False); set_jc(p, "left")
        parse_inline(p, text, size=12)
    return p

def add_image(doc, img_rel, base_dir):
    path = (base_dir / img_rel).resolve()
    if not path.exists():
        raise FileNotFoundError(f"crop not found: {path}")
    with Image.open(path) as im:
        w, h = im.size
    max_w, max_h = 15.5, 10.5
    width = min(max_w, max_h * w / h)
    p = doc.add_paragraph(); set_bidi(p, False); set_jc(p, "center")
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(3)
    p.add_run().add_picture(str(path), width=Cm(width))
    return path

def add_table(doc, rows):
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"; table.alignment = 2  # center
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:jc")): tblPr.remove(old)
    jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "center"); tblPr.append(jc)
    for old in tblPr.findall(qn("w:bidiVisual")): tblPr.remove(old)  # original DRAF tables have none
    width = Cm(17.0 / ncols)
    fsize = 10 if ncols >= 8 else 11 if ncols >= 4 else 12
    for ri, row in enumerate(table.rows):
        for ci, cell in enumerate(row.cells):
            cell.width = width; cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            parts = rows[ri][ci].split("<br>")
            for pi, part in enumerate(parts):
                p = cell.paragraphs[0] if pi == 0 else cell.add_paragraph()
                set_jc(p, "center")
                dominant_ar = len("".join(AR_RE.findall(part))) >= max(1, len(part.strip()) // 2) if part.strip() else False
                set_bidi(p, dominant_ar)
                p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
                parse_inline(p, part, size=fsize, force_rtl=dominant_ar)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

def render(fe, units, base_dir, clean=False):
    doc = Document(); style_document(doc, clean=clean)
    if clean:
        doc.core_properties.title = "Al-Qorin war Riyadhah"
        doc.core_properties.subject = ""
    else:
        doc.core_properties.title = "Al-Qorin war Riyadhah — Revisi 5 Lapis"
        doc.core_properties.subject = "Revisi terjemahan dokumenter mengikuti standar 123 artikel"
    images = []
    for kind, text in fe:
        if kind == "title":
            p = doc.add_paragraph(style="Title"); set_bidi(p, False); set_jc(p, "left")
            parse_inline(p, text, size=24, bold=True)
        elif kind == "quote":
            p = doc.add_paragraph(); set_bidi(p, False); set_jc(p, "left")
            p.paragraph_format.left_indent = Cm(0.5); parse_inline(p, text, size=11, italic=True, color=MUTED)
        else:
            body(doc, text, "terjemahan")
    for ui, u in enumerate(units):
        if ui: doc.add_page_break()
        heading(doc, u["heading"], 1)
        for ev in u["events"]:
            if ev[0] == "h2": heading(doc, ev[1], 2)
            elif ev[0] == "h3": heading(doc, ev[1], 3)
            elif ev[0] == "para": body(doc, ev[2], ev[1])
            elif ev[0] == "image": images.append(str(add_image(doc, ev[1], base_dir)))
            elif ev[0] == "table": add_table(doc, ev[1])
    return doc, images

# ------------------------------------------------------------ Amiri embedding
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
def obfuscate(data: bytes, guid: str) -> bytes:
    key = bytes.fromhex(guid.replace("{", "").replace("}", "").replace("-", ""))
    key32 = key[::-1] + key[::-1]
    return bytes(b ^ key32[i] for i, b in enumerate(data[:32])) + data[32:]

def embed_amiri(src_docx: Path, dst_docx: Path):
    variants = [("embedRegular", "Amiri-Regular.ttf", "Amiri-Regular.odttf"),
                ("embedBold", "Amiri-Bold.ttf", "Amiri-Bold.odttf"),
                ("embedItalic", "Amiri-Italic.ttf", "Amiri-Italic.odttf"),
                ("embedBoldItalic", "Amiri-BoldItalic.ttf", "Amiri-BoldItalic.odttf")]
    with zipfile.ZipFile(str(src_docx)) as z:
        parts = {n: z.read(n) for n in z.namelist()}
    # fontTable rels
    rels_name = "word/_rels/fontTable.xml.rels"
    if rels_name in parts:
        rels = etree.fromstring(parts[rels_name])
    else:
        rels = etree.Element(f"{{{REL}}}Relationships", nsmap={None: REL})
    used = {el.get("Id") for el in rels}
    def next_rid():
        n = 1
        while f"rId{n}" in used: n += 1
        used.add(f"rId{n}"); return f"rId{n}"
    for el in list(rels):
        if (el.get("Target") or "").startswith("fonts/Amiri-"): rels.remove(el)
    # fontTable
    ft = etree.fromstring(parts["word/fontTable.xml"])
    font_el = None
    for el in ft.findall(f"{{{W}}}font"):
        if el.get(f"{{{W}}}name") == FONT: font_el = el; break
    if font_el is None:
        font_el = etree.SubElement(ft, f"{{{W}}}font"); font_el.set(f"{{{W}}}name", FONT)
        for tag, val in (("panose1", "00000302060507050304"), ("charset", "01"), ("family", "roman"), ("pitch", "variable")):
            child = etree.SubElement(font_el, f"{{{W}}}{tag}"); child.set(f"{{{W}}}val", val)
    for tag, _, _ in variants:
        for old in font_el.findall(f"{{{W}}}{tag}"): font_el.remove(old)
    meta = []
    for tag, ttf, odttf in variants:
        data = (FONT_DIR / ttf).read_bytes()
        guid = "{" + str(uuid.uuid5(uuid.NAMESPACE_URL, f"kitab-al-qorin-{ttf}")).upper() + "}"
        parts[f"word/fonts/{odttf}"] = obfuscate(data, guid)
        rid = next_rid()
        rel = etree.SubElement(rels, f"{{{REL}}}Relationship")
        rel.set("Id", rid); rel.set("Type", f"{R}/font"); rel.set("Target", f"fonts/{odttf}")
        emb = etree.SubElement(font_el, f"{{{W}}}{tag}")
        emb.set(f"{{{R}}}id", rid); emb.set(f"{{{W}}}fontKey", guid)
        meta.append({"tag": tag, "ttf": ttf, "odttf": odttf, "guid": guid, "rid": rid, "bytes": len(data)})
    parts["word/fontTable.xml"] = etree.tostring(ft, xml_declaration=True, encoding="UTF-8", standalone=True)
    parts[rels_name] = etree.tostring(rels, xml_declaration=True, encoding="UTF-8", standalone=True)
    # content types
    ct = etree.fromstring(parts["[Content_Types].xml"])
    if not any(el.get("Extension") == "odttf" for el in ct.findall(f"{{{CT}}}Default")):
        d = etree.SubElement(ct, f"{{{CT}}}Default")
        d.set("Extension", "odttf"); d.set("ContentType", "application/vnd.openxmlformats-officedocument.obfuscatedFont")
    parts["[Content_Types].xml"] = etree.tostring(ct, xml_declaration=True, encoding="UTF-8", standalone=True)
    # settings: embedTrueTypeFonts (no saveSubsetFonts => full fonts)
    st = etree.fromstring(parts["word/settings.xml"])
    for tag in ("embedTrueTypeFonts", "saveSubsetFonts"):
        for old in st.findall(f"{{{W}}}{tag}"): st.remove(old)
    emb = etree.Element(f"{{{W}}}embedTrueTypeFonts")
    compat = st.find(f"{{{W}}}compat")
    if compat is not None: st.insert(list(st).index(compat), emb)
    else: st.append(emb)
    parts["word/settings.xml"] = etree.tostring(st, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(str(dst_docx), "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items(): z.writestr(name, data)
    verify_embedding(dst_docx, meta)
    return meta

def verify_embedding(docx_path: Path, meta):
    with zipfile.ZipFile(str(docx_path)) as z:
        names = set(z.namelist())
        for m in meta:
            part = f"word/fonts/{m['odttf']}"; assert part in names, part
            restored = obfuscate(z.read(part), m["guid"])  # XOR is its own inverse
            assert restored == (FONT_DIR / m["ttf"]).read_bytes(), m["ttf"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(DEFAULT_IN)); ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--units", default=""); ap.add_argument("--no-embed", action="store_true")
    ap.add_argument("--clean", action="store_true", help="omit documentary header/footer wording")
    args = ap.parse_args()
    inp, out = Path(args.input).resolve(), Path(args.output).resolve()
    only = {x.strip() for x in args.units.split(",") if x.strip()} or None
    fe, units = parse_md(inp, only)
    doc, images = render(fe, units, inp.parent, clean=args.clean)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.no_embed:
        doc.save(str(out)); meta = []
    else:
        tmp = out.with_suffix(".tmp.docx"); doc.save(str(tmp)); meta = embed_amiri(tmp, out); tmp.unlink()
    print(f"input={inp}\noutput={out}\nunits={len(units)} images={len(images)} embedded={len(meta)} bytes={out.stat().st_size}")
    print("unit_ids=" + ",".join(u["unit_id"] for u in units))

if __name__ == "__main__":
    main()
