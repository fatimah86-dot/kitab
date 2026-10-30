#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 82-83 revision to the final DOCX.

Retains the existing precision wafaq images: Halaman 82 after the
opening numeric sequence (its current position), and Halaman 83
after the Arabic block.  Excludes introductory/layout text,
numbered section labels, [Halaman ...] markers, and "(Ekstraksi
Ritual)".  Places the combined Tata Cara Praktik at the end of
Halaman 83.
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

AR82 = [
    "وجاوى ولبان ذكر وتفاح الجان وبخور السودان ويدفن على باب من شئت وهذا ما تكتب ٥٩٤٢١٣١٢٦٥ و ٨٩٤١١١١",
    "ونزعنا ما في صدورهم من غل اخوانا على سرر متقابلين فجمعناهم جمعا وهو على جمعهم اذا شاء قدير توكلوا يا خدام هذه الايات وهيجوا واجلبوا واسلبوا واجذبوا قلب كذا الى محبه كذا الوحا الوحا العجل العجل الساعة الساعة.",
    "باب محبة بسورة الفاتحة :",
    "تقرأ سورة الفاتحة ٣١ مرة ثم في المرة الاخيرة تكرر آيات نعبد و اياك نستعين ٣١ مرة ثم تقول اللهم كما جمعت بين ذاتك وصفاتك وأسمائك اجمَع بينى وبين روحانيه كذا بحق اهدنا الصراط المستقيم الى اخرها وصلى الله على سيدنا محمد وعلى اله وصحبه وسلم.",
    "باب تلبيس الجثة :",
    "تكتب على الاصابع هذه الاسماء وتتعزم بما تكتب [ada wafaq].",
]
LAT82 = [
    "Wajāwin wa lubānin żakarin wa tufāḥil-jānni wa bukhūris-sūdāni wa yudfanu ‘alā bābi man syi'ta wa hāżā mā taktubu (5942131265 wa 8941111).",
    "Wa naza‘nā mā fī ṣudūrihim min ghillin ikhwāναν ‘alā sururin mutaqābilīn, faja‘alnāhum jam‘an wa huwa ‘alā jam‘ihī iżā syā'a qadīrun tawakkalū yā khuddāma hāżihil-āyāti wa hayyijū wa ajlibū waslubū wajżibū qulba każā ilā maḥabbati każā al-waḥā al-waḥā al-‘ajala al-‘ajala as-sā‘ata as-sā‘ata.",
    "Bābu maḥabbatin bi-sūratil-fātiḥah:",
    "Taqra'u sūratal-fātiḥata 31 marratan tsumma fil-marratil-akhīrati tukarriru āyāte na‘budu wa iyyāka nasta‘īnu 31 marratan tsumma taqūlu allāhumma kamā jama‘ta baina żātika wa ṣifātika wa asmā'ika ijma‘ bainī wa baina rūḥāniyyati każā biḥaqqi ihdināṣ-ṣirāṭal-mustaqīma ilā ākhirihā wa ṣallallāhu ‘alā sayyidinā muḥammadin wa ‘alā ālihī wa ṣaḥbihī wa sallam.",
    "Bābu talbīsil-jutsah:",
    "Taktubu ‘alal-aṣābi‘i hāżihil-asmā'a wa ta'zimu bimā taktubu ( [ada wafaq] ).",
]
TERJ82 = [
    "Menggunakan kemenyan Jawa, luban dzakar, apel jin (tufāh al-jān), dan bukhur Sudan, lalu ditanam di depan pintu orang yang engkau kehendaki. Dan inilah angka/huruf rajah yang harus ditulis: (5942131265 dan 8941111).",
    '"Dan Kami lenyapkan segala rasa dendam yang berada di dalam dada mereka, mereka merasa bersaudara duduk berhadap-hadapan di atas dipan... Tuwakkalulah wahai khodam ayat-ayat ini, gerakkanlah, datangkanlah, rentangkanlah, dan tariklah hati si Fulan kepada kecintaan si Fulan. Al-Waha, Al-Waha, Al-\'Ajal, Al-\'Ajal, As-Sa\'ah, As-Sa\'ah."',
    "Bab Mahabbah (Pelet/Pengasihan) dengan Surah Al-Fatihah:",
    'Bacalah Surah Al-Fatihah sebanyak 31 kali, kemudian pada bacaan yang terakhir, ulangi ayat "Iyyaka na\'budu wa iyyaka nasta\'in" sebanyak 31 kali. Setelah itu, berdoalah: "Ya Allah, sebagaimana Engkau telah mengumpulkan antara Dzat-Mu, Sifat-Mu, dan Asma\'-Mu, maka kumpulkanlah antara aku dan ruhaniyah si Fulan..." hingga akhir Surah Al-Fatihah, ditutup dengan selawat.',
    "Bab Memasukkan / Menyelimuti Jasad (Talbīs Al-Jutsah):",
    "Menuliskan asma'-asma' ini pada jari-jari tangan, lalu membaca azimah dengan apa yang dituliskan: [ada wafaq].",
]

