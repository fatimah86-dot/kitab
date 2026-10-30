#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 78-79 revision to the final DOCX.

Retains the existing precision wafaq image on Halaman 78 directly
after its "[ada wafaq]" marker; Halaman 79 has no crop image.
Excludes introductory/layout text, numbered section labels,
[Halaman ...] markers, the editorial description after the Arabic
marker, and "(Ekstraksi Ritual)".
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

AR78 = [
    "وهو السميع العليم اسكن ايها الوجع والصداع والشقيقة والريح السوء من فلان او فلانه اسكن ساكنا كما سكن عرش الرحمن اسكن ايها الضارب والصداع والشقيقة ان يشاء يسكن الريح فيظللن رواكد علي ظهرها ان في ذلك لايات لكل صبار شكور اسكن بحق الم تر الى ربك كيف مد الظل ولو شاء لجعله ساكنا ثم جعلنا الشمس عليه دليلا ثم قبضنا الينا قبضا يسيرا اسكن ايها الوجع اسكن كما سكن كل شئ لعظمته اسكن بحق لو انزلنا هذا القرآن على جبال الى اخر السورة وهذا هو الوفق.",
    "[ada wafaq]",
]
LAT78 = [
    "Wa huwas-samī‘ul-‘alīmu uskun ayyuhal-waja‘u waṣ-ṣudā‘u wasy-syīqatu war-rīḥus-sū'u min fulānin au fulānata uskun sākinan kamā sakana ‘arsyur-raḥmāni uskun ayyuhal-ḍāribu waṣ-ṣudā‘u wasy-syīqatu in yasyā' yuskinir-rīḥa fayaẓlalna rawākida ‘alā ẓahrihā inna fī żālika laāyātin likulli ṣabbārin syakūrin uskun biḥaqqi alam tara ilā rabbika kaifa maddaẓ-ẓilla wa lau syā'a laja‘alahū sākinan tsumma ja‘alnas-syamsa ‘alaihi dalīlan tsumma qabaḍnā ilainā qabḍan yasīrā uskun ayyuhal-waja‘u uskun kamā sakana kullu syai'in li‘aẓamatihī uskun biḥaqqi lau anzalnā hāżal-qur'āna ‘alā jabalin ilā ākhiris-sūrati wa hāżā huwal-wafqu.",
    "( [ada wafaq] )",
]
TERJ78 = [
    "Dan Dialah Yang Maha Mendengar lagi Maha Mengetahui. Tenang dan redalah wahai rasa sakit, kepala berdenyut (pusing), migrain, dan angin buruk dari si Fulan atau Fulanah. Tenanglah sebagaimana tenangnya 'Arsy Allah Yang Maha Pemurah. Tenanglah wahai rasa sakit yang berdenyut, migrain, dan pusing; jika Allah menghendaki, Dia akan menenangkan angin sehingga jadilah kapal-kapal itu terdiam kaku di atas permukaan laut, sesungguhnya pada yang demikian itu terdapat tanda-tanda bagi setiap orang yang banyak bersabar lagi banyak bersyukur (QS. Asy-Syura: 33, Luqman: 31). Tenanglah demi hak: Apakah kamu tidak memperhatikan (ciptaan) Tuhanmu, bagaimana Dia memanjangkan bayang-bayang... (QS. Al-Furqan: 45 hingga akhir ayat). Tenanglah wahai rasa sakit, sebagaimana tenangnya segala sesuatu karena keagungan-Nya. Tenanglah demi hak: Kalau sekiranya Kami menurunkan Al-Quran ini kepada sebuah gunung... (QS. Al-Hasyr: 21) hingga akhir surah. Dan inilah Wafaqnya:",
    "[ada wafaq]",
]

