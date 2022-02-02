#!/usr/bin/env python3


import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pymongo
import time, datetime, random


# GLOBAL VARIABLES.
VENDOR = 'mtgoTraders'

# Tuples of (shortcode, [links]) for main loop.
MTGOTRADERSSITE = [
('DTK', [
'http://www.mtgotraders.com/store/dragons_of_tarkir.html?limit=160&page=1',
'http://www.mtgotraders.com/store/dragons_of_tarkir.html?limit=160&page=2'
]),
('FRF', [
'http://www.mtgotraders.com/store/fate_reforged.html?limit=160&page=1',
'http://www.mtgotraders.com/store/fate_reforged.html?limit=160&page=2'
]),
('KTK', [
'http://www.mtgotraders.com/store/khans_of_tarkir.html?limit=160&page=1',
'http://www.mtgotraders.com/store/khans_of_tarkir.html?limit=160&page=2'
]),
]


def stealth_soup(url):
    '''
    Returns a BeautifulSoup of the given url. Supply url.
    Gets links from get_expansions_links function
    '''
    # Progress marker.
    print('eating soup')
    
    # Change 'User-Agent' to disguise python.
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

    # GET request to generate HTTP Response Object.
    req = urllib.request.Request(url,headers=headers)
    resp = urllib.request.urlopen(req)
    
    soup = bs(resp.read())
    
    return soup


def get_pricePoints_mtgoTraders(soup):
    '''
    Extracts card update data from soup. Returns cardUpdates, a list of updates in dictionary form.
    '''
    
    # Progress marker.
    print('extracting edibles')
    
    pricePoints = []
    
    # Extract the table of cards from the page.
    cardTable = soup.find_all('table')[1]
    cards = cardTable.find_all('tr')
    
    for card in cards:
        # Assess premium first.
        if 'Foil' in card.find(class_='cardname').text:
            premium = 'Yes'
        else:
            premium = 'No'
            
        # Card name, strip '*Foil*' from text if there.
        name = card.find(class_='cardname').text.replace('*Foil*','').strip()
        shortcode = card.find(class_='set').text.strip()
        
        # Sell price by try/except loop in case of empty price field.
        try:
            sell = float(card.find(class_='price').text.replace('$','').strip())
        except:
            sell = None
            
        # Quantity, as a test because not all websites show this.
        quantity = int(card.find(class_='qty').text.strip())

        pricePoints.append(
            {
                'vendor': VENDOR,
                'name': name,
                'shortcode': shortcode,
                'premium': premium,
                'quantity': quantity,
                'buy': None,
                'sell': sell,
                'timestamp': datetime.datetime.utcnow()
            }
        )

    # Establish a mongoDB connection and declare which database to use.
    client = pymongo.MongoClient()
    db = client.card_data

    # insert pricePoints into collection
    db.pricePoints.insert_many(pricePoints)


def main():
    
    while True:
        try:
            for shortcode, links in MTGOTRADERSSITE:
                for link in links:
                    # get soup
                    soup = stealth_soup(link)

                    # extract pricePoints
                    get_pricePoints_mtgoTraders(soup)
                    
                    # interval between scrapes
                    time.sleep(random.randint(5,10))
                    
                print('done with: ' + VENDOR + ' ' + shortcode)
                
        except Exception as e:
            with open('ErrorLog_'+VENDOR+'.txt','a') as errorLog:
                errorLog.write('Error: ' + str(e))

        print('Finished '+VENDOR)
                
        # Get updates every hour.
        time.sleep(random.randint(3500,3600))
        
'''
if __name__ == '__main__':
    main()
'''
