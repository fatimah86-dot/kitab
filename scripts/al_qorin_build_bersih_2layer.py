#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the separate two-layer clean Al-Qorin edition.

The input is the already-derived clean *Halaman* Markdown.  This builder
never overwrites that input or either canonical clean file.  It writes a
new ``_2_LAYER`` Markdown edition in which each unit is reorganized as:

* LAYER 1 — KETERANGAN HALAMAN: the existing Arab, Latin, and Terjemahan
  bodies copied without textual changes;
* an optional one-line italic footnote, extracted only when the old clean
  Syarah explicitly marks an Arabic word/phrase as an unclear print or
  unsettled reading;
* LAYER 2 — TATACARA PRAKTIK, only where the old clean edition already
  records an actual procedure/requirement/reading.  Its prose is retained
  only as Media, ordered Langkah, and Tujuan; documentary meta-sentences
  and pure figure/dot inventories are not carried into the steps.

All unit headings and crop/image references are preserved.  Images that
were located in the old Syarah are moved to the end of Layer 1 (after
Terjemahan) because the Syarah heading itself is removed.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "al_qorin/AL_QORIN_123_BERSIH_HALAMAN.md"
DEFAULT_OUTPUT = ROOT / "al_qorin/AL_QORIN_123_BERSIH_2_LAYER.md"

UNIT_RE = re.compile(r"^##\s+(.+)$", flags=re.M)
SECTION_RE = re.compile(r"^###\s+(.+)$", flags=re.M)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMAGE_LINE_RE = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")
ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]")
QUOTE_RE = re.compile(r"«([^»]{1,140})»")
FIELD_RE = re.compile(r"^\*\*(Media|Waktu|Bukhur):\*\*\s*(.+)$", flags=re.S)

UNCERTAIN_RE = re.compile(
    r"("  #
    r"tidak\s+dapat\s+dipastikan|belum\s+dapat\s+dipastikan|"
    r"tidak\s+dipastikan|belum\s+pasti|tidak\s+terbaca(?:\s+pasti)?|"
    r"tidak\s+jelas|bacaan\s+terbuka|persoalan\s+terbuka|"
    r"tidak\s+dikenali|kemungkinan\s+salah\s+baca|bisa\s+salah\s+baca|"
    r"tercetak\s+rusak|cetakan(?:nya)?\s+tidak\s+jelas|"
    r"susunan(?:nya)?\s+tidak\s+jelas|hubungan[^.;]{0,70}belum\s+ditetapkan"
    r")",
    flags=re.I,
)
CANDIDATE_INTRO_RE = re.compile(r"\b(kemungkinan|mungkin|usulan|kandidat)\b", flags=re.I)

META_RE = re.compile(
    r"("  #
    r"dinisbatkan|din\s+isbatkan|dinukil\s+sebagai\s+isi|dicatat\s+sebagai\s+isi|"
    r"dicatat\s+karena\s+itu\s+isi|ini\s+pelaporan|pelaporan\s+isi\s+naskah|"
    r"dalam\s+kerangka\s+dokumenter|bukan\s+anjuran|bukan\s+resep|"
    r"bukan\s+nasihat|bukan\s+pertolongan\s+medis|tidak\s+ada\s+jaminan|"
    r"tanpa\s+jaminan|tidak\s+diverifikasi|jangan\s+menguji|"
    r"tidak\s+menggantikan\s+pengobatan|bukan\s+untuk\s+diamalkan|"
    r"tidak\s+bersumber\s+dari\s+Al-Qur|tidak\s+ada\s+dasar\s+Al-Qur|"
    r"persoalan\s+yang\s+diperdebatkan|dicatat\s+posisinya|"
    r"penilaian\s+penulis,?\s+bukan\s+hasil\s+uji|bukan\s+hasil\s+uji|"
    r"sengatan/gigitan\s+berbahaya\s+harus\s+ditangani\s+dokter"
    r")",
    flags=re.I,
)
NO_NEW_PRACTICE_RE = re.compile(
    r"tidak\s+ada\s+(?:tata\s+cara|praktik)\s+baru",
    flags=re.I,
)
FIGURE_INVENTORY_RE = re.compile(
    r"^(?:Titik\s+baris|Pencatatan\s+bentuk|B\d+(?:-\d+)?\b|\*\*RAJAH\b)",
    flags=re.I,
)

