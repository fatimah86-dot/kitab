#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 80-81 revision to the final DOCX.

Neither page has a precision wafaq crop and the supplied text has
no "[ada wafaq]" marker, so none is added.  Excludes the
introductory/layout text, numbered section labels, [Halaman ...]
markers, and "(Ekstraksi Ritual)".  Places the combined Tata Cara
Praktik at the end of Halaman 81.
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

AR80 = [
    "وهذا اصرافه :",
    "انصرف بسلام بامرة وتوكل بما امرتك به بحق هذه الاسماء قياس ٢ كياس ٢ عريوش ٢ بخش ٢ توكل ايها السيد مهربائيل باصراف مرة الى كذا اجب يا مرة وافعل ما امرتك به بحق هذه الاسماء ولا تخالف فتحرق بنار السموم هيا هيا الوحا الوحا العجل العجل الساعة الساعة.",
    "قسم لسعة العقارب والأفاعي :",
    "تقرأ الفاتحة سبعه بدون بسملة ولاتامين ثم تقول :",
    "باسي اذا ضاعت الاسباب يعتدى اذي سيفون الاحباب يا حجابي اذا لم يحجبني حجاب اقسمت عليك باسم ياسمم لاتسرح في الجسم ولا تعوم باذن الحي القيوم بحق سيدي احمد الرفاعي صاحب التوحيد بسره يجننك بريقه حبسك كر اكر اكبر ندى ممليزى فيرد والسماء والطارق الى الترائب اخرج باسم من العروق والمفاصل واللحم والدم والجلد والشعر الى الهوى بحق سيق بني.",
]
LAT80 = [
    "Wa hāżā iṣrāfuh:",
    "Inṣarif bisalāmin bi-amratin wa tawakkal bimā amartuka bihi biḥaqqi hāżihil-asmā'i qiyāsin (2x), kiyāsin (2x), ‘aryūsin (2x), bakhsyin (2x). Tawakkal ayyuhal-sayyidu mahrobā'īlu bi-iṣrāfi marratin ilā każā ajib yā marratu wa if'al mā amartuka bihi biḥaqqi hāżihil-asmā'i wa lā tukhālif fa-tuḥraqu bināris-sumūmi hayā hayā al-waḥā al-waḥā al-‘ajala al-‘ajala as-sā‘ata as-sā‘ata.",
    "Qasamu lis‘atil-‘aqāribi wal-afā‘ī:",
    "Taqra'ul-fātiḥata sab'atan bidūni basmalatin wa lā ta'mīnin tsumma taqūlu:",
    "Bāsī iżā ḍā‘atil-asbābu ya'tadī ażī saifūnal-aḥbābi yā ḥijābī iżā lam yaḥjubnī ḥijābun aqsamtu ‘alaika bismi yā samamu lā tasraḥ fil-jismi wa lā ta‘ūmu bi-iżnil-ḥayyil-qayyūmi biḥaqqi sayyidī aḥmadar-rifā‘ī ṣāḥibis-tawḥīdi bisurrihi yujannunka bi-rīqihi حبsuka kar akar akbar nadā mamlīzī fa-yaruddu was-samā'i wat-ṭāriqi ilal-tarā'ibi ukhruj bismi minal-‘urūqi wal-mafāṣili wal-laḥmi wad-dami wal-jildi wasy-sha‘ri ilal-hawā biḥaqqi sayqi banī.",
]
TERJ80 = [
    "Inilah Tata Cara Pengembalian/Penarikan Khodam (Isrāf):",
    '"Menulislah dengan keselamatan, perintah, dan wakallah dengan apa yang aku perintahkan kepadamu demi hak nama-nama ini: Qiyasin (2x), Kiyasin (2x), \'Aryusin (2x), Bakhsyin (2x). Bertawakallah wahai Tuan Mahrobail dalam mengembalikan Muroh kepada sekian... Datanglah wahai Muroh dan perbuatlah apa yang telah aku perintahkan kepadamu demi hak nama-nama ini, janganlah menyalahi, niscaya engkau akan dibakar dengan api racun. Cepatlah, cepatlah! Al-Waha, Al-Waha, Al-\'Ajal, Al-\'Ajal, As-Sa\'ah, As-Sa\'ah."',
    "القسم لسعة العقارب والأفاعي (Qasam untuk Sengatan Kalajengking dan Ular):",
    "Bacalah Surah Al-Fatihah sebanyak 7 kali tanpa Basmalah dan tanpa Ta'min (Aamiin), kemudian ucapkan:",
    '"Basi... (doa perlindungan dan penawar racun dengan tawasul kepada Asma\' Allah dan Syekh Ahmad Ar-Rifa\'i). Keluarlah wahai racun dari urat, sendi, daging, darah, kulit, dan rambut menuju ke udara demi hak..."',
]

