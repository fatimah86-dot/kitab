#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 66-67 revision to the final DOCX.

Excludes carried-over material: the workspace/format introduction,
image/source mapping, numbered section labels, [Halaman ...]
markers, markdown list bullets in textual titles, Indonesian
editorial descriptions after "[ada wafaq]", and the label
"(Ekstraksi Ritual)".  Keeps the "[ada wafaq]" markers and each
precision wafaq image at the marker position in its Arabic block.
Places the combined Tata Cara Praktik at the end of Halaman 67.
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

AR66 = [
    "( التَّعَوُّذُ مِنْ كُلِّ مَكْرُوهٍ )",
    "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّةِ مِنْ كُلِّ شَيْطَانٍ وَهَامَّةٍ وَمِنْ شَرِّ كُلِّ عَيْنٍ لَامَّةٍ وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ وَمِنْ شَرِّ مَنْ يَعْقِدُ بِالْمَرَاضِ وَمِنْ شَرِّ طَوَارِقِ اللَّيْلِ وَالنَّهَارِ إِلَّا طَارِقاً يَطْرُقُ بِخَيْرٍ مِنْكَ يَا رَحْمَنُ . أَعُوذُ بِعَفْوِكَ مَنْ عِقَابِكَ وَأَعُوذُ بِرِضَاكَ مِنْ سَخَطِكَ وَأَعُوذُ بِكَ مِنْكَ إِلَيْكَ لَا أُحْصِي ثَنَاءً عَلَيْكَ .",
    "لِلشِّفَاءِ مِنْ كُلِّ دَاءٍ وَجَمِيعِ الْأَسْقَامِ",
    "لِلْأَمْرَاضِ الَّذِي عَجَزَتْ عَنْهَا الْأَطِبَّاءُ تَكْتُبُ وَخُمَى وَتُسْفَى وَيُحْمَلُ وَهَذَا مَا يُكْتَبُ وَمَعَهُ آيَاتُ الشِّفَاءِ وَمَا يُنَاسِبُ",
    "([ada wafaq])",
]
LAT66 = [
    "(At-Ta‘awwużu min kulli makrūh)",
    "A‘ūzu bikalimātillāhit-tāmmatī min kulli syaiṭānin wa hāmmatin wa min syَرِّ kulli ‘ainin lāmmatin wa min syَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ wa min syَرِّ حَاسِدٍ iżā ḥasada wa min syَرِّ may-ya‘qidu bil-amrāḍi wa min syَرِّ ṭawāriqil-laili wan-nahāri illā ṭāriqan yaṭruqu bi-khairim-minkaya raḥmānu. A‘ūzu bi‘afwika min ‘iqābika wa a‘ūzu biriḍāka min sakhatika wa a‘ūzu bika minka ilaika lā uḥṣī tsanā'an ‘alaika.",
    "Lisy-syifā'i min kulli dā'in wa jamī‘il-asqām",
    "Lil-amrāḍil-lażī ‘ajazat ‘anhul-aṭibbā'u taktubu wa khumā wa tusfā wa yuḥmalu wa hāżā mā yuktubu wa ma‘ahu āyātus-syifā'i wa mā yunāsib.",
    "( [ada wafaq] )",
]
TERJ66 = [
    "(Doa Perlindungan dari Segala Hal yang Dibenci)",
    '"Aku berlindung dengan kalimat-kalimat Allah yang sempurna dari setiap setan, binatang berbisa, dari kejelekan setiap mata yang mencela, dari kejelekan wanita-wanita tukang sihir yang meniup pada buhul-buhul, dari kejelekan orang yang dengki apabila ia dengki, dari kejelekan orang yang mengikat (menyihir) dengan penyakit, dan dari kejelekan yang datang di malam dan siang hari kecuali yang datang membawa kebaikan dari-Mu wahai Zat Yang Maha Pengasih. Aku berlindung dengan ampunan-Mu dari siksa-Mu, aku berlindung dengan ridha-Mu dari murka-Mu, dan aku berlindung kepada-Mu dari-Mu (tidak mampu menghindar kecuali kepada-Mu), aku tidak dapat menghitung pujian atas-Mu."',
    "Untuk Penyembuhan dari Segala Penyakit dan Macam-Macam Penderitaan:",
    "Untuk penyakit-penyakit yang telah membuat para dokter angkat tangan (putus asa), ditulis, dilarutkan (untuk diminum), dan dibawa (dikalungkan). Dan inilah apa yang harus ditulis bersamanya disertai ayat-ayat kesembuhan dan yang selaras: ( [ada wafaq] )",
]

