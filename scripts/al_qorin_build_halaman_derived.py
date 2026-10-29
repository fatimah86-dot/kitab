#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build derived Al-Qorin Markdown editions with page labels.

The transformer never writes to its input.  It implements the requested
presentation-level cleanup on a copy:

* Markdown unit headings ``M10`` become a single ``Halaman 10`` label;
  repeated page wording already present in the heading is removed.
* Other standalone ``M<digits>`` references become ``Halaman <digits>``.
* A whole sentence containing ``klaim penulis`` (case-insensitive,
  including the overlapped substring in ``diklaim penulis``) or
  ``Batch <digits>`` is removed.
* ``[CATATAN PENERJEMAH: ...]`` labels, image lines, layer headings,
  tables' cell structure, and crop references are preserved.

This is a derived-edition builder only; the canonical Khatam masters
and DOCX files are intentionally not modified.

After that presentation cleanup, the builder applies a guarded list of
exact replacements for explicit unfinished markers in Layer 2 (Latin)
of the derived editions: Arabic/vocalization placeholders, “tidak
disalin penuh” process notes, continuation brackets, and marker
ellipses.  A replacement only supplies a reading determined by the
final vocalized Arabic in the same unit, removes a process marker when
the Latin continuation is already present, or turns a genuine page-edge
break into a plain ellipsis.  A few directly attached Terjemahan/note
sentences are aligned only so they no longer call a now-determined
reading unsettled.  Final Arabic, headings, images/crops, layer counts,
and the canonical masters are not changed.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAIRS = (
    (
        ROOT / "al_qorin/REVISI_AL_QORIN_123.md",
        ROOT / "al_qorin/REVISI_AL_QORIN_123_HALAMAN.md",
    ),
    (
        ROOT / "al_qorin/AL_QORIN_123_BERSIH.md",
        ROOT / "al_qorin/AL_QORIN_123_BERSIH_HALAMAN.md",
    ),
)

LABEL_RE = re.compile(r"\[CATATAN PENERJEMAH:[^\]]*\]")
KLAIM_RE = re.compile(r"klaim\s+penulis", re.IGNORECASE)
BATCH_RE = re.compile(r"\bBatch\s+\d+\b", re.IGNORECASE)
TARGET_RES = (KLAIM_RE, BATCH_RE)
MREF_RE = re.compile(r"\bM(\d+)\b")
UNIT_HEADING_RE = re.compile(r"^(##\s+)M(\d{2,3})\s+—\s+(.+)$")
IMAGE_LINE_RE = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")
PREFIX_RE = re.compile(r"^(\s*(?:>\s*)?(?:[-*+]\s+|\d+[.)]\s+)?)(.*)$")
ABBREVIATIONS = {
    "a", "an", "ay", "b", "c", "cet", "cit", "dll", "dr", "dsb", "dst",
    "ed", "hal", "hlm", "ibid", "loc", "mis", "no", "prof", "qs", "s",
    "terj", "ttg", "vol",
}
TERMINALS = ".!?؟"
CLOSERS = "”’\"'»›)]}*"
OPENERS = "“«\"'([{*"


