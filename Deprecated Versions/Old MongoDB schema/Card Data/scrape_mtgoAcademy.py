#!/usr/bin/env python3
'''
mtgoAcademy FORMAT:
NAME;SHINE;EDITION;SELL;DATE;TIME
BOOSTER;SET;BUY;SELL;DATE;TIME
Total pages: 134
Results per page: 20
Pause per page: 4 seconds
'''

# TODO: Add Quantity in Stock for each card.
# TODO: Add Booster data.
# TODO: Update csv format. Reference mtgo collection csv/txt export.

import urllib.request
import urllib.parse
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup as bs

# Timestamp for data.
NOW = datetime.utcnow()
URL = 'http://www.mtgoacademy.com/store/'
# FRF, KTK, M15, JOU, BNG, THS, VMA, and MMA.
EDITIONS = [
['FRF', [
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=17',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=18',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/frf/?page=19'
]],
['KTK', [
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=17',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=18',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=19',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=20',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=21',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=22',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=23',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=24',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=25',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=26',
'http://www.mtgoacademy.com/store/cards_by_set/khans_of_tarkir_block/ktk/?page=27'
]],
['M15', [
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=17',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=18',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=19',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=20',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=21',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=22',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=23',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=24',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=25',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=26',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=27',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=28',
'http://www.mtgoacademy.com/store/cards_by_set/core_set_block/m15/?page=29'
]],
['JOU', [
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/jou/?page=17'
]],
['BNG', [
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/bng/?page=17'
]],
['THS', [
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=17',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=18',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=19',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=20',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=21',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=22',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=23',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=24',
'http://www.mtgoacademy.com/store/cards_by_set/theros_block/ths/?page=25'
]],
['VMA', [
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=17',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=18',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=19',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=20',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=21',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=22',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=23',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=24',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=25',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=26',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=27',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=28',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=29',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=30',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=31',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=32',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/vma/?page=33'
]],
['MMA', [
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=2',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=3',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=4',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=5',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=6',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=7',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=8',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=9',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=10',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=11',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=12',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=13',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=14',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=15',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=16',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=17',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=18',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=19',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=20',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=21',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=22',
'http://www.mtgoacademy.com/store/cards_by_set/masters_block/mma/?page=23'
]]
]

def get_soup(url, page=1):
    '''
    Change headers for url request and generate html soup from url.
    page is the current page number for edition loop.
    '''
    # Progress marker.
    print('eating soup')
    
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    # Standard request if only 1 page, otherwise generate POST and then get soup.
    if page == 1:
        req = urllib.request.Request(url,headers=headers)
        resp = urllib.request.urlopen(req)
        soup = bs(resp.read())
        return soup
    else:
        values = {'page': page}
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')
        req = urllib.request.Request(url,data,headers=headers)
        resp = urllib.request.urlopen(req)
        soup = bs(resp.read())
        return soup

def get_edition_links(soup):
    '''
    Returns a list of links of editions sold on mtgoAcademy.
    '''
    # Progress marker.
    print('lotta links')
    # Find tags with links, then scrape href for each edition.
    tags = soup.find_all('a', attrs={'class':'ONLINE_CLASSIC'})
    links = [card.get('href') for card in tags]
    return links

def extract_data(soup):
    '''
    Extracts data for each card in soup. Returns data, a list of cards.
    '''
    # Progress marker.
    print('extracting magic')
    # List to which data will be appended.
    data = []
    cards = soup.find_all('div', attrs={'class':'product_thumb'})
    for card in cards:
        # Find name, shine, edition, and sell price.
        name = card.a.text
        if re.search('Premium', card.text):
            shine = 'foil'
        else:
            shine = 'regular'
        edition = re.search(r'Short Set Name: (\w{2,3})\n', card.text).group(1)
        sell = card.find('div', attrs={'class':'price'}).text.replace('$','').strip()
        
        # Gather bits of data for card into list to be joined and appended to data.
        card_data = [name, shine, edition, sell, str(NOW.date()), str(NOW.time())]
        data.append(';'.join(card_data))
    return data

def update_file(data):
    '''
    Saves card data to file. Takes a list of cards.
    '''
    #Progress marker.
    print('refrigerating')

    saveFile = open('data_mtgoAcademy.txt', 'a')
    for card in data:
        saveFile.write(card + '\n')
    saveFile.close()

def main():
    for edition in EDITIONS:
        for link in edition[1]:
            soup = get_soup(link)
            data = extract_data(soup)
            update_file(data)
            time.sleep(4)
          
if __name__ == '__main__':
    main()

# Test code.         
'''
for link in EDITIONS[0][1]:
    soup = get_soup(link)
    data = extract_data(soup)
    update_file(data)
    time.sleep(4)
'''
