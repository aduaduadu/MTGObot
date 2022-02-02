#!/usr/bin/env python3
'''
mtgoAcademy FORMAT:
NAME;SHINE;EDITION;SELL;DATE;TIME
BOOSTER;SET;BUY;SELL;DATE;TIME
Total pages: 1982
Results per page: 20
Pause per page: 4 seconds
'''

# BROKEN: Scrapes page 1 of each set for num_pages times.
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

    saveFile = open('data_mtgoAcademy_full.txt', 'a')
    for card in data:
        saveFile.write(card + '\n')
    saveFile.close()

def main():
    # First get all edition links.
    soup = get_soup(URL)
    links = get_edition_links(soup)
    for link in links:
        # Determine number of pages for each edition.
        soup = get_soup(link)
        num_pages = int(re.search(r'\((\d{1,2}) Pages\)', soup.text).group(1))
        for i in range(1, num_pages + 1):
            soup = get_soup(link, page=i)
            data = extract_data(soup)
            update_file(data)
            time.sleep(4)

if __name__ == '__main__':
    main()

# Test code.         
'''
soup = get_soup('http://www.mtgoacademy.com/store/')
links = get_edition_links(soup)
for link in links:
#for link in links[0:2]:
    num_pages = int(re.search(r'\((\d{1,2}) Pages\)', get_soup(link).text).group(1))
    #for i in range(1, num_pages + 1):
    for i in range(1, 4):
        soup = get_soup(link, page=i)
        data = extract_data(soup)
        for card in data:
            print(card)
        time.sleep(4)
'''