@dataclass
class Stats:
    headings_changed: int = 0
    body_refs_changed: int = 0
    sentences_removed_klaim: int = 0
    sentences_removed_batch: int = 0
    lines_changed: int = 0
    lines_emptied: int = 0
    latin_gap_corrections: int = 0
    removed_sentences: list[str] = field(default_factory=list)

    @property
    def sentences_removed(self) -> int:
        return self.sentences_removed_klaim + self.sentences_removed_batch


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_arabic(char: str) -> bool:
    return bool(char and re.match(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]", char))


def _starts_sentence(char: str) -> bool:
    return bool(char and (char.isupper() or char.isdigit() or char in OPENERS or _is_arabic(char)))


def _preceding_token(text: str, end: int) -> str:
    start = end
    while start > 0 and text[start - 1].isalpha():
        start -= 1
    return text[start:end]


def _is_sentence_boundary(text: str, punct_at: int, after_closers: int) -> bool:
    """Return True when the punctuation at punct_at plausibly ends a sentence."""

    if after_closers >= len(text):
        return True

    punct = text[punct_at]
    following = text[after_closers]

    if punct == ".":
        # Decimal points and alphanumeric strings such as file suffixes.
        if punct_at > 0 and text[punct_at - 1].isdigit() and following.isdigit():
            return False
        token = _preceding_token(text, punct_at)
        if token.lower() in ABBREVIATIONS:
            return False
        if len(token) == 1 and token.isupper():
            return False

    probe = after_closers
    while probe < len(text) and text[probe].isspace():
        probe += 1
    if probe >= len(text):
        return True
    return _starts_sentence(text[probe])


def split_sentences(text: str) -> list[str]:
    """Split one Markdown paragraph line into conservative sentence spans."""

    sentences: list[str] = []
    start = 0
    i = 0
    while i < len(text):
        char = text[i]
        if char not in TERMINALS:
            i += 1
            continue

        # An ellipsis is normally a continuation marker in this corpus.
        if char == "." and text.startswith("...", i):
            i += 3
            continue
        if char == "…":
            i += 1
            continue

        end = i + 1
        # Consume combined terminal punctuation such as ?! before closers.
        while end < len(text) and text[end] in "!?؟":
            end += 1
        while end < len(text) and text[end] in CLOSERS:
            end += 1

        if _is_sentence_boundary(text, i, end):
            sentence = text[start:end].strip()
            if sentence:
                sentences.append(sentence)
            start = end
            while start < len(text) and text[start].isspace():
                start += 1
            i = start
        else:
            i = end

    tail = text[start:].strip()
    if tail:
        sentences.append(tail)
    return sentences


def remove_target_sentences(text: str, stats: Stats) -> str:
    if not any(pattern.search(text) for pattern in TARGET_RES):
        return text

    kept: list[str] = []
    for sentence in split_sentences(text):
        has_klaim = bool(KLAIM_RE.search(sentence))
        has_batch = bool(BATCH_RE.search(sentence))
        if has_klaim or has_batch:
            if has_klaim:
                stats.sentences_removed_klaim += 1
            if has_batch:
                stats.sentences_removed_batch += 1
            stats.removed_sentences.append(sentence)
            continue
        kept.append(sentence)
    return " ".join(kept).strip()


def replace_body_refs(text: str, stats: Stats) -> str:
    def repl(match: re.Match[str]) -> str:
        stats.body_refs_changed += 1
        return f"Halaman {int(match.group(1))}"

    return MREF_RE.sub(repl, text)


def transform_text_span(text: str, stats: Stats) -> str:
    """Apply sentence removal and M-reference renaming outside labels."""

    if not text:
        return text

    pieces = LABEL_RE.split(text)
    labels = LABEL_RE.findall(text)
    if not labels:
        return replace_body_refs(remove_target_sentences(text, stats), stats)

    out: list[str] = []
    for index, piece in enumerate(pieces):
        transformed = replace_body_refs(
            remove_target_sentences(piece.strip(), stats), stats
        )
        if transformed:
            out.append(transformed)
        if index < len(labels):
            out.append(labels[index])
    return " ".join(out).strip()


def transform_line_body(body: str, stats: Stats) -> str:
    prefix_match = PREFIX_RE.match(body)
    if not prefix_match:
        return transform_text_span(body, stats)
    prefix, content = prefix_match.group(1), prefix_match.group(2)
    transformed = transform_text_span(content, stats)
    if not transformed:
        return ""
    return f"{prefix}{transformed}" if prefix else transformed


def split_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    body = stripped[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return re.split(r"(?<!\\)\|", body)


def transform_table_line(line: str, stats: Stats) -> str | None:
    cells = split_table_cells(line)
    if cells is None:
        return None
    transformed = [transform_text_span(cell.strip(), stats) for cell in cells]
    return "| " + " | ".join(transformed) + " |"


def transform_heading(line: str, stats: Stats) -> str | None:
    match = UNIT_HEADING_RE.match(line)
    if not match:
        return None
    number = int(match.group(2))
    title = match.group(3).strip()
    title = re.sub(
        rf"^Halaman\s+0*{number}\s*[,—:-]\s*", "", title, flags=re.IGNORECASE
    )
    title = re.sub(
        rf"\s*,\s*HALAMAN\s+0*{number}\s*$", "", title, flags=re.IGNORECASE
    )
    stats.headings_changed += 1
    return f"## Halaman {number} — {title}"


def transform_markdown(text: str, stats: Stats) -> str:
    out_lines: list[str] = []
    in_fence = False

    for original in text.splitlines():
        line = original.rstrip("\n")
        stripped = line.lstrip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        heading = transform_heading(line, stats)
        if heading is not None:
            changed = heading
        elif IMAGE_LINE_RE.match(line):
            changed = line
        elif line.startswith("#"):
            # Layer/subsection headings are structural.  Only standalone
            # references in top-level/front-matter headings are renamed.
            changed = replace_body_refs(line, stats) if line.startswith("# ") else line
        elif stripped.startswith("|"):
            changed = transform_table_line(line, stats) or line
        else:
            changed = transform_line_body(line, stats)

        if changed != line:
            stats.lines_changed += 1
            if line.strip() and not changed.strip():
                stats.lines_emptied += 1
        out_lines.append(changed)

    result = "\n".join(out_lines)
    if text.endswith("\n"):
        result += "\n"
    return result


@dataclass(frozen=True)
class ExactReplacement:
    label: str
    old: str
    new: str
    editions: tuple[str, ...] = ("research", "clean")
    expected: int = 1


_RESEARCH = "research"
_CLEAN = "clean"
_MARKER = "«…»"
_NOT_COPIED = "«…» [tidak disalin penuh pada sumber kerja]"
_NEXT_SEGMENT = "«…» [bersambung ke segmen berikutnya]"
_PREV_SEGMENT = "«…» [lanjutan dari segmen sebelumnya]"

_H97_LATIN_COMPLETED = (
    "Wa haadzihid da'waa taquulu: al-hamdu lillaahil ladzii khalaqal insaana "
    "min shalshaalin kal fakhkhaari wa khalaqa al-jaanna min maarijin min "
    "naarin. 'Azamtu 'alaikumaa yaa jamjatu yaa bnatal malikil ahmari ainamaa "
    "takuunii fii masyaariqil ardhi wa maghaaribihaa an takuunii musri'ataini "
    "anti wa abuuki thau'an aw karhan fa'tiyaa fattabi'aa thaa'i'aini. "
    "Ajiibii ajiibii yaa jamjatu yaa bnatal malikil ahmari anti wa abuuki "
    "bihaqqil malikil ghaalibi 'alaikumus sayyidi samsamaa-iila 'alaihis "
    "salaamu – wa qul uuhiya ilayya aakhirihaa."
)

_H98_LATIN = (
    "(Baabu istikhdaami najmata bintil malikil ahmari) Wa hiya sarii'atul "
    "ijaabati – wa hiyal latistakhdamahaa 'aliyyu bnul hajjaaji wa kaana "
    "yaf'alul 'ajaa-iba wal gharaa-iba wa yukhriju bihal 'afaariita wa "
    "yumliku bihaa kulla jabbaarin 'aniidin zhaalimin wa kulla maa turiidu. "
    "Fattaqillaaha fii sirrika wa 'alaika 'ahdullaahi an laa taf'ala bihaa "
    "illaa fil halaali wa laa tashrifhaa fii thaa'atillaahi ta'aalaa. "
    "Fa-idzaa aradtal 'amala bihaa fashum lillaahi sab'ata ayyaamin, ibtadi' "
    "min yaumil ahadi haitsu laa yakuunu fiihi riihun wa laa ghuyuumun wa laa "
    "matharun wal qamaru fiz ziyaadati, wa ajlis fii makaanin wahdaka, "
    "waktubil khaatamal aatiya fii yadikasy syimaali bish shandalil ahmari "
    "faqath wa 'azzim 'alaihi bil 'aziimati hattaa ta'tiyaka hamaamatun "
    "baidhaa-u tanzilu 'alaika falmahil khaatama wansharif. Wa fil yaumits "
    "tsaanii ajlis fil mahallil ladzii kunta fiihi waktubil khaatama 'alaa "
    "kaffikasy syimaali wa bakhkhir wa 'azzim bil 'aziimati ilaa an "
    "ta'tiyaka imra-atun dzaatu husnin wa jamaalin wa taquulu laka maa "
    "haajatuka, fa-azjirhaa bid da'wati wa qul lahaa qashdii muraafaqatuka "
    "wa takuunii lii khadiimatan wa mu'iinatan fiimaa atluuhu minka, "
    "fa-innahaa tasytarithu 'alaika syuruuthan wasma' liqawlihaa – fa-innahaa "
    "taquulu marhaban bika wa alfu laa biz zafiiqil muwaafiqi wa tamuddu "
    "laka yadahal yumnaa fatakuunu muhdiran fii yadika jariidatan khadhraa-a "
    "wa tamudduhaa lahaa tumsikuha fatu'aahidahaa 'alaihaa wa ta'khudzu "
    "'alaihal 'ahda wal miitsaaqa wa qul lahaa siirii fii amaanillaahi "
    "fa-innahaa tansharifu falmahil khaatama. (Fa-idzaa aradtal 'amala "
    "bihaa) faktubil khaatama wad da'waa hawlahu wa arba'ahu ma'aka watlud "
    "da'wata fa-innahaa ta'tiyaka hiya wa a'waanuhaa wa taqifu 'alaa "
    "yamiinika wa khuddaamuhaa ma'ahaa, fa-murhaa bimaa turiidu fa-innahaa "
    "tahkumu 'alaa junuudi abiihaa wa tu'thiikal maala wa ta'tii bith "
    "tha'aami wa hiya tuhriqu jamii'al jaanni wa tuhlikuzh zhaalima wa "
    "tajlibu bihaa banaatil muluuki wa tuzhhiru bihal khabaayaa wal kunuuza, "
    "fahtafizh 'alaa haadzihidz dzakhiirah."
)

# Guarded, derived-only repairs for explicit Layer-2 unfinished markers.
# “Fill” entries are taken from the final vocalized Arabic in the same
# unit; “bridge” entries remove only the process marker because the next
# Latin paragraph already continues the phrase; genuine page edges keep a
# plain ellipsis rather than inventing a completion.
LATIN_GAP_REPLACEMENTS: tuple[ExactReplacement, ...] = (
    # Halaman 3 — readings fixed by مَنَّ, بِآيَةِ الْعَجْزِ, and
    # فِي أُصُولِ الْمَوْجُودَاتِ in the final Arabic.
    ExactReplacement(
        "Halaman 3 Latin: manna",
        "Alladzii [من: vokalisasi belum ditetapkan] riwaaqit takwiini",
        "Alladzii manna biriwaaqit takwiini",
    ),
    ExactReplacement(
        "Halaman 3 Latin: bi-aayatil 'ajzi",
        "sulthaanal 'aqli [بية: bacaan belum ditetapkan] al'ajzi",
        "sulthaanal 'aqli bi-aayatil 'ajzi",
    ),
    ExactReplacement(
        "Halaman 3 Latin: ushuulil-mawjuudaati",
        "fii [اصوال: bacaan belum ditetapkan] almawjuudaati",
        "fii ushuulil-mawjuudaati",
    ),
    ExactReplacement(
        "Halaman 3 Terjemahan: manna",
        "yang—kata «man/min» sebelum “serambi penciptaan” belum dapat ditetapkan bacaannya—sesuai dengan perbedaan tingkatan maqam para pencari (al-qāṣidīn).",
        "yang telah menganugerahkan serambi penciptaan sesuai dengan perbedaan tingkatan maqam para pencari (al-qāṣidīn).",
    ),
    ExactReplacement(
        "Halaman 3 Terjemahan: tanda kelemahan (research)",
        "dengan «bīyah» kelemahan [kata penghubung ini belum pasti]",
        "dengan tanda kelemahan",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 3 Terjemahan: tanda kelemahan (clean)",
        "dengan «bīyah» kelemahan",
        "dengan tanda kelemahan",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 3 Terjemahan: prinsip-prinsip (research)",
        "dalam «aṣwāl» segala maujud [kata ini belum ditetapkan]",
        "dalam prinsip-prinsip segala maujud",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 3 Terjemahan: prinsip-prinsip (clean)",
        "dalam «aṣwāl» segala maujud",
        "dalam prinsip-prinsip segala maujud",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 3 note: manna (research)",
        "Huruf من jelas dalam ekstrak, tetapi مِنْ sebagai preposisi atau مَنَّ sebagai fi‘il tidak boleh dipilih hanya agar lancar. Karena itu من dipertahankan tanpa vokalisasi final; bukan kata tidak terbaca.",
        "Arab final membaca مَنَّ sebagai fi‘il (manna, “telah menganugerahkan”), bukan مِنْ sebagai preposisi; vokalisasi itu diikuti pada Latin dan Terjemahan.",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 3 note: manna (clean)",
        "Huruf من jelas dalam teks, tetapi مِنْ sebagai preposisi atau مَنَّ sebagai fi‘il tidak boleh dipilih hanya agar lancar. Karena itu من dipertahankan tanpa vokalisasi final; bukan kata tidak terbaca.",
        "Arab final membaca مَنَّ sebagai fi‘il (manna, “telah menganugerahkan”), bukan مِنْ sebagai preposisi; vokalisasi itu diikuti pada Latin dan Terjemahan.",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 3 note: ushul (research)",
        "اصوال jelas sebagai ekstrak, kandidat أصول/أحوال belum dipilih.",
        "Arab final membaca أُصُولِ (ushūl, “prinsip-prinsip/dasar-dasar”), sehingga kandidat أحوال tidak dipakai.",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 3 note: ushul (clean)",
        "اصوال jelas sebagai teks, kandidat أصول/أحوال belum dipilih.",
        "Arab final membaca أُصُولِ (ushūl, “prinsip-prinsip/dasar-dasar”), sehingga kandidat أحوال tidak dipakai.",
        editions=(_CLEAN,),
    ),
    # Halaman 11 — covered vessel and hand under the cover are explicit in
    # the final Arabic; the paragraph still ends at a genuine page edge.
    ExactReplacement(
        "Halaman 11 Latin: covered vessel (research)",
        f"wa yaj'alu fii inaa'ihi {_NOT_COPIED}, fa-idzaa shallal maghriba raka'as sunnata wa yajlisu mustaqbilal qiblati ba'dat tasmiyati",
        "wa yaj'alu fii aaniyatin mughaththaatin. Fa-idzaa shallal maghriba raka'as sunnata wa yajlisu mustaqbilal qiblati yumuddu yadahu min tahtil ghithaa'i ba'dat tasmiyati",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 11 Latin: covered vessel (clean)",
        f"wa yaj'alu fii inaa'ihi {_MARKER}, fa-idzaa shallal maghriba raka'as sunnata wa yajlisu mustaqbilal qiblati ba'dat tasmiyati",
        "wa yaj'alu fii aaniyatin mughaththaatin. Fa-idzaa shallal maghriba raka'as sunnata wa yajlisu mustaqbilal qiblati yumuddu yadahu min tahtil ghithaa'i ba'dat tasmiyati",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 11 Latin: page edge (research)",
        "wastidaamati" + _NEXT_SEGMENT,
        "wastidaamati...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 11 Latin: page edge (clean)",
        "wastidaamati" + _MARKER,
        "wastidaamati...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 11 note: covered vessel",
        "«فَخْمُهُ» dan kata setelah «في إنائه» tidak terbaca pasti pada cetakan; yang kedua ditandai elipsis, bukan diisi dengan kata karangan.",
        "«فَخْمُهُ» tidak terbaca pasti pada cetakan. Sesudah kata wadah, Arab final membaca «مُغَطَّاةٍ» dan klausa tangan dari bawah penutup, sehingga keduanya kini ditransliterasikan.",
    ),
    # Bridged segment breaks: removing the marker is enough because the
    # following Latin paragraph already carries the continuation.
    ExactReplacement(
        "Halaman 12 Latin: bridged anwaari (research)",
        "fii anwaari" + _NEXT_SEGMENT,
        "fii anwaari",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 12 Latin: bridged anwaari (clean)",
        "fii anwaari" + _MARKER,
        "fii anwaari",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 18 Latin: bridged subhaanahu (research)",
        "subhaanahu" + _NEXT_SEGMENT,
        "subhaanahu",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 18 Latin: bridged subhaanahu (clean)",
        "subhaanahu" + _MARKER,
        "subhaanahu",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 32 Latin: bridged faqad (research)",
        "Man 'arafa nafsahu faqad" + _NEXT_SEGMENT,
        "Man 'arafa nafsahu faqad",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 32 Latin: bridged faqad (clean)",
        "Man 'arafa nafsahu faqad" + _MARKER,
        "Man 'arafa nafsahu faqad",
        editions=(_CLEAN,),
    ),
    # Genuine page-edge breaks: keep the break visible without the
    # editorial process bracket.
    ExactReplacement(
        "Halaman 12 Latin: page edge fathan (research)",
        "tsumma fathan" + _NEXT_SEGMENT,
        "tsumma fathan...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 12 Latin: page edge fathan (clean)",
        "tsumma fathan" + _MARKER,
        "tsumma fathan...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 14 Latin: page edge fii (research)",
        "maa yaridu 'alaihi fii" + _NEXT_SEGMENT,
        "maa yaridu 'alaihi fii...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 14 Latin: page edge fii (clean)",
        "maa yaridu 'alaihi fii" + _MARKER,
        "maa yaridu 'alaihi fii...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 16 Latin: page edge ladzii (research)",
        "wa huwal ladzii" + _NEXT_SEGMENT,
        "wa huwal ladzii...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 16 Latin: page edge ladzii (clean)",
        "wa huwal ladzii" + _MARKER,
        "wa huwal ladzii...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 23 Latin: page edge sunnati (research)",
        "bizhaahiris sunnati" + _NEXT_SEGMENT,
        "bizhaahiris sunnati...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 23 Latin: page edge sunnati (clean)",
        "bizhaahiris sunnati" + _MARKER,
        "bizhaahiris sunnati...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 26 Latin: page edge kullu (research)",
        "wal qalbu haamilul qur'aani wa kullu" + _NEXT_SEGMENT,
        "wal qalbu haamilul qur'aani wa kullu...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 26 Latin: page edge kullu (clean)",
        "wal qalbu haamilul qur'aani wa kullu" + _MARKER,
        "wal qalbu haamilul qur'aani wa kullu...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 27 Latin: page edge qantharatuhu (research)",
        "wa qantharatuhu" + _NEXT_SEGMENT,
        "wa qantharatuhu...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 27 Latin: page edge qantharatuhu (clean)",
        "wa qantharatuhu" + _MARKER,
        "wa qantharatuhu...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 35 Latin: page edge jismaaniyyata (research)",
        "'ilalal jismaaniyyata" + _NEXT_SEGMENT,
        "'ilalal jismaaniyyata...",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 35 Latin: page edge jismaaniyyata (clean)",
        "'ilalal jismaaniyyata" + _MARKER,
        "'ilalal jismaaniyyata...",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 112 Latin: opening continuation (research)",
        _PREV_SEGMENT + " wath thahaari",
        "... wath thahaari",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 112 Latin: opening continuation (clean)",
        _MARKER + " wath thahaari",
        "... wath thahaari",
        editions=(_CLEAN,),
    ),
    # Halaman 60–63 — the transliterated list already follows each title,
    # so the “not copied in full” residue is removable.  Halaman 61 also
    # restores بِمَقْلُوبِهِ as a single moon-names heading.
    ExactReplacement(
        "Halaman 60 Latin: al-ayyaamu (research)",
        f"«Al-ayyaamu» {_NOT_COPIED} khalaqal",
        "«Al-ayyaamu» khalaqal",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 60 Latin: al-ayyaamu (clean)",
        f"«Al-ayyaamu» {_MARKER} khalaqal",
        "«Al-ayyaamu» khalaqal",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 60 Latin: al-abraaju (research)",
        f"«Al-abraaju» {_NOT_COPIED} 1 -",
        "«Al-abraaju» 1 -",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 60 Latin: al-abraaju (clean)",
        f"«Al-abraaju» {_MARKER} 1 -",
        "«Al-abraaju» 1 -",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 61 Latin: ad-daraari (research)",
        f"«Asmaa-ud daraaris sab'ati» {_NOT_COPIED} 1 -",
        "«Asmaa-ud daraaris sab'ati» 1 -",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 61 Latin: ad-daraari (clean)",
        f"«Asmaa-ud daraaris sab'ati» {_MARKER} 1 -",
        "«Asmaa-ud daraaris sab'ati» 1 -",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 61 Latin: moon names reversed (research)",
        f"Asmaa-ul qamari {_NOT_COPIED} asmaa-ul qamari maqluubuhu.",
        "Asmaa-ul qamari bi-maqluubihii.",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 61 Latin: moon names reversed (clean)",
        f"Asmaa-ul qamari {_MARKER} asmaa-ul qamari maqluubuhu.",
        "Asmaa-ul qamari bi-maqluubihii.",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 62 Latin: as-salaathiin (research)",
        f"«Asmaa-us salaathiinil malaa-ikati» {_NOT_COPIED} 1 -",
        "«Asmaa-us salaathiinil malaa-ikati» 1 -",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 62 Latin: as-salaathiin (clean)",
        f"«Asmaa-us salaathiinil malaa-ikati» {_MARKER} 1 -",
        "«Asmaa-us salaathiinil malaa-ikati» 1 -",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 62 Latin: al-muluuk (research)",
        f"«Asmaa-ul muluukis sab'ati» {_NOT_COPIED} 1 -",
        "«Asmaa-ul muluukis sab'ati» 1 -",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 62 Latin: al-muluuk (clean)",
        f"«Asmaa-ul muluukis sab'ati» {_MARKER} 1 -",
        "«Asmaa-ul muluukis sab'ati» 1 -",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 63 Latin: ar-ru-uus (research)",
        f"«Asmaa-ur ru-uusil arba'ati» {_NOT_COPIED} 1 -",
        "«Asmaa-ur ru-uusil arba'ati» 1 -",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 63 Latin: ar-ru-uus (clean)",
        f"«Asmaa-ur ru-uusil arba'ati» {_MARKER} 1 -",
        "«Asmaa-ur ru-uusil arba'ati» 1 -",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 63 Latin: ar-ruuhaniyyah (research)",
        f"«Asmaa-ur ruuhaniyyatis sab'ati» {_NOT_COPIED} 1 -",
        "«Asmaa-ur ruuhaniyyatis sab'ati» 1 -",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 63 Latin: ar-ruuhaniyyah (clean)",
        f"«Asmaa-ur ruuhaniyyatis sab'ati» {_MARKER} 1 -",
        "«Asmaa-ur ruuhaniyyatis sab'ati» 1 -",
        editions=(_CLEAN,),
    ),
    # Research Halaman 71 — the figure descriptor in Layer 2 should not
    # leave an Arabic glyph where a Latin letter name is intended.
    ExactReplacement(
        "Halaman 71 Latin: letter thaa (research)",
        "dan huruf «ط» pada keenam sisinya",
        "dan huruf thaa pada keenam sisinya",
        editions=(_RESEARCH,),
    ),
    # Halaman 74 — reproduce the exact 13× digit-9 and 13× يه sequence
    # instead of summarizing it as three repetitions.
    ExactReplacement(
        "Halaman 74 Latin: nine/yah sequence (research)",
        "(sembilan" + _NOT_COPIED + ") yah yah yah (berulang).",
        "9999999999999 yah yah yah yah yah yah yah yah yah yah yah yah yah.",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 74 Latin: nine/yah sequence (clean)",
        "(sembilan" + _MARKER + ") yah yah yah (berulang).",
        "9999999999999 yah yah yah yah yah yah yah yah yah yah yah yah yah.",
        editions=(_CLEAN,),
    ),
    # Halaman 96 — the markers separate already-transliterated verse
    # parts; a slash preserves that segmentation without implying a lacuna.
    ExactReplacement(
        "Halaman 96 Latin: verse separator 1 (research)",
        f"shahbii {_NEXT_SEGMENT} min",
        "shahbii / min",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 96 Latin: verse separator 1 (clean)",
        f"shahbii {_MARKER} min",
        "shahbii / min",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 96 Latin: verse separator 2 (research)",
        f"qubbi {_NEXT_SEGMENT} hattaa",
        "qubbi / hattaa",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 96 Latin: verse separator 2 (clean)",
        f"qubbi {_MARKER} hattaa",
        "qubbi / hattaa",
        editions=(_CLEAN,),
    ),
    # Halaman 97 — the first marker interrupts an already-continued
    # paragraph.  The da'wa is completed from this unit's final Arabic
    # (including أَجِيبِي أَجِيبِي and إِلَيَّ آخِرِهَا); the older
    # cross-page Latin at the start of Halaman 98 is deliberately not
    # copied because it carries different legacy readings.
    ExactReplacement(
        "Halaman 97 Latin: remove internal marker (research)",
        f"sarii'atul ijaabati {_NOT_COPIED} wa huwa",
        "sarii'atul ijaabati wa huwa",
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 97 Latin: remove internal marker (clean)",
        f"sarii'atul ijaabati {_MARKER} wa huwa",
        "sarii'atul ijaabati wa huwa",
        editions=(_CLEAN,),
    ),
    ExactReplacement(
        "Halaman 97 Latin: complete da'wa (research)",
        f"Wa haadzihid da'waa taquulu: al-hamdu lillaahil ladzii khalaqal insaana min shalshaalin kal fakhkhaari wa khalaqa {_NOT_COPIED} (bersambung ke halaman 98)",
        _H97_LATIN_COMPLETED,
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 97 Latin: complete da'wa (clean)",
        f"Wa haadzihid da'waa taquulu: al-hamdu lillaahil ladzii khalaqal insaana min shalshaalin kal fakhkhaari wa khalaqa {_MARKER}",
        _H97_LATIN_COMPLETED,
        editions=(_CLEAN,),
    ),
    # Halaman 98 — Layer 2 held unfinished Indonesian prose rather than
    # transliteration.  Replace that prose portion with transliteration of
    # the final Arabic heading/paragraph (Najmah); research keeps its
    # bracketed table descriptor.  Layer 3 already translates the passage.
    ExactReplacement(
        "Halaman 98 Latin: transliterate Najmah passage (research)",
        "[Jadwal angka dan huruf dalam tiga kolom dan empat baris — rujuk gambar halaman 98; rajah tidak digambar ulang.] (Bab penggunaan Jamjah putri Raja Merah.) Dan ia cepat menjawab; dialah yang dipakai oleh ‘Ali bin al-Hajjaj, dan ia melakukan hal-hal ajaib dan aneh, mengeluarkan ‘ifrit dengan perantaranya, dan membinasakan setiap orang yang congkak, keras kepala, dan zalim dengan perantaranya, dan segala yang engkau kehendaki. Maka bertakwalah kepada Allah dalam rahasiamu; atasmu perjanjian Allah bahwa engkau tidak menggunakannya kecuali dalam (perkara) halal, dan jangan mengarahkannya (kecuali) dalam ketaatan kepada Allah—Mahatinggi. Maka apabila engkau hendak mengamalkannya, berpuasalah untuknya tujuh hari, mulai dari hari Ahad, ketika tidak ada angin, tidak ada awan, tidak ada hujan, dan bulan sedang bertambah; dan duduklah di «…» [bersambung ke segmen berikutnya]",
        "[Jadwal angka dan huruf dalam tiga kolom dan empat baris — rujuk gambar halaman 98; rajah tidak digambar ulang.] " + _H98_LATIN,
        editions=(_RESEARCH,),
    ),
    ExactReplacement(
        "Halaman 98 Latin: transliterate Najmah passage (clean)",
        "(Bab penggunaan Jamjah putri Raja Merah.) Dan ia cepat menjawab; dialah yang dipakai oleh ‘Ali bin al-Hajjaj, dan ia melakukan hal-hal ajaib dan aneh, mengeluarkan ‘ifrit dengan perantaranya, dan membinasakan setiap orang yang congkak, keras kepala, dan zalim dengan perantaranya, dan segala yang engkau kehendaki. Maka bertakwalah kepada Allah dalam rahasiamu; atasmu perjanjian Allah bahwa engkau tidak menggunakannya kecuali dalam (perkara) halal, dan jangan mengarahkannya (kecuali) dalam ketaatan kepada Allah—Mahatinggi. Maka apabila engkau hendak mengamalkannya, berpuasalah untuknya tujuh hari, mulai dari hari Ahad, ketika tidak ada angin, tidak ada awan, tidak ada hujan, dan bulan sedang bertambah; dan duduklah di «…»",
        _H98_LATIN,
        editions=(_CLEAN,),
    ),
)

_LAYER2_GAP_MARKERS = (
    _MARKER,
    "[tidak disalin penuh pada sumber kerja]",
    "[bersambung ke segmen berikutnya]",
    "[lanjutan dari segmen sebelumnya]",
    "vokalisasi belum ditetapkan",
    "bacaan belum ditetapkan",
    "(bersambung ke halaman 98)",
    "huruf «ط»",
)


def apply_latin_gap_corrections(text: str, edition: str, stats: Stats) -> str:
    for replacement in LATIN_GAP_REPLACEMENTS:
        if edition not in replacement.editions:
            continue
        found = text.count(replacement.old)
        if found != replacement.expected:
            raise AssertionError(
                f"{replacement.label}: expected {replacement.expected} exact "
                f"occurrence(s) in {edition}, found {found}"
            )
        text = text.replace(replacement.old, replacement.new)
        stats.latin_gap_corrections += found
    return text


def layer2_gap_marker_hits(text: str) -> list[str]:
    hits: list[str] = []
    layer2_re = re.compile(
        r"^### 2\. Latin\s*$(.*?)(?=^### |^## |\Z)",
        flags=re.M | re.S,
    )
    for match in layer2_re.finditer(text):
        section = match.group(1)
        for marker in _LAYER2_GAP_MARKERS:
            hits.extend([marker] * section.count(marker))
    return hits


def structural_counts(text: str) -> dict[str, int]:
    return {
        "unit_or_page_headings": len(re.findall(r"^##\s+", text, flags=re.M)),
        "layer_headings": len(re.findall(r"^###\s+", text, flags=re.M)),
        "subsection_headings": len(re.findall(r"^####\s+", text, flags=re.M)),
        "images": len(re.findall(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$", text, flags=re.M)),
        "translator_labels": len(LABEL_RE.findall(text)),
        "remaining_m_refs": len(MREF_RE.findall(text)),
        "remaining_klaim_penulis": len(KLAIM_RE.findall(text)),
        "remaining_batch_numbered": len(BATCH_RE.findall(text)),
    }


def build_one(source: Path, output: Path) -> dict[str, object]:
    source = source.resolve()
    output = output.resolve()
    if source == output:
        raise ValueError("output must not overwrite its input")

    source_bytes = source.read_bytes()
    source_text = source_bytes.decode("utf-8")
    before = structural_counts(source_text)
    stats = Stats()
    output_text = transform_markdown(source_text, stats)
    edition = "clean" if "BERSIH" in source.name else "research"
    output_text = apply_latin_gap_corrections(output_text, edition, stats)
    remaining_gap_markers = layer2_gap_marker_hits(output_text)
    if remaining_gap_markers:
        raise AssertionError(
            "explicit Layer-2 gap markers remain after derived Latin "
            f"corrections: {remaining_gap_markers!r}"
        )
    after = structural_counts(output_text)

    invariant_keys = (
        "unit_or_page_headings",
        "layer_headings",
        "subsection_headings",
        "images",
        "translator_labels",
    )
    for key in invariant_keys:
        if before[key] != after[key]:
            raise AssertionError(f"structural count changed for {key}: {before[key]} -> {after[key]}")
    if after["remaining_m_refs"] != 0:
        raise AssertionError(f"standalone M references remain: {after['remaining_m_refs']}")
    if after["remaining_klaim_penulis"] != 0:
        raise AssertionError(
            f"'klaim penulis' remains after sentence removal: {after['remaining_klaim_penulis']}"
        )
    if after["remaining_batch_numbered"] != 0:
        raise AssertionError(
            f"numbered Batch references remain: {after['remaining_batch_numbered']}"
        )
    if stats.headings_changed != 122:
        raise AssertionError(f"expected 122 transformed page headings, got {stats.headings_changed}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output_bytes = output_text.encode("utf-8")
    output.write_bytes(output_bytes)

    return {
        "source": str(source),
        "output": str(output),
        "source_sha256": sha256_bytes(source_bytes),
        "output_sha256": sha256_bytes(output_bytes),
        "headings_changed": stats.headings_changed,
        "body_refs_changed": stats.body_refs_changed,
        "sentences_removed_klaim": stats.sentences_removed_klaim,
        "sentences_removed_batch": stats.sentences_removed_batch,
        "sentences_removed_total": stats.sentences_removed,
        "lines_changed": stats.lines_changed,
        "lines_emptied": stats.lines_emptied,
        "latin_gap_corrections": stats.latin_gap_corrections,
        "remaining_layer2_gap_markers": len(remaining_gap_markers),
        "before": before,
        "after": after,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="single Markdown input; requires --output")
    parser.add_argument("--output", type=Path, help="single derived Markdown output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if bool(args.input) ^ bool(args.output):
        raise SystemExit("--input and --output must be supplied together")

    pairs = ((args.input, args.output),) if args.input else DEFAULT_PAIRS
    for source, output in pairs:
        if source is None or output is None:
            continue
        result = build_one(source, output)
        print(
            "derived "
            f"source={result['source']} output={result['output']} "
            f"headings={result['headings_changed']} body_refs={result['body_refs_changed']} "
            f"removed_klaim_sentences={result['sentences_removed_klaim']} "
            f"removed_batch_sentences={result['sentences_removed_batch']} "
            f"lines_changed={result['lines_changed']} lines_emptied={result['lines_emptied']} "
            f"latin_gap_corrections={result['latin_gap_corrections']} "
            f"sha256={result['output_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
