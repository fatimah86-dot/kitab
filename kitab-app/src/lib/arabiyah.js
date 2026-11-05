/* Logika "Arabiyah Center" — ruang belajar bahasa Arab.
 * Seluruh respons dihasilkan secara lokal oleh aturan sederhana (bukan model
 * bahasa), sesuai catatan pada panduan aslinya.
 */

export const FEATURES = [
  {
    id: 'kamus',
    title: 'KAMUS ARAB',
    subtitle: 'Makna, sinonim, antonim',
    icon: '⌕',
    sample: 'أصيب المريض بالسرطان',
  },
  {
    id: 'nahwu',
    title: "NAHWU & I'RAB",
    subtitle: 'Kaidah dan analisis kalimat',
    icon: 'ن',
    sample: 'الْعِلْمُ نُورٌ',
  },
  {
    id: 'sharaf',
    title: 'SHARAF & WAZAN',
    subtitle: 'Akar kata dan tasrif',
    icon: 'ص',
    sample: 'كَتَبَ الطَّالِبُ الدَّرْسَ',
  },
  {
    id: 'balaghah',
    title: 'BALAGHAH',
    subtitle: "Majaz, kinayah, isti'arah",
    icon: 'ب',
    sample: 'رأيتُ أسدًا يخطبُ',
  },
  {
    id: 'imla',
    title: "IMLA' & KITABAH",
    subtitle: 'Ejaan dan penulisan',
    icon: '✎',
    sample: 'هاذا كتاب جميل',
  },
  {
    id: 'arudh',
    title: 'ARUDH & QAFIYAH',
    subtitle: 'Wazan dan bahr syair',
    icon: '♫',
    sample: 'قِفا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ',
  },
];

export const ARABIC_KEYS = [
  'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض',
  'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ء', 'أ', 'إ', 'لا',
];

// Panduan umum yang menyertai setiap respons agar hasil dapat dipakai
// sebagai bahan belajar, bukan hanya jawaban singkat.
const STUDY_GUIDE = `
Gunakan uraian ini sebagai pendamping belajar bahasa Arab. Mulailah dengan
membaca teks secara utuh, lalu tentukan batas kata dan hubungan antarkata.
Jangan langsung menyimpulkan makna dari satu kata tanpa melihat konteks,
karena bentuk yang sama dapat memiliki fungsi dan nuansa berbeda. Jika teks
tidak berharakat, beberapa bacaan mungkin dapat diterima; tandai bagian yang
memerlukan konteks tambahan alih-alih menganggap satu analisis pasti benar.
Perhatikan pula perbedaan antara makna kamus dan makna yang muncul dalam
susunan kalimat. Makna kamus memberi kemungkinan dasar, sedangkan konteks,
kolokasi, dan tujuan pembicara membantu memilih terjemahan yang alami.

Untuk berlatih mandiri, salin teks, beri harakat pada kata yang sudah dikenal,
kemudian jelaskan alasan pilihan harakat tersebut. Pisahkan isim, fi'il, dan
huruf; amati tanda yang tampak serta posisi kata dalam jumlah. Sesudah itu,
coba ubah satu unsur kalimat dan periksa bagaimana perubahan tersebut
memengaruhi makna atau hubungan gramatikal. Catat kosakata baru bersama
bentuk tunggal atau jamaknya, akar kata jika dapat dikenali, dan satu contoh
pemakaian. Untuk pembahasan syair, jangan menetapkan bahr hanya berdasarkan
kesan bunyi: teks perlu dibaca dengan pelafalan dan pemenggalan yang tepat.
Untuk koreksi tulisan, bedakan kesalahan ejaan dari pilihan gaya bahasa.

Istilah seperti marfu', manshub, majrur, dan majzum menjelaskan keadaan
gramatikal dalam konteks tertentu; tanda i'rab dapat tampak atau diperkirakan
dari kedudukan kata. Bentuk akhir kata juga dapat berubah karena konstruksi
yang mendahuluinya. Dalam sharaf, bandingkan bentuk kata dengan pola yang
sesuai dan perhatikan huruf asli serta huruf tambahan. Dalam balaghah, cari
petunjuk konteks sebelum menyebut suatu ungkapan sebagai majaz, kinayah,
atau isti'arah. Satu contoh dapat memiliki lebih dari satu pembacaan, maka
uraikan petunjuknya dan nyatakan tingkat kepastiannya.

Terjemahan yang baik mempertahankan makna, bukan selalu susunan kata Arab
secara harfiah. Bandingkan terjemahan literal dengan terjemahan natural,
kemudian jelaskan perubahan susunan yang diperlukan dalam bahasa Indonesia.
Jika sebuah teks hanya berupa potongan, jangan menambahkan konteks yang
tidak tersedia. Saat belajar, cocokkan hasil dengan kamus tepercaya, kitab
nahwu atau sharaf yang dipakai di kelas, dan guru yang memahami konteks.
Contoh dalam aplikasi ini merupakan bahan latihan edukatif. Respons dibuat
oleh aturan internal sederhana, bukan oleh model bahasa yang memahami
seluruh korpus atau konteks dunia nyata. Karena itu, khususnya untuk teks
klasik, istilah teknis, dan syair, verifikasi hasil sebelum mengutipnya sebagai
jawaban akademik. Kamu bisa mengirim teks berharakat atau tanpa harakat,
memakai keyboard virtual, lalu memilih mode yang sesuai untuk mendapatkan
sudut analisis yang lebih terarah.`;

