#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 62-63 revision to the final DOCX.

Only the supplied Arabic, Latin, Indonesian, and integrated practice
text is inserted.  Carried-over material from the pasted source is
excluded: the workspace/format introduction, image/source mapping,
numbered section labels, [Halaman ...] markers, markdown bullets in
textual lists, and the parenthetical section label "(Ekstraksi
Ritual)".  Non-literal heading glosses "(Pemuka Jin)" and
"(Khodam Bintang/Hari)" are omitted.  The supplied Tata Cara Praktik
replaces the old practice tails of both units and is placed at the
end of Halaman 63.
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

AR62 = [
    '" أَسْمَاءُ سَلَاطِينِ الْمَلَائِكَةِ "',
    "١- جَبْرِيلُ الْقَوِيُّ الْأَمِينُ",
    "٢- مِيكَائِيلُ مَلِكُ الْأَرْزَاقِ",
    "٣- عِزْرَائِيلُ مُوَكَّلٌ بِالْأَرْوَاحِ",
    "٤- إِسْرَافِيلُ مُوَكَّلٌ بِالنَّفْخِ فِي الصُّورِ",
    '" أَسْمَاءُ الْمُلُوكِ السَّبْعَةِ "',
    "١- مُذْهَبٌ",
    "٢- مُرَّةُ",
    "٣- الْأَحْمَرُ",
    "٤- بُرْقَانُ",
    "٥- شَمْهُورُشُ",
    "٦- الْأَبْيَضُ",
    "٧- مَيْمُونٌ",
    "مسئول عن يوم الاحد",
    "مسئول عن يوم الاثنين",
    "مسئول عن يوم الثلاثاء",
    "مسئول عن يوم الاربعاء",
    "مسئول عن يوم الخميس",
    "مسئول عن يوم الجمعة",
    "مسئول عن يوم السبت",
]
LAT62 = [
    "Asmā'u salāṭīnil-malā'ikati",
    "1- Jabrīlul-qawiyul-amīnu",
    "2- Mīkā'īlu malikul-arzāqi",
    "3- ‘Izrā'īlu muwakkalun bil-arwāḥi",
    "4- Isrāfīlu muwakkalun bin-naf-ḫi fiṣ-ṣūri",
    "Asmā'ul-mulūkis-sab‘ati",
    "1- Mudzhabun",
    "2- Murratun",
    "3- Al-Aḥmaru",
    "4- Burqānun",
    "5- Syamhūrusyu",
    "6- Al-Abyaḍu",
    "7- Maimūnun",
    "Mas'ūlun ‘an yaumil-aḥadi",
    "Mas'ūlun ‘an yaumil-itsnaini",
    "Mas'ūlun ‘an yaumit-tsulātsā'i",
    "Mas'ūlun ‘an yaumil-arbi‘ā'i",
    "Mas'ūlun ‘an yaumil-khamīsi",
    "Mas'ūlun ‘an yaumil-jumu‘ati",
    "Mas'ūlun ‘an yaumis-sabti",
]
TERJ62 = [
    '"Nama-nama Penghulu Malaikat"',
    "Jibril (Malaikat yang Kuat lagi Terpercaya)",
    "Mikail (Malaikat Pengurus Rezeki)",
    "Izrail (Malaikat yang Diserahi mengurus Arwah/Nyawa)",
    "Israfil (Malaikat yang Diserahi meniup Sangkakala)",
    '"Nama-nama Tujuh Raja Jin"',
    "Mudzhab",
    "Murrah",
    "Al-Ahmar",
    "Burqan",
    "Shamhurush",
    "Al-Abyad",
    "Maimun",
    "Bertanggung jawab atas hari Ahad",
    "Bertanggung jawab atas hari Senin",
    "Bertanggung jawab atas hari Selasa",
    "Bertanggung jawab atas hari Rabu",
    "Bertanggung jawab atas hari Kamis",
    "Bertanggung jawab atas hari Jumat",
    "Bertanggung jawab atas hari Sabtu",
]

