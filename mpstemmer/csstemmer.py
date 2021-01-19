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

    if is_in_dict(res, kosakata):
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
    if is_in_dict(res, kosakata):
        return res

    if res.endswith('i'):
        res = kata[:-1]
        res = remove_derivational_suffix(res, kosakata)
    elif kata.endswith('kan'):
        res = kata[:-3]
        res = remove_derivational_suffix(res, kosakata)
    elif kata.endswith('an'):
        res = kata[:-2]
        res = remove_derivational_suffix(res, kosakata)
    return res


def remove_prefixes(kata, kosakata, n_removed_suffixes, last_removed):
    res = kata
    # base case
    if is_in_dict(res, kosakata):
        return res

    if (res[:2] in ['di', 'ke', 'se', 'ku']) and (res[:2] != last_removed) and (n_removed_suffixes < 3):
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

    # TODO: lengkapi rule 7 - 9

    elif res.startswith('me'):
        # TODO: lengkapi rule 10 - 11

        # TODO: jangan lupa ubah ke `elif`
        # rule 12: mempe... --> mem-pe...
        if res.startswith('mempe'):
            res = remove_prefixes(res[3:], kosakata, n_removed_suffixes + 1, res[:2])

        # rule 13: mem{rV|V}... --> me-m{rV|V}... | me-p{rV|V}... (memrakarsa, memamerkan)
        elif (res.startswith('memr') and is_vowel(res[4])) or (res.startswith('mem') and is_vowel(res[3])):
            # if res[3] == 'r':
            case1 = 'm' + res[3:]
            case2 = 'p' + res[3:]
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:2])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 14:  men{c|d|j|z}... --> men-{c|d|j|z}...
        elif res.startswith(('menc', 'mend', 'menj', 'menz')):
            pass

        # rule 15: menV... --> me-nV... | me-tV...
        elif res.startswith('men') and is_vowel(res[3]):
            case1 = 'n' + res[3:]  # me-nV
            case2 = 't' + res[3:]  # me-tV
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:2])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 16: meng{g|h|q|k}... --> meng-{g|h|q|k}...
        elif res.startswith(('mengg', 'mengh', 'mengq', 'mengk')):
            res = remove_prefixes(res[5:], kosakata, n_removed_suffixes + 1, res[:2])

        # rule 17:  mengV... --> meng-V... | meng-kV...
        elif res.startswith('meng') and is_vowel(res[4]):
            case1 = res[4:]  # meng-V
            case2 = 'k' + res[4:]  # meng-kV
            case3 = 'h' + res[4:]
            # meng-hV --> tambahan sub-rule, untuk akomodasi konstruk tak baku: ngancurin -> mengancurin ->menghancurin
            if is_in_dict(case1, kosakata):
                res = remove_prefixes(case1, kosakata, n_removed_suffixes + 1, res[:2])
            elif is_in_dict(case2, kosakata):
                res = remove_prefixes(case2, kosakata, n_removed_suffixes + 1, res[:2])
            elif is_in_dict(case3, kosakata):
                res = remove_prefixes(case3, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 18: menyV... --> meny-sV...
        elif res.startswith('meny') and is_vowel(res[4]):
            res = 's' + res[4:]
            res = remove_prefixes(res, kosakata, n_removed_suffixes + 1, res[:2])

        # rule 19: mempV... --> mem-pV... where V != 'e' (mempunyai)
        elif res.startswith('memp') and is_vowel(res[4]) and (res[4] != 'e'):
            res = 'p' + res[4:]
            res = remove_prefixes(res, kosakata, n_removed_suffixes + 1, res[:2])
    
    elif res.startswith('pe'):
        # TODO: lengkapi rule 20 - 33
        pass

    return res


def stem(kata, kosakata):
    # in some rare occassions, we need to remove prefixes before suffixes
    # to reduce ambiguities
    if (
            (kata.startswith('be') and kata.endswith('i')) or
            (kata.startswith('be') and kata.endswith('lah')) or
            (kata.startswith('be') and kata.endswith('an')) or
            (kata.startswith('me') and kata.endswith('an')) or
            (kata.startswith('me') and kata.endswith('i')) or
            (kata.startswith('me') and kata.endswith('ku')) or
            (kata.startswith('di') and kata.endswith('i')) or
            (kata.startswith('se') and kata.endswith('an')) or
            (kata.startswith('pe') and kata.endswith('i')) or
            (kata.startswith('te') and kata.endswith('i'))
    ):
        res = remove_prefixes(kata, kosakata, 0, '')
        res = remove_inflectional_suffixes(res, kosakata)
        res = remove_derivational_suffix(res, kosakata)
    else:
        # regular precedence
        res = remove_inflectional_suffixes(kata, kosakata)
        res = remove_derivational_suffix(res, kosakata)
        res = remove_prefixes(res, kosakata, 0, '')

    return res
