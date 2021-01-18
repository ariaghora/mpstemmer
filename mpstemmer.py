import json
import editdistance
import csstemmer

"""
kumpulan kata dari KBBI daring
"""
KOSAKATA = [kata.lower() for kata in open('kbbi_words.txt', 'r').read().split('\n')]

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


def proc_suffix_in(kata):
    res = kata
    if kata.endswith('in'):
        res = kata[:-2]
    return res


def proc_prefix_ng(kata):
    res = kata


def proc_affix_ng_in(kata):
    """
    Stemming kata dengan pola (ngu|nge|ng)+word+in. Postfix -i diasumsikan tertangani via similarity search.
    :param kata:
    :return:
    """
    res = kata

    if kata.startswith('nge') and kata.endswith('in'):
        """ 
        Langsung buang afiks dan kembalikan hasilnya jika kemungkinan tidak terjadi overstemming (len(kata) > 4). 
        Kesalahan akan diakomodasi similarity search di tahap selanjutnya. 
        """
        res = kata[3:-2]
        if len(res) >= 4:
            return res

    elif kata.startswith('ng') and kata.endswith('in'):
        res = '-' + kata[2:-2]

    elif kata.startswith('ng') and kata.endswith('i'):
        res = '-' + kata[2:-1]

    elif kata.startswith('nge'):
        res = '-' + kata[3:]

    return res


def stem_kata(kata):
    """
    :param kata: kata tak baku.
    :return: kata yang dibakukan.
    """
    res = kata

    res, fixed = fix_common(res)
    if fixed:
        return res

    """ Lapis 1: cari di KBBI (eksak). """
    if res in KOSAKATA:
        return res

    """ Lapis 2: jika tidak ditemukan, ada kemungkinan kata masih terafiksasi. Lakukan stemming. """
    # TODO: implementasi stemmer untuk kata baku. Heeeelp.
    # res = stem_formal(res)

    """ Lapis 3: jika tidak ditemukan, ada kemungkinan kata tidak baku. Lakukan pembakuan. """
    res = proc_affix_ng_in(res)
    res = proc_suffix_in(res)

    """ Lapis 4: cari di KBBI (berdasarkan kemiripan/tak eksak). """
    res = get_top_1_matching(res)

    return res


def stem_kalimat(kalimat):
    """
    :param kalimat: Kalimat (baris kata terpisah spasi) yang akan dibakukan.
    Sementara ini, karakter non-alfanumerik akan dihilangkan.
    :return: Kalimat berisi kata-kata yang sudah dibakukan.
    """
    res = []
    words = kalimat.split(' ')
    for kata in words:
        res.append(stem_kata(kata))
    return ' '.join(res)


if __name__ == '__main__':
    kalimat_raw = 'ngerampok tuh dosa bang, apa ga takut?'
    kalimat_stem = stem_kalimat(kalimat_raw)
    print(f'           raw : {kalimat_raw}')
    print(f'hasil stemming : {kalimat_stem}')

    kalimat_raw = 'ngelupain mantan tuh nggak sulit kok'
    kalimat_stem = stem_kalimat(kalimat_raw)
    print(f'           raw : {kalimat_raw}')
    print(f'hasil stemming : {kalimat_stem}')

    print(csstemmer.stem('nilaiku', KOSAKATA))
    print(csstemmer.stem('berai', KOSAKATA))
    print(csstemmer.stem('bukankah', KOSAKATA))

    print(csstemmer.stem('bercerita', KOSAKATA))
    print(csstemmer.stem('berlarian', KOSAKATA))
    print(csstemmer.stem('belajar', KOSAKATA))
    print(csstemmer.stem('beterbangan', KOSAKATA))

    print(csstemmer.stem('terangkat', KOSAKATA))
    print(csstemmer.stem('terundung', KOSAKATA))