AR63 = [
    '" أَسْمَاءُ الرُّؤُوسِ الْأَرْبَعَةِ "',
    "١- مَازِرُ ٢- كَطَمُ ٣- قَسْوَرَةُ ٤- طَيْكَلُ",
    '" أَسْمَاءُ الرُّوحَانِيَّةِ السَّبْعَةِ "',
    "١- رُوفَائِيلُ ٢- جَبْرَائِيلُ ٣- سَمْسَمَائِيلُ ٤- مِيكَائِيلُ ٥- صَرْفِيائِيلُ ٦- عَنْبَائِيلُ ٧- كَسْفِيائِيلُ",
    "هَكَذَا أَخِي الْمُؤْمِنَ أَقْدَمُ لَكَ كُلَّ شَيْءٍ عَنِ الْأَيَّامِ فَإِنْ أَرَدْتَ عِلَاجَ أَحَدٍ فِي أَيِّ يَوْمٍ مِنَ الْأَيَّامِ السَّبْعَةِ عَلَيْكَ بِاحْضَارِ الْمَلِكِ الْعُلْوِيِّ الْيَوْمِ وَالْمَلِكِ الرُّوحَانِيِّ بِالِاسْتِعَانَةِ بِالرُّؤُوسِ الْأَرْبَعَةِ مَعَ الكَوَاكِبِ وَالْبُخُورِ وَالْعَزِيمَةِ وَاصْرِفِ الْعُمَّارَ ثُمَّ ابْدَأِ الْعِلَاجَ مَعَ الْقَرِينِ فَهُوَ يَطْبَعُ هَذِهِ الْأَسْمَاءَ كُلَّهَا .",
    "وَنَكْتَفِي بِهَذَا الْقَدْرِ فِي كِتَابٍ آخَرَ .",
    "( تبطيل السحر وبخور لجميع الرياح مجرب )",
    "تَنْشْلُوكَ ٢ طِلَمَاسَحُ ٢ أَطْسُهَ ٢ اسكُمويه ٢ عَضْبِيرَةَ ٢ حَكْمُوااْ تَنْسَبِهِ ٢",
    "بِحَقِّ هَذِهِ الْأَسْمَاءِ عَلَيْكَ يَاسِيدَ بَيْظُطْرُوى اصْرِفْ وَابْطِلِ الْمَرَضَ وَالْعَرَضَ والقرائن والتوابع والزوابع والريح الاحمر والداء الاكبر والعين والنفس والحسد",
]
LAT63 = [
    "Asmā'ur-ru'ūsil-arba‘ah",
    "1- Māziru, 2- Kaṭamu, 3- Qaswaratu, 4- Ṭaikalu",
    "Asmā'ur-rūḥāniyyatis-sab‘ati",
    "1- Rūfā'īlu, 2- Jabrā'īlu, 3- Samsamā'īlu, 4- Mīkā'īlu, 5- Ṣarfiyā'īlu, 6- ‘Anbā'īlu, 7- Kasfiyā'īlu",
    "Hāżakā akhīl-mu'mina uqdimu laka kulla syai'in ‘anil-ayyāmi, fa-in aradta ‘ilāja aḥadin fī ayyi yaumin minal-ayyāmiis-sab‘ati ‘alaika bi-iḥḍāril-malikil-‘ulwiyyil-yauma wal-malikir-rūḥāniyya bil-isti‘ānati bir-ru'ūsil-arba‘ati ma‘al-kawākibi wal-bukhūri wal-‘azīmati wa iṣrifil-‘ummāra tsumma ibda'il-‘ilāja ma‘al-qarīni fahuwa yaṭba‘u hāżihil-asmā'a kullahā.",
    "Wa naktafī bihāżal-qadri fī kitābin ākhar.",
    "(Tabṭīlus-siḥri wa bukhurun lijamī‘ir-riyāḥi mujarrab)",
    "Tansylūka (2x), Ṭilamāsahu (2x), Aṭsuha (2x), Iskūmuhi (2x), ‘Aḍbīratu (2x), Ḥakmuwān tansabihi (2x)",
    "Biḥaqqi hāżihil-asmā'i ‘alaika yā sayyida Baiẓuṭruwā iṣrif wa abṭilil-maraḍa wal-‘araḍa wal-qarā'ina wat-tawābi‘a waz-zawābi‘a war-rīḥal-aḥmara wad-dā'al-akbara wal-ceyna wan-nafsa wal-ḥasada.",
]
TERJ63 = [
    '"Nama-nama Empat Pimpinan"',
    "Maziru, 2. Kathamu, 3. Qaswaratu, 4. Thaikalu",
    '"Nama-nama Tujuh Ruhaniyah"',
    "Rufa'il, 2. Jabra'il, 3. Samsama'il, 4. Mikail, 5. Sharfiyail, 6. Anbayil, 7. Kasfiyail",
    "Begitulah wahai saudaraku yang beriman, aku telah mempersembahkan kepadamu segala sesuatu tentang hari-hari. Maka jika engkau ingin mengobati seseorang pada hari apa saja dari tujuh hari tersebut, engkau wajib menghadirkan Raja Langit (Ulwiy) hari itu serta Raja Ruhaniyyah dengan meminta bantuan kepada Empat Pemimpin (Ar-Ru'us Al-Arba'ah), disertai dengan (penyesuaian) planet-planetnya (kawakib), bukhur (wewangian), dan azimat/azimah. Lakukanlah sharful 'ummar (menyingkirkan penunggu tempat), kemudian mulailah pengobatan terhadap Qarin (jin pendamping), karena ia akan tunduk pada seluruh nama-nama ini.",
    "Dan kita cukupkan sampai di sini sekadar kadar ini pada kitab yang lain.",
    "(Metode Membatalkan Sihir dan Buhur untuk Segala Macam Penyakit Angin/Medis-Nonmedis yang Telah Teruji):",
    "Tansyluka (2x), Tilamashahu (2x), Athsuha (2x), Iskumuhi (2x), Adbiratu (2x), Hakmuwan tansabihi (2x).",
    '"Demi hak nama-nama ini, wahai Tuan Baizhutruwa, singkirkanlah dan batalkanlah penyakit, gangguan fisik, unsur qarin, unsur tawabi\' (pengikut), zawabih (angin puyuh), angin merah (rih ahmar), penyakit berat, \'ain (pandangan mata jahat), gangguan jiwa (nafs), dan hasad (dengki)."',
]

