import urllib.request
from bs4 import BeautifulSoup as bs

URL = 'http://magic.wizards.com/en/game-info/products/card-set-archive'

def get_soup(url):
    '''Returns url as soup object.'''
    # Progress marker.
    print('eating soup')
    resp = urllib.request.urlopen(url)
    soup = bs(resp.read())
    return soup

setDetails = []
soup = get_soup(URL)
sections = soup.find_all('li')
for section in sections:
    if section.find('span','nameSet'):
        name = section.find('span','nameSet').text.strip()
        quantity = section.find('span','quantity').text.strip()
        setDetails.append((name, quantity))
        
newSetCodes = []
for setCode in setCodes:
    expansion = input(setCode+':')
    newSetCodes.append((setCode, expansion))