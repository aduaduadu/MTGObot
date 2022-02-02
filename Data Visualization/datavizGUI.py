from tkinter import *
from tkinter import ttk

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

import sqlite3
conn = sqlite3.connect('mtgo_storeV2.db')
c = conn.cursor()

#return a list of distinct expansions in cards database
def get_exps():
    return [i for (i,) in conn.execute('SELECT DISTINCT expansion FROM cards')]

def get_names():
    query = 'SELECT DISTINCT name FROM cards WHERE expansion=?'
    values = (expBox.get(),)
    names = [i for (i,) in conn.execute(query, values)]
    names.sort()
    return names

def update_nameBox():
    nameBox['values'] = get_names()

#returns mtgo_id for given set of identifiers
def identify_id(name, expansion, premium):
    try:
        query = 'SELECT mtgo_id FROM cards WHERE name=? AND expansion=? AND premium=?'
        values = (name, expansion, premium)
        c.execute(query, values)
        mtgo_id = c.fetchone()[0]
        if mtgo_id == None:
            raise Exception
        return mtgo_id
    except Exception as e:
        print('ERROR: card cannot be identified')
        print(e, name, expansion, premium)

def make_graph():
    name = nameBox.get()
    expansion = expBox.get()
    premium = premiumBox.get()
    buysell = buysellBox.get()

    mtgo_id = identify_id(name, expansion, premium)
    table = 'p'+str(mtgo_id)
    query = 'SELECT * FROM ' + table
    # + " WHERE (timestamp > '2018-08-15')"
    card = pd.read_sql(query, conn, index_col='timestamp',
                       parse_dates=['timestamp'])
    
    for VENDOR in ['clanteam', 'mtgoacademy', 'mtgotraders']:
        s = card[card.vendor == VENDOR][buysell]
        plt.plot(s, label=VENDOR)
    
    plt.xticks(rotation=45)
    plt.ylabel(buysell + ' price')
    plt.title(name + '\nFoil: ' + premium)
    plt.tight_layout()
    plt.legend()
    plt.show()
    
root = Tk()
root.title("Card Data Visualization")

mainframe = ttk.Frame(root, padding="20 20 20 20")
mainframe.pack()

expBox = ttk.Combobox(mainframe, values=get_exps())
expBox.pack()
nameBox = ttk.Combobox(mainframe, postcommand=update_nameBox)
nameBox.pack()
premiumBox = ttk.Combobox(mainframe, values=['Yes', 'No'])
premiumBox.pack()
buysellBox = ttk.Combobox(mainframe, values=['buy', 'sell'])
buysellBox.pack()
b1 = ttk.Button(mainframe, text='Show Data', command=make_graph)
b1.pack()

root.mainloop()
