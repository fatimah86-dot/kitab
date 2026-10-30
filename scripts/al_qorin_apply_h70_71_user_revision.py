#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 70-71 revision to the final DOCX.

The existing precision wafaq images are retained.  Excludes
carried-over material: introductory/source-side text, numbered
section labels, [Halaman ...] markers, descriptive text after the
Arabic and Indonesian "[ada wafaq]" markers, and "(Ekstraksi
Ritual)".  Markdown asterisks are normalized to document bullets or
removed from textual lists.  Places the combined Tata Cara Praktik
at the end of Halaman 71.
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

AR70 = [
    "مِنَ الْحَيِّ ذَلِكُمُ اللَّهُ رَبُّكُمْ فَأَنَّى تُؤْفَكُونَ .",
    "تَحْمِلُ حِجَابَ بَعْدَ الطُّهْرِ مِنَ الْحَيْضِ مُبَاشَرَةً وَيَعْمَلُ عَدَدَ ٣ أطباق وَيُنْجَمُ تَحْتَ السَّمَاءِ وَتُشْرَبُ كُلَّ يَوْمٍ وَاحِدٍ قَبْلَ الْإِفْطَارِ فَإِنَّهَا تَحْمَلُ بِأَذْنِ اللَّهِ .",
    "لِإِبْطَالِ الْأَسْحَارِ :",
    "تَكْتُبُ عَلَى الْكَفِّ الْيُمْنَى مَابَاتَى ✡ ف ق ج ثم تكتب على الكَفِّ الشَّمَالِ ✡ م خ م ت ثُمَّ ضَعِ الْكَفَّيْنِ مَفْتُوحَتَيْنِ عَلَى الْبُخُورِ جَاوِي وَكُزْبَرَةِ وَكَنْدَرِ ثُمَّ تَقْرَأُ قَوْلَهُ تَعَالَى : قَالَ مَنْ يُحْيِي الْعِظَامَ وَهِيَ رَمِيمٌ إِلَى آخِرِ سُورَةِ يس حَتَّى تَنْطِقَ الْكَفُوفَ وَامُرْ بِفَكِّ السِّحْرِ وَفَكِّ الْمَرْبُوطِ تَنْزِلُ الْكَفَّيْنِ عَلَى الذَّكَرِ فَإِنَّهُ يَنْحَلُ السِّحْرُ .",
    "لِلْحَمْلِ :",
    "لِلْمَرْأَةِ الَّتِي لَمْ تَحْمِلْ وَلَمْ يَعِشْ لَهَا الْأَوْلَادَ يُكْتَبُ لَهَا هَذَا الْحِرْزُ وَتَحْمِلُهُ بَعْدَ الطُّهْرِ مِنَ الْحَيْضِ فَإِنَّهَا تَحْمَلُ بِإِذْنِ اللَّهِ تَعَالَى وَهَذَا مَا تَكْتُبُ :",
    "[ada wafaq]",
]
LAT70 = [
    "Minal-ḥayyi żālikumullāhu rabbukum fa-annā tu'fakūn.",
    "Taḥmulu ḥijāba ba‘daṭ-ṭuhri minal-ḥaiḍi mubāsyaratan wa ya‘malu ‘adada tsalātsati aṭbāqin wa yunjamu taḥtas-samā'i wa tusyrabu kulla yaumin wāḥidin qablal-ifṭāri fa-innahā taḥmalu bi-iżnillāh.",
    "Li-ibṭālil-ashār:",
    "Taktubu ‘alal-kaffil-yumnā mābātā (✡ fā' qāf jīm) tsumma taktubu ‘alal-kaffis-syamāli (✡ mīm khā' mīm tā') tsumma ۡḍa‘il-kaffaini maftūḥataini ‘alal-bukhūri jāwiyin wa kuzbaratin wa kandarin tsumma taqra'u qaulahu ta‘ālā: Qāla man yuḥyil-iẓāma wa hiya ramīmun ilā ākhiri sūrati yāsīn ḥattā tanṭiqal-kaffūfa wa amur bi-fakkis-siḥri wa fakkil-marbūṭi tanzulal-kaffaini ‘alad-żakari fa-innahū yanḥalus-siḥr.",
    "Lil-ḥaml:",
    "Lil-mar'atillatī lam taḥmal wa lam ya'is lahāl-aulādu yuktabu lahā hāżal-ḥirzu wa taḥmiluhū ba‘daṭ-ṭuhri minal-ḥaiḍi fa-innahā taḥmalu bi-iżnillāhi ta‘ālā wa hāżā mā taktubu:",
    "( [ada wafaq] )",
]
TERJ70 = [
    '"Dari yang hidup Dia mengeluarkan yang mati dan dari yang mati Dia mengeluarkan yang hidup..." (QS. Yunos: 31 / Ar-Rum: 19). Demikianlah Allah, maka ke manakah kamu dipalingkan?',
    "Bawalah hijab (azimat) ini segera setelah suci dari haid, dan dibuat sebanyak 3 lembar/piring (atbaq), ditaruh di bawah bintang-bintang (di bawah langit malam) untuk menyerap energi, lalu diminum setiap hari satu kali sebelum sarapan (buka puasa), maka ia akan hamil dengan izin Allah.",
    "Untuk Membatalkan Sihir:",
    "Tulislah pada telapak tangan kanan: Mabata ✡ F J, kemudian tulislah pada telapak tangan kiri: ✡ M Kh M T. Setelah itu, letakkan kedua telapak tangan dalam keadaan terbuka di atas bukhur berupa: kemenyan Jawa, ketumbar, dan kendar (luban zakar). Lalu bacalah firman Allah Ta'ala: \"Ia berkata, 'Siapakah yang dapat menghidupkan tulang belulang, yang telah hancur luluh?'\" hingga akhir Surah Yasin, sampai kedua telapak tangan tersebut bergerak berucap/berisyarat. Perintahkanlah untuk membuka sihir dan melepaskan ikatan (marbuth), lalu turunkan kedua telapak tangan ke atas kemaluan ( laki-laki yang terkena ikatan), maka sihir tersebut akan terurai.",
    "Untuk Kehamilan:",
    "Bagi perempuan yang belum pernah hamil atau anak-anaknya tidak pernah panjang umur (sering keguguran/meninggal saat bayi), dituliskan baginya hirz (azimat) ini dan dibawanya setelah suci dari haid, maka ia akan hamil dengan izin Allah Ta'ala. Dan inilah yang harus ditulis: [ada wafaq].",
]