# Seven old practice sections have no **Media:** field.  These entries are
# confined to the medium/reference already named in that section.
MEDIA_OVERRIDES: dict[int, str] = {
    4: "Bacaan al-Fatihah.",
    7: "Tidak ada media material yang dinyatakan secara tersendiri; yang dinyatakan ialah khalwat/riyadhah.",
    38: "Tidak ada media material yang dinyatakan secara tersendiri.",
    61: "Daftar buruj 5–12, tujuh bintang/planet, dan dua kolom nama bulan.",
    62: "Daftar empat sulthan malaikat dan tujuh raja menurut hari.",
    107: "Nama-nama yang disebut bersama Nabi Adam.",
    122: "Salat dua rakaat, selawat, dan bacaan al-Fatihah.",
}

# Two field-only sections need their stated time/media expressed as steps.
STEP_OVERRIDES: dict[int, tuple[str, ...]] = {
    98: (
        "Berpuasa tujuh hari mulai hari Ahad, saat tidak ada angin, awan, atau hujan dan bulan sedang bertambah.",
        "Mengikuti azimah dengan bilangan dan huruf pada tujuh hari pertama, dengan rajah di kepala halaman.",
    ),
    105: (
        "Berpuasa tiga hari pada rangkaian Ahad–Senin–Selasa atau Selasa–Rabu–Kamis, sebagaimana kedua rangkaian pada cetakan dipertahankan.",
        "Membaca sepuluh nama menurut bilangan jummal masing-masing (1072, 535, 1403, 1598, 517, 646, 1813, 1314, 908, dan 1598) hingga pagi.",
    ),
}

