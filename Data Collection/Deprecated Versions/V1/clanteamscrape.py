import requests_html
import db_functions

#takes connection to db
def clanteamscrape(conn):

    VENDOR = 'clanteam'
    URL = 'http://mtgoclanteam.com/Cards'

    EXPANSIONS = db_functions.get_exps(conn)

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

            #render javascript on page, beautiful
            #requires Python 3.7 and requests_html library
            r.html.render()

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
                mtgo_id = db_functions.identify_id(conn,name,EXPANSION,PREMIUM)
                db_functions.log_prices(conn,VENDOR,mtgo_id,buy,sell)
                #db_functions.log_print(VENDOR,EXPANSION,PREMIUM,name,str(buy),str(sell))
                
    session.close()
