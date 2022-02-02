import requests_html
import db_functions
from mtgsdk import Set

def mtgotradersscrape(conn):
    VENDOR = 'mtgotraders'
    URL = 'https://www.mtgotraders.com/store/'
    EXPANSIONS = db_functions.get_exps(conn)
    session = requests_html.HTMLSession()

    for EXPANSION in EXPANSIONS:

        #mtgsdk has Dominaria as 'DOM' not 'DAR' like mtgo
        if EXPANSION == 'DAR':
            expName = Set.find('DOM').name.lower()
        else:
            expName = Set.find(EXPANSION).name.lower()
        #example output: 'RIX' -> 'rivals_of_ixalan'
        expName = '_'.join(expName.split(' '))
        
        url = URL + expName + '.html'
        payload = {'limit': 160,
                   'sortby': 'price_desc'}
        r = session.get(url, params=payload)

        #find how many pages the data is on
        NUMPAGES = len(r.html.find('.searchopt-pages',first=True).find('li')) 

        #NUMPAGES is each page plus 'Next' link
        for page in range(1,NUMPAGES):
            payload = {'limit': 160,
                       'sortby': 'price_desc',
                       'page': page}
            r = session.get(url, params=payload)
            r.html.render()
            print(r.url)

            cssCardTable = '.productlistbox > table:nth-child(3) > tbody:nth-child(1)'

            for row in r.html.find(cssCardTable,first=True).find('tr'):
                name = row.find('.cardname',first=True).text
                if '*Foil*' in name:
                    premium = 'Yes'
                    name = name.replace(' *Foil*','')
                else:
                    premium = 'No'
                    
                buy = row.find('.buyprice',first=True).text
                if buy == '-':
                    buy = None
                else:
                    buy = float(buy)

                sell = row.find('.price',first=True).text
                if sell == '-':
                    sell = None
                else:
                    sell = float(sell.lstrip('$'))

                #identify unique card and log price data
                mtgo_id = db_functions.identify_id(conn,name,EXPANSION,premium)
                db_functions.log_prices(conn,VENDOR,mtgo_id,buy,sell)
                #db_functions.log_print(VENDOR,EXPANSION,premium,name,str(buy),str(sell))

    session.close()
