#!/usr/bin/env python3


import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pymongo
import time, datetime, random


# GLOBAL VARIABLES.
VENDOR = 'jbStore'
# Tuples of (shortcode, [links]) for main loop.
JBSTORESITE = [
('DTK', [
'http://www.jbmtgo.com/?mod=sett&fra=0&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=19&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=38&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=57&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=76&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=95&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=114&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=133&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=152&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=171&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=190&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=209&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=228&sett=Dragons%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=247&sett=Dragons%20of%20Tarkir'
]),
('FRF', [
'http://www.jbmtgo.com/?mod=sett&fra=0&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=13&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=26&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=39&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=52&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=65&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=78&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=91&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=104&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=117&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=130&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=143&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=156&sett=Fate%20Reforged',
'http://www.jbmtgo.com/?mod=sett&fra=169&sett=Fate%20Reforged'
]),
('KTK', [
'http://www.jbmtgo.com/?mod=sett&sett=Khans%20of%20Tarkir&fra=0',
'http://www.jbmtgo.com/?mod=sett&fra=18&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=36&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=54&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=72&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=90&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=109&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=126&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=144&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=162&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=180&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=198&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=216&sett=Khans%20of%20Tarkir',
'http://www.jbmtgo.com/?mod=sett&fra=234&sett=Khans%20of%20Tarkir'
])
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


# Needs more testing. Currently not used in main loop.
def get_scrapeLinks_jbStore():
    jbSite = 'http://www.jbmtgo.com/'
    scrapeLinks = []
    
    soup = get_soup(jbSite)
    # Get div table with set menu.
    expansionsTable = soup.find('div',id='meny')
    # Get links for all pages except last two, which are boosters and complete sets.
    # URL of main page concatonated with the href link portion (above) for each expansion.
    # Could edit code later to scrape those last two.
    expansionPages = [jbSite+link.get('href') for link in expansionsTable.find_all('a')[:-2]]
    # Each expansion here is a link to the first page of its corresponding set.
    for expansion in expansionPages:
        soup = get_soup(expansion)
        # Link table is a div tag with id='tabmeny'.
        linkTable = soup.find('div',id='tabmeny')
        expansionLinks = [jbSite+link.get('href') for link in linkTable.find_all('a')]
        for link in expansionLinks:
            scrapeLinks.append(link)
        # Courtesy.
        time.sleep(1)
    print('done!')
    return scrapeLinks


def get_pricePoints_jbStore(soup, shortcode):
    '''
    Returns a list of formatted card data from URL.
    '''
    
    # Progress marker.
    print('extracting edibles')
    
    # Create a list for card data to be written to file.
    pricePoints = []
    
    # Find all card sections in the soup.
    cards = soup.find_all('div', attrs={'cardmain'})
    
    for card in cards:    
        # Name
        name = card.h2.text.strip()
        # Price
        if re.search('Out of stock', card.text) and re.search('Foil out of stock', card.text):
            # If card has neither normal nor foil prices.
            sell = None
            sellFoil = None
        elif re.search('Out of stock', card.text):
            # If card just has foil price.
            sell = None
            sellFoil = float(re.search(r'\$(\d+\.\d+)', card.text).group(1))
        elif re.search('Foil out of stock', card.text):
            # If card just has normal price.
            sell = float((re.search(r'\$(\d+\.\d+)', card.text).group(1)))
            sellFoil = None
        else:
            # Card has both normal and foil prices.
            # First find all prices in card. First is normal, second is foil.
            prices = card.find_all('strong')
            sell = float(re.search(r'\$(\d+\.\d+)', prices[0].text).group(1))
            sellFoil = float(re.search(r'\$(\d+\.\d+)', prices[1].text).group(1))
            
        # Due to the way jbStore displays prices, create foil and non-foil updates for each card.
        regPoint = {
            'vendor': VENDOR,
            'name': name,
            'shortcode': shortcode,
            'premium': 'No',
            'buy': None,
            'sell': sell,
            'timestamp': datetime.datetime.utcnow()
        }
        foilPoint = {
            'vendor': VENDOR,
            'name': name,
            'shortcode': shortcode,
            'premium': 'Yes',
            'buy': None,
            'sell': sellFoil,
            'timestamp': datetime.datetime.utcnow()
        }
        
        pricePoints.append(regPoint)
        pricePoints.append(foilPoint)
        
    # Establish a mongoDB connection and declare which database to use.
    client = pymongo.MongoClient()
    db = client.card_data

    # insert pricePoints into collection
    db.pricePoints.insert_many(pricePoints)


def main():
    
    while True:
        try:
            for shortcode, links in JBSTORESITE:
                for link in links:
                    # get soup
                    soup = stealth_soup(link)

                    # extract pricePoints
                    get_pricePoints_jbStore(soup, shortcode)

                    # interval between scrapes
                    time.sleep(random.randint(5,10))

                print('done with: ' + VENDOR + ' ' + shortcode)
                    
        except Exception as e:
            with open('ErrorLog_'+VENDOR+'.txt','a') as errorLog:
                errorLog.write('Error: ' + str(e))

        print('Finished '+VENDOR)
                
        # Scrape data every hour.
        time.sleep(random.randint(3500,3600))
        
'''
if __name__ == '__main__':
    main()
'''