# Tujuan is never inferred from a general theme.  Each entry below is the
# purpose/topic explicitly carried by the prose of the old practice section
# (or by its immediately stated chapter heading in that section).  Pages
# whose old summary states no separate goal say so plainly.
PURPOSE_BY_PAGE: dict[int, str] = {
    4: "Menghadiahkan bacaan al-Fatihah kepada Nabi Muhammad, keluarga beliau, dan pengarang sebelum memulai.",
    7: "Tidak dinyatakan secara tersendiri pada halaman ini.",
    11: "Menjalani jadwal riyadhah salik berkeluarga yang dirinci pada halaman ini.",
    12: "Melanjutkan jadwal riyadhah sampai genap delapan puluh hari.",
    13: "Menyelesaikan rangkaian riyadhah sampai delapan puluh hari.",
    14: "Merespons tabir/lintasan yang muncul selama riyadhah.",
    15: "Memenuhi syarat salik yang dinyatakan naskah.",
    29: "Menjalani khalwat delapan puluh hari.",
    36: "Memenuhi syarat khalwat dan aturan berbuka yang dinyatakan.",
    37: "Mengatur kadar zikir jahr sampai keadaan tenang.",
    38: "Tidak berhenti atau terhijab oleh tanda dan cahaya yang tampak selama riyadhah.",
    39: "Menyempurnakan delapan puluh hari.",
    40: "Menjalani tahapan sembilan puluh hari yang dirinci naskah.",
    41: "Tidak dinyatakan secara tersendiri pada halaman ini.",
    42: "Menjalani wirid Jumat, sedekah harian, dan riyadhah kecil tiga hari.",
    49: "Pengobatan orang yang kerasukan.",
    50: "Lanjutan pengobatan orang yang kerasukan.",
    51: "Mengobati golongan siang pada siang dan golongan malam pada malam.",
    52: "Memenuhi syarat kerja pengobatan yang dinyatakan naskah.",
    53: "Memenuhi syarat kerja pengobatan yang dinyatakan naskah.",
    54: "Memenuhi syarat kerja pengobatan yang dinyatakan naskah.",
    55: "Menghalangi ‘ifrit dan membaca susunan bacaan yang dinyatakan.",
    56: "Menutup susunan bacaan dan menempatkan «نهاية القرين» pada tempat yang halal.",
    57: "Pengobatan segala penyakit.",
    58: "Menyelesaikan doa dan wafaq untuk segala penyakit.",
    59: "Menguasai daftar pengetahuan prasyarat yang dituntut penulis.",
    60: "Mengetahui padanan hari, planet, logam, dan awal buruj.",
    61: "Mengetahui buruj 5–12, tujuh bintang/planet, dan nama-nama bulan.",
    62: "Mengetahui empat sulthan malaikat dan tujuh raja menurut hari.",
    63: "Memulai pengobatan qarin dan pembatalan sihir.",
    64: "Pembatalan sihir.",
    65: "Pengobatan dari penyakit.",
    66: "Perlindungan dari segala yang dibenci dan kesembuhan dari segala penyakit.",
    67: "Membatalkan sihir dan melepaskan orang yang terikat.",
    68: "Pengusiran dan kehamilan.",
    69: "Kehamilan.",
    70: "Kehamilan dan mengurai sihir.",
    71: "Mencegah jatuhnya janin dan faidah kehamilan.",
    72: "Kehamilan.",
    73: "Kehamilan.",
    74: "Kehamilan.",
    75: "Pembakaran ‘āriḍ dan menghadirkan individu jin.",
    76: "Mendengar salam yang disebut naskah dan mengangkat perdarahan.",
    77: "Mengangkat perdarahan dan menghilangkan sakit kepala kronis.",
    78: "Menenangkan sakit kepala.",
    79: "Mengirim bantuan yang kuat ke arah yang dituju.",
    80: "Menyelesaikan pengiriman dan membaca qasam untuk sengatan kalajengking/gigitan ular.",
    81: "Melanjutkan qasam sengatan serta mengembalikan pasangan sebagaimana dirumuskan naskah.",
    82: "Mahabbah.",
    83: "Talbīs al-juttsah dan keamanan dari rasa takut.",
    84: "Memenuhi kebutuhan dan mahabbah.",
    85: "Mahabbah dan pertunangan.",
    86: "Memudahkan persalinan.",
    97: "Menggunakan Ratu Jamjah dan meminta perjanjian.",
    98: "Memenuhi syarat penggunaan lanjutan yang dinyatakan.",
    99: "Menghadirkan sosok yang disebut naskah dan mengambil perjanjian.",
    100: "Mengucapkan azimah dalam rangkaian penggunaan Jamjah.",
    101: "Menghadirkan individu jin untuk memenuhi keperluan.",
    102: "Menghadirkan individu jin sampai terdengar suara salam.",
    105: "Tidak dinyatakan secara tersendiri pada halaman ini.",
    106: "Memenuhi keperluan yang dinyatakan naskah.",
    107: "Menghadirkan raja-raja jin.",
    108: "Menghadirkan dengan tiga nama dan mengetahui rijāl al-ghaib.",
    109: "Menyampaikan salam kepada rijāl al-ghaib dan menghadap keperluan.",
    111: "Memenuhi keperluan melalui doa yang dibaca tiga kali.",
    112: "Melanjutkan doa tawasul dan permohonan ampun.",
    115: "Menghadap rijāl al-ghaib dan menyebutkan keperluan.",
    116: "Mencegah qarinah Umm ash-Shibyān dan bab qarinah bagi perempuan yang keguguran.",
    117: "Menangkal jin dari pemegang kitab dan membaca ayat perlindungan.",
    119: "Penjagaan dari gangguan malam dan siang.",
    120: "Mengetahui nama-nama qarinah dan menulis al-Burūj/al-Ḥadīd untuk digantungkan.",
    121: "Membuat ḥijāb al-qarnā’.",
    122: "Menghadiahkan al-Fatihah untuk Syekh Muhammad Sibami.",
}


@dataclass
class Stats:
    units: int = 0
    layer2_units: int = 0
    omitted_no_new_practice: int = 0
    footnotes: int = 0
    moved_syarah_images: int = 0
    practice_steps: int = 0
    source_images: int = 0
    output_images: int = 0
    omitted_pages: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class Unit:
    heading: str
    page: int
    sections: dict[str, str]


@dataclass(frozen=True)
class Practice:
    media: str
    steps: tuple[str, ...]
    purpose: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def trim_blank_lines(text: str) -> str:
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def ensure_period(text: str) -> str:
    text = normalize_space(text).rstrip()
    if text and text[-1] not in ".!?":
        text += "."
    return text


def capitalize_first(text: str) -> str:
    for i, ch in enumerate(text):
        if ch.isalpha():
            if ch.islower():
                return text[:i] + ch.upper() + text[i + 1 :]
            return text
    return text


