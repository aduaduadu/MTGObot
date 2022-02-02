import sqlite3
import clanteamscrape
import mtgoacademyscrape
import mtgotradersscrape
import time

spiders = [
    clanteamscrape.clanteamscrape,
    mtgoacademyscrape.mtgoacademyscrape,
    mtgotradersscrape.mtgotradersscrape
    ]

while True:

    conn = sqlite3.connect('mtgo_store.db')

    start = time.time()
    for spider in spiders:
        try:
            spider(conn)
            print('VENDOR COMPLETE')
        except Exception as e:
            print('ERROR:')
            print(spider)
            print(e)
    end =  time.time()

    conn.close()
    
    print('Loop duration: ' + str((end-start)/60) + ' minutes')
    print(20*'#' + 'TIMEOUT' + 20*'#')

    #puase for an hour
    time.sleep(3600)