AR71 = [
    "فَائِدَةٌ لِعَدَمِ سُقُوطِ الْجَنِينِ :",
    "يُكْتَبُ وَيُحْمَلُ وَحَوْلَهُ آيَاتِ الْحِفْظِ وَمَا يُنَاسِبُ .",
    "اعْلَمْ أَنَّ مِنْ أَسْرَارِ حَرْفِ الطَّاءِ أَنَّ مِنْ كَتَبَهَا هَكَذَا وَكَتَبَ حَوْلَهَا ( طَسْم ) مِائَةَ مَرَّةً وَتِسْعَةَ ١٠٩ ثم كتب حوله البسمله وفى ذلك فى الشهر الثالث من حمل المرأة .",
    "وَبَعْدَ وَضْعِ الْمَوْلُودِ تَرْفَعُهُ مِنْ عَلَيْهَا وَتَلْبَسُهُ لِلْمَوْلُودِ فَإِنَّهُ يَحْفَظُ مِنَ الْقَرَائِنِ وَالتَّوَابِعِ وَالْعَوَارِضِ وَخِلَافِهِ .",
    "مُجَرَّبٌ صَحِيحٌ .",
    "[ada wafaq]",
    "فَائِدَةٌ لِلْحَمْلِ :",
    "تَكْتُبُ هَذِهِ الْآيَاتِ وَقْتَ الظُّهْرِ فِي يَوْمِ سَعِيدٍ وَتُمْحَى بِلَبَنِ مَاعِزٍ تَكُونُ سَوْدَاءَ وَتَشْرَبُهَا الْمَرْأَةُ بَعْدَ الطُّهْرِ مِنَ الْحَيْضِ",
]
LAT71 = [
    "Fā'idatun li-'adami suqūtil-janīn:",
    "Yuktabu wa yuḥmalu wa ḥaulahū āyātul-ḥifẓi wa mā yunāsib.",
    "I'lam anna min asrāri ḥarfis-ṭā'i anna man katabahā hākadzā wa kataba ḥaulahā (Ṭā Sīn Mīm) mi'ata marratatin wa tis'atan wa mi'atan (109) tsumma kataba ḥaulahal-basmalata wa fī żālika fīsy-syahris-sālisi min ْhamlil-mar'ah.",
    "Wa ba'da waḍ'il-maulūdi tarfa'uhū min 'alaihā wa talbasuhū lil-maulūdi fa-innahū yaḥfazu minal-qarā'ini wat-tawābi'i wal-'awāriḍi wa khilāfih.",
    "Mujarrabun ṣaَحīḥ.",
    "( [ada wafaq] )",
    "Fā'idatun lil-ḥaml:",
    "Taktubu hāżihil-āyāte waqtaẓ-ẓuhri fī yaumin sa'īdin wa tumḥā libani mā'izin takūnu sauda'a wa tasyrubuhal-mar'atu ba'daṭ-ṭuhri minal-ḥaiḍi.",
]
TERJ71 = [
    "Faedah Agar Janin Tidak Gugur:",
    "Ditulis dan dibawa, serta di sekelilingnya dituliskan ayat-ayat penjagaan (Al-Hifzh) dan yang selaras.",
    "Ketahuilah sesungguhnya di antara rahasia huruf Tha (ط) adalah barangsiapa yang menulisnya seperti ini, lalu menulis di sekelilingnya huruf طَسْم (Tha Sin Mim) sebanyak 109 kali, kemudian menuliskan kalimat Basmalah di sekelilingnya. Hal itu dilakukan pada bulan ketiga kehamilan sang istri.",
    "Setelah anak tersebut lahir, angkatlah (lepas) azimat itu dari ibu, lalu pakaikan/pakaikan kepada bayi yang baru lahir tersebut, karena hal itu dapat menjaga sang anak dari gangguan jin qarin, tawabi', 'awarid, dan lain-lain. Ini terbukti Mujarab lagi Shahih.",
    "[ada wafaq]",
    "Faedah untuk Kehamilan:",
    "Tulislah ayat-ayat ini pada waktu zuhur di hari yang baik, lalu lunturkan (tulisannya) dengan susu kambing berwarna hitam, kemudian diminum oleh sang istri setelah suci dari haid.",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Terapi Air Minum 3 Piring untuk Kehamilan (Hal. 70): Azimat ditulis sebanyak 3 lembar media (piring/kertas), diinapkan di bawah langit (dinyunjam / terkena cahaya bintang/langit malam), lalu dilarutkan dan diminum setiap hari menjelang pagi sebelum makan selama 3 hari berturut-turut setelah suci haid.",
    "- Metode Deteksi & Pembongkar Sihir Melalui Telapak Tangan (Hal. 70): Teknik khusus menggunakan tulisan asma'/huruf di kedua telapak tangan, diasapi bukhur khusus (Jawa, ketumbar, kendar), dibacakan Surah Yasin secara penuh hingga tangan pasien merespon/bergerak untuk membuka simpul sihir atau ikatan marbuth.",
    "- Azimat Penjaga Janin Bulan Ketiga & Bayi (Hal. 71): Pembuatan rajah huruf Tha dilingkari Tha Sin Mim sebanyak 109 kali plus Basmalah pada usia kehamilan 3 bulan untuk mencegah keguguran. Setelah lahir, azimat dipindahkan untuk dipakai oleh sang anak sebagai perisai dari qarin dan tawabi'.",
    "- Ramuan Peluntur Susu Kambing Hitam (Hal. 71): Penulisan ayat/rajah khusus pada waktu zuhur di hari baik, dilebur menggunakan susu kambing hitam murni, lalu diminum oleh istri yang mendambakan keturunan setelah bersih dari haid.",
]

