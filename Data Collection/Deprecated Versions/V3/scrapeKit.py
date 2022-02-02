import datetime
import numpy as np
import pandas as pd
import sqlite3

'''
DB = 'mtgo_storeV2.db'
conn = sqlite3.connect('mtgo_storeV2.db')
c = conn.cursor()
'''

#return a list of distinct expansions in cards database
def get_exps(conn):
    return [i for (i,) in conn.execute('SELECT DISTINCT expansion FROM cards')]


#returns mtgo_id for given set of identifiers
def identify_id(conn, name, expansion, premium):
    try:
        query = 'SELECT mtgo_id FROM cards WHERE name=? AND expansion=? AND premium=?'
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
