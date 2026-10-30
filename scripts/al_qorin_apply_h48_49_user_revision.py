#!/usr/bin/env python3
"""Replace Halaman 48-49 in AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx.

User-supplied verbatim revision (2026-10-30), except the wafaq: the
existing image paragraph in unit 49 keeps its element and position
(after the Terjemahan). The "✡ wafak" placeholder at the end of the
user's Arabic p.49 is rendered as "✡" only. The user's extra
"4. Tata Cara Praktik" section (with manuscript-authenticity notes)
follows the wafaq. Markdown artifacts (* bullets, &gt;) are rendered
as plain paragraphs ("- " bullets, quote lines without ">").
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

AR48 = [
    "الْفَصْلُ الْحَادِي عَشَرَ",
    "أَنْوَاعُ عِلَاجَاتِ الْجِنِّ",
    "أَعْلَمُ أَيُّهَا الطَّالِبُ الْمُؤْمِنُ إِنْ أَرَدْتَ أَنْ أُعَلِّمَكَ بِأَدْوِيَةٍ يَنْتَفِعُ بِهَا مَنْ بَعْدَكَ وَأُشَارِكُكَ فِي الْأَجْرِ إِنْ شَاءَ اللَّهُ تَعَالَى أَنَّ هُنَاكَ أَنْوَاعاً مِنَ الْجِنِّ يُصْرِعُونَ النِّسَاءَ وَالرِّجَالَ وَهُمْ مُخْتَلِفُونَ أَعْرِفُ مِنْهُمْ خَلْقاً كَثِيراً وَلَكِنْ إِنْ شَاءَ اللَّهُ تَعَالَى سَأُعَرِّفُكَ أَيُّهَا الْمُؤْمِنُ بِسَبْعِينَ رَهْطٍ تَقْرِيباً لَكَ وَلِغَيْرِكَ كُلُّ رَهْطٍ مِنْهَا أَيْ مِنَ الْجِنِّ فِيهِ سَبْعُونَ أَلْفَ قَبِيلَةٍ وَكُلُّ قَبِيلَةٍ فِيهَا سَبْعُونَ أَلْفَ .",
    "وَلَوْ وَقَعَتْ إِبْرَةٌ مِنَ السَّمَاءِ مَا وَقَعَتْ إِلَّا عَلَيْهِمْ .",
    "فَالْعَفَارِيتُ مِنْهُمْ سَكَنُوا الْعُيُونَ وَالْكُهُوفَ وَالشَّيَاطِينُ سَكَنُوا الدِّيَارَ وَعَمَرُوا الْقُبُورَ ( يَعْنِي نَزَلُوا بِقُرْبِ قُبُورِ الْإِنْسِ )",
    "وَأَمَّا الطَّوَاغِيتُ فَسَكَنُوا بِقُرْبِ الدَّمِ فَإِنَّمَا نُحِرَ دَمٌ حَضَرُوا عِنْدَهُ وَإِنْ هُرِيقَتْ نُقْطَةُ دَمٍ قَدِمُوا إِلَيْهَا فِي أَسْرَعَ مِنَ الْبَرْقِ الْخَاطِفِ وَالرِّيحِ الْعَاصِفِ .",
    "وَبَعْضُ الزَّوَابِعَةِ رَكِبُوا الرِّيَاحَ وَبَعْضٌ مِنْ كِبَارِ الشَّيَاطِينِ سَكَنُوا بِقُرْبِ النَّارِ لِأَنَّ الْأَصْلَ الْأَوَّلَ مِنْهَا .",
]
LAT48 = [
    "Al-Faṣlul-ḥādī ‘asyara",
    "Anwā‘u ‘ilājātil-jinn",
    "A‘lamu ayyuhaṭ-ṭālibul-mu'minu in aradta an u‘allimaka bi'adwiyatin yantafi‘u bihā mam ba‘daka wa usyārikuka fil-ajri in syā'allāhu ta‘ālā, anna hunāka anwā‘am-minal-jinni yuṣri‘ūnan-nisā'a war-rijāla wa hum mukhtalifūna, a‘rifu minhum khalqan katsīran, wa lakin in syā'allāhu ta‘ālā sa'u‘arrifuka ayyuhal-mu'minu bisab‘īna rahṭin taqrīban laka wa lighairika kullu rahṭim-minhā aim-minal-jinni fīhi sab‘ūna alfa qabīlatin wa kullu qabīlatin fīhā sab‘ūna alf.",
    "Wa lau waqa‘at ibratum-minas-samā'i mā waqa‘at illā ‘alaihim.",
    "Fal-‘afārītu minhum sakanūl-‘uyūna wal-kuhūfa, wasy-syayāṭīnu sakanūd-diyāra wa ‘amarūl-qubūra (ya‘nī nazalū biqurbi qubūril-insi).",
    "Wa ammat-ṭawāghītu fasakanū biqurbid-dami fa-innamā nuḥira damun ḥaḍarū ‘indahū wa in hurīqat nuqṭatu damin qadimū ilaihā fī asra‘a minal-barqil-khāṭifi war-rīḥil-‘āṣif.",
    "Wa ba‘ḍuz-zawābi‘ati rakibūr-riyāḥa, wa ba‘ḍum-min kibārisy-syayāṭīni sakanū biqurbin-nāri li'annal-aṣlal-awwala minhā.",
]
TERJ48 = [
    "Fasal Kesebelas",
    "Macam-macam Pengobatan Jin",
    "Ketahuilah wahai penuntut (ilmu) yang beriman, apabila engkau menginginkan agar aku mengajarkan kepadamu obat-obatan yang bermanfaat bagi orang-orang setelahmu dan aku turut menyertaimu dalam pahalanya—insya Allah Ta'ala—(ketahuilah) bahwa sesungguhnya terdapat berbagai macam jin yang merasuk/merobohkan (mashru') perempuan maupun laki-laki, dan wujud mereka berbeda-beda. Aku mengenali sangat banyak makhluk di antara mereka, namun—insya Allah Ta'ala—aku akan memperkenalkan kepadamu wahai orang yang beriman, sekitar 70 golongan demi (kebaikan) dirimu dan orang selainmu. Setiap satu golongan tersebut—yakni dari bangsa jin—di dalamnya terdapat 70 ribu kabilah, dan setiap satu kabilah di dalamnya terdapat 70 ribu (jin). Seandainya sebatang jarum jatuh dari langit, niscaya jarum itu tidak akan jatuh melainkan mengenai mereka (saking banyaknya jumlah mereka).",
    "Maka golongan Ifrit di antara mereka tinggal di mata air dan gua-gua; golongan Setan tinggal di rumah-rumah dan meramaikan kuburan (yakni mereka bermukim di dekat kuburan manusia). Adapun golongan Thaghut, mereka bermukim di dekat darah. Apabila ada darah yang disembelih (ditumpahkan), mereka akan hadir di sana, dan jika ada setetes darah yang mengalir, mereka akan datang menujunya lebih cepat dari kilat yang menyambar dan angin badai. Sebagian golongan Zawabighah (angin puyuh) menunggangi angin, dan sebagian dari dedengkot setan bermukim di dekat api, karena asal-usul penciptaan pertama mereka adalah dari api.",
]

AR49 = [
    "وَبَعْضُ التَّوَاقِيفِ الْعَفَارِيتِ يَعْنِي الْمُتَشَكِّلِينَ عَلَى صُورَةِ الْإِنْسِ سَكَنُوا بِقُرْبِ الْأَشْجَارِ الْعَالِيَةِ وَالشَّوْكِ الْعَلِيقِ وَدَخَلُوا فِي الْبَسَاتِينِ .",
    "وَبَعْضُ السَّبَاسِبِ سَكَنُوا الْجِبَالَ وَالْخَرَائِبَ الْخَالِيَةَ وَكَثْرَةُ هَؤُلَاءِ مُضِرَّةٌ بِالرِّجَالِ وَالنِّسَاءِ مِنْ بَنِي آدَمَ .",
    "وَفِي شَيَاطِينِ الْعَفَارِيتِ مَنْ يُجَامِعُ نِسَاءَ الْإِنْسِ وَبَعْضُهُمْ يُحِبُّونَ أَنْ تَكُونَ الْإِنْسِيَّةُ زَوْجَةً لَهُمْ .",
    "وَبَعْضُهُمْ يُفْسِدُونَ خِلْقَةَ الْإِنْسَانِ أَيْ يُبْطِلُونَ عُضْواً مِنْ أَعْضَائِهِ .",
    "وَلَكِنْ هُنَاكَ سَبْعِينَ وَصْفاً وَمَا يَحْتَاجُ إِلَيْهِمْ مَهِمَّا ظَهَرَ مِنَ الْعِلَاجِ وَأَمَّا أَصْحَابُ الصَّرْعِ فَفِيهِمْ ثَلَاثَةٌ وَأَرْبَعُونَ نَوْعاً كُلُّ نَوْعٍ لَابُدَّ مِنْ عِلَاجِهِ .",
    "( الْأَوَّلُ ) فَمَهْمَا انْصَرَعَ أَوْ امْرَأَةٌ أَوْ صَبِيٌّ أَوْ صَبِيَّةٌ فَاكْتُبْ لَهُ بَيْنَ عَيْنَيْهِ ( أَفَمَنْ كَانَ مُؤْمِناً كَمَنْ كَانَ فَاسِقاً ) إِلَى قَوْلِهِ تَنْزِيلاً نُزُلاً نُزُلاً وَفِي يَدِهِ الْيُمْنَى خَاتَمُ سُلَيْمَانَ وَلَهُ سَبْعَةُ قُرُونٍ فِي بَاطِنِ كُلِّ قَرْنٍ مِنْهَا حَرْفٌ مِنْ حُرُوفِ ف ج ش ث خ ز مَعَ هَذِهِ الْخَوَاتِمِ خَاتَمُ سُلَيْمَانَ ✡",
]
LAT49 = [
    "Wa ba‘ḍut-tawāqīfil-‘afārīti ya‘nīl-mutasyakkilīna ‘alā ṣūratil-insi sakanū biqurbil-asyjāril-‘āliyati wasy-syaukil-‘alīqi wa dakhalū fil-basātīn.",
    "Wa ba‘ḍus-sabāsibi sakanūl-jibāla wal-kharā'ibal-khāliyata wa katsratu hā'ulā'i muḍirratum-bir-rijāli wan-nisā'i mim-banī ādam.",
    "Wa fī syayāṭīnil-‘afārīti may-yujāmi‘u nisā'al-insi wa ba‘ḍuhum yuḥibbūna an takūnal-insiyyatu zaujatal-lahum.",
    "Wa ba‘ḍuhum yufsidūna khilqatal-insāni ai yubṭilūna ‘uḍwam-min a‘ḍā'ih.",
    "Wa lakin hunāka sab‘īna waṣfan wa mā yaḥtāju ilaihim mahimmā ẓahara minal-‘ilāji, wa ammā aṣḥābuṣ-ṣar‘i fafīhim tsalātsatun wa arba‘ūna nau‘an kullu nau‘il-lābudda min ‘ilājih.",
    "(Al-Awwalu) Famahmamm-ṣara‘a au imra'atun au ṣabiyyun au ṣabiyyatun faktub lahū baina ‘ainaihi (Afaman kāna mu'minan kamang-kāna fāsiqan) ilā qaulihi tanzīlan nuzulan nuzulan wa fī yadihil-yumnā khātamu sulaimāna wa lahū sab‘atu qurūnin fī bāṭini kulli qarnim-minhā ḥarfum-min ḥurūfi \"Fā' Jīm Syīn Tsā' Khā' Zāy\" ma‘a hāżihil-khawātimi khātamu sulaimāna (Wafaq/Rajah bintang).",
]
TERJ49 = [
    "Sebagian penjelmaan Ifrit—yakni mereka yang merubah bentuk menyerupai wujud manusia—bermukim di dekat pepohonan yang tinggi, semak berduri (syaukul 'aliq), dan mereka memasuki kebun-kebun. Sebagian golongan Sabasib (jin padang pasir) bermukim di pegunungan dan reruntuhan yang kosong; dan kelompok ini sangat banyak memberikan mudharat (bahaya) bagi kaum laki-laki maupun perempuan dari keturunan Adam.",
    "Dan di kalangan setan Ifrit, ada yang menyetubuhi wanita manusia, dan sebagian mereka menginginkan agar perempuan manusia tersebut menjadi istri bagi mereka. Sebagian mereka ada yang merusak fisik manusia, yakni melumpuhkan salah satu anggota tubuh (manusia) dari fungsi anggota tubuhnya.",
    "Namun, terdapat 70 sifat (gejala) dan apa-apa yang dibutuhkan dari mereka bagaimanapun bentuk pengobatannya tampak. Adapun mengenai penderita kesurupan (ashhabus-shar'i), terdapat 43 macam kesurupan di dalam tubuh mereka, yang mana setiap macamnya pasti ada obatnya.",
    "(Macam Pertama): Maka barangsiapa yang kesurupan, baik ia perempuan, anak laki-laki, maupun anak perempuan, maka tulislah di antara kedua matanya (di dahinya): (Maka apakah orang yang beriman seperti orang yang fasik?) hingga firman-Nya: (Tanzilan nuzulan nuzulan). Dan (tulislah) di telapak tangan kanannya Khatam (Rajah) Sulaiman, yang mana rajah tersebut memiliki tujuh ujung tanduk (bintang sudut tujuh). Di dalam setiap sudut/tanduk tersebut tulislah salah satu huruf dari huruf-huruf: (Fa - Jim - Syin - Tsa - Kha - Zai), beserta dengan rajah-rajah ini yaitu Khatam Sulaiman (Bintang bersudut lima)",
]

# (template_kind, text) — kind: 'terj' or 'arab'
TATACARA49 = [
    ("terj", "4. Tata Cara Praktik"),
    ("terj", "Berdasarkan Halaman 49, fasal ini memberikan petunjuk teknis pengobatan untuk meruqyah/mengobati orang yang kesurupan (gangguan jin yang merasuk ke fisik/saraf)."),
    ("terj", "Langkah-Langkah Pengobatan Kesurupan (Macam Pertama):"),
    ("terj", "- Penulisan di Dahi: Tulislah di antara kedua mata (dahi) pasien kesurupan (baik laki-laki, perempuan, maupun anak-anak) potongan ayat Al-Qur'an (Surah As-Sajdah: 18):"),
    ("arab", "أَفَمَنْ كَانَ مُؤْمِنًا كَمَنْ كَانَ فَاسِقًا ۚ"),
    ("terj", "Dilanjutkan dengan kalimat penetapan (Tanzilan nuzulan nuzulan)."),
    ("terj", "- Penulisan Rajah di Tangan Kanan: Pada telapak tangan kanan pasien, gambarlah Rajah Khatam Sulaiman (simbol Bintang Sudut Tujuh/Heptagram)."),
    ("terj", "- Penyisipan Huruf Gaib: Di dalam ketujuh sudut/tanduk bintang tersebut, isilah masing-masing dengan satu huruf hijaiyah berikut secara berurutan: ف (Fa), ج (Jim), ش (Syin), ث (Tsa), خ (Kha), ز (Zai)."),
    ("terj", "- Penulisan Simbol Khatam Akhir: Di bawah atau di samping rajah tersebut, tuliskan deretan simbol Khatam Sulaiman (Tujuh Segel Perjanjian) sebagaimana yang tertera di naskah: Simbol Bintang sudut lima (✡), garis tegak ( /|\\ ), huruf Mim (م), simbol pagar (#), angka satu empat kali (١١١١), huruf Ha (هـ), dan Wawu (و)."),
    ("terj", "⚠️ Catatan Keaslian Manuskrip"),
    ("terj", "- Penyisipan Huruf (Hal 49, Baris 14): Teks menyebutkan Khatam memiliki tujuh sudut/tanduk (sab'atu qurun), namun huruf yang disebutkan untuk diisi hanya ada enam (ف ج ش ث خ ز). Dalam tradisi ilmu wafaq kuno, huruf ketujuh yang sering disembunyikan/dihilangkan dari deretan ini adalah huruf ظ (Zha)."),
    ("terj", "- Kutipan Ayat (Hal 49, Baris 11-12): Tertulis إِلَى قَوْلِهِ تَنْزِيلاً نُزُلاً نُزُلاً (Hingga firman-Nya: Tanzilan nuzulan nuzulan). Ini bukanlah ayat Al-Qur'an secara utuh, melainkan modifikasi penegasan (Taukid/Taqrir) yang sering digunakan dalam praktik ruqyah hikmah agar entitas jin segera turun/keluar."),
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


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = {}
    for i, t in enumerate(texts):
        m = re.match(r"^=== Halaman (\d+) — (.+) ===$", t.strip())
        if m:
            heads[int(m.group(1))] = i
    h48, h49, h50 = heads[48], heads[49], heads[50]
    els = [p._element for p in paras]
    head48_el, head49_el, head50_el = els[h48], els[h49], els[h50]

    img_els = [els[i] for i in range(h48, h50) if has_drawing_el(els[i])]
    if len(img_els) != 1 or not (h49 < els.index(img_els[0]) < h50):
        raise AssertionError("expected exactly 1 wafaq image inside unit 49")
    img_el = img_els[0]

    arab_tpl = deepcopy(els[h48 + 1])
    latin_tpl = deepcopy(els[h48 + 5])
    terj_tpl = deepcopy(els[h48 + 7])
    if not texts[h48 + 5].startswith("Al-fashlul"):
        raise AssertionError("latin template mismatch")
    blank_tpl = deepcopy(els[h49 - 1])
    if texts[h49 - 1].strip() != "":
        raise AssertionError("blank template mismatch")

    body = head48_el.getparent()
    removed = 0
    node = head48_el.getnext()
    while node is not None and node is not head50_el:
        nxt = node.getnext()
        if node is not img_el and node is not head49_el and node.tag == qn("w:p"):
            body.remove(node)
            removed += 1
        node = nxt

    new48 = [make_para(arab_tpl, t) for t in AR48]
    new48 += [make_para(latin_tpl, t) for t in LAT48]
    new48 += [make_para(terj_tpl, t) for t in TERJ48]
    for el in new48:
        head49_el.addprevious(el)
    head49_el.addprevious(make_para(blank_tpl, ""))

    new49 = [make_para(arab_tpl, t) for t in AR49]
    new49 += [make_para(latin_tpl, t) for t in LAT49]
    new49 += [make_para(terj_tpl, t) for t in TERJ49]
    for el in new49:
        img_el.addprevious(el)

    anchor = img_el
    for kind, t in TATACARA49:
        el = make_para(arab_tpl if kind == "arab" else terj_tpl, t)
        anchor.addnext(el)
        anchor = el
    anchor.addnext(make_para(blank_tpl, ""))

    doc.save(TARGET)

    out = Document(TARGET)
    ot = [p.text for p in out.paragraphs]
    oh = {}
    for i, t in enumerate(ot):
        m = re.match(r"^=== Halaman (\d+) — (.+) ===$", t.strip())
        if m:
            oh[int(m.group(1))] = i
    if sorted(oh) != list(range(1, 123)):
        raise AssertionError("headings broken")
    if ot[oh[48] + 1 : oh[49]] != AR48 + LAT48 + TERJ48 + [""]:
        raise AssertionError("unit48 mismatch")
    exp49 = AR49 + LAT49 + TERJ49 + [""] + [t for _, t in TATACARA49] + [""]
    if ot[oh[49] + 1 : oh[50]] != exp49:
        got = ot[oh[49] + 1 : oh[50]]
        for a, b in zip(got, exp49):
            if a != b:
                print("MISMATCH:\n got:", repr(a[:100]), "\n exp:", repr(b[:100]))
        raise AssertionError(f"unit49 mismatch len {len(got)} vs {len(exp49)}")
    if len(out.inline_shapes) != 26:
        raise AssertionError("image count changed")
    if media_hashes(TARGET) != media_hashes(SOURCE_FOR_MEDIA):
        raise AssertionError("media hashes/order changed")

    print(f"removed_old_paras={removed}")
    print(f"total_paragraphs={len(ot)}")
    print(f"bytes={TARGET.stat().st_size}")
    print(f"sha256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")
    print("H48_49_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