AR67 = [
    "الْفَصْلُ الرَّابِعَ عَشَرَ",
    "لِإِبْطَالِ السِّحْرِ وَحَلِّ الْمَرْبُوطِ",
    "اكْتُبِ الطِّلَاسِمَ الْآتِيَةَ فِي سَبْعِ وَرَقَاتِ أَبْيَضَ وَضَعْ فِي كُلِّ وَرَقَةٍ جَاوِي وَلُبَانَ ذَكَرٍ ومَسْتِكَى وَعُودَ الْقَمَرِي وَرَقَةً فِي النَّارِ يَتَلَقَّى دُخَانَهَا الْمَسْحُورُ أَوِ الْمَوْبُوطُ وَاقْرَأْ عَلَيْهَا سُورَةَ يَس الَّتِي مُبِينٍ الْأُولَى وَالثَّانِيَةَ إِلَى مُبِينٍ الثَّانِيَةِ وَهَكَذَا إِلَى أَنْ تَنْتَهِيَ الْأَوْرَاقُ السَّبْعَةِ حَتَّى نِهَايَةِ السُّورَةِ فَإِنَّ الْمَسْحُورَ وَالْمَرْبُوطَ يَبْرَأُ بِإِذْنِ اللَّهِ تَعَالَى وَهَذِهِ الْأَسْمَاءِ ..",
    "([ada wafaq])",
    "لِإِبْطَالِ السِّحْرِ وَصَرْفِ الْعَوَارِضِ وَحَلِّ الْمَرْبُوطِ :",
    "اكْتُبِ الْآتِي فِي ثَلَاثِ وَرَقَاتٍ وَضَعْ فِيهِمْ الْبُخُورَ حَبَّةَ الْبَرْكَةِ وَفَاسُوخِ مَغْرِبِيٍّ وَشَجَرَةِ مَرْيَمَ وَمَسْتِكَةَ وَكَنْدَرِ وَسَدْرٍ نَاشِفٍ وَتَبَخَّرْ بِهِمِ الْمَرِيضُ وَالْمَسْحُورُ وَالْمَعْقُودُ وَلِتَعْوَارِضِ وَالرِّيحِ الْأَحْمَرِ وَخِلَافِهِ فَإِنَّهُ يَبْرَأُ بِإِذْنِ اللَّهِ تَعَالَى وَهَذَا مَا تَكْتُبُ :",
]
LAT67 = [
    "Al-Faṣlur-rābi‘u ‘asyara",
    "Li-ibṭālis-siḥri wa ḥallil-marbūṭ",
    "Uktubil-ṭilāsimal-ātī fī sab‘i waraqātin abyaḍa wa ۡḍa‘ fī kulli waraqatin jāwiyan wa lubāna żakarin wa mastikā wa ‘ūdal-qamari waraqatan fin-nārī yata-laqqā dukhānahal-masḥūru awil-maubūṭu wa aqra' ‘alaihā sūrata yāsīn allatī mubīnil-ūlā was-tsāniyata ilā mubīnis-tsāniyati wa hākadzā ilā an tantahiyal-awrāqu-s-sab‘atu ḥattā nihāyatis-sūrati fa-innal-masḥūra wal-marbūṭa yabra'u bi-iżnillāhi ta‘ālā wa hāżihil-asmā'i..",
    "( [ada wafaq] )",
    "Li-ibṭālis-siḥri wa ṣarfil-‘awāriḍi wa ḥallil-marbūṭ:",
    "Uktubil-ātī fī tsalātsi waraqātin wa ۡḍa‘ fīhimul-bukhūra ḥabbatal-barokati wa fāsūkhin maghribiyyin wa syajarati maryama wa mastikata wa kandara wa sidrin nāsyifin wa tabakhar bihimul-marīḍu wal-masḥūru wal-ma‘qūdu wa lita‘wāriḍi war-rīḥil-aḥmari wa khilāfihī fa-innahu yabra'u bi-iżnillāhi ta‘ālā wa hāżā mā taktubu:",
]
TERJ67 = [
    "Fasal Keempat Belas",
    "Untuk Membatalkan Sihir dan Melepaskan Orang yang Terkena Ikatan (Marbuth)",
    "Tulislah tlasim (simbol rahasia) berikut pada tujuh lembar kertas putih, dan letakkan pada setiap lembarnya: kemenyan Jawa (jawi), kemenyan laki-laki (luban dzakar), mastika, dan kayu gaharu ('ud qamari). Bakarlah satu lembar kertas di atas api, lalu biarkan orang yang terkena sihir atau marbuth menghirup asapnya, sambil dibacakan atasnya Surah Yasin. (Caranya): Mulailah membaca hingga kata Mubin pertama, lalu tiupkan; lanjutkan hingga kata Mubin kedua, lalu tiupkan; begitu seterusnya hingga selesai tujuh lembar kertas sampai akhir surah. Maka sesungguhnya orang yang terkena sihir dan marbuth akan sembuh dengan izin Allah Ta'ala, beserta (perantara) nama-nama ini: ( [ada wafaq] )",
    "Untuk Membatalkan Sihir, Menyingkirkan Gangguan Jin ('Awarid), dan Melepaskan Orang yang Terkena Ikatan:",
    "Tulislah rajah berikut pada tiga lembar kertas, dan letakkan di dalam bungkusan kertas tersebut bukhur berupa: jintan hitam (habbah barakah), fasukh maghribi, kayu/akar maryam, mastika, kendar ( kemenyan arab ), dan daun bidara kering. Jadikan bahan-bahan tersebut sebagai bukhur (asapan) bagi orang yang sakit, terkena sihir, ma'qud (terikat), serta untuk mengatasi gangguan 'awarid, angin merah (rih ahmar), dan penyakit lainnya. Maka sesungguhnya ia akan sembuh dengan izin Allah Ta'ala. Dan inilah apa yang harus engkau tulis:",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "Berdasarkan Halaman 66 dan 67, bab ini berfokus pada Terapi Pengobatan Penyakit Kronis/Medis Berat serta Protokol Total Pembatalan Sihir, Ruqyah, dan Pelepasan Ikatan Sihir Penunduk (Marbuth/Ma'qud).",
    "Metode 1: Terapi Asap Tlasim & Surah Yasin (Halaman 67 - Bagian 1)",
    "- Media Penulisan: Siapkan 7 lembar kertas putih.",
    "- Campuran Buhur Setiap Lembar: Pada setiap lembar kertas, letakkan racikan bukhur berupa: Kemenyan Jawa, Luban Dzakar, Mastika, dan Kayu Gaharu.",
    "- Teknis Pembakaran & Penghirupan: Bakar kertas pertama di atas bara api, lalu arahkan asapnya agar dihirup oleh pasien yang terkena sihir atau marbuth.",
    "- Metode Pembacaan Surah Yasin Bertahap: Selama proses pengasapan kertas demi kertas (hingga habis 7 lembar), bacakan Surah Yasin dengan metode Mubin (berhenti dan tiup setiap kali menjumpai kata مُبِينٍ dalam ayat Yasin hingga tuntas sampai akhir surat).",
    "Metode 2: Terapi Buhur Tujuh Serbuk Pembersih Sihir (Halaman 67 - Bagian 2)",
    "- Media Penulisan: Siapkan 3 lembar kertas bertuliskan rajah khusus.",
    "- Racikan Buhur Khusus: Bungkus di dalam kertas tersebut ramuan bukhur: Habbatus Sauda (Jintan Hitam), Fasukh Maghribi, Kayu Maryam, Mastika, Kendar, dan Daun Bidara Kering.",
    "- Penggunaan: Digunakan sebagai media pengasapan (tabakhhur) secara langsung kepada pasien untuk memusnahkan pengaruh sihir, gangguan jin, angin merah (rih ahmar), dan ikatan gaib (marbuth).",
]