AR81 = [
    "غالب على على بن ابى طالب بحق ما كان وما يكون وبحق ما في اللوح المحفوظ لجميع في مكان اللدغة ومنها الى يسر ظهور بدعق محبه صورة محبه سقفا طيس سقـا طيم اخوان مخبط احم ادم حماء امين بحق السيد نور الدين والسيد سعد الدين اخضع فرن من مسورة كدى كرندى ساق هندی مريش حجاب بسم الله الماء وبحمد الله وصلى الله على سيدنا محمد وعلى اله وصحبه وسلم.",
    "فائدة لرجوع المراة الى زوجها :",
    "يكتب الاتي وتخملها المراة عليها فان الزوج يرجع اليها وهذا ماتكتب البسملة انه عن رجعة لقادر ٧ مرات وان امراة خافت من بعلها نشوداً أو أعراضاً فلا جناح عليهما ان يصلحا بينهما صلحا والصلح خير ٧ مرات والانشراح كلها.",
    "باب للصلح بين الزوجين :",
    "يكتب يوم الخميس فى قوة الهلال والبخور عمال سندورس.",
]
LAT81 = [
    "Ghālibun ‘alā ‘aliyyin bnu abī ṭālibin biḥaqqi mā kāna wa mā yakūnu wa biḥaqqi mā fil-lauhil-maḥfūẓi li-jamī'in fī makānin-lladgati wa minhā ilā yusri ẓuhūrin...",
    "Fā'idatun li-rujū'il-mar'ati ilā zaujihā:",
    "Yaktubul-ātī wa taḥmiluhā-l-mar'atu ‘alaihā fa-innal-zauja yarji‘u ilaihā wa hāżā mā taktubu:",
    'Al-basmalata "Innahū ‘alā raj‘atihi laqādir" (7 marrāt).',
    'Wa "Wa in imra\'atun khāfat min ba\'lihā nusyūdan au i\'rāḍan falā junāḥa ‘alaihimā an yuṣliḥā bainahumā ṣulḥan waṣ-ṣulḥu khair" (7 marrāt).',
    'Wa "Al-Insyirāḥ" kullahā.',
    "Bābun lil-ṣulḥi bainaz-zaujain:",
    "Yaktubu yaumal-khamīsi fī quwwatil-hilāli wal-bukhūru ‘ummālu sandūrsin.",
]
TERJ81 = [
    "(Kelanjutan doa penawar sengatan hewan berbisa dengan tawasul kepada kekuasaan Ali bin Abi Thalib dan rahasia Lauh Mahfuz).",
    "Faedah agar Istri Kembali kepada Suaminya:",
    "Dituliskan ayat-ayat berikut, lalu dibawa/dikalungkan oleh sang istri, maka suami akan kembali kepadanya. Dan inilah yang harus ditulis:",
    'Basmalah, lalu membaca ayat: "Sesungguhnya Allah benar-benar kuasa untuk mengembalikannya" (QS. Thariq: 8) sebanyak 7 kali.',
    'Membaca ayat: "Dan jika seorang wanita khawatir akan nusyuz atau sikap tidak acuh dari suaminya, maka tidak mengapa bagi keduanya mengadakan perdamaian yang sebenar-benarnya, dan perdamaian itu lebih baik" (QS. An-Nisa: 128) sebanyak 7 kali.',
    "Membaca Surah Al-Insyirah secara utuh.",
    "Bab untuk Perdamaian Antara Suami Istri:",
    "Ditulis pada hari Kamis saat bulan sedang kuat (purnama/tumbuh), dan bukhurnya menggunakan Ummal Sandurs.",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Protokol Israf (Pengiriman Pulang Khodam) (Hal. 80): Pembacaan azimah penutup untuk menyudahi ritual pemanggilan atau pengiriman gaib dengan menggunakan asma' khusus (Qiyasin, Kiyasin, 'Aryusin, Bakhsyin) serta ancaman pembakaran energi bagi entitas yang membangkang.",
    "- Ruqyah / Pengobatan Sengatan Kalajengking dan Ular (Hal. 80 & 81):",
    "- Membaca Surah Al-Fatihah 7 kali tanpa Basmalah dan Aamiin.",
    "- Melanjutkan pembacaan mantra/qasam penawar racun penangkal bisa hewan berbisa yang ditiupkan atau diusapkan pada area bekas sengatan.",
    "- Amalan Pengasihan / Rujukan Suami Istri (Hal. 81):",
    "- Menuliskan ayat-ayat mahabbah pengembalian pasangan (QS. Al-Thariq: 8 sebanyak 7x, QS. An-Nisa: 128 sebanyak 7x, dan Surah Al-Insyirah).",
    "- Dijadikan azimat untuk dibawa/dikalungkan oleh pihak istri agar keharmonisan rumah tangga pulih kembali.",
    "- Waktu Khusus Ritual Perdamaian Rumah Tangga (Hal. 81): Penulisan wafaq atau amalan damai suami-istri harus dikerjakan pada hari Kamis dalam kondisi fase bulan yang kuat (fase awal bulan/purnama), disertai pembakaran bukhur jenis Sandurs.",
]