def split_units(text: str) -> tuple[str, list[Unit]]:
    matches = list(UNIT_RE.finditer(text))
    if not matches:
        raise ValueError("no unit headings found")
    front = text[: matches[0].start()]
    units: list[Unit] = []
    for idx, match in enumerate(matches):
        heading = match.group(1).strip()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        sections = split_sections(body, heading)
        if heading == "SAMPUL":
            page = 0
        else:
            page_match = re.match(r"Halaman\s+(\d+)\b", heading)
            if not page_match:
                raise ValueError(f"unexpected unit heading: {heading!r}")
            page = int(page_match.group(1))
        units.append(Unit(heading=heading, page=page, sections=sections))
    return front, units


def split_sections(body: str, heading: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(body))
    if not matches:
        raise ValueError(f"unit has no layer headings: {heading}")
    preface = body[: matches[0].start()].strip()
    if preface:
        raise ValueError(f"unexpected text before first layer in {heading}: {preface[:80]!r}")
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        name = match.group(1).strip()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        if name in sections:
            raise ValueError(f"duplicate section {name!r} in {heading}")
        sections[name] = trim_blank_lines(body[match.end() : end])
    expected_prefix = ["1. Arab", "2. Latin", "3. Terjemahan", "4. Syarah"]
    names = list(sections)
    if names[:4] != expected_prefix:
        raise ValueError(f"unexpected first sections in {heading}: {names!r}")
    if len(names) > 5 or (len(names) == 5 and names[4] != "5. Khususiyah dan Tatacara Praktik"):
        raise ValueError(f"unexpected sections in {heading}: {names!r}")
    return sections


def paragraphs(text: str) -> list[str]:
    return [trim_blank_lines(p) for p in re.split(r"\n\s*\n", text) if p.strip()]


def extract_syarah_images(syarah: str) -> tuple[str, list[str]]:
    kept: list[str] = []
    images: list[str] = []
    for para in paragraphs(syarah):
        lines = para.splitlines()
        remaining: list[str] = []
        for line in lines:
            if IMAGE_LINE_RE.match(line.strip()):
                images.append(line.strip())
            else:
                remaining.append(line)
        cleaned = trim_blank_lines("\n".join(remaining))
        if cleaned:
            kept.append(cleaned)
    return "\n\n".join(kept), images


def source_quotes_before_candidate(segment: str, limit: int | None = None) -> list[str]:
    """Arabic quotes that name the source term, excluding later proposals."""
    end = limit if limit is not None else len(segment)
    candidate = CANDIDATE_INTRO_RE.search(segment[:end])
    if candidate and candidate.start() > 0:
        end = min(end, candidate.start())
    found: list[str] = []
    for match in QUOTE_RE.finditer(segment[:end]):
        term = normalize_space(match.group(1))
        if term == "…" or not ARABIC_RE.search(term):
            continue
        if len(term) > 120:
            continue
        if term not in found:
            found.append(term)
    return found


def uncertain_marker(segment: str) -> re.Match[str] | None:
    for match in UNCERTAIN_RE.finditer(segment):
        prefix = segment[max(0, match.start() - 36) : match.start()].lower()
        if re.search(r"\b(bukan|tanpa menyebut|bukan penanda|bukan menyatakan)\b[^ ]*(?:\s+\S+){0,5}$", prefix):
            continue
        return match
    return None


def extract_footnote(syarah_without_images: str) -> str | None:
    terms: list[str] = []
    for para in paragraphs(syarah_without_images):
        flat = normalize_space(para)
        segments = [s.strip() for s in re.split(r";\s*|(?<=[.!?])\s+", flat) if s.strip()]
        previous_source_quotes: list[str] = []
        for segment in segments:
            marker = uncertain_marker(segment)
            if marker:
                quoted = source_quotes_before_candidate(segment, marker.start())
                if not quoted and previous_source_quotes:
                    quoted = [previous_source_quotes[-1]]
                for term in quoted:
                    if term not in terms:
                        terms.append(term)
                    if len(terms) >= 3:
                        break
            previous_source_quotes = source_quotes_before_candidate(segment)
            if len(terms) >= 3:
                break
        if len(terms) >= 3:
            break
    if not terms:
        return None
    label = "kata" if len(terms) == 1 and " " not in terms[0] else "kata/frasa"
    joined = ", ".join(f"«{term}»" for term in terms)
    return f"*[Footnote: {label} {joined} cetakan/bacaannya tidak jelas, dibiarkan.]*"