FORBIDDEN = [
    "arabic-manuscript-translator",
    "Berdasarkan format pola",
    "instruksi Anda untuk menuliskan",
    "Pada gambar yang dilampirkan",
    "source 12",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi",
    "[Halaman",
    "Sisi Kanan",
    "Sisi Kiri",
    "Tabel Wafaq dan Asma",
    "Deretan Rajah dan Huruf Tlasim",
    "(Ekstraksi Ritual)",
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
    if page == 66:
        return (
            [("ar", x) for x in AR66]
            + [("img", None)]
            + [("la", x) for x in LAT66]
            + [("te", x) for x in TERJ66]
        )
    return (
        [("ar", x) for x in AR67[:4]]
        + [("img", None)]
        + [("ar", x) for x in AR67[4:]]
        + [("la", x) for x in LAT67]
        + [("te", x) for x in TERJ67]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 66:
        return AR66 + [""] + LAT66 + TERJ66 + [""]
    return AR67[:4] + [""] + AR67[4:] + LAT67 + TERJ67 + TATACARA + [""]


def expected_image_position(page: int) -> int:
    return len(AR66) if page == 66 else 4


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[66] + 1])
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[66], heads[67])
        if texts[i].startswith("(At ta'awwudzu min kulli makruuhin)")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[66], heads[67])
        if texts[i].startswith("“Perlindungan dari segala yang dibenci.”")
    )
    blank_tpl = deepcopy(els[heads[67] - 1])
    if texts[heads[67] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (66, 67):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[66]].getparent()
    removed = 0
    inserted = 0
    for n in (66, 67):
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

    for n in (66, 67):
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

    revised = "\n".join(ot[oh[66] : oh[68]])
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
    print("H66_67_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
