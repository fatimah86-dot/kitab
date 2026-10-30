#!/usr/bin/env python3
"""Build AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx from the 2-layer DOCX.

Per the user's final instruction (2026-10-30):
- Delete ONLY: everything before Halaman 1 (cover/SAMPUL, so the text
  starts at the basmalah of Halaman 1), Layer headings, the
  1. Arab:/2. Latin:/3. Terjemahan: labels, PARAGRAF (in the Halaman 1
  heading), and all [Footnote: ... cetakan/bacaannya tidak jelas] lines.
- Keep === Halaman X — ... === headings and all other content verbatim.
- Correct the khadam name misprint أَصْبَاوُثْ -> أَصْبَاوُت (final ت),
  Latin reading ashba-uuti / Ashba-uuti.
- Hijaiyah letters written as Latin letters/names inside Latin and
  Terjemahan letter-sequences are restored to Arabic glyphs (curated
  exact-substring replacements only; ordinary words untouched).
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "al_qorin/AL_QORIN_123_BERSIH_2_LAYER.docx"
DEFAULT_OUTPUT = ROOT / "al_qorin/AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx"

DELETE_STYLES = {"Title", "Heading 2", "Heading 3"}
EXACT_DELETE = {
    "SAMPUL",
    "LAYER 1 - KETERANGAN HALAMAN:",
    "LAYER 1",
    "LAYER 2",
    "PARAGRAF",
    "AL-QORIN WAR RIYADHAH",
    "1. Arab:",
    "2. Latin:",
    "3. Terjemahan:",
}
CONTAINS_DELETE = (
    "footnote",
    "[footnote",
    "cetakan/bacaannya tidak jelas",
)

HEADING_RE = re.compile(r"^=== Halaman (\d+) — (.+) ===$")

# Curated exact-substring corrections: (old, new, expected_occurrences).
# Only letter-sequences denoting hijaiyah glyphs, plus the khadam name.
REPLACEMENTS: list[tuple[str, str, int]] = [
    # Khadam name, Latin/Terjemahan readings -> ashba-uuti
    ("aduunaay ashbaa-uut aala", "aduunaay ashba-uuti aala", 1),
    ("Ashba'ut, Al Syadday", "Ashba-uuti, Al Syadday", 1),
    ("ashbaawuts", "ashba-uuti", 2),
    ("Ashba'uts", "Ashba-uuti", 2),
    # Muqatta'at enumeration, Latin
    (
        "Alif laam miim, alif laam miim shaad, alif laam miim raa, alif laam raa, "
        "alif laam miim raa, kaaf haa yaa 'ain shaad, thaa haa, thaa siin miim, "
        "alif laam miim (berulang lima kali), yaa siin, shaad, haa miim, "
        "haa miim 'ain siin qaaf, haa miim (berulang), qaaf, nuun.",
        "ا ل م, ا ل م ص, ا ل م ر, ا ل ر, ا ل م ر, ك ه ي ع ص, ط ه, ط س م, "
        "ا ل م (berulang lima kali), ي س, ص, ح م, ح م ع س ق, ح م (berulang), ق, ن.",
        1,
    ),
    # Muqatta'at enumeration, Terjemahan
    (
        "Alif Lam Mim; Alif Lam Mim; Alif Lam Mim Shad; Alif Lam Mim Ra; "
        "Alif Lam Ra; Alif Lam Mim Ra; Kaf Ha Ya ‘Ain Shad; Tha Ha; "
        "Tha Sin Mim; Alif Lam Mim lima kali; Ya Sin; Shad; Ha Mim; "
        "Ha Mim ‘Ain Sin Qaf; Ha Mim lima kali; Qaf; Nun.",
        "ا ل م; ا ل م; ا ل م ص; ا ل م ر; ا ل ر; ا ل م ر; ك ه ي ع ص; ط ه; "
        "ط س م; ا ل م lima kali; ي س; ص; ح م; ح م ع س ق; ح م lima kali; ق; ن.",
        1,
    ),
    ("tis'aa) alif laam miim.", "tis'aa) ا ل م.", 1),
    ("Alif Lam Mim …", "ا ل م …", 1),
    ("«Alif Lām Mīm»", "«ا ل م»", 1),
    ("bagian pertama “Ya Sin. Demi", "bagian pertama “ي س. Demi", 1),
    ("(bintang) fa qaaf jim,", "(bintang) ف ق ج,", 1),
    ("(bintang) mim kha mim ta,", "(bintang) م خ م ت,", 1),
    ("rahasia huruf tha'", "rahasia huruf ط", 1),
    ("“Tha Sin Mim”", "“ط س م”", 1),
    ("fa jim syin ts (tsa) zh (zha) kha z (zai),", "ف ج ش ث ظ خ ز,", 1),
    (", alif laam miim, Allaahu", ", ا ل م, Allaahu", 1),
    ("al-Fatihah; fa, jim, syin, tsa, zha, kha, za;", "al-Fatihah; ف, ج, ش, ث, ظ, خ, ز;", 1),
    ("Bismillahirrahmanirrahim. Alif Lam Mim. Allah,", "Bismillahirrahmanirrahim. ا ل م. Allah,", 1),
    ("syuyuukhan, alif laam miim, min", "syuyuukhan, ا ل م, min", 1),
    ("faatiha(ti) fa jim syin takhtakhir", "faatiha(ti) ف ج ش takhtakhir", 1),
    ("kaaf haa yaa 'ain shaad ilaa", "ك ه ي ع ص ilaa", 1),
    ("Surah al-Fatihah, fa, jim, syin, dan", "Surah al-Fatihah, ف, ج, ش, dan", 1),
    ("Kaf Ha Ya 'Ain Shad sampai", "ك ه ي ع ص sampai", 1),
    ("bismillaahir rahmaanir rahiim alif laam miim dzaalikal", "bismillaahir rahmaanir rahiim ا ل م dzaalikal", 1),
    ("99 thaa haa 93 min 4 shaad daal", "99 ط ه 93 min 4 ص د", 1),
    ("Bismillahirrahmanirrahim. Alif Lam Mim. Itulah", "Bismillahirrahmanirrahim. ا ل م. Itulah", 1),
    ("99, Thaha, 93, min, 4, Shad, Dal.", "99, طه, 93, min, 4, ص, د.", 1),
    # Abjad as spaced Latin letters (Latin of Halaman 120/121 area)
    (
        "- a b t ts j h kh d dz r z s sy sh dh th zh ' gh f q k l m n h w l a y -",
        "- ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ل ا ي -",
        1,
    ),
    (
        "- a b t ts j h kh d dz r z s sy sh dh th zh -",
        "- ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ -",
        1,
    ),
    # Abjad as letter-names (Terjemahan)
    (
        "ditulis huruf-huruf berikut: alif, ba, ta, tsa, jim, ha, kha, dal, dzal, "
        "ra, zai, sin, syin, shad, dhad, tha, zha, 'ain, ghain, fa, qaf, kaf, lam, "
        "mim, nun, ha, wau, lam, alif, ya.",
        "ditulis huruf-huruf berikut: ا, ب, ت, ث, ج, ح, خ, د, ذ, ر, ز, س, ش, ص, "
        "ض, ط, ظ, ع, غ, ف, ق, ك, ل, م, ن, ه, و, ل, ا, ي.",
        1,
    ),
    (
        "“huruf-huruf Ajam” berikut: alif, ba, ta, tsa, jim, ha, kha, dal, dzal, "
        "ra, zai, sin, syin, shad, dhad, tha, zha.",
        "“huruf-huruf Ajam” berikut: ا, ب, ت, ث, ج, ح, خ, د, ذ, ر, ز, س, ش, ص, "
        "ض, ط, ظ.",
        1,
    ),
    # Letter/number string, Latin (mapped 1:1 from the Arabic paragraph)
    (
        "- h ' gh w 91119 wa 1116 wa th a 115 119 sh sh sh 11 55 m sh' b a j w l "
        "sh a a w l a 922 wa 111 th a ' a h 5115 111 196 55 wa k l w r 5 ' 6 ' w "
        "49 wa 111 d ' 191 wa 151.",
        "- ح ع غ و 91119 wa 1116 wa ط ا 115 119 ص ص ص 11 55 م صع ب ا ج و ل "
        "ص ا أ و ل أ 922 wa 111 ط أ ع ا ه 5115 111 196 55 wa ك ل و ر 5 ع 6 ع و "
        "49 wa 111 د ع 191 wa 151.",
        1,
    ),
    # Letter/number string, Terjemahan
    (
        "ha', 'ain, ghain, wau, 91119, wau, 1116, wau, tha', alif, 115, 119, "
        "shad, shad, shad, 11, 55, mim, sha' (shad dan 'ain tertulis rapat), "
        "ba', alif, jim, wa-l, shad, alif, alif berhamzah, wau, lam, "
        "alif berhamzah, 922, wau, 111, tha', alif berhamzah, 'ain, alif, ha', "
        "5115, 111, 196, 55, wau, kaf, lam, wau, ra', 5, 'ain, 6, 'ain, wau, "
        "49, wau, 111, dal, 'ain, 191, wau, 151.",
        "ح, ع, غ, و, 91119, و, 1116, و, ط, ا, 115, 119, "
        "ص, ص, ص, 11, 55, م, صع (ص dan ع tertulis rapat), "
        "ب, ا, ج, ول, ص, ا, أ, و, ل, "
        "أ, 922, و, 111, ط, أ, ع, ا, ه, "
        "5115, 111, 196, 55, و, ك, ل, و, ر, 5, ع, 6, ع, و, "
        "49, و, 111, د, ع, 191, و, 151.",
        1,
    ),
    ("(seratus jim)", "(seratus ج)", 1),
]

ARABIC_REPLACEMENTS: list[tuple[str, str, int]] = [
    ("أَصْبَاوُثْ", "أَصْبَاوُت", 6),
    ("أصباؤوتي", "أصباؤوت", 0),
    ("أصباوث", "أصباوت", 0),
    ("اصباوث", "اصباوت", 0),
]


def normalized(text: str) -> str:
    return " ".join(text.split())


def has_drawing(paragraph) -> bool:
    return bool(paragraph._p.xpath('.//*[local-name()="drawing"]'))


def deletion_reason(paragraph) -> str | None:
    if has_drawing(paragraph):
        return None
    if paragraph.style.name in DELETE_STYLES:
        return f"style:{paragraph.style.name}"
    text = normalized(paragraph.text)
    if text in EXACT_DELETE:
        return "exact"
    lowered = paragraph.text.lower()
    for needle in CONTAINS_DELETE:
        if needle.lower() in lowered:
            return f"contains:{needle}"
    return None


def clean_heading_text(text: str) -> str:
    text = re.sub(r"\bPARAGRAF\b\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("— —", "—").strip(" —") if text.endswith("—") else text
    return text


def restore_heading(doc, paragraph) -> None:
    new_text = f"=== {clean_heading_text(paragraph.text)} ==="
    paragraph.style = doc.styles["Normal"]
    runs = paragraph.runs
    if runs:
        runs[0].text = new_text
        runs[0].bold = True
        for extra in runs[1:]:
            extra._element.getparent().remove(extra._element)
    else:
        run = paragraph.add_run(new_text)
        run.bold = True


def apply_replacements(doc, table) -> Counter:
    counts: Counter = Counter()
    for old, new, expected in table:
        found = 0
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if old in run.text:
                    found += run.text.count(old)
                    run.text = run.text.replace(old, new)
        if found != expected:
            raise AssertionError(
                f"replacement {old[:50]!r}: expected {expected}, found {found}"
            )
        counts[old[:40]] = found
    return counts


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def media_hashes(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.startswith("word/media/")]
        return [hashlib.sha256(archive.read(n)).hexdigest() for n in names]


def font_part_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return len([n for n in archive.namelist() if n.startswith("word/fonts/")])


def build(input_path: Path, output_path: Path) -> Counter:
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    if input_path == output_path:
        raise ValueError("output must not overwrite its input")
    if output_path.name != "AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx":
        raise ValueError("output filename must be AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx")

    doc = Document(input_path)
    stats: Counter = Counter()
    paragraphs = list(doc.paragraphs)

    # 1) Delete everything before the Halaman 1 heading (cover/SAMPUL),
    #    so the document begins at Halaman 1 with the basmalah.
    start = next(
        i
        for i, p in enumerate(paragraphs)
        if p.style.name == "Heading 1" and normalized(p.text).startswith("Halaman 1 —")
    )
    for paragraph in paragraphs[:start]:
        if has_drawing(paragraph):
            raise AssertionError("cover prefix unexpectedly carries an image")
        element = paragraph._element
        element.getparent().remove(element)
        stats["removed:prefix_before_basmalah"] += 1

    # 2) Restore Halaman headings; delete only the listed sampah.
    for paragraph in list(doc.paragraphs):
        if paragraph.style.name == "Heading 1" and not has_drawing(paragraph):
            restore_heading(doc, paragraph)
            stats["headings_restored"] += 1
            continue
        reason = deletion_reason(paragraph)
        if reason is not None:
            stats[f"removed:{reason}"] += 1
            element = paragraph._element
            element.getparent().remove(element)

    # 3) Khadam-name correction + hijaiyah glyph restoration.
    arabic_counts = apply_replacements(doc, ARABIC_REPLACEMENTS)
    stats["arabic_ashbaut_fixed"] = arabic_counts["أَصْبَاوُثْ"]
    latin_counts = apply_replacements(doc, REPLACEMENTS)
    stats["curated_text_replacements"] = sum(latin_counts.values())

    doc.core_properties.title = ""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)

    # Acceptance checks.
    out = Document(output_path)
    texts = [p.text for p in out.paragraphs]
    styles = Counter(p.style.name for p in out.paragraphs)
    if any(style in styles for style in DELETE_STYLES | {"Heading 1"}):
        raise AssertionError(f"structural styles remain: {styles}")
    if normalized(texts[0]) != "=== Halaman 1 — PUJIAN PERTAMA ===":
        raise AssertionError(f"document must start at Halaman 1 heading, got {texts[0]!r}")
    if normalized(texts[1]) != "بسم الله الرحمن الرحيم":
        raise AssertionError(f"second paragraph must be the basmalah, got {texts[1]!r}")

    heading_numbers: list[int] = []
    joined = "\n".join(texts)
    for paragraph in out.paragraphs:
        text = normalized(paragraph.text)
        if text in EXACT_DELETE:
            raise AssertionError(f"exact banned line remains: {text!r}")
        lowered = paragraph.text.lower()
        for needle in CONTAINS_DELETE:
            if needle.lower() in lowered:
                raise AssertionError(f"banned text remains: {needle!r}")
        if "layer 1" in lowered or "layer 2" in lowered:
            raise AssertionError("a Layer label remains")
        if "PARAGRAF" in paragraph.text:
            raise AssertionError("PARAGRAF remains")
        m = HEADING_RE.match(text)
        if m:
            heading_numbers.append(int(m.group(1)))
    if heading_numbers != list(range(1, 123)):
        raise AssertionError(f"expected Halaman 1..122 headings, got {len(heading_numbers)}")
    if "أَصْبَاوُثْ" in joined or joined.count("أَصْبَاوُت") != 6:
        raise AssertionError("khadam name correction incomplete")
    for bad in ("ashbaawuts", "Ashba'uts", "ashbaa-uut"):
        if bad in joined:
            raise AssertionError(f"old Latin khadam form remains: {bad}")
    if re.search(r"(?<![A-Za-z])[a-z](?: [a-z']){3,}", joined):
        raise AssertionError("spaced Latin single-letter sequence remains")

    if len(out.inline_shapes) != 26:
        raise AssertionError(f"expected 26 inline images, got {len(out.inline_shapes)}")
    if media_hashes(output_path) != media_hashes(input_path):
        raise AssertionError("embedded media hashes/order changed")
    if font_part_count(output_path) != 4:
        raise AssertionError("embedded font parts were not preserved")

    stats["output_paragraphs"] = len(out.paragraphs)
    stats["output_nonempty_paragraphs"] = sum(1 for t in texts if t.strip())
    stats["media_labels"] = sum(normalized(t) == "Media:" for t in texts)
    stats["step_labels"] = sum(normalized(t).startswith("Langkah ke-") for t in texts)
    stats["tujuan_labels"] = sum(normalized(t).startswith("Tujuan") for t in texts)
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    stats = build(args.input, args.output)
    print(f"input={args.input.resolve()}")
    print(f"output={args.output.resolve()}")
    print(f"stats={dict(stats)}")
    print(f"bytes={args.output.resolve().stat().st_size}")
    print(f"sha256={sha256(args.output.resolve())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