const FEATURE_GUIDES = {
  kamus: `
Mode kamus mengutamakan makna kata dalam konteks, keluarga kata, dan
kemungkinan padanan bahasa Indonesia. Periksa apakah kata itu nomina, verba,
atau partikel, lalu cari bentuk dasar sebelum menyimpulkan maknanya. Sinonim
tidak selalu dapat saling menggantikan dalam setiap kalimat; perhatikan
kolokasi dan tingkat formalitas. Untuk mufrad dan jamak, bahasa Arab memiliki
bentuk jamak taksir maupun jamak beraturan, sehingga bentuknya perlu
diverifikasi. Turunan kata juga harus diperiksa berdasarkan pola dan konteks,
bukan hanya kemiripan huruf. Pada kalimat contoh, identifikasi kata kunci
terlebih dahulu, tentukan hubungan kata tersebut dengan kata di sekitarnya,
dan pilih terjemahan yang wajar dalam bahasa Indonesia. Catat makna dasar,
makna kontekstual, sinonim yang dekat, serta antonim jika memang ada.`,
  nahwu: `
Mode nahwu memeriksa susunan kalimat dan fungsi setiap kata. Mulailah dengan
mengenali apakah susunan berupa jumlah ismiyyah atau jumlah fi'liyyah.
Dalam jumlah ismiyyah, carilah mubtada' dan khabar; dalam jumlah fi'liyyah,
periksa fi'il, fa'il, dan kemungkinan maf'ul bih. Setelah fungsi kata
dikenali, jelaskan keadaan i'rab dan tanda yang relevan. Jangan menetapkan
tanda akhir secara terpisah dari amil dan kedudukan kata. Huruf jar dapat
menjadikan isim sesudahnya majrur, sementara partikel lain dapat memengaruhi
i'rab dengan cara berbeda. I'rab yang tepat sebaiknya menyebut jenis kata,
fungsi, keadaan, tanda, dan alasan ringkasnya. Bila teks tanpa harakat,
nyatakan harakat yang diasumsikan dan kemungkinan pembacaan alternatif.`,
  sharaf: `
Mode sharaf berfokus pada struktur kata, akar, pola, dan perubahan bentuk.
Kenali huruf asli terlebih dahulu; jangan menganggap semua kata pasti berasal
dari akar tiga huruf yang sederhana. Setelah itu bandingkan bentuk dengan
wazan yang sesuai, identifikasi huruf tambahan, dan amati perubahan makna
yang mungkin ditimbulkan pola. Untuk fi'il, perhatikan bentuk madhi, mudhari',
dan amr, serta bentuk aktif atau pasif jika relevan. Tasrif tidak cukup
dihafalkan sebagai daftar; hubungkan setiap bentuk dengan dhamir, waktu,
dan fungsi dalam kalimat. Jika kata merupakan istilah modern, nama diri,
atau serapan, analisis akar dan wazan dapat berbeda dari kata klasik biasa.
Gunakan kamus sharaf untuk menguji bentuk yang tidak dikenal.`,
  balaghah: `
Mode balaghah membantu membaca efek makna dan gaya ungkapan. Mulailah dari
makna literal, lalu cari petunjuk yang membuat pembacaan literal kurang
sesuai atau menghasilkan gambaran tertentu. Majaz memerlukan hubungan makna
dan qarinah; isti'arah dapat membangun peminjaman gambaran atau sifat;
kinayah menyampaikan maksud melalui ungkapan yang tidak selalu menyebutnya
secara langsung. Jangan memberi label hanya karena kalimat terasa puitis.
Jelaskan unsur yang dibandingkan atau maksud tersirat, bukti dari konteks,
dan efek retoris yang mungkin timbul. Dalam teks sastra, satu ungkapan dapat
mengandung lebih dari satu lapisan makna. Analisis balaghah sebaiknya
dibedakan dari i'rab dan terjemahan dasar, meskipun ketiganya saling
membantu memahami teks.`,
  imla: `
Mode imla' dan kitabah memeriksa ejaan serta keterbacaan tulisan. Perhatikan
bentuk hamzah, alif, ta marbuthah, ta maftuhah, alif layyinah, dan pemisahan
kata. Koreksi ejaan tidak selalu sama dengan tashih nahwu; sebuah kalimat
dapat dieja dengan benar namun susunannya masih memerlukan perbaikan. Saat
menyarankan koreksi, bandingkan teks asli dan bentuk usulan, lalu jelaskan
alasan perubahan secara ringkas. Untuk tulisan tanpa harakat, hindari
menganggap ketiadaan harakat sebagai kesalahan, karena teks Arab modern
sering ditulis tanpa harakat. Perhatikan pula tujuan tulisan: materi
pembelajaran untuk pemula dapat memakai harakat lebih lengkap, sedangkan
teks umum biasanya tidak. Baca ulang kalimat setelah koreksi untuk
memastikan maksud penulis tetap terjaga.`,
  arudh: `
Mode arudh dan qafiyah merupakan bantuan awal untuk menelaah syair. Bacalah
bait dengan pelafalan yang dimaksud, sebab bunyi, washl, waqaf, dan bentuk
akhir kata dapat memengaruhi pemenggalan. Arudh menelaah pola bunyi dan
taf'ilah, sedangkan qafiyah menelaah bagian akhir bait serta unsur bunyinya.
Jangan menetapkan bahr dengan menghitung huruf tertulis saja; yang perlu
diperhatikan ialah bunyi yang dilafalkan sesuai kaidah dan riwayat bacaan.
Bait yang dikirim sebagai potongan mungkin tidak cukup untuk menguji
pola keseluruhan. Respons otomatis di sini hanya memberi panduan membaca,
bukan pemindaian prosodi yang akurat. Untuk analisis pasti, cocokkan bait
lengkap dengan kitab arudh dan pembacaan guru atau ahli.`,
};