def clean_practice_text(text: str) -> str:
    text = normalize_space(text)
    text = re.sub(
        r"\s*\([^()]*?(?:tidak\s+diverifikasi|ringkasan\s+Metode|dipotong\s+tegas\s+pada\s+catatan\s+sumber)[^()]*?\)",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"\s+menurut\s+ringkasan\s+Metode\b", "", text, flags=re.I)
    text = re.sub(r"yang\s+dinisbatkan\s+kepadanya\b", "padanannya", text, flags=re.I)
    text = re.sub(r"yang\s+dinisbatkan(?:\s+penulis)?\b", "yang disebutkan", text, flags=re.I)
    text = re.sub(r"\s+—\s*(?:bukan\s+anjuran|tanpa\s+jaminan)[^.]*$", "", text, flags=re.I)
    return normalize_space(text)


def clean_meta_clause(clause: str) -> str | None:
    clause = clean_practice_text(clause).strip(" .")
    if not clause:
        return None
    if NO_NEW_PRACTICE_RE.search(clause):
        return None
    if re.search(r"^(?:halaman\s+berhenti|halaman\s+ini\s+berhenti|tata\s+caranya\s+menyusul)\b", clause, flags=re.I):
        return None

    # Drop a documentary tail after an em dash or comma while retaining the
    # manuscript action that precedes it.
    for sep in (" — ", " – ", ", "):
        if sep in clause:
            head, tail = clause.split(sep, 1)
            if META_RE.search(tail) and len(head) >= 12:
                clause = head.strip()
                break
    if META_RE.search(clause):
        # A semicolon has already isolated most meta tails.  If a whole
        # remaining sentence is attribution/caveat only, discard it.
        if not re.search(
            r"\b(membaca|dibaca|menulis|ditulis|membakar|dibakar|salat|berzikir|digantung|menghadap|duduk|berpuasa|berbuka|mengulang|menghadirkan|menyebut)\b",
            clause,
            flags=re.I,
        ):
            return None
        clause = re.sub(r";.*$", "", clause).strip()

    clause = re.sub(r"^Sumber\s+menyebut\s+", "", clause, flags=re.I)
    clause = re.sub(r"^Klaim\s+bahwa\s+", "", clause, flags=re.I)
    clause = re.sub(r"^Praktik:\s*", "", clause, flags=re.I)
    clause = re.sub(r"^Penulis\s+melanjutkan\s+jadwal\s+riyadhah\s+[^:]+:\s*", "", clause, flags=re.I)
    clause = re.sub(r"\s+Dinisbatkan\s+(?:pada|kepada)\s+penulis.*$", "", clause, flags=re.I)
    clause = re.sub(r"\s+Din\s+Isbatkan.*$", "", clause, flags=re.I)
    clause = clause.strip(" .")
    if not clause or META_RE.search(clause):
        # Do not let a residual caveat become a numbered instruction.
        if META_RE.search(clause):
            return None
    return capitalize_first(clause)


