import itertools


def apply_list_func(lst, func):
    res = []
    for i in lst:
        res += func(i)
    return res


class CSSNonstandard:
    def fix_ell_CeC(self, kata, kosakata):
        # ...CeC 
        # >> temen, pegel, nyesel, ngenes
        pass
    
    def fix_ell_CrV_ell(self, kata):
        # ...CrV... --> ...CerV... | ...CrV... 
        # >> crita, trampil, terawang, sebrang --> cerita | terampil | terawang | seberang
        res = [kata]
        if 'r' in kata:
            idx = kata.index('r')
            if (idx > 0) and (idx < len(kata) - 1) and not(kata[idx - 1] in 'aiueo') and (kata[idx + 1] in 'aiueo'):
                res.append(kata[:idx]+'e'+kata[idx:])                
        return res

    def remove_inflectional_suffixes(self, kata):
        res = [] #kata
        tmp = kata
        while tmp.endswith(('kah', 'lah', 'tah', 'pun', 'nya', 'ku', 'mu')):
            if tmp.endswith(('ku', 'mu')):
                tmp = tmp[:-2]
                res.append(tmp)
            if tmp.endswith(('kah', 'lah', 'tah', 'pun', 'nya')):
                tmp = tmp[:-3]
                res.append(tmp)
        if len(res) == 0:
            return [kata]
        return res
    
    def remove_derivational_suffix(kata, kosakata):
        res = []
        tmp = kata
        while tmp.endswith(('in', 'kan', 'an')):
            if tmp.endswith(('in', 'an')):
                tmp = tmp[:-2]
            
            if
        
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

    def remove_prefix(self, kata):
        res = []

        if kata.startswith('nge'):
            ridx = len(kata)                
            res.append(kata[3:])
            res.append('k'+kata[2:])

        # ngVC... --> ng-VC... | ng-hVC... | ng-kVC...
        elif kata.startswith('ng'):  
            res.append(kata[2:])
            res.append('h'+kata[2:])
            res.append('k'+kata[2:])   

        elif kata.startswith('ny'):    
            res.append(kata[2:])
            res.append('h'+kata[2:])
            res.append('k'+kata[2:]) 
        
        if len(res) == 0:
            return [kata]
        return res

    def stem(self, kata):
        nosuffixes = self.remove_inflectional_suffixes(kata)#self.remove_inflectional_suffixes(kata)
        noprefixes = apply_list_func(nosuffixes, self.remove_prefix)

        no_ell_CrV_ells = apply_list_func(noprefixes, self.fix_ell_CrV_ell)
        
        return no_ell_CrV_ells

if __name__ == '__main__':
    stemmer = CSSNonstandard()
    print(stemmer.stem('ngrapikan'))
    print(stemmer.stem('ngelakuinnyapun'))