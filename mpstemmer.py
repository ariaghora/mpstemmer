import json
import editdistance
import csstemmer

"""
kumpulan kata dari KBBI daring. Gunakan set karena lebih cepat daripada list untuk method
`__contains()__`.
"""
KOSAKATA = {kata.lower() for kata in open('kbbi_words.txt', 'r').read().split('\n')}

"""
kumpulan kata tak baku yang lazim ditemui
"""
COMMON_INFORMAL = json.loads(open('./common_informal.json', 'r').read())


def get_top_n_matching(kata, n):
    """
    Mencari n kata yang paling mirip dengan `kata`, diukur berdasarkan string edit distance
    :param kata: kata kunci pencarian
    :param n: jumlah kata termirip yang dicari
    :return: `list` berisi `n` kata yang paling mirip dengan `kata`
    """
    dists = [{'dist': editdistance.eval(kata, x), 'word': x} for x in KOSAKATA]
    dists_sorted = sorted(dists, key=lambda x: x['dist'])
    return [x['word'] for x in dists_sorted[:n]]


def get_top_1_matching(kata):
    return get_top_n_matching(kata, 1)[0]


def fix_common(kata):
    """
    Bakukan kata tak baku yang lazim ditemui, seperti 'ngga' (tidak), 'bgt' (banget), dll.
    :param kata: kata yang akan diperbaiki
    :return: tuple `res` (str) dan `fixed` (bool), masing-masing berisi kata yang dibakukan dan status
    apakah kata berhasil dibakukan (atau ditemui pada daftar kata informal lazim).
    """
    res = kata
    fixed = False
    abb_dict = COMMON_INFORMAL

    if kata in abb_dict.keys():
        res = abb_dict[kata]
        fixed = True
    return res, fixed


def proc_prefix_ng(kata):
    res = kata


def check_nonstandard_affixed(kata):
    """
    Heuristik cepat dan sederhana untuk menentukan baku-tidaknya suatu kata.
    Pastikan sebelumnya kata memang tidak ditemukan di kosakata KBBI (dengan pencarian eksak).
    :param kata:
    :return:
    """
    res = kata
    maybe_nonstandard = False
    if res.startswith(('m', 'n', 'ng', 'ny', 'ke')) or res.endswith(('i', 'in', 'an')):
        maybe_nonstandard = True

    return maybe_nonstandard


def ensure_standard_root(kata, kosakata):
    """
    Kata diasumsikan tidak baku. Harus dilakukan pemeriksaan terlebih dahulu sebelum menggunakan fungsi ini.
    Pastikan suffix telah dibuang terlebih dahulu.
    Fungsi ini melakukan perbaikan minor untuk kata-kata seperti, sebel->sebal, (se|menye|nye)sel->nyesal.
    :param kata:
    :param kosakata:
    :return:
    """
    res = kata
    if not (res[-1] in 'aiueo') and (res[-2] == 'e'):
        case1 = res
        case2 = case1[:-2] + 'a' + case1[-1:]

        if case1 in kosakata:
            res = case1
        elif case2 in kosakata:
            res = case2

    return res


def fix_nonstandard_prefix(kata):
    """
    Kata diasumsikan tidak baku. Harus dilakukan pemeriksaan terlebih dahulu sebelum menggunakan fungsi ini.
    Fungsi ini tidak benar-benar memperbaiki suffix hingga memperoleh bentuk valid, a.l., ngeberesin --> mengeberes.
    Stemming lanjutan akan ditangani oleh stemmer standar, a.l., confix-stripping, dll.
    :param kata:
    :return:
    """
    res = kata
    if res.startswith(('m', 'n', 'ng', 'ny')):
        res = 'me' + res

    return res


def fix_nonstandard_suffix(kata):
    res = kata
    # buang suffix sederhana
    if res.endswith('in'):
        res = res[:-2]
    elif res.endswith('i'):
        res = res[:-1]
    return res


def stem_kata(kata, kosakata, rigor=False):
    """
    :param kata: kata tak baku.
    :return: kata yang dibakukan.
    """
    res = kata

    """ 
    Lapis 1: cari di KBBI (eksak). 
    """
    if res in KOSAKATA:
        return res

    """ 
    Lapis 2: cek kemungkinan kata tak baku terafiksasi. Jika ya, bakukan afiksasi.
    """
    maybe_nonstandard = check_nonstandard_affixed(res)
    if maybe_nonstandard:
        res = fix_nonstandard_suffix(res)
        if res in kosakata:
            return res
        res = fix_nonstandard_prefix(res)
        if res in kosakata:
            return res

    """ 
    Lapis 3: Setelah lapis 2, ada kemungkinan kata masih terafiksasi. Lakukan stemming standar,
    karena afiksasi telah dibakukan di lapis 2. 
    """
    res = csstemmer.stem(res, kosakata)

    """ 
    Lapis 4: Hasil lapis 3 belum tentu memperoleh akar kata baku. Karena itu, jika sebelumnya kata telah
    terindikasi tidak baku, pastikan akar kata dibakukan. 
    """
    if maybe_nonstandard:
        res = ensure_standard_root(res, kosakata)

    """ 
    Lapis 5: Opsional. Pencarian lebih detail melalui similarity search. 
    PERINGATAN!!! Ini bisa memakan banyak waktu. 
    """
    if rigor:
        res = get_top_1_matching(res)

    return res


def stem_kalimat(kalimat, kosakata):
    """
    :param kalimat: Kalimat (baris kata terpisah spasi) yang akan dibakukan.
    Sementara ini, karakter non-alfanumerik akan dihilangkan.
    :return: Kalimat berisi kata-kata yang sudah dibakukan.
    """
    res = []
    words = kalimat.split(' ')
    for kata in words:
        res.append(stem_kata(kata, kosakata))
    return ' '.join(res)


if __name__ == '__main__':
    kalimat_raw = 'ngerampok tuh dosa bang, apa ga takut?'
    kalimat_stem = stem_kalimat(kalimat_raw, KOSAKATA)
    print(f'           raw : {kalimat_raw}')
    print(f'hasil stemming : {kalimat_stem}')

    kalimat_raw = 'ngelupain mantan tuh nggak sulit kok'
    kalimat_stem = stem_kalimat(kalimat_raw, KOSAKATA)
    print(f'           raw : {kalimat_raw}')
    print(f'hasil stemming : {kalimat_stem}')

    print(stem_kata('nilaiku', KOSAKATA))
    print(stem_kata('berai', KOSAKATA))
    print(stem_kata('bukankah', KOSAKATA))

    print(stem_kata('bercerita', KOSAKATA))
    print(stem_kata('berlarian', KOSAKATA))
    print(stem_kata('belajar', KOSAKATA))
    print(stem_kata('beterbangan', KOSAKATA))

    print(stem_kata('terangkat', KOSAKATA))
    print(stem_kata('terundung', KOSAKATA))

    print(stem_kata('kuberesin', KOSAKATA))
    print(stem_kata('ngancem', KOSAKATA))
    print(stem_kata('nyesel', KOSAKATA))
    print(stem_kata('ngelurusin', KOSAKATA))
