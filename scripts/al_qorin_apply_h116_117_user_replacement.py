#!/usr/bin/env python3
"""Replace Halaman 116-117 in AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx.

User-supplied verbatim replacement (2026-10-30): both units are replaced
entirely with the text below, EXCEPT the wafaq image paragraph in unit
116, which keeps its original element/position (after the Terjemahan).
Headings === Halaman 116/117 === and the blank separators stay.
The duplicated Terjemahan of p.116 uses the user's second copy
("(Baca Asma' Suryani)"). No Media/Langkah/Tujuan block is added.
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

AR116 = [
    "الْفَصْلُ الثَّانِي وَالْعِشْرُونَ",
    "الْقَرِينَةُ",
    "بَابٌ لِمَنْعِ الْقَرِينَةِ أُمِّ الصِّبْيَانِ:",
    "اكْتُبْ وَفْقَ الْبَسْمَلَةِ الشَّرِيفَةِ الْآتِي فِي وَرَقَةٍ بَيْضَاءَ ثُمَّ اكْتُبْ حَوْلَهُ مَا يَأْتِي وَهُوَ هَذَا ----- ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ثُمَّ اكْتُبْ مِائَةَ مِيمٍ هَكَذَا م كهو لهو آهِيَاً شَرَاهِيَاً أَدُونَايَّ أَصْبَاؤُتِ آلِ شَدَّايَّ ١٤ مَرَّةً وَاكْتُبْ آيَاتِ الْحِفْظِ كُلَّهَا وَآيَةَ الْكُرْسِيِّ وَآخِرَ سُورَةِ الْبَقَرَةِ وَآخِرَ سُورَةِ التَّوْبَةِ وَآخِرَ سُورَةِ الْحَشْرِ آخِرَ سُورَةِ الْحَدِيدِ إِلَى الصُّدُورِ وَالصَّمَدِيَّةَ وَالْمُعَوِّذَتَيْنِ وَيُبَخَّرُ وَتَحْمِلُهُ الْمَقْرُونَةُ وَالْمَرْأَةُ الَّتِي تُسْقِطُ الْأَوْلَادَ.",
    "بَابٌ آخَرُ لِلْقَرِينَةِ:",
    "يُكْتَبُ وَيُحْمَلُ لِلْمَرْأَةِ الَّتِي تُسْقِطُ الْأَوْلَادَ وَخِلَافِهِ وَيُبَخَّرُ وَتَحْمِلُهُ الْمَرْأَةُ وَهَذَا مَا تَكْتُبُ:",
]

LAT116 = [
    "Al-faṣluts-tsānī wal-‘isyrūna",
    "Al-qarīnah",
    "Bābul-liman‘il-qarīnati ummiṣ-ṣibyān:",
    "Uktub wafqal-basmalatisy-syarīfatil-ātī fī waraqatim-baiḍā'a tsummaktub ḥaulahū mā ya'tī wa huwa hādzā: (alif bā' tā' tsā' jīm ḥā' khā' dāl dzāl rā' zāy sīn syīn ṣād ḍād ṭā' ẓā') tsummaktub mi'ata mīmin hākadzā mīm kahuwa lahuwa āhyān syarāhiyān adūnāyya aṣbā'ūti āli syaddāyya arba‘ata ‘asyara marratan waktub āyātil-ḥifẓi kullahā wa āyatal-kursiyyi wa ākhira sūratil-baqarati wa ākhira sūratit-taubati wa ākhira sūratil-ḥasyri ākhira sūratil-ḥadīdi ilaṣ-ṣudūri waṣ-ṣamadiyyata wal-mu‘awwiżataini wa yubakhkharu wa taḥmiluhul-maqrūnatu wal-mar'atullatī tusqiṭul-aulād.",
    "Bābun ākharu lil-qarīnah:",
    "Yuktabu wa yuḥmalu lil-mar'atillatī tusqiṭul-aulāda wa khilāfahū wa yubakhkharu wa taḥmiluhul-mar'atu wa hādzā mā tuktab(u):",
]

TERJ116 = [
    "Fasal Kedua Puluh Dua",
    "Qarinah (Gangguan Jin Perempuan)",
    "Bab Untuk Mencegah Qarinah Ummu Shibyan:",
    'Tulislah wafak Basmalah yang mulia berikut ini pada selembar kertas putih, kemudian tulislah di sekelilingnya apa yang berikut ini, yaitu: (Alif - Ba - Ta - Tsa - Jim - Ha - Kha - Dal - Dzal - Ra - Zai - Sin - Syin - Shad - Dhad - Tha - Zha). Kemudian tulislah seratus huruf Mim seperti ini (م), lalu كهو لهو (Baca Asma\' Suryani): "Āhyān syarāhiyān adūnāyya aṣbā\'ūti āli syaddāyya" sebanyak 14 kali. Dan tulislah ayat-ayat Al-Hifzh (penjagaan) seluruhnya, Ayat Kursi, bagian akhir Surah Al-Baqarah, bagian akhir Surah At-Taubah, bagian akhir Surah Al-Hasyr, bagian akhir Surah Al-Hadid sampai pada kalimat "As-Shudur", serta Surah As-Shamdiyyah (Al-Ikhlas) dan Al-Mu\'awwidzatain (Al-Falaq dan An-Nas). Kemudian diasapi dengan bukhur, lalu dibawa/dikalungkan oleh perempuan yang dibarengi gangguan (qarinah) dan oleh perempuan yang (sering) mengalami keguguran anak.',
    "Bab Lain Untuk (Mencegah) Qarinah:",
    "Ditulis dan dibawa/dikalungkan untuk perempuan yang (sering) keguguran anak dan untuk gangguan selainnya, serta diasapi (dengan bukhur), lalu perempuan itu membawanya. Dan inilah apa yang (harus) engkau tulis:",
]

AR117 = [
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    "أَرْقَا شَرْقَا عَرْمُوقَاشٍ اسْتَطَافٍ سَطُوفٍ خَطُوفٍ خَطَّافٍ",
    "شَعْدَاشٍ شَتُوخٍ اللَّهُ رَبُّ الْعِزَّةِ وَالْعَظَمَةِ بَامَهْشَلُوا",
    "وَسُبُّوحٍ إِنْ قَجٍ شَتُوخٍ أَرْمُوحَثِيثَا الْقَدِيمُ الْأَزَلِيُّ الدَّائِمُ الْأَبَدِيُّ",
    "إِنَّ الَّذِينَ فَتَنُوا الْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ ثُمَّ لَمْ يَتُوبُوا فَلَهُمْ",
    "عَذَابُ جَهَنَّمَ وَلَهُ عَذَابُ الْحَرِيقِ أَنْشُدُكُمْ يَا مَعْشَرَ الْجِنِّ",
    "بِاللَّهِ الْعَزِيزِ الْوَاحِدِ الْقَهَّارِ الْحَفِيظِ الْوَافِي الْمَانِعِ الْوَاقِعِ",
    "وَبِالْعَهْدِ الَّذِي أَخَذَهُ عَلَيْكُمْ سَيِّدُنَا سُلَيْمَانُ بْنُ دَاوُدَ",
    "عَلَيْهِمَا السَّلَامُ لَا تَدْنُوا وَلَا تَقْرَبُوا حَامِلَ كِتَابِي هَذَا أَوْ حَامِلَ",
    "هَذَا الْهَيْكَلِ وَاتْرُكُوهُ وَانْصَرِفُوا عَنْهُ وَاحْفَظُوهُ فِي حِرْزِ اللَّهِ",
    "وَحِمَايَتِهِ بِحَقِّ هَذِهِ الْأَسْمَاءِ وَالْآيَاتِ وَبِسِرِّ الْقُرْآنِ الْعَظِيمِ",
    "اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ لَهُ مَا فِي",
    "السَّمَوَاتِ وَمَا فِي الْأَرْضِ مَنْ ذَا الَّذِي يَشْفَعُ إِلَّا بِإِذْنِهِ يَعْلَمُ",
    "مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ وَلَا يُحِيطُونَ بِشَيْءٍ مِنْ عِلْمِهِ إِلَّا",
    "بِمَا شَاءَ وَسِعَ كُرْسِيُّهُ السَّمَوَاتِ وَالْأَرْضَ وَلَا يَئُودُهُ حِفْظُهُمَا",
    "وَهُوَ الْعَلِيُّ الْعَظِيمُ لَا إِكْرَهَ فِي الدِّينِ قَدْ تَبَيَّنَ الرُّشْدُ مِنَ",
    "الْغَرِيبِ فَمَنْ يَكْفُرْ بِالطَّاغُوتِ وَيُؤْمِنْ بِاللَّهِ فَقَدِ اسْتَمْسَكَ",
]

LAT117 = [
    "Bismillāhir-raḥmānir-raḥīm.",
    "Irqā syarqā ‘armūqāsyin istaṭāfin saṭūfin khaṭūfin khaṭṭāfin",
    "sya‘dāsyin syatūkhin, Allāhu rabbul-‘izzati wal-‘aẓamati bi-āmahasylū",
    "wa subbūḥin in qajin syatūkhin armūḥatsītsāl-qadīmul-azaliyyud-dā'imul-abadī.",
    "Innal-lażīna fatanul-mu'minīna wal-mu'mināti tsumma lam yatūbū falahum",
    "‘ażābu jahannama wa lahū ‘ażābul-ḥarīq. (Q.S. Al-Buruj: 10, tertulis wa lahū)",
    "Ansyidukum yā ma‘syaral-jinni",
    "billāhil-‘azīzil-wāḥidil-qahhāril-ḥafīẓil-wāfil-māni‘il-wāqi‘i",
    "wa bil-‘ahdil-lażī akhażahū ‘alaikum sayyidunā sulaimānub-nu dāwūda",
    "‘alaihimās-salāmu lā tadnū wa lā taqrabū ḥāmila kitābī hāżā au ḥāmila",
    "hāżal-haikali watrukūhu wanṣarifū ‘anhu waḥfaẓūhu fī ḥirzillāhi",
    "wa ḥimāyatihī biḥaqqi hāżihil-asmā'i wal-āyāti wa bisirril-qur'ānil-‘aẓīm.",
    "Allāhu lā ilāha illā huwal-ḥayyul-qayyūmu lā ta'khużuhū sinatuw-wa lā naumun lahū mā fis-",
    "samāwāti wa mā fil-arḍi man żal-lażī yasyfa‘u illā bi-iżnihī ya‘lamu",
    "mā baina aidīhim wa mā khalfahum wa lā yuḥīṭūna bisyai'im-min ‘ilmihī illā",
    "bimā syā'a wasi‘a kursiyyuhus-samāwāti wal-arḍa wa lā ya'ūduhū ḥifẓuhumā",
    "wa huwal-‘aliyyul-‘aẓīmu lā ikraha fid-dīni qat-tabayyanar-rusydu minal-",
    "gharībi famay-yakfur biṭ-ṭāghūti wa yu'mim-billāhi faqadistamsaka.",
]

TERJ117 = [
    "Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.",
    "(Asma' Suryani/Penundukan): Irqa, Sharqa, 'Armuqasy, Istathaf, Satuf, Khatuf, Khattaf, Sya'dasy, Syatukh. Allah adalah Tuhan Pemilik Keperkasaan dan Keagungan dengan Bi-amhasylu dan Maha Suci In Qajin Syatukh Armuhatsitsa Yang Maha Terdahulu, Maha Azali, Maha Langgeng, lagi Maha Abadi.",
    '"Sesungguhnya orang-orang yang mendatangkan fitnah kepada orang-orang mukmin laki-laki dan perempuan kemudian mereka tidak bertobat, maka bagi mereka azab Jahannam dan bagi mereka azab yang membakar."',
    "Aku bersumpah kepada kalian wahai golongan jin, demi Allah Yang Maha Perkasa, Maha Esa, Maha Menundukkan, Maha Memelihara, Maha Menepati, Maha Mencegah, lagi Maha Menjatuhkan ketetapan, dan demi janji yang telah diambil dari kalian oleh junjungan kami Sulaiman bin Daud 'alaihimas-salam: janganlah kalian mendekat dan jangan menghampiri pembawa tulisanku ini atau pembawa azimat (haikal) ini. Tinggalkanlah dia, berpalinglah darinya, dan jagalah dia dalam perlindungan Allah serta penjagaan-Nya, demi hak nama-nama dan ayat-ayat ini serta demi rahasia Al-Qur'an yang Agung.",
    '(Ayat Kursi dan Ayat Pembenteng): "Allah, tidak ada tuhan selain Dia Yang Maha Hidup lagi terus-menerus mengurus makhluk-Nya... (hingga akhir bagian)... Barangsiapa ingkar kepada Thagut dan beriman kepada Allah, maka sungguh ia telah berpegang teguh..."',
    "Tata cara praktiknya sepenuhnya kembali pada kaidah di akhir halaman 116: seluruh teks dari halaman 117 tersebut ditulis pada kertas, diasapi dengan bukhur, lalu dibawa atau dikalungkan oleh wanita yang sering mengalami keguguran akibat gangguan jin Qarinah.",
]


def has_drawing_el(el) -> bool:
    return bool(el.xpath('.//*[local-name()="drawing"]'))


def para_text(el) -> str:
    return "".join(node.text or "" for node in el.iter() if node.tag == qn("w:t"))


def make_para(template_el, text: str):
    """Clone template paragraph (keeps pPr/direction), single run with text."""
    el = deepcopy(template_el)
    # keep first run as formatting donor
    runs = el.findall(qn("w:r"))
    donor = deepcopy(runs[0]) if runs else None
    for child in list(el):
        if child.tag != qn("w:pPr"):
            el.remove(child)
    if donor is not None:
        # strip all text nodes in donor, set one
        for t in donor.iter():
            if t.tag == qn("w:t"):
                t.text = ""
        texts = [t for t in donor.iter() if t.tag == qn("w:t")]
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
    heads = {}
    for i, p in enumerate(paras):
        m = re.match(r"^=== Halaman (\d+) — (.+) ===$", p.text.strip())
        if m:
            heads[int(m.group(1))] = i
    i116, i117, i118 = heads[116], heads[117], heads[118]
    els = [p._element for p in paras]
    head116_el, head117_el, head118_el = els[i116], els[i117], els[i118]

    img_els = [els[i] for i in range(i116, i117) if has_drawing_el(els[i])]
    if len(img_els) != 1:
        raise AssertionError(f"expected exactly 1 wafaq image in unit 116, got {len(img_els)}")
    img_el = img_els[0]
    if any(has_drawing_el(els[i]) for i in range(i117, i118)):
        raise AssertionError("unit 117 unexpectedly carries an image")

    # Templates: first Arabic para of 116, Latin para, Terjemahan para, blank.
    arab_tpl = deepcopy(els[i116 + 1])
    latin_tpl = deepcopy(els[i116 + 7])  # 'Al-fashluts tsaani ...'
    terj_tpl = deepcopy(els[i116 + 9])   # first Terjemahan para
    assert para_text(latin_tpl).startswith("Al-fashluts"), para_text(latin_tpl)[:40]
    blank_el_src = next(els[i] for i in range(i118, len(els)) if para_text(els[i]).strip() == "" and not has_drawing_el(els[i]))

    # Remove everything strictly between heading116 and heading118
    # except img_el and heading117.
    body = head116_el.getparent()
    node = head116_el.getnext()
    removed = 0
    while node is not None and node is not head118_el:
        nxt = node.getnext()
        if node is not img_el and node is not head117_el and node.tag == qn("w:p"):
            body.remove(node)
            removed += 1
        node = nxt

    # Insert new 116 content before image (Arab, Latin, Terjemahan).
    new116 = [make_para(arab_tpl, t) for t in AR116]
    new116 += [make_para(latin_tpl, t) for t in LAT116]
    new116 += [make_para(terj_tpl, t) for t in TERJ116]
    for el in new116:
        img_el.addprevious(el)
    # blank separator between image and heading117
    head117_el.addprevious(make_para(blank_el_src, ""))

    # Insert new 117 content after heading117.
    new117 = [make_para(arab_tpl, t) for t in AR117]
    new117 += [make_para(latin_tpl, t) for t in LAT117]
    new117 += [make_para(terj_tpl, t) for t in TERJ117]
    anchor = head117_el
    for el in new117:
        anchor.addnext(el)
        anchor = el
    anchor.addnext(make_para(blank_el_src, ""))

    doc.save(TARGET)

    # QA
    out = Document(TARGET)
    texts = [p.text for p in out.paragraphs]
    heads2 = {}
    for i, t in enumerate(texts):
        m = re.match(r"^=== Halaman (\d+) — (.+) ===$", t.strip())
        if m:
            heads2[int(m.group(1))] = i
    if sorted(heads2) != list(range(1, 123)):
        raise AssertionError("headings broken")
    s, e = heads2[116], heads2[117]
    unit116 = texts[s + 1 : e]
    expected116 = AR116 + LAT116 + TERJ116 + ["", ""]
    if unit116 != expected116:
        for a, b in zip(unit116, expected116):
            if a != b:
                print("MISMATCH116:\n got:", repr(a[:120]), "\n exp:", repr(b[:120]))
        raise AssertionError(f"unit116 mismatch len {len(unit116)} vs {len(expected116)}")
    s2, e2 = heads2[117], heads2[118]
    unit117 = texts[s2 + 1 : e2]
    expected117 = AR117 + LAT117 + TERJ117 + [""]
    if unit117 != expected117:
        for a, b in zip(unit117, expected117):
            if a != b:
                print("MISMATCH117:\n got:", repr(a[:120]), "\n exp:", repr(b[:120]))
        raise AssertionError(f"unit117 mismatch len {len(unit117)} vs {len(expected117)}")
    if len(out.inline_shapes) != 26:
        raise AssertionError("image count changed")
    if media_hashes(TARGET) != media_hashes(SOURCE_FOR_MEDIA):
        raise AssertionError("media hashes/order changed")
    joined = "\n".join(texts)
    for frag in ("مِائَةَ مِيمٍ", "أَصْبَاؤُتِ", "١٤ مَرَّةً", "arba‘ata ‘asyara",
                 "(Baca Asma' Suryani)", "sebanyak 14 kali",
                 "Tata cara praktiknya sepenuhnya kembali pada kaidah di akhir halaman 116"):
        if frag not in joined:
            raise AssertionError(f"missing fragment: {frag}")

    print(f"removed_old_paras={removed}")
    print(f"total_paragraphs={len(texts)}")
    print(f"bytes={TARGET.stat().st_size}")
    print(f"sha256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")
    print("H116_117_REPLACEMENT_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