TATACARA = [
    "4. Tata Cara Praktik",
    "Berdasarkan Halaman 62 dan 63, bab ini merangkum kunci makrifat elemen hari dan tata cara penarikan/pengobatan menggunakan bantuan hizib/azimah raja hari dan empat pemuka jin.",
    "Langkah-Langkah Praktik Pengobatan / Ruqyah:",
    "- Penyelarasan Hari & Raja Jin: Jika ingin melakukan pengobatan atau ritual pada hari tertentu (misal hari Ahad), sesuaikan dengan Raja Jin yang bertugas pada hari tersebut (misal: Raja Mudzhab untuk hari Ahad, Murrah untuk Senin, dst.).",
    "- Keterlibatan Unsur Ruhani: Panggil atau hadirkan energi/khodam Raja Ulwiy dan Ruhaniyyah hari tersebut dengan meminta bantuan kepada 4 Pemimpin utama (Maziru, Kathamu, Qaswaratu, Thaikalu).",
    "- Syarat Pendukung: Pengobatan harus disesuaikan dengan planet (kawakib) yang menaungi hari itu, membakar bukhur yang sesuai, serta membaca azimah yang selaras.",
    "- Pembersihan Lokasi (Sharful 'Ummar): Sebelum memulai terapi pada pasien, wajib melakukan sharful 'ummar (mengusir atau meminta izin penghuni gaib tempat tersebut agar tidak mengganggu proses pengobatan).",
    "- Eksekusi Pembatalan Sihir: Bacakan Asma' Suryani/Sya'tsah yang tertera di halaman 63 (Tansyluka, Tilamashahu, dst.) sebanyak dua kali ulangan secara beruntung, ditutup dengan doa permohonan kepada entitas penjaga/pemegang asma tersebut (Baizhutruwa) agar melenyapkan seluruh pengaruh sihir, angin merah, qarin, 'ain, hingga penyakit berat dari tubuh pasien.",
]

