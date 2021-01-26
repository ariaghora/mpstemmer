## Performance comparison

### Standard affixed words

Following reports are based on the result of running `simplebenchmark.py`.

|Method|1 trial|100 trials (avg. per trial)|1000 trials (avg. per trial)|
|------|-------|---------------------------|----------------------------|
|PySastrawi|55.56 ms|1.56 ms|1.07 ms|
|**mpstemmer**|1.95 ms|0.52 ms|0.50 ms|
|**mpstemmer** (skip checking nonstandard words)|1.62 ms|0.50 ms|0.48 ms|

- Refer to `benchmark_dataset` folder for the reference of used data
- Lower is better

### Nonstandard affixed words

#### Correct stemming rate
On 60-words test cases, following is the performance comparison.
You may refer to the refered article for the list of words.

|Method|Correct stemming rate|
|------|---------------------|
|PySastrawi|33.33%|
|Putra, et al. (2018)|96.6%|
|Qulub, et al. (2018)|85%|
|**mpstemmer** (non-rigorous) |90%|
|**mpstemmer** (rigorous mode)|95%|

- Other than mpstemmer, the scores are based on reported number in each paper
- More benchmarks are to be added.
- The mpstemmer's performance at current early stage is okay.
- Mpstemmer (rigorous) means we perform an additional step: computing levenshtein distance agaist the dictionary in case the stemming result cannot be found in the dictionary
- Mpstemmer (non-rigorous) works without computing any distance, so it is way faster than the other three.
- Gotta work harder to improve the performance :sleepy:.

#### Mpstemmer (non-rigorous) stemming result

|No|Word|Stemming Result|Remark|
|--|----|---------------|------|
| 1 | nerjang | terjang | Correct |
| 2 | nuduh | tuduh | Correct |
| 3 | nerima | terima | Correct |
| 4 | negur | tegur | Correct |
| 5 | mukul | pukul | Correct |
| 6 | mimpin | mimpin | Wrong. It should be "pimpin" |
| 7 | nyoba | nyoba | Wrong. It should be "coba" |
| 8 | nyiram | siram | Correct |
| 9 | nyuruh | suruh | Correct |
| 10 | nyimpen | simpan | Correct |
| 11 | nyebrang | nyebrang | Wrong. It should be "seberang" |
| 12 | nganggep | anggap | Correct |
| 13 | ngamuk | amuk | Correct |
| 14 | ngambil | ambil | Correct |
| 15 | ngebuka | buka | Correct |
| 16 | ngebantu | bantu | Correct |
| 17 | ngelepas | lepas | Correct |
| 18 | kebayang | bayang | Correct |
| 19 | keinjek | injak | Correct |
| 20 | kekabul | kabul | Correct |
| 21 | kepergok | pergok | Correct |
| 22 | ketipu | tipu | Correct |
| 23 | keulang | ulang | Correct |
| 24 | kewujud | wujud | Correct |
| 25 | critain | critain | Wrong. It should be "cerita" |
| 26 | betulin | betul | Correct |
| 27 | manjain | manja | Correct |
| 28 | gangguin | ganggu | Correct |
| 29 | gantian | ganti | Correct |
| 30 | ikutan | ikut | Correct |
| 31 | musuhan | musuh | Correct |
| 32 | sabunan | sabun | Correct |
| 33 | temenan | teman | Correct |
| 34 | tukeran | tukar | Correct |
| 35 | nanyain | nanyain | Wrong. It should be "tanya" |
| 36 | nunjukin | tunjuk | Correct |
| 37 | mentingin | penting | Correct |
| 38 | megangin | pegang | Correct |
| 39 | nyelametin | selamat | Correct |
| 40 | nyempetin | sempat | Correct |
| 41 | ngorbanin | ngorbanin | Wrong. It should be "korban" |
| 42 | ngadepin | hadap | Correct |
| 43 | ngebuktiin | bukti | Correct |
| 44 | ngewarnain | warna | Correct |
| 45 | kedengeran | dengar | Correct |
| 46 | ketemuan | temu | Correct |
| 47 | beneran | benar | Correct |
| 48 | ginian | begini | Correct |
| 49 | kawinan | kawin | Correct |
| 50 | mainan | main | Correct |
| 51 | parkiran | parkir | Correct |
| 52 | duluan | dulu | Correct |
| 53 | gendutan | gendut | Correct |
| 54 | karatan | karat | Correct |
| 55 | palingan | paling | Correct |
| 56 | sabaran | sabar | Correct |
| 57 | kebagusan | bagus | Correct |
| 58 | sanaan | sana | Correct |
| 59 | cepetan | cepat | Correct |
| 60 | sepagian | pagi | Correct |

