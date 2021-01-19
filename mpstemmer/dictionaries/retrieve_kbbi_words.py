"""
Script untuk mengunduh daftar kata dari kbbi.co.id
"""

import requests
from bs4 import BeautifulSoup

URL_BASE = 'https://kbbi.co.id/daftar-kata'


def words_from_url(url):
    html = BeautifulSoup(requests.get(url).text)
    row = html.find('div', {'class': 'row'})
    items = row.find_all('li')
    return [item.text for item in items]


def get_last_page_num():
    kbbi_page = requests.get(URL_BASE).text
    soup = BeautifulSoup(kbbi_page)
    last_page_url = [x.find('a')['href']
                     for x in soup.find('ul', {'class': 'pagination'})
                     ][-1]
    last_page_num = int(last_page_url[last_page_url.find('=') + 1:])
    return last_page_num


def retrieve_all_words(verbose=True):
    last_page_num = get_last_page_num()

    if verbose:
        print(f'Total halaman: {last_page_num}')

    page_range = range(1, last_page_num + 1)

    all_words = []
    for i in page_range:
        if verbose:
            print(f'Mengunduh {i} dari {last_page_num} halaman')
        all_words += words_from_url(f'{URL_BASE}?page={i}')
    if verbose:
        print('Selesai mengunduh')
    return all_words


with open('kbbi_words.txt', 'w') as f:
    words = retrieve_all_words()
    f.write('\n'.join(words))
