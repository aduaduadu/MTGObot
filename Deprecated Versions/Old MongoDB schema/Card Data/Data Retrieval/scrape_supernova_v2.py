#!/usr/bin/env python3


import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pymongo
import time, datetime, random


# GLOBAL VARIABLES.
URL = 'http://supernovabots.com/prices_0.txt'
VENDOR = 'supernova'

# Map for scraping entire website. Tuples are (premium,url).
SUPERNOVASITE = [
    ('http://supernovabots.com/prices_0.txt','No'),
    ('http://supernovabots.com/prices_3.txt','Yes')
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


# Function specifically for supernovabots Website. Uses regular expressions.
def get_pricePoints_supernova(soup, premium):
    '''
    Extracts pricePoints data from soup    
    '''
    
    # Progress marker.
    print('extracting edibles')

    # initialize list of price_points to be extracted 
    pricePoints = []

    # Split up soup into individual lines, as each card is on its own line.
    soupSplit = soup.text.splitlines()
    cardList = [line for line in soupSplit if re.search(r'\[\w{2,3}\]', line)]
    
    for card in cardList:
        # Match object. Each card line separates values with specific quantities of characters and spaces.
        # Reference:    (1    )(2    )(3    )
        m = re.search(r'(.{42})(.{10})(.{10})', card)
        
        # Search includes all characters found within a card name: \w, space, comma, and apostrophe.
        name = re.search(r'([ ,\'\w]+)', m.group(1)).group(1).strip()
        shortcode = re.search(r'\[(\w{2,3})\]', m.group(1)).group(1).strip()
        
        try:
            buy = float(m.group(2).strip())
        except:
            buy = None
        try:
            sell = float(m.group(3).strip())
        except:
            sell = None

        # one card vendor price point
        pricePoints.append(
            {
                # vendor is currently hard-coded in.
                'vendor': VENDOR,
                
                'name': name,
                'shortcode': shortcode,
                'premium': premium,
                
                # Store both buy and sell price as numbers (floats).
                'buy': buy,
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
            for url, premium in SUPERNOVASITE:

                # get soup from url
                soup = stealth_soup(url)

                # update pricePoints collection
                get_pricePoints_supernova(soup, premium)

                # interval between scrapes
                time.sleep(random.randint(5,10))
                print('done with: ' + VENDOR + ' ' + premium)
                
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