FORBIDDEN = [
    "Berikut adalah transkripsi",
    "mengambil teks secara autentik",
    "Pada gambar yang dilampirkan",
    "Sisi Kanan",
    "Sisi Kiri",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi",
    "[Halaman",
    "Tabel Wafaq Segi Empat",
    "Wafaq Huruf Tha",
    "(Ekstraksi Ritual)",
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
    if page == 70:
        return (
            [("ar", x) for x in AR70]
            + [("img", None)]
            + [("la", x) for x in LAT70]
            + [("te", x) for x in TERJ70]
        )
    return (
        [("ar", x) for x in AR71[:6]]
        + [("img", None)]
        + [("ar", x) for x in AR71[6:]]
        + [("la", x) for x in LAT71]
        + [("te", x) for x in TERJ71]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 70:
        return AR70 + [""] + LAT70 + TERJ70 + [""]
    return AR71[:6] + [""] + AR71[6:] + LAT71 + TERJ71 + TATACARA + [""]


def expected_image_position(page: int) -> int:
    return len(AR70) if page == 70 else 6


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[70] + 1])
    if has_drawing_el(arab_tpl) or not texts[heads[70] + 1].startswith("مِنَ الْحَيِّ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[70], heads[71])
        if texts[i].startswith("(Minal hayyi dzaalikumul laahu")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[70], heads[71])
        if texts[i].startswith("“… dari yang hidup.")
    )
    blank_tpl = deepcopy(els[heads[71] - 1])
    if texts[heads[71] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (70, 71):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[70]].getparent()
    removed = 0
    inserted = 0
    for n in (70, 71):
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
                next_heading_el.addprevious(deepcopy(images[n]))
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

    for n in (70, 71):
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
        if image_positions != [expected_image_position(n)]:
            raise AssertionError(
                f"unit {n} image positions {image_positions}, expected {[expected_image_position(n)]}"
            )

    revised = "\n".join(ot[oh[70] : oh[72]])
    if revised.count("[ada wafaq]") != 6:
        raise AssertionError(f"[ada wafaq] count {revised.count('[ada wafaq]')} != 6")
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
    print("H70_71_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