UNITS = {
    62: AR62 + LAT62 + TERJ62,
    63: AR63 + LAT63 + TERJ63 + TATACARA,
}
COUNTS = {
    62: (len(AR62), len(LAT62), len(TERJ62), 0),
    63: (len(AR63), len(LAT63), len(TERJ63), len(TATACARA)),
}
FORBIDDEN = [
    "arabic-manuscript-translator",
    "Berdasarkan format pola",
    "Pada gambar yang dilampirkan",
    "source 10",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi Washal",
    "[Halaman",
    "(Ekstraksi Ritual)",
    "(Pemuka Jin)",
    "(Khodam Bintang/Hari)",
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


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    if any(has_drawing_el(els[i]) for i in range(heads[62], heads[64])):
        raise AssertionError("units 62-63 unexpectedly carry an image")

    arab_tpl = deepcopy(els[heads[62] + 1])
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[62], heads[63])
        if texts[i].startswith("«Asmaa-us salaathiinil")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[62], heads[63])
        if texts[i].startswith("“Nama-nama para sultan malaikat”")
    )
    blank_tpl = deepcopy(els[heads[63] - 1])
    if texts[heads[63] - 1].strip() != "":
        raise AssertionError("blank template mismatch")

    body = els[heads[62]].getparent()
    removed = 0
    for n in (62, 63):
        heading_el = els[heads[n]]
        next_heading_el = els[heads[n + 1]]
        node = heading_el.getnext()
        while node is not None and node is not next_heading_el:
            nxt = node.getnext()
            if node.tag == qn("w:p"):
                body.remove(node)
                removed += 1
            node = nxt

        arab_count, latin_count, terj_count, _ = COUNTS[n]
        for pos, text in enumerate(UNITS[n]):
            template = (
                arab_tpl
                if pos < arab_count
                else latin_tpl
                if pos < arab_count + latin_count
                else terj_tpl
            )
            next_heading_el.addprevious(make_para(template, text))
        next_heading_el.addprevious(make_para(blank_tpl, ""))

    doc.save(TARGET)

    out = Document(TARGET)
    ot = [p.text for p in out.paragraphs]
    oh = find_heads(ot)
    if sorted(oh) != list(range(1, 123)):
        raise AssertionError("headings broken")
    for n in (62, 63):
        got = ot[oh[n] + 1 : oh[n + 1]]
        expected = UNITS[n] + [""]
        if got != expected:
            for a, b in zip(got, expected):
                if a != b:
                    print(f"UNIT {n} MISMATCH:\n got: {a[:120]!r}\n exp: {b[:120]!r}")
            raise AssertionError(f"unit {n} mismatch len {len(got)} vs {len(expected)}")

    revised = "\n".join(ot[oh[62] : oh[64]])
    for fragment in FORBIDDEN:
        if fragment.lower() in revised.lower():
            raise AssertionError(f"carried-over fragment remains: {fragment}")
    if len(out.inline_shapes) != 26:
        raise AssertionError("image count changed")
    if media_hashes(TARGET) != media_hashes(SOURCE_FOR_MEDIA):
        raise AssertionError("media hashes/order changed")

    print(f"removed_old_paras={removed}")
    print(f"inserted_paras={sum(len(v) for v in UNITS.values())}")
    print(f"total_paragraphs={len(ot)}")
    print(f"bytes={TARGET.stat().st_size}")
    print(f"sha256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")
    print("H62_63_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
