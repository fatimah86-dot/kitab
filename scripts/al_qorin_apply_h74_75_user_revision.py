#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 74-75 revision to the final DOCX.

Retains the existing precision wafaq image on Halaman 74 directly
after its "[ada wafaq]" marker; Halaman 75 has no crop image.
Excludes the introductory/layout text, numbered section labels, and
page markers.  Places the supplied combined Tata Cara Praktik at the
end of Halaman 75.
"""

from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "al_qorin/AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx"
SOURCE_FOR_MEDIA = ROOT / "al_qorin/AL_QORIN_123_BERSIH_2_LAYER.docx"

COUNT_LINE = "انا عدد ١١ = انا ١٤ مَرَّةً هو ١٣ مَرَّةً يَاه ياه ياهو"
WAW_YAH_LINE = " ".join(["و"] * 11) + "  " + " ".join(["يه"] * 13)

AR74 = [
    "فَحَمَلَتْهُ بِلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ .",
    "( غِيرَةٌ مُجَرَّبٌ ) لِلْمَرْأَةِ الَّتِي لَمْ تَحْمِلْ وَالْفَرَسِ وَالنَّاقَةِ وَالْبَقَرَةِ وَالْخَيْلِ وَجَمِيعِ الْأَشْجَارِ تَكْتُبُ هَذِهِ الْأَسْمَاءِ وَأَنْتَ طَاهِرٌ وَيُطْلَقُ عَلَيْهَا فَإِنَّهُمْ يَحْمِلُونَ بِإِذْنِ اللَّهِ تَعَالَى وَهِيَ هَذِهِ الْأَسْمَاءِ الَّتِي تُكْتَبُ :",
    COUNT_LINE,
    WAW_YAH_LINE,
    "( غِيره لِلْحَمْلِ مُجَرَّبٌ ) اكْتُبْ هَذِهِ الْأَسْمَاءَ فِي نُسْخَتَيْنِ وَاحِدَةٌ بِحَمْلِهَا الرَّجُلُ وَالثَّانِيَةُ تَحْمِلُهَا الْمَرْأَةُ فَإِنَّ اللَّهَ تَعَالَى يَعْطِيهُمُ الْحَمْلَ بِإِذْنِ اللَّهِ تَعَالَى",
    "[ada wafaq]",
    "فَرْدَحْكُمُ عَدْهَا قُدُّوسٌ حَجَى قَيُّومٌ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ .",
]
LAT74 = [
    "Fa-ḥamalat-hu bilā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīm.",
    "(Ghīratun mujarrabun) lil-mar'atillatī lam taḥmal wal-farasi wan-nāqati wal-baqarati wal-khaili wa jamī‘il-asjāri taktubu hāżihil-asmā'a wa anta ṭāhirun wa yuṭlaqu ‘alaihā fa-innahum yaḥmalūna bi-iżnillāhi ta‘ālā wa hiya hāżihil-asmā'u allatī tuktubu:",
    COUNT_LINE,
    WAW_YAH_LINE,
    "(Ghairuhū lil-ḥamli mujarrabun) uktub hāżihil-asmā'a fī nusukhataini wāḥidatun biḥamlihar-rajulu was-tsāniyatu taḥmuhuhā-l-mar'atu fa-innal-laha ta‘ālā yu‘ṭīhimul-ḥamla bi-iżnillāhi ta‘ālā.",
    "( [ada wafaq] )",
    "Fardahkum ‘adhā qudūsun ḥajā qayyūmun wa lā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīm.",
]
TERJ74 = [
    '"Maka ia mengandungnya, dengan tiada daya dan tiada kekuatan melainkan dengan pertolongan Allah Yang Maha Tinggi lagi Maha Agung."',
    "(Ghairah yang Teruji): Untuk wanita yang belum kunjung hamil, serta (bisa juga diamalkan untuk) kuda, unta, sapi, kambing, dan seluruh pepohonan. Tulislah nama-nama ini dalam keadaan suci, lalu gantungkan/asapkan padanya, maka mereka akan mengandung dengan izin Allah Ta'ala. Dan inilah nama-nama yang harus ditulis:",
    COUNT_LINE,
    WAW_YAH_LINE,
    "(Cara Lain untuk Kehamilan yang Teruji): Tulislah nama-nama ini dalam dua salinan (lembar): satu salinan dibawa/dipakai oleh sang suami, dan salinan kedua dibawa oleh sang istri, maka sesungguhnya Allah Ta'ala akan menganugerahkan kehamilan kepada mereka dengan izin Allah Ta'ala.",
    "[ada wafaq]",
    "Fardahkum 'adha qudusun hajā qayyumun wa la haula wa la quwwata illa billahil 'aliyyil 'azhim.",
]

AR75 = [
    "الْفَصْلُ الْخَامِسَ عَشَرَ",
    "لِاحْتِرَاقِ الْعَارِضِ",
    "تَقُولُ : احْرِقْ مِنْ عَصَ مِنْ عَصٍ يَابُوطُ ٣ طُوشِ ٣ هَرْمَا هِرْشُ ٣ هَطُوشِ ٢ احْرِقِ الْجِنَّ وَالْعَارِضَ وَالضَّرْبَةَ وَالضَّارِبَ ضَرِيحَ الرَّمْدِ ضَرِيحَ السَّمِّ السُّوءِ ضَرِيحَ لَمْفَنْجَلْ مَهْرِجْ مَهْمَا كَانَ مِنْ هَذِهِ الْجُثَّةِ فُلَانِ ابْنِ فُلَانَةَ بَارَكَ فِيكُمْ وَعَلَيْكُمْ .",
    "الْبُخُورُ عَنْكَبوتٌ وَكُزْبَرَةٌ عِنْدَ غُرُوبِ الشَّمْسِ قَبْلَ الْغُرُوبِ .",
    "اسْتِحْضَارُ فَرْدٍ مِنْ أَفْرَادِ الْجِنِّ :",
    "أَوَّلاً تَدْخُلُ مَكَاناً طَاهِراً طَاهِراً وَأَنْتَ طَاهِرُ الْبَدَنِ وَالثَّوْبِ وَتُغْلِقُ الْمَكَانَ جَيِّداً بِحَيْثُ إِنْ لَا يَدْخُلَهُ أَيُّ نُورٍ وَلَا مِنْ ثَقْبٍ، الْكَالُونُ يَكُونُ مَسْدُوداً أَيْضاً ثُمَّ تَقِفُ وَتَسْتَقْبِلُ الْقِبْلَةَ بِخُضُوعٍ وَخُشُوعٍ ثُمَّ تَقُولُ :",
    "مَا شَاءَ اللَّهُ عَدَدَ ٣ - لا إِلَهَ إِلَّا اللَّهُ ٧",
    "لا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ عَدَدَ ٧",
    "سُورَةَ الْجِنِّ عَدَدَ ٧",
]
LAT75 = [
    "Al-Faṣlul-khāmisu ‘asyara",
    "Li-iḥtirāqil-‘āriḍ",
    "Taqūlu: Iḥriq min ‘aṣin min ‘aṣin yābūṭu (3x) ṭūsyin (3x) harmā hirsyu (3x) haṭūsyin (2x) iḥriqil-jinna wal-‘āriḍa waḍ-ḍarbata waḍ-ḍāriba َḍarīḥar-ramdi َḍarīḥas-sammis-sū'i َḍarīḥa lamfanjal mahrig mahmā kāna min hāżihil-jutsati fulāni bnu fulānata bāraka fīkum wa ‘alaikum.",
    "Al-bukhūru ‘ankabūtun wa kuzbaratun ‘inda ghurūbis-syamsi qablal-ghurūb.",
    "Istiḥzāru fardin min afrādil-jinn:",
    "Awwalan tadkhulu makānan ṭāhiran ṭāhiran wa anta ṭāhirul-badani wats-tsaubi wa tughliqu-l-makāna jayyidan biḥaiṡu in lā yadkhulahu ayyu nūrin wa lā min ْthaqbin, al-kālūnu yakūnu masdūdan aiḍan tsumma taqifu wa tastaqbilul-qiblata bikhuḍū‘in wa khusyū‘in tsumma taqūlu:",
    "Mā syā'allāhu ‘adada 3 - Lā ilāha illallāhu 7",
    "Lā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīmi ‘adada 7",
    "Sūratal-jinni ‘adada 7",
]
TERJ75 = [
    "Fasal Kelima Belas: Untuk Membakar Jin Pengganggu (Al-'Ariḍ)",
    "Engkau membaca (azimah): \"Bakarlah dari yang membangkang... (seperti lafaz asma' Suryani: Yabutha 3x, Tushin 3x, Harma Hirsyu 3x, Hathushin 2x). Bakarlah bangsa jin, al-'ariḍ (pengganggu), pukulan, dan pemukul, (demikian pula) kepedihan belekan (ramd), kepedihan racun yang buruk, kepedihan Lamfanjal Mahrig, siapapun orangnya dari jasad Fulan bin Fulanah ini, semoga keberkahan tercurah pada kalian dan atas kalian.\"",
    "Buhur (wewangian): Sarang labah-labah ('ankabut) dan ketumbar (kuzbarah), dibakar saat menjelang terbenamnya matahari.",
    "Tata Cara Pemanggilan Satu Oknum Jin (Istiḥzār Fard min Afrādil-Jinn):",
    "Pertama, masuklah ke dalam ruangan yang suci, sementara badan dan pakaianmu dalam keadaan suci. Tutuplah ruangan tersebut dengan rapat sehingga tidak ada cahaya sedikit pun yang masuk dari celah atau lubang mana pun, kunci pintu juga harus ditutup rapat. Kemudian berdirilah menghadap kiblat dengan penuh ketundukan dan kekhusyukan, lalu bacalah:",
    "Mā syā'allāh (3 kali)",
    "Lā ilāha illallāh (7 kali)",
    "Lā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīm (7 kali)",
    "Membaca Surah Al-Jin (7 kali)",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "Azimat Pengasapan Kesuburan Universal (Hal. 74): Penulisan asma' khusus (Ana 11, Yahu, Bahu, dll.) dalam keadaan suci, yang tidak hanya berfungsi untuk wanita yang sulit hamil, tetapi juga dapat diapresiasikan untuk hewan ternak (kuda, unta, sapi) dan tanaman agar produktif/subur dengan izin Allah.",
    "Metode Azimat Ganda Suami-Istri (Hal. 74): Menuliskan rajah dan asma' kehamilan dalam dua salinan kembar, di mana satu salinan dibawa oleh suami dan salinan kedua dibawa oleh istri sebagai bentuk ikhtiar batin bersama.",
    "Ruqyah Pembakaran Jin Pengganggu / Al-'Ariḍ (Hal. 75):",
    "- Mengamalkan bacaan azimah sumpah panas (Iḥriq min 'aṣin...) yang ditujukan untuk melumpuhkan dan membakar jin pengganggu pada tubuh pasien (Fulan bin Fulanah).",
    "- Menggunakan media bukhur khusus berupa sarang labah-labah dan ketumbar yang dibakar pada waktu menjelang magrib (sebelum matahari terbenam).",
    "Protokol Ruang Khusus Pemanggilan Golongan Jin (Hal. 75): Panduan isolasi mandiri di tempat/ruangan yang gelap gulita tanpa cahaya, berpakaian dan berbadan suci, menghadap kiblat, serta membentengi diri dengan zikir tertentu (Ma sya' Allah 3x, Tahlil 7x, Hauqalah 7x, dan membaca Surah Al-Jin sebanyak 7 kali).",
]

FORBIDDEN = [
    "Berikut adalah transkripsi",
    "berdasarkan gambar manuskrip",
    "Pada tata letak manuskrip",
    "Sisi Kanan",
    "Sisi Kiri",
    "Teks Arab (Transkripsi",
    "[Halaman",
    "&amp;",
]


def has_drawing_el(el) -> bool:
    return bool(el.xpath('.//*[local-name()="drawing"]'))


def make_para(template_el, text: str):
    el = deepcopy(template_el)
    runs = el.findall(qn("w:r"))
    donor = deepcopy(runs[0]) if runs else None
    for child in list(el):
        if child.tag != qn("w:pPr"):
            el.remove(child)
    if donor is not None:
        texts = [t for t in donor.iter() if t.tag == qn("w:t")]
        for t in texts:
            t.text = ""
        if texts:
            texts[0].text = text
            texts[0].set(qn("xml:space"), "preserve")
            for extra in texts[1:]:
                extra.getparent().remove(extra)
        el.append(donor)
    return el


def media_hashes(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.startswith("word/media/")]
        return [hashlib.sha256(z.read(n)).hexdigest() for n in names]


def find_heads(paragraph_texts: list[str]) -> dict[int, int]:
    heads: dict[int, int] = {}
    for i, text in enumerate(paragraph_texts):
        m = re.match(r"^=== Halaman (\d+) — (.+) ===$", text.strip())
        if m:
            heads[int(m.group(1))] = i
    return heads


def build_sequence(page: int) -> list[tuple[str, str | None]]:
    if page == 74:
        return (
            [("ar", x) for x in AR74[:6]]
            + [("img", None)]
            + [("ar", x) for x in AR74[6:]]
            + [("la", x) for x in LAT74]
            + [("te", x) for x in TERJ74]
        )
    return (
        [("ar", x) for x in AR75]
        + [("la", x) for x in LAT75]
        + [("te", x) for x in TERJ75]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 74:
        return AR74[:6] + [""] + AR74[6:] + LAT74 + TERJ74 + [""]
    return AR75 + LAT75 + TERJ75 + TATACARA + [""]


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[74] + 1])
    if has_drawing_el(arab_tpl) or not texts[heads[74] + 1].startswith("فَلَحَمَلَتْهُ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[74], heads[75])
        if texts[i].startswith("Fahamalat-hu bilaa haulin")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[74], heads[75])
        if texts[i].startswith("“… maka ia mengandungnya")
    )
    blank_tpl = deepcopy(els[heads[75] - 1])
    if texts[heads[75] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    found74 = [
        deepcopy(els[i])
        for i in range(heads[74], heads[75])
        if has_drawing_el(els[i])
    ]
    if len(found74) != 1:
        raise AssertionError(f"unit 74 image count {len(found74)} != 1")
    if any(has_drawing_el(els[i]) for i in range(heads[75], heads[76])):
        raise AssertionError("unit 75 unexpectedly carries an image")
    image74 = found74[0]

    body = els[heads[74]].getparent()
    removed = 0
    inserted = 0
    for n in (74, 75):
        heading_el = els[heads[n]]
        next_heading_el = els[heads[n + 1]]
        node = heading_el.getnext()
        while node is not None and node is not next_heading_el:
            nxt = node.getnext()
            if node.tag == qn("w:p"):
                body.remove(node)
                removed += 1
            node = nxt

        for kind, text in build_sequence(n):
            if kind == "img":
                next_heading_el.addprevious(deepcopy(image74))
            else:
                next_heading_el.addprevious(make_para(templates[kind], str(text)))
            inserted += 1
        next_heading_el.addprevious(make_para(blank_tpl, ""))

    doc.save(TARGET)

    out = Document(TARGET)
    ot = [p.text for p in out.paragraphs]
    oh = find_heads(ot)
    if sorted(oh) != list(range(1, 123)):
        raise AssertionError("headings broken")

    for n in (74, 75):
        got_idx = list(range(oh[n] + 1, oh[n + 1]))
        got = [ot[i] for i in got_idx]
        expected = expected_texts(n)
        if got != expected:
            for a, b in zip(got, expected):
                if a != b:
                    print(f"UNIT {n} MISMATCH:\n got: {a[:140]!r}\n exp: {b[:140]!r}")
            raise AssertionError(f"unit {n} mismatch len {len(got)} vs {len(expected)}")
        image_positions = [
            j for j, i in enumerate(got_idx) if has_drawing_el(out.paragraphs[i]._element)
        ]
        expected_positions = [6] if n == 74 else []
        if image_positions != expected_positions:
            raise AssertionError(
                f"unit {n} image positions {image_positions}, expected {expected_positions}"
            )

    revised = "\n".join(ot[oh[74] : oh[76]])
    if revised.count("[ada wafaq]") != 3:
        raise AssertionError(f"[ada wafaq] count {revised.count('[ada wafaq]')} != 3")
    for fragment in FORBIDDEN:
        if fragment.lower() in revised.lower():
            raise AssertionError(f"carried-over fragment remains: {fragment}")
    if len(out.inline_shapes) != 26:
        raise AssertionError("image count changed")
    if media_hashes(TARGET) != media_hashes(SOURCE_FOR_MEDIA):
        raise AssertionError("media hashes/order changed")

    print(f"removed_old_paras={removed}")
    print(f"inserted_paras={inserted}")
    print(f"total_paragraphs={len(ot)}")
    print(f"bytes={TARGET.stat().st_size}")
    print(f"sha256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")
    print("H74_75_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
