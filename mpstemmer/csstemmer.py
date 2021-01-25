"""
Confix-stripping stemmer, Adriani et al., 2007

[[[DP+]DP+]DP+] root-word [[+DS][+PP][+P]]
"""


def is_vowel(c):
    return c in 'aiueo'


def is_consonant(c):
    # faster than checking 21 other characters
    return not (c in 'aiueo')


def is_in_dict(kata, kosakata):
    return kata in kosakata


def remove_inflectional_suffixes(kata, kosakata):
    res = kata

    if is_in_dict(res, kosakata) or (len(res) <= 5):
        return res

    if res[-3:] in ['kah', 'lah', 'tah', 'pun', 'nya']:
        res = remove_inflectional_suffixes(res[:-3], kosakata)
        # res = res[-3:]
    if res[-2:] in ['ku', 'mu']:
        # res = remove_inflectional_suffixes(res[:-2], kosakata)
        res = res[:-2]
    return res


def remove_derivational_suffix(kata, kosakata):
    res = kata
    if is_in_dict(res, kosakata) or (len(res) <= 5):
        return res

    if res.endswith('i'):
        res = kata[:-1]
        # res = remove_derivational_suffix(res, kosakata)
    elif kata.endswith('kan'):
        res = kata[:-3]
        # res = remove_derivational_suffix(res, kosakata)
    elif kata.endswith(('an')):
        res = kata[:-2]
        # res = remove_derivational_suffix(res, kosakata)
    return res


