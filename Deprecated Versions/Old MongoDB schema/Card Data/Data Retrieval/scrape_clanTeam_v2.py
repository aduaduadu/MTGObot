#!/usr/bin/env python3


import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re
import pymongo
import time, datetime, random


# GLOBAL VARIABLES.
VENDOR = 'clanTeam'
PREMIUM = 'No'


# could update this part to use selenium webdriver
def get_expansionLinks_clanTeam():
    '''
    returns links to all available sets on clanTeam website
    '''
    
    clanTeamSite = 'http://www.mtgoclanteam.com'

    # Change 'User-Agent' to disguise python.
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

    req = urllib.request.Request(clanTeamSite+'/Cards',headers=headers)
    resp = urllib.request.urlopen(req)
    
    soup = bs(resp.read())
    
    # Get div table with set menu.
    setMenu = soup.find('div',id='templatemo_menucards')
    # Set links are all hrefs except the first one.
    links = [clanTeamSite+link.get('href') for link in setMenu.find_all('a')[1:]]

    return links


# uses selenium webdriver and mongodb to update pricePoints
def get_pricePoints_clanTeam(browser, url):

    # Progress marker
    print('getting points')

    # open url
    browser.get(url)

    # initialize list for pricePoints
    pricePoints = []

    # determine shortcode from url
    shortcode = url.split('=')[1]

    # identify critical parts of webpage
    cardTable = browser.find_element_by_css_selector('#cardtable > tbody:nth-child(2)')
    cardList = cardTable.find_elements_by_tag_name('tr')

    for row in cardList:
        elements = row.find_elements_by_tag_name('td')

        name = elements[0].text
        stock = elements[4].text

        # buy as float
        try:
            buy = float(elements[2].text)
        except:
            buy = None

        # if no stock (ie. stock str empty) then sell = None
        if len(stock) == 0:
            sell = None
        else:
            try:
                sell = float(elements[3].text)
            except:
                sell = None

        # one card vendor price point
        pricePoints.append(
            {
                'vendor': VENDOR,
                'name': name,
                'shortcode': shortcode,
                'premium': PREMIUM,
                
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

    links = get_expansionLinks_clanTeam()

    # alter User Agent
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')
    browser = webdriver.Firefox(profile)
    
    while True:
        try:
            
            for url in links:
                
                # updates pricePoints collection
                get_pricePoints_clanTeam(browser, url)

                # interval between scrapes
                time.sleep(random.randint(5,10))
                shortcode = url.split('=')[1]
                print('done with ' + shortcode)
                
        except Exception as e:
            with open('ErrorLog_'+VENDOR+'.txt','a') as errorLog:
                errorLog.write('Error: ' + str(e))

        # progress marker
        print('Finished')
                
        # Get updates every hour.
        time.sleep(random.randint(3500,3600))

        
'''
if __name__ == '__main__':
    main()
'''