AR79 = [
    "الفصل السادس عشر",
    "باب ارسال عون شديد",
    "إذا اردت العمل به تصوم يوم السبت برياضة ثم خذ جريدة خضراء واكتب عليها سورة والعاتيات ضحبا الى اخرها وبعد العشاء تأخذ مجمَرة جديدة وتبخر بصندل على نار قوية وانت ماسك الجريدة في يدك وعزم بالقسم سبعين مرة حتى تهتز الجريدة في يدك فاصرفه لمن تريد باصرافه الاتي ولا تتأخر بل تصرفه بكل سرعة لمن تريده وان تأخرت يضربك بالمجمَرة التى أمامك وهذا هو القسم تقول :",
    "سريع ٢ رفيع ٢ مطيع ٢ سلطيع ٢ هليع ٢ مليع يخلفش ٢ بمخلفش ٢ بحق ديعوج ٢ دليكوش ٢ اصطفار ٢ عمياخ اجب يا مرة وتوكل بكذا مسلطك عليه . نزلت ملائكة الغضب على من عصى الله ومن يشرك بالله فينزل عليه كسفا من السماء فخطفه الطير او تهوي به الريح في مكان سحيق الوحا العجل الساعة الساعة.",
]
LAT79 = [
    "Al-Faṣlus-sādisu ‘asyara",
    "Bābu irsāli ‘aunin syadīd",
    "Iżā aradtal-عمل bihi taṣūmu yaumas-sabti bi-riyāḍatin tsumma khuż jarīdatan khaḍrā'a wa uktub ‘alaihā sūrata wal-‘ādِيāti ḍabḥan ilā ākhirihā wa ba‘dal-‘isysyā'i ta'khużum-majmaratan jadīdatan wa tubakhiru bi-ṣandalin ‘alā nārin qawiyatin wa anta mā sikul-jarīdata fī yadika wa ‘azim bil-qasmi sab‘īna marratan ḥattā tahtaza-l-jarīdatu fī yadika fa-iṣrifhu liman turīdu bi-iṣrāfihil-ātī wa lā tata'akhkhar bal taṣrafuhu bikulli sur‘atin liman turīdu wa in ta'akhkharta yaḍribuka bil-majmaratil-latī amāmaka wa hāżā huwal-qasmu taqūlu:",
    "Sarī‘un (2x), rafī‘un (2x), muṭī‘un (2x), salṭīun (2x), halī‘un (2x), malī‘un (2x), yukhlifusy (2x), bimukhlifusy (2x), biḥaqqi di‘ūjin, dalīkūsyin, iṣṭafārin, ‘amyākha, ajib yā murratu wa tawakkal bikażā musallaṭaka ‘alaihi. Nazalat malā'ikatul-ghaḍabi ‘alā man ‘aṣallāha wa man yusyrik billāhi fa-yanzilu ‘alaihi kisfan minas-samā'i fakhaṭafuhul-ṭairu au tahwī bihir-rīḥu fī makānin saḥīqin al-waḥā al-‘ajala as-sā‘ata as-sā‘ata.",
]
TERJ79 = [
    "Fasal Keenam Belas: Bab Pengiriman Bantuan Gaib yang Kuat (Irsāl 'Aun Syadīd)",
    "Apabila engkau ingin mengamalkan ilmu ini, berpuasahlah pada hari Sabtu dengan melakukan riyadah (laku spiritual), kemudian ambillah sehelai pelepah daun yang hijau, lalu tulislah di atasnya Surah Al-'Adiyat (wal-'adiyati dhabha...) sampai akhir surah.",
    "Selepas shalat Isya, ambillah sebuah tempat perbuhuran (majmarah) yang baru, lalu bakarlah kayu cendana (sandali) di atas api yang besar. Sementara tanganmu memegang pelepah daun tadi, bacakanlah Azimah/Qasam sebanyak 70 kali hingga pelepah daun itu bergetar di tanganmu.",
    "Setelah bergetar, arahkan/palingkan ia kepada siapa saja yang engkau kehendaki dengan bacaan penarikan/pengarahan (ishraf) berikut. Janganlah menunda, laksanakan dengan cepat kepada orang yang engkau kehendaki; karena jika engkau terlambat, ia (khodam) akan memukulmu dengan tempat perbuhuran yang ada di hadapanmu.",
    "Dan inilah bacaan Qasam (sumpah) yang harus diucapkan:",
    "\"Sarī'un (2x), Rafī'un (2x), Muṭī'un (2x), Salṭī'un (2x), Halī'un (2x), Malī'un (2x), Yukhlifusy (2x), Bimukhlifusy (2x), demi hak Di'uj, Dalikusy, Isthafar, 'Amyakh. Datanglah wahai (Raja Jin) Muroh, dan wakilkanlah urusan sekian... yang telah aku kuasakan atasnya. Telah turun malaikat-malaikat kemurkaan atas orang yang mendurhakai Allah dan mempersekutukan Allah, maka jatuhlah ia dari langit lalu disambar oleh burung atau diterbangkan oleh angin ke tempat yang jauh. Al-waha, al-'ajal, as-sa'ah, as-sa'ah.\"",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Pengobatan / Ruqyah Mengatasi Sakit Kepala Menengah, Migrain, dan Nyeri (Hal. 78):",
    "- Membacakan ayat-ayat perlindungan dan penenang (seperti penggalan QS. Asy-Syura: 33, Al-Furqan: 45, dan Al-Hasyr: 21) yang ditujukan untuk meredakan denyutan sakit kepala atau migrain pada pasien.",
    "- Menyertakan penggunaan media rajah/wafaq penyembuhan yang tertera pada halaman tersebut.",
    "- Protokol Amalan Pengiriman Khodam / Kekuatan Gaib (Irsāl 'Aun Syadīd) (Hal. 79):",
    "- Puasa & Riyadah: Memulai amalan dengan berpuasa pada hari Sabtu disertai ritual spiritual.",
    "- Media Pelepah Hijau: Menyiapkan sehelai pelepah daun hijau dan menuliskan Surah Al-'Adiyat di atasnya.",
    "- Pengasapan & Pembacaan Qasam: Setelah Isya, membakar kayu cendana di dalam tempat perbuhuran (majmarah) baru, memegang pelepah daun, lalu membaca Qasam khusus pengiriman khodam sebanyak 70 kali sampai pelepah daun tersebut bergetar secara nyata di tangan.",
    "- Peringatan Pengendalian: Praktisi harus sigap mengarahkan energi atau khodam tersebut dengan cepat sesuai hajatnya, karena keterlambatan kendali dikhawatirkan mendatangkan bahaya fisik dari energi khodam yang memanas (terpukul wadah bukhur).",
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
    "Tabel Wafaq Rajah",
    "Nama Khodam/Malaikat",
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
    if page == 78:
        return (
            [("ar", x) for x in AR78]
            + [("img", None)]
            + [("la", x) for x in LAT78]
            + [("te", x) for x in TERJ78]
        )
    return (
        [("ar", x) for x in AR79]
        + [("la", x) for x in LAT79]
        + [("te", x) for x in TERJ79]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 78:
        return AR78 + [""] + LAT78 + TERJ78 + [""]
    return AR79 + LAT79 + TERJ79 + TATACARA + [""]


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[78] + 1])
    if has_drawing_el(arab_tpl) or not texts[heads[78] + 1].startswith("وَهُوَ السَّمِيعُ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[78], heads[79])
        if texts[i].startswith("Wa huwas samii'ul 'aliimu.")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[78], heads[79])
        if texts[i].startswith("“") and "dan Dialah Yang Maha Mendengar" in texts[i][:60]
    )
    blank_tpl = deepcopy(els[heads[79] - 1])
    if texts[heads[79] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    found78 = [
        deepcopy(els[i])
        for i in range(heads[78], heads[79])
        if has_drawing_el(els[i])
    ]
    if len(found78) != 1:
        raise AssertionError(f"unit 78 image count {len(found78)} != 1")
    if any(has_drawing_el(els[i]) for i in range(heads[79], heads[80])):
        raise AssertionError("unit 79 unexpectedly carries an image")
    image78 = found78[0]

    body = els[heads[78]].getparent()
    removed = 0
    inserted = 0
    for n in (78, 79):
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
                next_heading_el.addprevious(deepcopy(image78))
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

    for n in (78, 79):
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
        expected_positions = [2] if n == 78 else []
        if image_positions != expected_positions:
            raise AssertionError(
                f"unit {n} image positions {image_positions}, expected {expected_positions}"
            )

    revised = "\n".join(ot[oh[78] : oh[80]])
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
    print("H78_79_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
