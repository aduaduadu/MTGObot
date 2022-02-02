import requests_html, sqlite3, time, datetime
from mtgsdk import Set
import numpy as np
import pandas as pd


DB = 'mtgobot.db'
SETSTOSCRAPE = ['GRN','XLN','KLD','HOU','RIX','DAR','AKH','M19','AER']


#returns mtgo_id for given set of identifiers
def identify_id(conn, name, expansion, premium):
    try:
        query = '''SELECT mtgo_id FROM cards
                WHERE name=? AND expansion=? AND premium=?'''
        values = (name, expansion, premium)
        c = conn.cursor()
        c.execute(query, values)
        mtgo_id = c.fetchone()[0]
        if mtgo_id == None:
            raise Exception
        return mtgo_id
    except Exception as e:
        print('ERROR: card cannot be identified')
        print(e, expansion, name, premium)

def log_prices(conn, vendor, mtgo_id, buy, sell):
    tick = {'timestamp': [datetime.datetime.now()],
	    'vendor': [vendor],
	    'buy': [buy],
	    'sell': [sell]}
    tickdata = pd.DataFrame(tick)
    tickdata.to_sql('p'+str(mtgo_id), conn,
                    if_exists='append', index=False)

#roughly same speed, slightly slower most trials
def log_prices_sql(conn, vendor, mtgo_id, buy, sell):
    timestamp = datetime.datetime.now()
    table = 'p'+str(mtgo_id)
    query = 'INSERT INTO '+table+' (timestamp, vendor, buy, sell) VALUES (?,?,?,?)'
    values = (timestamp, vendor, buy, sell)
    conn.execute(query, values)
    conn.commit()


# Scrape 1: clanteam
def s1():
    conn = sqlite3.connect(DB)
    VENDOR = 'clanteam'
    URL = 'http://mtgoclanteam.com/Cards'
    EXPANSIONS = SETSTOSCRAPE

    session = requests_html.HTMLSession()
    r = session.get(URL)
    
    #sliced after index 1 to avoid 'all' link
    EXPANSIONSONSITE = [e.text for e in r.html.find('#templatemo_menucards',first=True).find('a')[1:]]
    #all expansions on site that are in mtgo_store cards table
    EXPANSIONS = [i for i in EXPANSIONSONSITE if i in EXPANSIONS]
                
    for (PREMIUM, VALUE) in [('Yes', 'true'), ('No', 'false')]:
        for EXPANSION in EXPANSIONS:
            PARAMS = {'edition': EXPANSION, 'foil': VALUE}
            r = session.get(URL, params=PARAMS)
            print(r.url)
            r.html.render() # Render javascript on page

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
                mtgo_id = identify_id(conn, name, EXPANSION, PREMIUM)
                log_prices(conn, VENDOR, mtgo_id, buy, sell)

    session.close()
    conn.close()


# Scrape 2: mtgoacademy
def s2():
    conn = sqlite3.connect(DB)
    VENDOR = 'mtgoacademy'
    URL = 'http://www.mtgoacademy.com/store/cards_by_set/'
    EXPANSIONS = SETSTOSCRAPE

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
                mtgo_id = identify_id(conn, name, EXPANSION, premium)
                log_prices(conn, VENDOR, mtgo_id, buy, sell)
                
    session.close()
    conn.close()

# Scrape 3: mtgotraders
def s3():
    conn = sqlite3.connect(DB)
    VENDOR = 'mtgotraders'
    URL = 'https://www.mtgotraders.com/store/'
    EXPANSIONS = SETSTOSCRAPE
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

        #NUMPAGES is each page plus 'Next' link
        NUMPAGES = len(r.html.find('.searchopt-pages',first=True).find('li'))
        for page in range(1,NUMPAGES):
            payload = {'limit': 160,
                       'sortby': 'price_desc',
                       'page': page}
            r = session.get(url, params=payload)
            r.html.render()
            print(r.url)

            cssSelector = '.productlistbox > table:nth-child(3) > tbody:nth-child(1)'
            for row in r.html.find(cssSelector, first=True).find('tr'):
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
                mtgo_id = identify_id(conn, name, EXPANSION ,premium)
                log_prices(conn, VENDOR, mtgo_id, buy, sell)

    session.close()
    conn.close()

'''
if __name__ == '__main__':
    scrapers = [s1, s2, s3]
    while True:
        start = time.time()
        for s in scrapers:
            try:
                s()
                print('VENDOR COMPLETE')
            except Exception as e:
                print(e, s)
        
        print('Loop duration: ' + str((time.time()-start)/60) + ' minutes')
        print('Time: ' + time.asctime())
        print(40*'#' + 'TIMEOUT' + 40*'#')
        time.sleep(3600)
'''
