#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the clean Al-Qorin reading edition from the user's Arab/Latin files.

Layers rendered per unit:
  1. Arab          -- user's archived Arabic TXT
  2. Latin         -- user's archived Latin TXT
  3. Terjemahan    -- current integrated Indonesian layer, presentation-cleaned
  4. Syarah        -- substantive reading/lexical notes, presentation-cleaned;
                      the user's centered crop is inserted here when present
  5. Khususiyah dan Tatacara Praktik -- only for units whose integrated data
                      contains a source practice with specified
                      waktu/media/bukhur, plus three source-checked manual
                      inclusions (M04, M38, M122)

The clean Markdown intentionally has no build/status front matter.  Work
process bracket markers are removed only in this presentation edition; the
archived user files and the research master remain byte-identical.
Outputs:
  al_qorin/AL_QORIN_123_BERSIH.md
  al_qorin/work/clean_user_edition_units.json (ignored work data)
"""
import copy
import json
import re
from pathlib import Path

from al_qorin_parse_user_arab_latin import ORDER, load_user_arab_latin
from al_qorin_parse_user_arab_replacement_h62 import (
    load_user_arab_replacement_h62,
)
from al_qorin_parse_user_arab_replacement_h63_122 import (
    load_user_arab_replacement_h63_122,
)
from al_qorin_parse_user_arab_replacement_h63_revised import (
    load_user_arab_replacement_h63_revised,
)
from al_qorin_parse_user_arab_replacement_h66_69_revised import (
    load_user_arab_replacement_h66_69_revised,
)
from al_qorin_parse_user_arab_replacement_h82_83_97_98_revised import (
    load_user_arab_replacement_h82_83_97_98_revised,
)
from al_qorin_parse_user_arab_replacement_h11_revised import (
    load_user_arab_replacement_h11_revised,
)
from al_qorin_parse_user_arab_replacement_h70_74_revised import (
    load_user_arab_replacement_h70_74_revised,
)
from al_qorin_parse_user_arab_replacement_h76_revised import (
    load_user_arab_replacement_h76_revised,
)
from al_qorin_parse_user_arab_replacement_h78_80_revised import (
    load_user_arab_replacement_h78_80_revised,
)
from al_qorin_wafaq_markers import WAFAQ_MARKER

ROOT = Path(__file__).resolve().parents[1]
ALQ = ROOT / "al_qorin"
WORK = ALQ / "work"
OUT_MD = ALQ / "AL_QORIN_123_BERSIH.md"
OUT_JSON = WORK / "clean_user_edition_units.json"
UNSPECIFIED = "tidak disebutkan dalam sumber unit ini"
MANUAL_KHUSUSIYAH = {"M04", "M38", "M122"}
EXPECTED_CROPS = [49, 58, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78,
                  82, 83, 84, 85, 86, 98, 109, 116, 120, 121]


def normalize_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" +([,.;:!?])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()


def strip_work_markers(text):
    """Remove only explicit work-process segmentation markers."""
    text = re.sub(
        r"\s*\[(?:tidak disalin penuh|bersambung|lanjutan dari segmen|baris tidak lengkap)[^\]]*\]",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\s*\((?:bersambung ke halaman|lanjutan dari segmen)[^)]*\)",
        "",
        text,
        flags=re.I,
    )
    return normalize_spaces(text)


def strip_translation_brackets(text):
    def repl(match):
        inside = match.group(1).strip()
        low = inside.lower()
        if inside.startswith("CATATAN PENERJEMAH"):
            return match.group(0)
        keywords = (
            "belum", "sumber", "segmen", "hubungan", "susunan", "makna kata",
            "dipertahankan", "tidak dapat", "penyunting", "pindaian", "ekstrak",
        )
        return "" if any(k in low for k in keywords) else match.group(0)

    text = re.sub(r"\[([^\]]{1,220})\]", repl, text)
    return normalize_spaces(text)


def clean_latin(text):
    """Remove Indonesian image-reference brackets from the Latin layer.

    The centered user crop is rendered in Syarah, so bracketed directions
    such as "lihat pindaian halaman ..." are presentation apparatus rather
    than transliteration.
    """
    text = strip_work_markers(text)
    text = re.sub(
        r"\s*\[[^\]]*(?:pindaian|gambar|rajah|jadwal angka|dua tabel|baris angka)[^\]]*\]\s*",
        " ",
        text,
        flags=re.I,
    )
    return normalize_spaces(text)


def clean_translation(text):
    text = strip_work_markers(text)
    text = re.sub(
        r"\s*\[[^\]]*(?:digambar ulang|rajah tidak digambar ulang|rujuk gambar|lihat gambar|gambar halaman|tercetak rajah)[^\]]*\]\s*",
        " ",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"^\[[^\]]*(?:rajah|gambar|tabel|angka dan rumus|tercetak)[^\]]*\]\s*",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"\s*Saya tidak menggambar ulang.*$", "", text, flags=re.I)
    return strip_translation_brackets(text)


def clean_indonesian_prose(text):
    text = strip_work_markers(text)
    text = re.sub(r"\s*\[(?:Dinisbatkan|dinisbatkan)[^\]]*\]\s*", " ", text)
    replacements = [
        (r"\bmenurut saya\b", "menurut bacaan ini"),
        (r"\bbelum saya verifikasi\b", "belum terverifikasi"),
        (r"\btidak saya verifikasi\b", "tidak terverifikasi"),
        (r"\btidak saya karang\b", "tidak dikarang"),
        (r"\btidak saya reproduksi\b", "tidak direproduksi"),
        (r"\bsaya tidak memberi\b", "tidak diberi"),
        (r"\bdapat saya periksa\b", "dapat diperiksa"),
        (r"\btidak anjurkan\b", "tidak dianjurkan"),
        (r"\btidak hapus\b", "tidak dihapus"),
        (r"\btidak menambal\b", "tidak ditambal"),
        (r"\bbiarkan\b", "dibiarkan"),
        (r"\btandai\b", "ditandai"),
        (r"\bnyatakan agar\b", "dinyatakan agar"),
        (r"\btidak saya\b", "tidak"),
        (r"\bbelum saya\b", "belum"),
        (r"\bdapat saya\b", "dapat"),
        (r"\bsaya tidak\b", "tidak"),
        (r"\bsaya baca\b", "dibaca"),
        (r"\bsaya tulis\b", "ditulis"),
        (r"\bsaya kutip\b", "dikutip"),
        (r"\bsaya pertahankan\b", "dipertahankan"),
        (r"\bsaya mencatat\b", "tercatat"),
        (r"\bsaya mencatat dan menerjemahkan\b", "tercatat dan diterjemahkan"),
        (r"\bsaya\b", ""),
        (r"\bekstrak\b", "teks"),
        (r"\bpindaian\b", "cetakan"),
        (r"\bdraf\b", "teks"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text, flags=re.I)
    # Removing a bare first-person pronoun leaves double spaces; normalize
    # now so the passive-repair patterns below see ordinary word sequences.
    text = normalize_spaces(text)
    # A second narrow pass repairs passive forms created when an initial
    # first-person pronoun was removed (for example "saya tidak hapus").
    text = re.sub(r"\btidak anjurkan\b", "tidak dianjurkan", text, flags=re.I)
    text = re.sub(r"\btidak hapus\b", "tidak dihapus", text, flags=re.I)
    text = re.sub(r"\btidak menambal\b", "tidak ditambal", text, flags=re.I)
    global_passives = {
        "kenali": "dikenali",
        "pastikan": "dipastikan",
        "pahami": "dipahami",
        "temukan": "ditemukan",
        "jadikan": "dijadikan",
        "ganti": "diganti",
        "koreksi": "dikoreksi",
        "pilih": "dipilih",
        "gambar ulang": "digambar ulang",
        "hitung ulang": "dihitung ulang",
        "terjemahkan": "diterjemahkan",
        "perbaiki": "diperbaiki",
    }
    for active, passive in global_passives.items():
        text = re.sub(rf"\btidak {re.escape(active)}\b", f"tidak {passive}", text, flags=re.I)
        text = re.sub(rf"\bdapat {re.escape(active)}\b", f"dapat {passive}", text, flags=re.I)
    text = re.sub(r"\byang kenali\b", "yang dikenali", text, flags=re.I)
    text = re.sub(r"\bbisa periksa\b", "dapat diperiksa", text, flags=re.I)
    text = re.sub(r"\bterjemahannya beri tanda\b", "terjemahannya diberi tanda", text, flags=re.I)

    # Only convert these active verbs where the syntax shows a subjectless
    # editorial clause (start, punctuation, or "dan"); this preserves
    # legitimate subjects such as "penulis tidak menyebut".
    contextual_passives = {
        "menambahkannya": "ditambahkan",
        "menambahkan": "ditambahkan",
        "menambah": "ditambah",
        "memverifikasinya": "diverifikasi",
        "memverifikasi": "diverifikasi",
        "mengubah": "diubah",
        "mengoreksi": "dikoreksi",
        "menyarankan": "disarankan",
        "menghitung": "dihitung",
        "menguji": "diuji",
        "mengiyakan": "diiyakan",
        "mengikutinya": "diikuti",
        "mengarang": "dikarang",
        "membenarkan": "dibenarkan",
        "mengesahkannya": "disahkan",
        "memaksakan": "dipaksakan",
        "menafsirkannya": "ditafsirkan",
        "menafsirkan": "ditafsirkan",
        "menghapus": "dihapus",
        "memutuskan": "diputuskan",
        "mengklaim": "diklaim",
    }
    verb_pattern = "|".join(re.escape(v) for v in sorted(contextual_passives, key=len, reverse=True))

    def _contextual_not(match):
        prefix, negation, verb = match.groups()
        passive = contextual_passives[verb.lower()]
        negation = "Tidak" if negation[:1].isupper() else "tidak"
        return f"{prefix}{negation} {passive}"

    text = re.sub(
        rf"(^|[;:,.—]\s*|\bdan\s+)(tidak)\s+({verb_pattern})\b",
        _contextual_not,
        text,
        flags=re.I | re.M,
    )

    clause_passives = {
        "menuliskannya": "ditulis",
        "terjemahkan": "diterjemahkan",
        "menjelaskannya": "dijelaskan",
        "mencatatnya": "dicatat",
        "menandainya": "ditandai",
        "menulis": "ditulis",
        "mencatat": "dicatat",
        "menandai": "ditandai",
        "menyatakan": "dinyatakan",
        "menyatakannya": "dinyatakan",
        "catat": "dicatat",
        "beri": "diberi",
        "salin": "disalin",
        "ikuti": "diikuti",
        "ambil": "diambil",
        "sebutkan": "disebutkan",
    }
    clause_pattern = "|".join(re.escape(v) for v in sorted(clause_passives, key=len, reverse=True))

    def _clause_passive(match):
        prefix, only, verb = match.groups()
        passive = clause_passives[verb.lower()]
        only = only or ""
        if prefix == "" or prefix.rstrip().endswith("."):
            if only:
                only = only[:1].upper() + only[1:]
            else:
                passive = passive[:1].upper() + passive[1:]
        return f"{prefix}{only}{passive}"

    text = re.sub(
        rf"(^|[.;:,—]\s*|\bdan\s+)(hanya\s+)?({clause_pattern})\b",
        _clause_passive,
        text,
        flags=re.I | re.M,
    )
    exact_repairs = [
        (r"\bnyatakan terbuka\b", "dinyatakan terbuka"),
        (r"\bitu nyatakan, tidak ratakan\b", "itu dinyatakan dan tidak diratakan"),
        (r"\btanpa menambal\b", "tanpa ditambal"),
        (r"\btidak menambalnya\b", "tidak ditambal"),
        (r"Tidak menyambung sendiri; sambungannya ada di unit M117\.",
         "Sambungannya ada di unit berikutnya (M117)."),
        (r"\bberi tanda kutip ganda\b", "diberi tanda kutip ganda"),
        (r"» catat sebagai\b", "» dicatat sebagai"),
        (r"\bbukan menyembunyikannya\b", "bukan disembunyikan"),
        (r"— perhatikan bahwa penulis menulis\b", "; penulis menulis"),
        (r"Halaman ini \{tanpa nomor halaman\} yang terbaca pada cetakan;",
         "Nomor halaman tidak terbaca pada cetakan;"),
    ]
    for pattern, repl in exact_repairs:
        text = re.sub(pattern, repl, text, flags=re.I)
    text = re.sub(r"\s+dalam pekerjaan ini\b", "", text, flags=re.I)
    text = re.sub(r";\s*itu di luar tugas penerjemahan\b", "", text, flags=re.I)
    text = re.sub(
        r";\s*Arab, Latin, dan Terjemahan kanonis tidak diganti dalam integrasi "
        r"selektif ini, dan ejaan nama-nama non-Arab dari paket unggahan tidak diadopsi",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r";\s*dalam integrasi selektif ini Lapis 1[–-]3 tidak diganti, sehingga "
        r"perbedaan tersebut hanya dinyatakan sebagai selisih bacaan",
        "; perbedaan itu dicatat sebagai selisih bacaan",
        text,
        flags=re.I,
    )
    text = text.replace("teks kanonis", "teks Arab di atas")
    text = text.replace("klausa Arab kanonis", "klausa Arab di atas")
    text = text.replace("Metode kanonis", "uraian sumber")
    text = re.sub(r"(?<=\. )([a-z])", lambda m: m.group(1).upper(), text)
    text = re.sub(r"\s*—?\s*lihat Catatan penyunting\b", "", text, flags=re.I)
    text = text.replace("Catatan penyunting", "Keterangan lafaz")
    return normalize_spaces(text)


DROP_SYARAH_MARKERS = (
    "harakat dan tanda baca",
    "tidak digambar ulang",
    "digambar ulang di sini",
    "wajib diambil dari cetakan",
    "untuk penerbitan",
    "bukan pengesahan",
    "tidak dianjurkan dipakai",
    "dicatat tidak dianjurkan",
    "tidak ada halaman berikutnya dalam cetakan",
    "bukan mengamalkan",
    "sebagai anjuran",
    "sedang diedit",
    "teks dicatat karena",
    "catatan editorial",
)


def make_syarah(unit):
    out = []
    for note in unit.get("catatan_penyunting") or []:
        cleaned = clean_indonesian_prose(note)
        low = cleaned.lower()
        if len(cleaned) < 25 or any(marker in low for marker in DROP_SYARAH_MARKERS):
            continue
        if cleaned and cleaned[0].islower():
            cleaned = cleaned[0].upper() + cleaned[1:]
        out.append(cleaned)
    if out:
        return out
    if unit["unit_id"] == "SAMPUL":
        return [
            "Sampul memuat judul kitab, nama pengarang, keterangan keanggotaan, "
            "kedudukan lembaga, dan nama penerbit."
        ]
    topic = unit["heading"].split("—", 1)[-1].strip()
    topic = re.sub(r"^Halaman \d+,\s*", "", topic)
    return [f"Bagian ini membahas {topic[:1].lower() + topic[1:]}."]


def clean_metode_paragraph(text):
    low = text.lower()
    if "tidak ada petunjuk praktik" in low or "**tidak ada praktik**" in low:
        return ""
    if low.startswith("halaman ini tidak memuat wafaq") or low.startswith("halaman ini memuat wafaq"):
        return ""
    text = re.sub(
        r"^Praktik(?: yang disebut sumber| dari sumber)?(?:\s*\([^)]*\))?\s*:\s*",
        "",
        text,
    )
    text = re.sub(
        r"^Praktik(?: yang disebut sumber| dari sumber)?(?:\s*\([^)]*\))?\s+",
        "",
        text,
    )
    if re.match(r"^(Baris|Sisi|Bagian dalam|Lambang|Bentuk|Petak|Sel)\b", text):
        return ""
    text = clean_indonesian_prose(text)
    # The user's crop supplies the graphic itself in Syarah.  Cut a Metode
    # paragraph at the point where it stops describing practice and starts
    # giving reproduction/layout apparatus.
    graphic_markers = (
        "pada akhir halaman tercetak gambar",
        "wafaq ini tidak digambar ulang",
        "tidak digambar ulang",
        "tidak direproduksi",
        "hanya boleh diambil dari gambar",
        "wajib dipakai bila",
        "catatan editorial",
    )
    low = text.lower()
    cuts = [low.find(marker) for marker in graphic_markers if marker in low]
    if cuts:
        cut = min(cuts)
        semicolon = text.rfind("; ", 0, cut)
        sentence = text.rfind(". ", 0, cut)
        cut = max(semicolon, sentence)
        text = text[:cut].rstrip(" ;") if cut > 0 else ""
        if text and not text.endswith((".", "!", "?")):
            text += "."
    low = text.lower()
    if any(marker in low for marker in DROP_SYARAH_MARKERS):
        return ""
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def clean_khususiyah_field(value):
    value = re.sub(r"\s*\([^)]*\bcrop\b[^)]*\)", "", value, flags=re.I)
    value = re.sub(
        r"\s*\([^)]*(?:Terjemahan kanonis|lihat Catatan|Catatan penyunting)[^)]*\)",
        "",
        value,
        flags=re.I,
    )
    value = re.sub(r";[^;]*Catatan penyunting.*$", "", value, flags=re.I)
    value = clean_indonesian_prose(value)
    value = re.sub(r"\bcrop asli \d+\.jpg\b", "gambar wafaq halaman ini", value, flags=re.I)
    if value and value[0].islower():
        value = value[0].upper() + value[1:]
    return value


def make_khususiyah(unit):
    specific = {
        key: clean_khususiyah_field(value)
        for key, value in unit["khususiyah"].items()
        if value != UNSPECIFIED
    }
    include = bool(specific) or unit["unit_id"] in MANUAL_KHUSUSIYAH
    if not include:
        return []
    if unit["unit_id"] == "M122":
        return [
            "Salat dua rakaat, berselawat kepada Nabi sepuluh kali, kemudian "
            "membaca al-Fatihah untuk Syekh Muhammad Sibami."
        ]
    if unit["unit_id"] == "M04":
        return [
            "Membaca al-Fatihah yang dihadiahkan kepada Nabi Muhammad, "
            "keluarga beliau, dan pengarang sebelum memulai."
        ]
    if unit["unit_id"] == "M38":
        return [
            "Selama riyadhah, pelaku diperingatkan agar tidak berhenti atau "
            "terhijab oleh tanda dan cahaya yang tampak—putih, hijau, dan "
            "merah—serta tidak menyibukkan pikiran dengan menoleh kepadanya."
        ]
    out = []
    for paragraph in unit.get("metode") or []:
        cleaned = clean_metode_paragraph(paragraph)
        if cleaned:
            out.append(cleaned)
    labels = {"waktu": "Waktu", "media": "Media", "bukhur": "Bukhur"}
    for key in ("waktu", "media", "bukhur"):
        if key in specific and specific[key]:
            out.append(f"**{labels[key]}:** {specific[key]}")
    return out


def main():
    integrated = {
        u["unit_id"]: u
        for u in json.loads((WORK / "integrated_units.json").read_text(encoding="utf-8"))
    }
    if list(integrated) != ORDER:
        raise SystemExit("integrated unit order is not SAMPUL + M01-M122")
    user = load_user_arab_latin(ROOT)
    arab_replacement = {
        **load_user_arab_replacement_h62(ROOT)["units"],
        **load_user_arab_replacement_h63_122(ROOT)["units"],
    }
    # The user's later one-page revision supersedes only M63.
    arab_replacement["M63"] = load_user_arab_replacement_h63_revised(ROOT)[
        "units"
    ]["M63"]
    # A later four-page revision supersedes only M66-M69.
    arab_replacement.update(
        load_user_arab_replacement_h66_69_revised(ROOT)["units"]
    )
    # A later final revision supersedes only M82, M83, M97, and M98.
    arab_replacement.update(
        load_user_arab_replacement_h82_83_97_98_revised(ROOT)["units"]
    )
    # A later one-page revision supersedes only M11.
    arab_replacement["M11"] = load_user_arab_replacement_h11_revised(ROOT)[
        "units"
    ]["M11"]
    # A later two-page revision supersedes only M70 and M74.
    arab_replacement.update(
        load_user_arab_replacement_h70_74_revised(ROOT)["units"]
    )
    # A later one-page revision supersedes only M76.
    arab_replacement["M76"] = load_user_arab_replacement_h76_revised(ROOT)[
        "units"
    ]["M76"]
    # A later two-page revision supersedes only M78 and M80.
    arab_replacement.update(
        load_user_arab_replacement_h78_80_revised(ROOT)["units"]
    )
    if list(arab_replacement) != ORDER:
        raise SystemExit("combined user Arabic replacements do not cover 123 units")

    clean_units = []
    khususiyah_count = 0
    crops = []
    for uid in ORDER:
        base = copy.deepcopy(integrated[uid])
        # The two later user submissions together supersede Arabic for all
        # 123 units; the earlier archived user TXT remains only a provenance
        # record for the preceding Arabic lock.
        arab_source = arab_replacement[uid]
        arab = [strip_work_markers(x) for x in arab_source]
        latin = [clean_latin(x) for x in user["latin"]["units"][uid]]
        # Presentation cleaning must not become a silent source rewrite: after
        # removing the same explicit work/image-reference markers, the user
        # sources and source-locked integrated layers must still be identical.
        if arab != [strip_work_markers(x) for x in base["arab"]]:
            raise SystemExit(f"{uid}: user Arabic differs from source-locked integrated Arabic")
        if latin != [clean_latin(x) for x in base["latin"]]:
            raise SystemExit(f"{uid}: user Latin differs from source-locked integrated Latin")

        clean = {
            "unit_id": uid,
            "heading": base["heading"],
            "page": base.get("page"),
            "arab": arab,
            "latin": latin,
            "terjemahan": [clean_translation(x) for x in base["terjemahan"]],
            "syarah": make_syarah(base),
            "crop_page": base.get("crop_page"),
            "khususiyah_praktik": make_khususiyah(base),
        }
        clean["terjemahan"] = [x for x in clean["terjemahan"] if x]
        if not all(clean[k] for k in ("arab", "latin", "terjemahan", "syarah")):
            raise SystemExit(f"{uid}: an always-rendered clean layer is empty")
        if clean["khususiyah_praktik"]:
            khususiyah_count += 1
        if clean["crop_page"]:
            crops.append(clean["crop_page"])
            if not (ALQ / f"wafaq_qorin/{clean['crop_page']}.jpg").exists():
                raise SystemExit(f"{uid}: user crop is missing")
        clean_units.append(clean)

    if crops != EXPECTED_CROPS:
        raise SystemExit(f"crop set differs: {crops}")

    lines = ["# AL-QORIN WAR RIYADHAH", ""]
    for unit in clean_units:
        lines += [f"## {unit['heading']}", "", "### 1. Arab", ""]
        crop_rendered_in_arab = False
        for paragraph in unit["arab"]:
            if paragraph.strip() == WAFAQ_MARKER:
                if crop_rendered_in_arab:
                    raise SystemExit(
                        f"{unit['unit_id']}: duplicate {WAFAQ_MARKER} marker"
                    )
                if not unit["crop_page"]:
                    raise SystemExit(
                        f"{unit['unit_id']}: {WAFAQ_MARKER} has no user crop"
                    )
                page = unit["crop_page"]
                lines += [f"![Wafaq halaman {page}](wafaq_qorin/{page}.jpg)", ""]
                crop_rendered_in_arab = True
            else:
                lines += [paragraph, ""]
        lines += ["### 2. Latin", ""]
        for paragraph in unit["latin"]:
            lines += [paragraph, ""]
        lines += ["### 3. Terjemahan", ""]
        for paragraph in unit["terjemahan"]:
            lines += [paragraph, ""]
        lines += ["### 4. Syarah", ""]
        for idx, paragraph in enumerate(unit["syarah"]):
            lines += [paragraph, ""]
            if idx == 0 and unit["crop_page"] and not crop_rendered_in_arab:
                page = unit["crop_page"]
                lines += [f"![Wafaq halaman {page}](wafaq_qorin/{page}.jpg)", ""]
        if unit["khususiyah_praktik"]:
            lines += ["### 5. Khususiyah dan Tatacara Praktik", ""]
            for paragraph in unit["khususiyah_praktik"]:
                lines += [paragraph, ""]

    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps(clean_units, ensure_ascii=False, indent=1), encoding="utf-8")
    print(
        f"clean edition units={len(clean_units)} khususiyah_units={khususiyah_count} "
        f"crops={len(crops)} output={OUT_MD}"
    )


if __name__ == "__main__":
    main()