def split_top_level(text: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    start = 0
    paren = 0
    bracket = 0
    quote = False
    for i, ch in enumerate(text):
        if ch == "«":
            quote = True
        elif ch == "»":
            quote = False
        elif not quote and ch == "(":
            paren += 1
        elif not quote and ch == ")":
            paren = max(0, paren - 1)
        elif not quote and ch == "[":
            bracket += 1
        elif not quote and ch == "]":
            bracket = max(0, bracket - 1)
        elif ch == delimiter and paren == 0 and bracket == 0 and not quote:
            parts.append(text[start:i])
            start = i + 1
    parts.append(text[start:])
    return [p.strip() for p in parts if p.strip()]


ACTION_START_RE = re.compile(
    r"^(?:lalu|kemudian|setelah|sesudah|sebelum|ketika|bila|apabila|"
    r"membaca|dibaca|menulis|ditulis|membakar|dibakar|menggantung|digantung|"
    r"berzikir|salat|duduk|menghadap|memakai|menyebut|mengulang|menghadirkan|"
    r"bertanya|meletakkan|diminum|berbuka|berpuasa|menjauhi|meninggalkan|"
    r"menjaga|bersedekah|berwudu|mandi|tidur|bangun|tetap|mengatur|tidak|"
    r"meminta|pergi|masuk|berbaring|berdiri|menoleh|mengucapkan|membatasi|"
    r"mengurangi|memperbanyak|menyediakan|mengangkat|bekerja|mengobati|"
    r"memenuhi|memecah|makan|minum|mengambil|memberi|mendengar|melihat)\b",
    flags=re.I,
)


def split_comma_actions(clause: str) -> list[str]:
    pieces = split_top_level(clause, ",")
    if len(pieces) <= 1:
        return pieces
    merged: list[str] = [pieces[0]]
    for piece in pieces[1:]:
        if ACTION_START_RE.match(piece.strip()) and len(merged[-1]) >= 18:
            merged.append(piece.strip())
        else:
            merged[-1] = merged[-1].rstrip() + ", " + piece.strip()
    return merged


def extract_steps(prose_paragraphs: list[str]) -> list[str]:
    steps: list[str] = []
    for para in prose_paragraphs:
        flat = clean_practice_text(para)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=(?:[A-Z«\(\[]|\*\*))", flat) if s.strip()]
        if not sentences and flat:
            sentences = [flat]
        for sentence in sentences:
            for semicolon_clause in split_top_level(sentence, ";"):
                for clause in split_comma_actions(semicolon_clause):
                    cleaned = clean_meta_clause(clause)
                    if not cleaned:
                        continue
                    # Bracketed figure descriptions are not instructions.
                    if FIGURE_INVENTORY_RE.match(cleaned):
                        continue
                    sentence_step = ensure_period(cleaned)
                    if sentence_step not in steps:
                        steps.append(sentence_step)
    return steps


def token_overlap(a: str, b: str) -> float:
    tokens_a = {t for t in re.findall(r"[a-zà-ÿ0-9]+", a.lower()) if len(t) > 3}
    tokens_b = {t for t in re.findall(r"[a-zà-ÿ0-9]+", b.lower()) if len(t) > 3}
    if not tokens_a:
        return 1.0
    return len(tokens_a & tokens_b) / len(tokens_a)


def convert_practice(page: int, body: str) -> Practice | None:
    if NO_NEW_PRACTICE_RE.search(body):
        return None

    fields: dict[str, str] = {}
    prose: list[str] = []
    for para in paragraphs(body):
        flat = normalize_space(para)
        field_match = FIELD_RE.match(flat)
        if field_match:
            fields[field_match.group(1)] = clean_practice_text(field_match.group(2))
            continue
        if FIGURE_INVENTORY_RE.match(flat):
            continue
        # Pure dot/figure inventories can be packed into one paragraph with
        # many pipe separators; the crop itself remains in Layer 1.
        if flat.count("|") >= 8 and not re.search(r"\b(ditulis|membaca|dibaca|salat|berzikir)\b", flat, flags=re.I):
            continue
        prose.append(para)

    steps = list(STEP_OVERRIDES.get(page, ())) or extract_steps(prose)

    waktu = fields.get("Waktu", "")
    if waktu and page not in STEP_OVERRIDES:
        joined_steps = " ".join(steps)
        if token_overlap(waktu, joined_steps) < 0.45:
            steps.insert(0, ensure_period(f"Waktu yang dinyatakan: {waktu}"))

    if not steps:
        # Field-only residue other than the explicit overrides above is not
        # enough to manufacture an ordered procedure.
        return None

    media_parts: list[str] = []
    if page in MEDIA_OVERRIDES:
        media_parts.append(MEDIA_OVERRIDES[page].rstrip("."))
    elif fields.get("Media"):
        media_parts.append(fields["Media"].rstrip("."))
    if fields.get("Bukhur"):
        bukhur = fields["Bukhur"].rstrip(".")
        if bukhur.lower() not in " ".join(media_parts).lower():
            media_parts.append(f"Bukhur: {bukhur}")
    if not media_parts:
        media_parts.append("Tidak ada media material yang dinyatakan secara tersendiri")
    media = ensure_period("; ".join(media_parts))

    purpose = PURPOSE_BY_PAGE.get(page)
    if purpose is None:
        raise AssertionError(f"missing explicit Tujuan mapping for practice page {page}")
    return Practice(media=media, steps=tuple(steps), purpose=ensure_period(purpose))


def build_markdown(source_text: str, stats: Stats) -> str:
    front, units = split_units(source_text)
    stats.units = len(units)
    stats.source_images = len(IMAGE_RE.findall(source_text))
    if len(units) != 123:
        raise AssertionError(f"expected 123 units, got {len(units)}")
    expected_pages = [0] + list(range(1, 123))
    if [u.page for u in units] != expected_pages:
        raise AssertionError("unit sequence is not SAMPUL + Halaman 1..122")

    out: list[str] = []
    front_trimmed = front.rstrip()
    if front_trimmed:
        out.append(front_trimmed)
        out.append("")

    for unit in units:
        arab = unit.sections["1. Arab"]
        latin = unit.sections["2. Latin"]
        terjemahan = unit.sections["3. Terjemahan"]
        syarah_without_images, syarah_images = extract_syarah_images(unit.sections["4. Syarah"])
        stats.moved_syarah_images += len(syarah_images)
        footnote = extract_footnote(syarah_without_images)
        if footnote:
            stats.footnotes += 1

        out.append(f"## {unit.heading}")
        out.append("")
        out.append("### LAYER 1 - KETERANGAN HALAMAN")
        out.append("")
        out.append("#### 1. Arab")
        out.append("")
        out.append(arab)
        out.append("")
        out.append("#### 2. Latin")
        out.append("")
        out.append(latin)
        out.append("")
        out.append("#### 3. Terjemahan")
        out.append("")
        out.append(terjemahan)
        for image in syarah_images:
            out.append("")
            out.append(image)
        if footnote:
            out.append("")
            out.append(footnote)

        old_practice = unit.sections.get("5. Khususiyah dan Tatacara Praktik")
        if old_practice is not None:
            practice = convert_practice(unit.page, old_practice)
            if practice is None:
                stats.omitted_no_new_practice += 1
                stats.omitted_pages.append(unit.page)
            else:
                stats.layer2_units += 1
                stats.practice_steps += len(practice.steps)
                out.append("")
                out.append("### LAYER 2 - TATACARA PRAKTIK")
                out.append("")
                out.append(f"**Media:** {practice.media}")
                out.append("")
                out.append("**Langkah:**")
                out.append("")
                for idx, step in enumerate(practice.steps, 1):
                    out.append(f"{idx}. {step}")
                out.append("")
                out.append(f"**Tujuan:** {practice.purpose}")
        out.append("")

    output = "\n".join(out).rstrip() + "\n"
    validate_output(source_text, output, stats)
    return output


def output_layer1_bodies(output: str) -> dict[tuple[int, str], str]:
    bodies: dict[tuple[int, str], str] = {}
    unit_matches = list(UNIT_RE.finditer(output))
    for idx, match in enumerate(unit_matches):
        heading = match.group(1).strip()
        page = 0 if heading == "SAMPUL" else int(re.match(r"Halaman\s+(\d+)", heading).group(1))  # type: ignore[union-attr]
        end = unit_matches[idx + 1].start() if idx + 1 < len(unit_matches) else len(output)
        block = output[match.end() : end]
        h4 = list(re.finditer(r"^####\s+(.+)$", block, flags=re.M))
        for j, hm in enumerate(h4):
            body_end = h4[j + 1].start() if j + 1 < len(h4) else len(block)
            if hm.group(1).strip() == "3. Terjemahan":
                layer2 = block.find("\n### LAYER 2", hm.end())
                if layer2 != -1:
                    body_end = min(body_end, layer2)
            bodies[(page, hm.group(1).strip())] = trim_blank_lines(block[hm.end() : body_end])
    return bodies


def validate_output(source_text: str, output: str, stats: Stats) -> None:
    stats.output_images = len(IMAGE_RE.findall(output))
    if IMAGE_RE.findall(source_text) != IMAGE_RE.findall(output):
        raise AssertionError("image/crop reference list changed")
    if "### 4. Syarah" in output or "Khususiyah dan Tatacara Praktik" in output:
        raise AssertionError("old Syarah/Khususiyah heading remains")
    if len(re.findall(r"^### LAYER 1 - KETERANGAN HALAMAN$", output, flags=re.M)) != 123:
        raise AssertionError("Layer 1 heading count is not 123")
    if len(re.findall(r"^### LAYER 2 - TATACARA PRAKTIK$", output, flags=re.M)) != stats.layer2_units:
        raise AssertionError("Layer 2 heading count does not match stats")
    for name in ("1. Arab", "2. Latin", "3. Terjemahan"):
        if len(re.findall(rf"^#### {re.escape(name)}$", output, flags=re.M)) != 123:
            raise AssertionError(f"subheading count is not 123: {name}")

    _, source_units = split_units(source_text)
    bodies = output_layer1_bodies(output)
    for unit in source_units:
        if bodies[(unit.page, "1. Arab")] != unit.sections["1. Arab"]:
            raise AssertionError(f"Arab body changed on page {unit.page}")
        if bodies[(unit.page, "2. Latin")] != unit.sections["2. Latin"]:
            raise AssertionError(f"Latin body changed on page {unit.page}")
        translation_out = bodies[(unit.page, "3. Terjemahan")]
        if not translation_out.startswith(unit.sections["3. Terjemahan"]):
            raise AssertionError(f"Terjemahan body changed on page {unit.page}")

    for block in re.split(r"^### LAYER 2 - TATACARA PRAKTIK$", output, flags=re.M)[1:]:
        block = block.split("\n## ", 1)[0]
        if "**Media:**" not in block or "**Langkah:**" not in block or "**Tujuan:**" not in block:
            raise AssertionError("a Layer 2 block lacks Media/Langkah/Tujuan")
        if not re.search(r"^1\.\s+\S", block, flags=re.M):
            raise AssertionError("a Layer 2 block lacks numbered steps")
        if META_RE.search(block):
            found = META_RE.search(block).group(0)  # type: ignore[union-attr]
            raise AssertionError(f"documentary meta wording remains in Layer 2: {found!r}")

    footnotes = re.findall(r"^\*\[Footnote: .+\]\*$", output, flags=re.M)
    if len(footnotes) != stats.footnotes:
        raise AssertionError("footnote count does not match stats")
    if any("\n" in note for note in footnotes):
        raise AssertionError("a footnote is not one line")


def build_one(source: Path, output: Path) -> dict[str, object]:
    source = source.resolve()
    output = output.resolve()
    if source == output:
        raise ValueError("output must not overwrite its input")
    if not output.name.endswith("_2_LAYER.md"):
        raise ValueError("output filename must end with _2_LAYER.md")
    protected = {
        (ROOT / "al_qorin/AL_QORIN_123_BERSIH.md").resolve(),
        (ROOT / "al_qorin/AL_QORIN_123_BERSIH_HALAMAN.md").resolve(),
        (ROOT / "al_qorin/REVISI_AL_QORIN_123.md").resolve(),
        (ROOT / "al_qorin/REVISI_AL_QORIN_123_HALAMAN.md").resolve(),
    }
    if output in protected:
        raise ValueError("refusing to overwrite a canonical/derived master")

    source_bytes = source.read_bytes()
    stats = Stats()
    output_text = build_markdown(source_bytes.decode("utf-8"), stats)
    output_bytes = output_text.encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(output_bytes)
    return {
        "source": str(source),
        "output": str(output),
        "source_sha256": sha256_bytes(source_bytes),
        "output_sha256": sha256_bytes(output_bytes),
        "units": stats.units,
        "layer2_units": stats.layer2_units,
        "omitted_no_new_practice": stats.omitted_no_new_practice,
        "omitted_pages": stats.omitted_pages,
        "footnotes": stats.footnotes,
        "moved_syarah_images": stats.moved_syarah_images,
        "practice_steps": stats.practice_steps,
        "source_images": stats.source_images,
        "output_images": stats.output_images,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result = build_one(args.input, args.output)
    print(
        "2-layer "
        f"source={result['source']} output={result['output']} "
        f"units={result['units']} layer2_units={result['layer2_units']} "
        f"omitted_no_new_practice={result['omitted_no_new_practice']} "
        f"omitted_pages={result['omitted_pages']} footnotes={result['footnotes']} "
        f"moved_syarah_images={result['moved_syarah_images']} "
        f"practice_steps={result['practice_steps']} images={result['output_images']} "
        f"sha256={result['output_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