def remove_prefixes(kata, kosakata, n_removed_suffixes, last_removed):
    res = kata
    # base case
    if (is_in_dict(res, kosakata)) or (len(res) <= 5):
        return res

    elif (res[:2] in ['di', 'ke', 'se', 'ku']) and (res[:2] != last_removed) and (n_removed_suffixes < 3):
        # simple prefix, just remove it
        res = remove_prefixes(res[2:], kosakata, n_removed_suffixes + 1, res[:2])

    elif res.startswith('be'):
        # rule 1: berV --> ber-V | be-rV
        if (res[2] == 'r') and is_vowel(res[3]):
            case1 = res[3:]  # ber-V
            case2 = res[2:]  # be-rV
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:2])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 2: berCAP... --> ber-CAP..., C != 'r', P != 'er'
        # C, A, P = res[3], res[4], res[5:7]
        elif (res[2] == 'r') and (res[3] != 'r') and is_consonant(res[3]) and (res[5:7] != 'er'):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:2])

        # rule 3: berCAerV... --> ber-CAerV..., C != 'r' (bercerita, bergerigi)        
        elif (res[2] == 'r') and (res[3] != 'r') and is_consonant(res[3]):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:2])

        # rule 4: belajar... --> bel-ajar...
        elif res[:7] == 'belajar':
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:2])

        # rule 5: beC1erC... --> be-C1erC..., C1 != {'r'|'l'}  (beterbangan)
        elif not (res[2] in ['r', 'l']) and is_consonant(res[2]) and is_consonant(res[5]):
            res = remove_prefixes(res[2:], kosakata, n_removed_suffixes + 1, res[:2])

    elif res.startswith('te'):
        # rule 6: terV... --> ter-V... | te-rV... (terangkat | terundung)
        if (res[2] == 'r') and is_vowel(res[3]):
            case1 = res[3:]  # ter-V
            case2 = res[2:]  # te-rV
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:2])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 7: terCP... --> ter-CP... where C!=‘r’ and P!=‘er’
        elif res.startswith('ter') and (res[3] != 'r') and (res[4:6] != 'er'):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:3])

        # rule 8: terCer... --> ter-Cer... where C!=‘r’
        elif res.startswith('ter') and (res[3] != 'r') and (res[4:6] == 'er'):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:3])

        # rule 9: teC1erC2... --> te-C1erC2... where C!=‘r’
        elif (res[2] != 'r') and (res[3:5] == 'er') and (is_consonant(res[5])):
            res = remove_prefixes(res[2:], kosakata, n_removed_suffixes + 1, res[:2])

    elif res.startswith('me'):
        # rule 10: me{l|r|w|y}V... --> me-{l|r|w|y}V...
        if res.startswith(('mel', 'mer', 'mew', 'mey')) and is_vowel(res[3]):
            res = remove_prefixes(res[2:], kosakata, n_removed_suffixes + 1, res[:2])

        # rule 11: mem{b|f|v}... --> mem-{b|f|v}...
        elif res.startswith(('memb', 'memf', 'memv')):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:4])

        # rule 12: mempe... --> mem-pe...
        elif res.startswith('mempe'):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:5])

        # rule 13: mem{rV|V}... --> me-m{rV|V}... | me-p{rV|V}... (memrakarsa, memamerkan)
        elif (res.startswith('memr') and is_vowel(res[4])) or (res.startswith('mem') and is_vowel(res[3])):
            # if res[3] == 'r':
            case1 = 'm' + res[3:]
            case2 = 'p' + res[3:]
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:4])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:4])

        # rule 14:  men{c|d|j|z}... --> men-{c|d|j|z}...
        elif res.startswith(('menc', 'mend', 'menj', 'menz')):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:4])

        # rule 15: menV... --> me-nV... | me-tV...
        elif res.startswith('men') and is_vowel(res[3]):
            case1 = 'n' + res[3:]  # me-nV
            case2 = 't' + res[3:]  # me-tV
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:3])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:3])

        # rule 16: meng{g|h|q|k}... --> meng-{g|h|q|k}...
        elif res.startswith(('mengg', 'mengh', 'mengq', 'mengk')):
            res = remove_prefixes(res[4:], kosakata, n_removed_suffixes + 1, res[:4])

        # rule 17:  mengV... --> meng-V... | meng-kV...
        elif res.startswith('meng') and is_vowel(res[4]):
            case1 = res[4:]  # meng-V
            case2 = 'k' + res[4:]  # meng-kV
            case3 = 'h' + res[4:]

            # TODO: Add more cases, with ensured standard word

            # meng-hV --> tambahan sub-rule, untuk akomodasi konstruk tak baku: ngancurin -> mengancurin ->menghancurin
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:4])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:4])
            elif is_in_dict(case3, kosakata):
                res = remove_prefixes(case3, kosakata, n_removed_suffixes + 1, res[:4])

        # rule 18: menyV... --> meny-sV...
        elif res.startswith('meny') and is_vowel(res[4]):
            res = 's' + res[4:]
            res = remove_prefixes(res, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 19: mempV... --> mem-pV... where V != 'e' (mempunyai)
        elif res.startswith('memp') and is_vowel(res[4]) and (res[4] != 'e'):
            res = 'p' + res[4:]
            res = remove_prefixes(res, kosakata, n_removed_suffixes + 1, res[:4])

    elif res.startswith('pe'):
        # rule 20: pe{w|y}V... --> pe-{w|y}V...
        if res.startswith(('pew', 'pey')) and is_vowel(res[3]):
            res = res[2:]
            res = remove_prefixes(res, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 21: perV... --> per-V... | pe-rV...
        elif res.startswith('per') and is_vowel(res[3]):
            case1 = res[3:]
            case2 = res[2:]
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:3])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 22: perCAP... --> per-CAP..., C != 'r', P != 'er'
        # C, A, P = res[3], res[4], res[5:7]
        elif (res[2] == 'r') and (res[3] != 'r') and is_consonant(res[3]) and (res[5:7] != 'er'):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:3])

        # rule 23: perCAerV... --> per-CAerV..., C != 'r' (perceraian)        
        elif (res[2] == 'r') and (res[3] != 'r') and is_consonant(res[3]):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:3])

        # rule 24: pem{b|f|v}... --> pem-{b|f|v}...
        elif res.startswith(('pemb', 'pemf', 'pemv')):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:4])

        # rule 25: pem{rV|V}... --> pe-m{rV|V}... | pe-p{rV|V}... (pemrakarsa, pemamerkan)
        elif (res.startswith('pemr') and is_vowel(res[4])) or (res.startswith('pem') and is_vowel(res[3])):
            # if res[3] == 'r':
            case1 = 'm' + res[3:]
            case2 = 'p' + res[3:]
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:4])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:4])

        # rule 26:  pen{c|d|j|z}... --> pen-{c|d|j|z}...
        elif res.startswith(('penc', 'pend', 'penj', 'penz')):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:4])

        # rule 27: penV... --> pe-nV... | pe-tV...
        elif res.startswith('pen') and is_vowel(res[3]):
            case1 = 'n' + res[3:]  # pe-nV
            case2 = 't' + res[3:]  # pe-tV
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:3])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:3])

        # rule 28: peng{g|h|q}... --> peng-{g|h|q|k}...
        elif res.startswith(('pengg', 'pengh', 'pengq', 'pengk')):
            res = remove_prefixes(res[4:], kosakata, n_removed_suffixes + 1, res[:4])

        # rule 29:  pengV... --> peng-V... | peng-kV...
        elif res.startswith('peng') and is_vowel(res[4]):
            case1 = res[4:]  # peng-V
            case2 = 'k' + res[4:]  # peng-kV
            case3 = 'h' + res[4:]

            # peng-hV --> tambahan sub-rule, untuk akomodasi konstruk tak baku: pengancur ->penghancur
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:4])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:4])
            elif is_in_dict(case3, kosakata):
                res = remove_prefixes(case3, kosakata, n_removed_suffixes + 1, res[:4])

        # TODO: lengkapi rule 30 - 33

    return res


def stem(kata, kosakata):
    """
    Untuk beberapa kasus, prefix harus dibuang terlebih dahulu.
    """
    if (
            (kata.startswith('be') and kata.endswith(('lah', 'an', 'i'))) or
            (kata.startswith('me') and kata.endswith('i')) or
            (kata.startswith('di') and kata.endswith('i')) or
            (kata.startswith('pe') and kata.endswith('i')) or
            (kata.startswith('te') and kata.endswith('i'))
    ):
        res = remove_prefixes(kata, kosakata, 0, '')
        res = remove_inflectional_suffixes(res, kosakata)
        res = remove_derivational_suffix(res, kosakata)

        if is_in_dict(res, kosakata):
            return res

    res = remove_inflectional_suffixes(kata, kosakata)
    res = remove_derivational_suffix(res, kosakata)
    res = remove_prefixes(res, kosakata, 0, '')

    if is_in_dict(res, kosakata):
        return res

    """
    Di algoritma original, sebelum nilai fungsi dikembalikan, perlu dilakukan lookup.
    Namun, mpstemmer tidak melakukan itu walau `res` terakhir tidak ada pada kamus, karena masih akan ada proses
    lanjutan (perbaikan kata tak baku).
    """
    return res
