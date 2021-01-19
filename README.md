# mpstemmer
Multi-phase stemmer: stemmer for Indonesian.

The base stemmer algorithm is based on Adriani et al. (2007), modified to work with both standard (baku) and nonstandard (tak baku) words.

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

## Performance comparison

On standard 60-words test cases, following is the performance comparison.
You may refer to the refered article for the list of words.

|Method|Correct stemming rate|
|------|---------------------|
|Putra, et al. (2018)|96.6%|
|Qulub, et al. (2018)|85%|
|**mpstemmer**|81.67%|

More benchmarks are to be added.
The mpstemmer's performance at current early stage is somewhat low.
Gotta work harder :sleepy:.

## References

- Adriani, M., Asian, J., Nazief, B., Tahaghoghi, S.M. and Williams, H.E., 2007. Stemming Indonesian: A confix-stripping approach. ACM Transactions on Asian Language Information Processing (TALIP), 6(4), pp.1-33.
- Putra, Rahardyan Bisma Setya, Ema Utami, and Suwanto Raharjo. "Optimalisasi Stemming Kata Berimbuhan Tidak Baku Pada Bahasa Indonesia Dengan Levenshtein Distance." Jurnal Informatika: Jurnal Pengembangan IT 3.2 (2018): 200-205.
- Qulub, Mudawil, Ema Utami, and Andi Sunyoto. "Stemming Kata Berimbuhan Tidak Baku Bahasa Indonesia Menggunakan Algoritma Jaro-Winkler Distance." Creative Information Technology Journal 5.4 (2020): 254-263.

## Known issues
- Implemented rules so far:
  - [x] "be-": rule 1-5 (completed)
  - [ ] "te-": rule 6
  - [ ]  "me-": rule 12-19
  - [ ]  "pe-": -