function normalizeArabic(text) {
  return text.replace(/[ًٌٍَُِّْٰـ]/g, '').trim();
}

export function generateSmartResponse(input, feature) {
  const cleanInput = input.trim();
  const normalized = normalizeArabic(cleanInput);
  const isCancerExample =
    normalized.includes('أصيب') && normalized.includes('المريض') && normalized.includes('بالسرطان');

  let specific = '';

  if (isCancerExample) {
    specific = `
Contoh yang kamu kirim: «${cleanInput}».
Terjemahan natural yang mungkin: “Pasien itu menderita kanker” atau “Pasien
tersebut terkena kanker.” Terjemahan disesuaikan dengan konteks kalimat
yang lebih luas.

Analisis awal nahwu: «أُصيبَ» adalah fi'il madhi mabni lil-majhūl (kata kerja
lampau pasif), dengan harakat yang diasumsikan untuk pembacaan ini. «المريضُ»
dapat dianalisis sebagai nā'ib al-fā'il yang marfu'; dhammah pada akhir kata
merupakan tanda yang tampak dalam bentuk berharakat. «بِـ» adalah huruf jar,
dan «السَّرَطانِ» isim majrur sesudahnya; frasa «بالسرطان» berhubungan dengan
fi'il dan menjelaskan sebab atau keadaan yang dialami pasien. Pada tulisan
tanpa harakat, analisis ini merupakan pembacaan yang paling wajar untuk
konstruksi tersebut, tetapi tetap perlu mempertimbangkan konteks.

Akar kata: «أُصيبَ» berkaitan dengan akar ص و ب, dengan perubahan bentuk yang
perlu dipahami melalui pola sharaf; «المريض» berkaitan dengan akar م ر ض.
«السرطان» adalah istilah penyakit modern yang lazim dipakai untuk kanker;
analisis akar katanya tidak otomatis memberi informasi medis. Catatan ini
hanya menjelaskan bahasa dan tidak dimaksudkan sebagai diagnosis atau nasihat
kesehatan.

Contoh tambahan: «أُصيبَ اللاعبُ في قدمِهِ» berarti “Pemain itu mengalami
cedera pada kakinya.” Perhatikan pola pasif dan nā'ib al-fā'il pada «اللاعبُ».
`;
  } else {
    specific = `
Teks yang kamu kirim: «${cleanInput}».
Terjemahan awal belum dapat dipastikan tanpa konteks tambahan. Perhatikan
kata-kata yang dapat dikenali, hubungan antarkata, dan harakat yang mungkin
berubah karena posisi gramatikal. Jika ada kata yang belum jelas, kirimkan
kalimat lengkap atau tambahkan harakat agar pembacaan bisa diperiksa dengan
lebih terarah. Dalam mode ${feature.title}, fokuskan perhatian pada
${feature.subtitle.toLowerCase()}.
`;
  }

  return [`MODE ${feature.title}`, specific, FEATURE_GUIDES[feature.id], STUDY_GUIDE].join('\n\n');
}
