import csv
import datetime


#converts mtgo_id to table name str
def table_str(mtgo_id):
    return 'p'+str(mtgo_id)


#returns mtgo_id for given set of identifiers
def identify_id(conn, name, expansion, premium):
    c = conn.cursor()
    try:
        c.execute('SELECT mtgo_id FROM cards WHERE name = ? AND expansion = ? AND premium = ?',
                     (name, expansion, premium))
        return c.fetchone()[0]
    except Exception as e:
        print("ERROR couldn't identify card")
        print(e)
        print(name)
        print(expansion)
        print(premium)
    c.close()


#loads in wish list csv (stripped of header row) to db 'cards'
def init_cards_db(conn):
    wishlist = 'Wish List.csv'
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cards
              (mtgo_id INTEGER NOT NULL,
              name TEXT NOT NULL,
              expansion TEXT NOT NULL,
              rarity TEXT NOT NULL,
              collector TEXT,
              premium TEXT NOT NULL,
              type TEXT,
              cmc TEXT,
              sell REAL,
              buy REAL,
              PRIMARY KEY(mtgo_id)
              )''')
    
    with open(wishlist, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            (name, ignore, mtgo_id, rarity, expansion, collector, premium) = row
            c.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?)',
                      (mtgo_id, name, expansion, rarity, collector, premium, None, None, None, None)
                      )
            print(name)
            
    conn.commit()


#logs 1 buy/sell sample to db
#creates new table for mtgo_id if not exists
def log_prices(conn, vendor, mtgo_id, buy, sell):
    c = conn.cursor()
    query = 'CREATE TABLE IF NOT EXISTS ' + table_str(mtgo_id) + '''
    (sample_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    vendor TEXT NOT NULL,
    buy REAL,
    sell REAL)'''
    c.execute(query)

    #update mtgo_id table with sample data
    query = 'INSERT INTO ' + table_str(mtgo_id) + '''
    (timestamp, vendor, buy, sell) VALUES (?,?,?,?)'''
    c.execute(query, (datetime.datetime.now(), vendor, buy, sell))
    conn.commit()
    c.close()


def log_print(a,b,c,d,e,f):
    print('logged {}|{}|{}|{}|{}|{}'.format(a,b,c,d,e,f))


#return a list of distinct expansions in cards database
def get_exps(conn):
    return [i for (i,) in conn.execute('SELECT DISTINCT expansion FROM cards')]
