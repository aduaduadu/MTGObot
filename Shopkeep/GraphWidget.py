import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


class GraphWidget(tk.Tk):
    def __init__(self, conn, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.conn = conn
        self.c = self.conn.cursor()

        self.mainframe = ttk.Frame(self, padding="20 20 20 20")
        self.mainframe.pack()
        self.title = 'Card Data Visualization'

        self.expBox = ttk.Combobox(self.mainframe, values=self.get_exps())
        self.expBox.pack()
        self.nameBox = ttk.Combobox(self.mainframe, postcommand=self.update_nameBox)
        self.nameBox.pack()
        self.premiumBox = ttk.Combobox(self.mainframe, values=['Yes', 'No'])
        self.premiumBox.pack()
        self.buysellBox = ttk.Combobox(self.mainframe, values=['buy', 'sell'])
        self.buysellBox.pack()
        self.b1 = ttk.Button(self.mainframe, text='Show Data', command=self.make_graph)
        self.b1.pack()
        
    #return a list of distinct expansions in cards database
    def get_exps(self):
        return [i for (i,) in self.conn.execute('SELECT DISTINCT expansion FROM cards')]

    def get_names(self):
        query = 'SELECT DISTINCT name FROM cards WHERE expansion=?'
        values = (self.expBox.get(),)
        names = [i for (i,) in self.conn.execute(query, values)]
        names.sort()
        return names

    def update_nameBox(self):
        self.nameBox['values'] = self.get_names()

    #returns mtgo_id for given set of identifiers
    def identify_id(self, name, expansion, premium):
        try:
            query = 'SELECT mtgo_id FROM cards WHERE name=? AND expansion=? AND premium=?'
            values = (name, expansion, premium)
            self.c.execute(query, values)
            mtgo_id = self.c.fetchone()[0]
            if mtgo_id == None:
                raise Exception
            return mtgo_id
        except Exception as e:
            print('ERROR: card cannot be identified')
            print(e, name, expansion, premium)

    def make_graph(self):
        name = self.nameBox.get()
        expansion = self.expBox.get()
        premium = self.premiumBox.get()
        buysell = self.buysellBox.get()

        mtgo_id = self.identify_id(name, expansion, premium)
        table = 'p'+str(mtgo_id)
        query = 'SELECT * FROM ' + table
        # + " WHERE (timestamp > '2018-08-15')"
        card = pd.read_sql(query, self.conn, index_col='timestamp',
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


if __name__ == '__main__':
    conn = sqlite3.connect('mtgobot.db')
    root = GraphWidget(conn)
    root.mainloop()
