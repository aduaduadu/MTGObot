import requests_html
import scrapeKit
import sqlite3


def mtgoacademyscrape():
    conn = sqlite3.connect('mtgo_storeV2.db')
    VENDOR = 'mtgoacademy'
    URL = 'http://www.mtgoacademy.com/store/cards_by_set/'
    EXPANSIONS = scrapeKit.get_exps(conn)

    session = requests_html.HTMLSession()
    
    for EXPANSION in EXPANSIONS:
        url = URL + EXPANSION.lower() + '/'
        r = session.get(url)

        #find number of pages to paginate for each expansion
        NUMPAGES = r.html.find('div.pagination:nth-child(2) > div:nth-child(2)',first=True).text
        NUMPAGES = int(NUMPAGES.split('(')[1].rstrip(' Pages)'))
        
        '''mtgoacademy doesn't have m19 on website yet can
        prevent program break by checking how many pages
        are on the page searched if pages > 100: break'''
        if NUMPAGES > 100:
            print('ERROR with ' + EXPANSION)
            continue

        for PAGE in range(1,NUMPAGES+1):

            payload = {'page': PAGE}
            r = session.get(url, params=payload)
            print(r.url)

            rows = r.html.find('.product_thumb')

            for row in rows:
                #premium determined in each row
                if row.find('.premium-category'):
                    premium = 'Yes'
                else:
                    premium = 'No'

                #extract data
                name = row.find('p',first=True).find('a',first=True).text
                buy = None
                sell = float(row.find('.price',first=True).text.lstrip('$'))

                #identify mtgo_id and log data
                mtgo_id = scrapeKit.identify_id(conn, name, EXPANSION, premium)
                scrapeKit.log_prices(conn, VENDOR, mtgo_id, buy, sell)

    session.close()
    conn.close()