FORBIDDEN = [
    "Berikut adalah transkripsi",
    "berdasarkan gambar manuskrip",
    "Pada tata letak manuskrip",
    "Sisi Kanan",
    "Sisi Kiri",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi",
    "[Halaman",
    "(Ekstraksi Ritual)",
    "&amp;",
]

UNITS = {
    80: AR80 + LAT80 + TERJ80,
    81: AR81 + LAT81 + TERJ81 + TATACARA,
}
COUNTS = {
    80: (len(AR80), len(LAT80)),
    81: (len(AR81), len(LAT81)),
}


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

    if any(has_drawing_el(els[i]) for i in range(heads[80], heads[82])):
        raise AssertionError("units 80-81 unexpectedly carry an image")

    arab_tpl = deepcopy(els[heads[80] + 1])
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[80], heads[81])
        if texts[i].startswith("Wa haadzaa ishrifhu.")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[80], heads[81])
        if texts[i].startswith("“Inilah pemberangkatannya:")
    )
    blank_tpl = deepcopy(els[heads[81] - 1])
    if texts[heads[81] - 1].strip() != "":
        raise AssertionError("blank template mismatch")

    body = els[heads[80]].getparent()
    removed = 0
    inserted = 0
    for n in (80, 81):
        heading_el = els[heads[n]]
        next_heading_el = els[heads[n + 1]]
        node = heading_el.getnext()
        while node is not None and node is not next_heading_el:
            nxt = node.getnext()
            if node.tag == qn("w:p"):
                body.remove(node)
                removed += 1
            node = nxt

        arab_count, latin_count = COUNTS[n]
        for pos, text in enumerate(UNITS[n]):
            template = (
                arab_tpl
                if pos < arab_count
                else latin_tpl
                if pos < arab_count + latin_count
                else terj_tpl
            )
            next_heading_el.addprevious(make_para(template, text))
            inserted += 1
        next_heading_el.addprevious(make_para(blank_tpl, ""))

    doc.save(TARGET)

    out = Document(TARGET)
    ot = [p.text for p in out.paragraphs]
    oh = find_heads(ot)
    if sorted(oh) != list(range(1, 123)):
        raise AssertionError("headings broken")
    for n in (80, 81):
        got = ot[oh[n] + 1 : oh[n + 1]]
        expected = UNITS[n] + [""]
        if got != expected:
            for a, b in zip(got, expected):
                if a != b:
                    print(f"UNIT {n} MISMATCH:\n got: {a[:140]!r}\n exp: {b[:140]!r}")
            raise AssertionError(f"unit {n} mismatch len {len(got)} vs {len(expected)}")
        if any(
            has_drawing_el(out.paragraphs[i]._element)
            for i in range(oh[n], oh[n + 1])
        ):
            raise AssertionError(f"unit {n} unexpectedly has an image after patch")

    revised = "\n".join(ot[oh[80] : oh[82]])
    if "[ada wafaq]" in revised:
        raise AssertionError("unexpected [ada wafaq] marker inserted")
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
    print("H80_81_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
