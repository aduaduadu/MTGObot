import clanteamscrapeV2
import mtgoacademyscrapeV2
import mtgotradersscrapeV2
import time

scrapers = [clanteamscrapeV2.clanteamscrape,
            mtgoacademyscrapeV2.mtgoacademyscrape,
            mtgotradersscrapeV2.mtgotradersscrape]

while True:
    start = time.time()
    for scraper in scrapers:
        try:
            scraper()
            print('VENDOR COMPLETE')
        except Exception as e:
            print(e, scraper)
    
    print('Loop duration: ' + str((time.time()-start)/60) + ' minutes')
    print('Time: ' + time.asctime())
    print(40*'#' + 'TIMEOUT' + 40*'#')
    time.sleep(3600)
