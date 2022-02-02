#!/usr/bin/env python3
# TODO: unfinished.

import pymongo
import sys
import urllib.request
import urllib.parse
import re
import time
import datetime
from bs4 import BeautifulSoup as bs
from pprint import pprint

def get_soup(url):
    '''
    Change headers for url request and generate html soup from url.
    '''
    # Progress marker
    print('eating soup')

    # Change headers to disguise python.
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    # Request html data from url and run through BeautifulSoup parser to get soup.
    req = urllib.request.Request(url,headers=headers)
    resp = urllib.request.urlopen(req)
    soup = bs(resp.read())
    return soup

def get_expansionLinks_mtgoEmpire():
    mtgoEmpireSite = 'http://www.mtgoempire.com/LEG_INV.html'
    soup = get_soup(mtgoEmpireSite)
    
    return links

mtgoEmpireSite = 'http://www.mtgoempire.com/LEG_INV.html'
soup = get_soup(mtgoEmpireSite)
almostCards = soup.text.split('\n')

'''
(5  )(44                                        )(6   )(10      )(6   )(12        )(70                                                                  )
SOM  Wurmcoil Engine                             M     9.26      (1)   11.33       MtgoEmpire2(4) black_lotus_bot(1) infinite_manabot(1) mtgo_depot_1(1)
DTK  Crater Elemental                            R     0.004     (12)  0.05        MtgoEmpire(4) cardkingdom(4) 
DTK  Damnable Pact                               R     0.004     (12)  0.05        MtgoEmpire(4) cardkingdom(4)
'''