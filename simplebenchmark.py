import time
import mpstemmer

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

kata_uji_std = [
    'nerjang', 'nuduh', 'nerima', 'negur', 'mukul',
    'mimpin', 'nyoba', 'nyiram', 'nyuruh', 'nyimpen',
    'nyebrang', 'nganggep', 'ngamuk', 'ngambil', 'ngebuka',
    'ngebantu', 'ngelepas', 'kebayang', 'keinjek', 'kekabul',
    'kepergok', 'ketipu', 'keulang', 'kewujud', 'critain',
    'betulin', 'manjain', 'gangguin', 'gantian', 'ikutan',
    'musuhan', 'sabunan', 'temenan', 'tukeran', 'nanyain',
    'nunjukin', 'mentingin', 'megangin', 'nyelametin', 'nyempetin',
    'ngorbanin', 'ngadepin', 'ngebuktiin', 'ngewarnain', 'kedengeran',
    'ketemuan', 'beneran', 'ginian', 'kawinan', 'mainan',
    'parkiran', 'duluan', 'gendutan', 'karatan', 'palingan',
    'sabaran', 'kebagusan', 'sanaan', 'cepetan', 'sepagian'
]

kata_uji_std_jawaban = [
    'terjang', 'tuduh', 'terima', 'tegur', 'pukul',
    'pimpin', 'coba', 'siram', 'suruh', 'simpan',
    'seberang', 'anggap', 'amuk', 'ambil', 'buka',
    'bantu', 'lepas', 'bayang', 'injak', 'kabul',
    'pergok', 'tipu', 'ulang', 'wujud', 'cerita',
    'betul', 'manja', 'ganggu', 'ganti', 'ikut',
    'musuh', 'sabun', 'teman', 'tukar', 'tanya',
    'tunjuk', 'penting', 'pegang', 'selamat', 'sempat',
    'korban', 'hadap', 'bukti', 'warna', 'dengar',
    'temu', 'benar', 'begini', 'kawin', 'main',
    'parkir', 'dulu', 'gendut', 'karat', 'paling',
    'sabar', 'bagus', 'sana', 'cepat', 'pagi',
]


def run_mpstemmer(dataset, check_nonstandard, n_trials):
    time_avg = 0.
    stemmer_mpstemmer = mpstemmer.MPStemmer(check_nonstandard)
    for i in range(n_trials):
        stemmer_mpstemmer.check_nonstandard = check_nonstandard
        start = time.time()
        output = stemmer_mpstemmer.stem_kalimat(dataset)
        elapsed = time.time() - start
        time_avg += elapsed
    time_avg /= n_trials
    return time_avg, output


def run_pysastrawi(dataset, n_trials):
    time_avg = 0.
    factory = StemmerFactory()
    stemmer_pysastrawi = factory.create_stemmer()
    for i in range(n_trials):
        start = time.time()
        output = stemmer_pysastrawi.stem(dataset)
        elapsed = time.time() - start
        time_avg += elapsed
    time_avg /= n_trials
    return time_avg, output


if __name__ == '__main__':

    stemmer_mpstemmer = mpstemmer.MPStemmer(True)
    factory = StemmerFactory()
    stemmer_pysastrawi = factory.create_stemmer()

    n_benar = 0
    for i, kata in enumerate(kata_uji_std):
        try:
            akar = stemmer_mpstemmer.stem(kata, rigor=False)
            pesan = "(OK)"
            if akar != kata_uji_std_jawaban[i]:
                pesan = f'(Salah. Seharusnya "{kata_uji_std_jawaban[i]}")'
            else:
                n_benar += 1
            print(f'{i + 1}. {kata} -> {akar} {pesan}')
        except:
            print(f'error saat memroses `{kata}`')

    print(f'akurasi kata60: {float(n_benar) / len(kata_uji_std)}')

    print('***')

    import re

    with open('benchmark_dataset/indoprogress_1.txt', 'r') as f:
        indoprogress_1 = f.read().lower().replace('\n', ' ')
        indoprogress_1 = re.sub(r'[\W-]+', ' ', indoprogress_1)

    print('indoprogress 1 n words: ', len(indoprogress_1))

    n_trials = 1000

    """
    mpstemmer with checking nonstandard words
    """
    time_avg, output = run_mpstemmer(indoprogress_1, True, n_trials)
    print(time_avg)

    """
    mpstemmer without checking nonstandard words
    """
    time_avg, output = run_mpstemmer(indoprogress_1, False, n_trials)
    print(time_avg)
    print(output)

    """
    pysastrawi
    """
    time_avg, output = run_pysastrawi(indoprogress_1, n_trials)
    print(time_avg)
    print(output)