AR83 = [
    "واحد وعشرين مرة والبخور مطلق وهو كزبرة ولبان ذكر فانه يلبس الكف ويصرمه وبرميه الي الارض وهذا ما تكتب وبه تعزم وتقول :",
    "بطو شليش ٢ بقوشليش ٢ بهوشكيش ٢ اهماكيش ٢ بهما هما اجب يا ابى جناح والبس الكف وفرق الاصابع وارمى هذه الجثة الي الارض من هو الاول والاخر والظاهر والباطن وهو بكل شئ عليم اجب بالذي شق سمعك وبصرك وخلقك من نار السموم اجب بالذي تجلى للجبل فجعله دكّا وخر موسى صعقاً.",
    "من لطائف الاسرار",
    "فائدة للأمان من الخوف :",
    "اكتب الطلسم الاتي مع ايات الخوف واية الكرسي في كاغد وبخره بلبان ذكر وجاوى ومستكى وعود ويحمل فانه يذهب الخوف وهذا الطلسم كما ترى [ada wafaq].",
]
LAT83 = [
    "Wāḥidun wa ‘isyrūna marratan wal-bukhūru muṭlaqun wa huwa kuzbaratun wa lubānun żakaru fa-innahu yulbisul-kaffa wa yuṣarramuhu wa yarmīhi ilal-arḍi wa hāżā mā taktubu wa bihi ta‘zimu wa taqūlu:",
    "Baṭū syalyīsin (2x), baqūsyīsin (2x), bahūsyīsin (2x), ihmākyīsin (2x), bahamā hamā ajib yā abā janāḥin wal-busil-kaffa wa farriqil-aṣābi‘a wa armī hāżihil-jutsata ilal-arḍi man huwal-awwalu wal-ākhiru waz-ẓāhiru wal-bāṭinu wa huwa bikulli syai'in ‘alīmun ajib bil-lażī syaqqa sam‘aka wa baṣaraka wa khalaqaka min nāris-sumūmi ajib bil-lażī tajallā lil-jabali faja‘alahu dakkā' wa kharra mūsā ṣa‘iqā.",
    "Min laṭā'ifil-asrār",
    "Fā'idatun lil-amāni minal-khauf:",
    "Uktubil-ṭalasimal-ātī ma‘a āyātil-khaufi wa āyatal-kursiyyi fī kāghadin wa bakh-harhu bilubānin żakarin wa jāwiyin wa mastikatin wa ‘ūdin wa yaḥmalu fa-innahu yażhabul-khaufu wa hāżā-ṭ-ṭalasumu kamā tarā ( [ada wafaq] ).",
]
TERJ83 = [
    "Dibaca sebanyak 21 kali dengan bukhur bebas (yaitu campuran ketumbar dan luban dzakar), maka ia akan membuat telapak tangan (pasangan media) kerasukan/bergerak, lalu membantingnya dan melemparkannya ke tanah. Inilah teks yang harus ditulis dan dijadikan azimah bacaan:",
    '"Baṭū syalyīsin (2x)... Datanglah wahai Abu Janah, pakaikanlah pada telapak tangan, renggangkan jari-jarinya, dan bantinglah jasad ini ke bumi demi (zat) Yang Maha Awal dan Maha Akhir, Maha Zahir dan Maha Batin, dan Dia Maha Mengetahui segala sesuatu..."',
    "Dari Kelembutan Rahasia-Rahasia (Min Laṭā'if Al-Asrār)",
    "Faedah untuk Keamanan dari Rasa Takut:",
    "Tulislah tlasim berikut bersama ayat-ayat tentang rasa takut (seperti ayat ketenangan) dan Ayat Kursi pada selembar kertas. Asapi kertas tersebut dengan luban dzakar, kemenyan Jawa, mastika, dan kayu gaharu, lalu bawalah (dikalungkan/disimpan). Maka rasa takut itu akan hilang. Inilah tlasimnya: [ada wafaq].",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Ritual Mahabbah / Pengasihan Tanam Media (Hal. 82):",
    "- Menyiapkan ramuan bukhur khusus (kemenyan Jawa, luban dzakar, apel jin, bukhur Sudan) beserta tulisan angka/huruf rajah khusus.",
    "- Membacakan ayat mahabbah (QS. Al-Hijr: 47 dan penggalan ayat jam'u) dengan menyertakan nama target (si Fulan) agar tunduk dan mencintai pengamal, lalu bukhur/tulisan tersebut ditanam di depan rumah target.",
    "- Amalan Mahabbah Khusus Surah Al-Fatihah (Hal. 82): Mengamalkan bacaan Surah Al-Fatihah sebanyak 31 kali dengan pengulangan khusus pada ayat Iyyaka na'budu... sebanyak 31 kali di pengujung hitungan, diiringi doa mahabbah mutlak untuk menyatukan batin target.",
    "- Praktik Talbīs Al-Kaff / Gerak Tangan Gaib (Hal. 82 & 83):",
    "- Menuliskan asma' rajah esoteris pada jari-jari tangan.",
    "- Membaca azimah khusus penundukan (Baṭū syalyīsin, Abu Janah, dll.) sebanyak 21 kali diiringi pembakaran bukhur ketumbar dan luban dzakar untuk menarik entitas merasuki atau menggerakkan tangan media (mirip praktik deteksi/mediumship tradisional).",
    "- Azimat Penangkal Rasa Takut / Kecemasan Ekstrem (Hal. 83):",
    "- Menuliskan tlasim khusus perlindungan bersama Ayat Kursi dan ayat-ayat Al-Khauf di atas kertas.",
    "- Melakukan pengasapan (tahnik/bukhur) menggunakan campuran luban dzakar, kemenyan Jawa, mastika, dan kayu gaharu.",
    "- Menyimpan atau membawa tulisan tersebut sebagai perisai batin untuk menghilangkan rasa takut, fobia, atau kecemasan yang berlebihan.",
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
    if page == 82:
        return (
            [("ar", AR82[0]), ("img", None)]
            + [("ar", x) for x in AR82[1:]]
            + [("la", x) for x in LAT82]
            + [("te", x) for x in TERJ82]
        )
    return (
        [("ar", x) for x in AR83]
        + [("img", None)]
        + [("la", x) for x in LAT83]
        + [("te", x) for x in TERJ83]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 82:
        return AR82[:1] + [""] + AR82[1:] + LAT82 + TERJ82 + [""]
    return AR83 + [""] + LAT83 + TERJ83 + TATACARA + [""]


def expected_image_position(page: int) -> int:
    return 1 if page == 82 else 5


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[82] + 1])
    if has_drawing_el(arab_tpl) or not texts[heads[82] + 1].startswith("وَجَاوِيّ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[82], heads[83])
        if texts[i].startswith("Wa jaawiyyun wa lubaanu dzakarin")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[82], heads[83])
        if texts[i].startswith("Daftar lanjutan dalam rangkaian ini menyebut")
    )
    blank_tpl = deepcopy(els[heads[83] - 1])
    if texts[heads[83] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (82, 83):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[82]].getparent()
    removed = 0
    inserted = 0
    for n in (82, 83):
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

    for n in (82, 83):
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

    revised = "\n".join(ot[oh[82] : oh[84]])
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
    print("H82_83_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
