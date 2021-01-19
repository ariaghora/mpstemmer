import mpstemmer

if __name__ == '__main__':
    stemmer = mpstemmer.MPStemmer()

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

    n_benar = 0
    for i, kata in enumerate(kata_uji_std):
        try:
            akar = stemmer.stem(kata, rigor=False)
            pesan = "(OK)"
            if akar != kata_uji_std_jawaban[i]:
                pesan = f'(Salah. Seharusnya "{kata_uji_std_jawaban[i]}")'
            else:
                n_benar += 1
            print(f'{kata} -> {akar} {pesan}')
        except:
            print(f'error saat memroses `{kata}`')
    
    print(f'akurasi kata60: {float(n_benar) / len(kata_uji_std)}')


    print('***')

    print(stemmer.stem('mengemudi'))
    print(stemmer.stem('memperjuangkan'))