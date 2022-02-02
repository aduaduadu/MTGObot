###THIS CODE IS UNUSABLE ATM###

import requests_html
import db_functions
from fake_useragent import UserAgent


def cardhoarderscrape():
    VENDOR = 'cardhoarder'
    URL = 'https://www.cardhoarder.com/cards/index/sort:sell-desc/viewtype:list'
    EXPANSIONS = db_functions.get_exps()
    print(EXPANSIONS)


    for EXPANSION in EXPANSIONS[:2]:

        URL = '''https://www.cardhoarder.com/cards/index/sort:sell-desc/viewtype:list?data%5Bsearch%5D=&data%5Bis_foil%5D=all&data%5Bsets%5D%5B0%5D={}'''.format(EXPANSION)

        session = requests_html.HTMLSession()
        session.headers['User-Agent'] = UserAgent().random
        r = session.get(URL)
        print(r)
        print(r.html.text)
        r.html.find('.pagination')[0].links

        #HOW TO GET AROUND INCAPSULA BOT DETECTION?

        #pages = r.html.find('.pagination')

"""
        #rows are cards on page, cells hold data in rows
        for row in r.html.find('tbody')[0].find('tr'):
            cells = row.find('td')
            #names on foil/premium webpage have extra text
            name = cells[0].text.replace('FOIL','').strip()
            #buy/sell price could be empty ( == '' )
            #also, must convert buy/sell str to float if exists
            if cells[2].text == '':
                buy = None
            else:
                buy = float(cells[2].text)
            if cells[3].text == '':
                sell = None
            else:
                sell = float(cells[3].text)

            #identify unique card and log price data
            mtgo_id = db_functions.identify_id(name, EXPANSION, PREMIUM)
            db_functions.log_prices(VENDOR, mtgo_id, buy, sell)
            #print('logged ' + EXPANSION + '|' + PREMIUM '|' + name)

    print('done')
"""
