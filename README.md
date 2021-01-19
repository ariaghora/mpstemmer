# mpstemmer
Multi-phase stemmer: stemmer untuk bahasa indonesia, kata baku dan tidak baku.

## Installation
`pip install --upgrade git+https://github.com/ariaghora/mpstemmer.git`

## Usage

```python
from mpstemmer import MPStemmer

stemmer = MPStemmer()

print(stemmer.stem('mengemudi')) # => kemudi
print(stemmer.stem('belajar')) # => ajar
print(stemmer.stem('ngelepas')) # => lepas
print(stemmer.stem('kebayang')) # => bayang

print(stemmer.stem_kalimat('ngelupain mantan tuh ngga susah kok bro'))
# => lupa mantan itu tidak susah kok bro
```

## Reference
The base stemmer algorithm is based on Adriani et al. (2007)

Adriani, M., Asian, J., Nazief, B., Tahaghoghi, S.M. and Williams, H.E., 2007. Stemming Indonesian: A confix-stripping approach. ACM Transactions on Asian Language Information Processing (TALIP), 6(4), pp.1-33.

## Known issues
- Implemented rules so far:
  - [x] "be-": rule 1-5 (completed)
  - [ ] "te-": rule 6
  - [ ]  "me-": rule 12-19
  - [ ]  "pe-": -
