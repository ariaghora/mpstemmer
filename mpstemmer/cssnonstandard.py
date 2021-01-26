import itertools

class CSSNonstandard:
    def fix_ell_CeC(self, kata, kosakata):
        # ...CeC 
        # >> temen, pegel, nyesel, ngenes
        pass
    
    def fix_ell_CrV_ell(self, kata, kosakata):
        # ...CrV... --> ...CerV... | ...CrV... 
        # >> crita, trampil, terawang, sebrang --> cerita | terampil | terawang | seberang
        res = [kata]
        if 'r' in kata:
            idx = kata.index('r')
            if (idx > 0) and (idx < len(kata) - 1) and not(kata[idx - 1] in 'aiueo') and (kata[idx + 1] in 'aiueo'):
                res.append(kata[:idx]+'e'+kata[idx:])                
        return res

    def remove_prefix(self, kata, kosakata):
        # res = [kata]
        res = []

        if kata.startswith('nge'):
            ridx = len(kata)
            if kata.endswith(('in', 'i')):
                ridx = kata.rindex('i')
                res.append(kata[3:ridx])
                res.append('k'+kata[2:ridx])    
            res.append(kata[3:])
            res.append('k'+kata[2:])

        # ngVC... --> ng-VC... | ng-hVC... | ng-kVC...
        elif kata.startswith('ng'):
            ridx = len(kata)
            if kata.endswith(('in', 'i')):
                ridx = kata.rindex('i')
                res.append(kata[2:ridx])
                res.append('h'+kata[2:ridx])
                res.append('k'+kata[2:ridx])
            res.append(kata[2:])
            res.append('h'+kata[2:])
            res.append('k'+kata[2:])   
        return res

    def stem(self, kata):
        noprefixes = self.remove_prefix(kata, None)

        no_ell_CrV_ells = []
        for word in noprefixes:
            no_ell_CrV_ells += self.fix_ell_CrV_ell(word, None)
        return no_ell_CrV_ells

stemmer = CSSNonstandard()
print(stemmer.stem('ngorbanin'))