#### Mpstemmer (rigorous) stemming result
|No|Word|Stemming Result|Remark|
|--|----|---------------|------|
| 1 | nerjang | terjang | Correct |
| 2 | nuduh | tuduh | Correct |
| 3 | nerima | terima | Correct |
| 4 | negur | tegur | Correct |
| 5 | mukul | pukul | Correct |
| 6 | mimpin | merik | Wrong. It should be "pimpin" |
| 7 | nyoba | coba | Correct |
| 8 | nyiram | siram | Correct |
| 9 | nyuruh | suruh | Correct |
| 10 | nyimpen | simpan | Correct |
| 11 | nyebrang | seberang | Correct |
| 12 | nganggep | anggap | Correct |
| 13 | ngamuk | amuk | Correct |
| 14 | ngambil | ambil | Correct |
| 15 | ngebuka | buka | Correct |
| 16 | ngebantu | bantu | Correct |
| 17 | ngelepas | lepas | Correct |
| 18 | kebayang | bayang | Correct |
| 19 | keinjek | injak | Correct |
| 20 | kekabul | kabul | Correct |
| 21 | kepergok | pergok | Correct |
| 22 | ketipu | tipu | Correct |
| 23 | keulang | ulang | Correct |
| 24 | kewujud | wujud | Correct |
| 25 | critain | cerita | Correct |
| 26 | betulin | betul | Correct |
| 27 | manjain | manja | Correct |
| 28 | gangguin | ganggu | Correct |
| 29 | gantian | ganti | Correct |
| 30 | ikutan | ikut | Correct |
| 31 | musuhan | musuh | Correct |
| 32 | sabunan | sabun | Correct |
| 33 | temenan | teman | Correct |
| 34 | tukeran | tukar | Correct |
| 35 | nanyain | pena | Wrong. It should be "tanya" |
| 36 | nunjukin | tunjuk | Correct |
| 37 | mentingin | penting | Correct |
| 38 | megangin | pegang | Correct |
| 39 | nyelametin | selamat | Correct |
| 40 | nyempetin | sempat | Correct |
| 41 | ngorbanin | mengor | Wrong. It should be "korban" |
| 42 | ngadepin | hadap | Correct |
| 43 | ngebuktiin | bukti | Correct |
| 44 | ngewarnain | warna | Correct |
| 45 | kedengeran | dengar | Correct |
| 46 | ketemuan | temu | Correct |
| 47 | beneran | benar | Correct |
| 48 | ginian | begini | Correct |
| 49 | kawinan | kawin | Correct |
| 50 | mainan | main | Correct |
| 51 | parkiran | parkir | Correct |
| 52 | duluan | dulu | Correct |
| 53 | gendutan | gendut | Correct |
| 54 | karatan | karat | Correct |
| 55 | palingan | paling | Correct |
| 56 | sabaran | sabar | Correct |
| 57 | kebagusan | bagus | Correct |
| 58 | sanaan | sana | Correct |
| 59 | cepetan | cepat | Correct |
| 60 | sepagian | pagi | Correct |


## References

- Adriani, M., Asian, J., Nazief, B., Tahaghoghi, S.M. and Williams, H.E., 2007. Stemming Indonesian: A confix-stripping approach. ACM Transactions on Asian Language Information Processing (TALIP), 6(4), pp.1-33.
- Putra, Rahardyan Bisma Setya, Ema Utami, and Suwanto Raharjo. "Optimalisasi Stemming Kata Berimbuhan Tidak Baku Pada Bahasa Indonesia Dengan Levenshtein Distance." Jurnal Informatika: Jurnal Pengembangan IT 3.2 (2018): 200-205.
- Qulub, Mudawil, Ema Utami, and Andi Sunyoto. "Stemming Kata Berimbuhan Tidak Baku Bahasa Indonesia Menggunakan Algoritma Jaro-Winkler Distance." Creative Information Technology Journal 5.4 (2020): 254-263.
