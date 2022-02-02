import os, time, datetime, win32gui, win32con, pywinauto, sqlite3
import pandas as pd
from getpass import getpass
from matplotlib import pyplot as plt
from mtgoScreens import *
from Trade import *
from GraphWidget import GraphWidget 


class Shopkeep(DataScreen):
    def __init__(self, conn):
        self.conn = conn
        self.c = conn.cursor()
        self.EXPbinder = self.create_ir_dict('Expansion Images\\Binder\\')
        self.EXPywr = self.create_ir_dict('Expansion Images\\YWR\\')
        self.EXPpwr = self.create_ir_dict('Expansion Images\\PWR\\')
        if self.get_handle('Magic: The Gathering Online'):
            self.reknit()
        # CONSTANTS for testing purposes
        self.VENDORS = ['clanteam', 'mtgoacademy', 'mtgotraders']
        self.TID = 67879
        self.TENP = ('DAR', 'Teferi, Hero of Dominaria', 'No')
        self.TAD = ['This', 'is', '1234 A St', '', 'Any City',
                    'MI', 'United States', '12345', '123456788']

    def reknit(self):
        h = self.get_handle('Magic: The Gathering Online')
        self.mtgo = pywinauto.Application(backend='uia').connect(handle=h)

    def click(self, control):
        control.click_input()
        pywinauto.mouse.move((30,30))

    def mtgo4ground(self):
        win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT,
                                          0, win32con.SPIF_SENDWININICHANGE |
                                          win32con.SPIF_UPDATEINIFILE)
        win32gui.SetForegroundWindow(self.get_handle('Magic:'))

    def launch_mtgo(self):
        if self.get_handle('Magic: The Gathering Online'):
            print('mtgo already loaded')
        else:
            MTGOPATH = r'C:\Users\David\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Wizards of the Coast, LLC\Magic The Gathering Online .appref-ms'
            os.startfile(MTGOPATH)
            while self.get_handle('Magic: The Gathering Online') == None:
                print('launching...')
                time.sleep(1)
            self.reknit()
            dlg = self.mtgo['Magic: The Gathering Online']
            uEdit = dlg.child_window(auto_id="UsernameTextBox",
                                     control_type="Edit")
            uEdit.wrapper_object().set_edit_text('wilkedave')
            pEdit = dlg.child_window(auto_id="PasswordBox",
                                     control_type="Edit")
            pEdit.wrapper_object().set_edit_text('Achesprain456')
            #pEdit.wrapper_object().set_edit_text(getpass('pw: '))
            login = dlg.descendants(title="LOG IN",
                                    control_type="Button")[1]
            login.click()

    def create_ir_dict(self, imFolderPath):
        EXP = {}
        for filename in os.listdir(imFolderPath):
            im = cv2.imread(imFolderPath+filename)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            EXP[filename.split('.')[0]] = im
        return EXP

    def wait_for_trade_request(self):
        try:
            while self.get_handle('Trade Request') == None:
                print('Waiting for trade request...')
                time.sleep(1)
            self.tr = TradeRequest(sk)
        except Exception as e:
            print('Trade Request was unsuccessful:', e)

        while self.get_handle('Trade:') == None:
            print('Loading Trade window...')
            time.sleep(1)
        self.trade = Trade(sk, self.tr.partner)
        #self.trade.mainloop()

    def open_graph_widget(self):
        '''Launches a GUI that generates time series data line graphs
        from price history data for a chosen mtgo_id'''
        gw = GraphWidget(self.conn)

    # Returns a list of distinct EXP in cards database
    def get_exps(self):
        query = 'SELECT DISTINCT expansion FROM cards'
        return [i for (i,) in self.conn.execute(query)]

    def get_cards(self):
        '''Returns DataFrame of cards table'''
        return pd.read_sql('SELECT * FROM cards', self.conn)

    # Graphs price data from past [all time]
    def make_graph(self, mtgo_id, buysell):
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
        plt.title(str(self.identify_enp(mtgo_id)))
        plt.tight_layout()
        plt.legend()
        plt.show()

    def calc_sma(self, mtgo_id):
        '''Calculates 1, 2, 3, 7, 14, and 30 -day simple moving averages
        for 1 card with mtgo_id == mtgo_id'''
        periods = [1,2,3,7,14,30] # day intervals to calc SMAs
        table = 'p' + str(mtgo_id)
        query = 'SELECT * FROM ' + table
        df = pd.read_sql(query, sk.conn)

        output = []
        for p in periods:
            print('____________')
            print(p,'day SMA')
            td = datetime.timedelta(days=p)
            date = datetime.datetime.now() - td
            for v in self.VENDORS:
                rows = (df.timestamp > date.isoformat()) & (df.vendor == v)
                sma = df.loc[rows, 'sell'].mean()
                print(round(sma, 2), v)
                output.append((p, v, round(sma, 3)))
        return output

    def init_cards_table(self, conn):
        start = time.time()
        df = pd.read_csv('ALL MTGO CARDS.csv')
        df.drop(['Quantity', 'Unnamed: 7'], axis=1, inplace=True)
        df.columns = ['name', 'mtgo_id', 'rarity',
                      'expansion', 'collector', 'premium']
        # Create the rest of the columns
        df['stock'] = pd.Series(np.zeros(df.shape[0], dtype=np.int16))
        df['for_sale'] = pd.Series(np.zeros(df.shape[0], dtype=np.int8))
        df['market_buy'] = pd.Series(dtype=np.float64)
        df['market_sell'] = pd.Series(dtype=np.float64)
        df['buy'] = pd.Series(dtype=np.float64)
        df['sell'] = pd.Series(dtype=np.float64)
        #df.to_sql('cards', conn, if_exists='replace', index=False)
        print('Seconds taken: ', time.time() - start)
        return df

    def set_inventory(self):
        start = time.time()
        cards = self.get_cards()
        df = pd.read_csv('Full Trade List.csv')
        for index, row in df.iterrows():
            cards.loc[cards.mtgo_id == row['ID #'], 'stock'] = row.Quantity
        print('Inventory Time: {}s'.format(round(time.time() - start, 2)))
        return cards

    def check_inventory(self):
        start = time.time()
        incorrectIds = []
        cards = self.get_cards()
        df = pd.read_csv('Full Trade List.csv')
        for index, row in df.iterrows():
            stockSeries = cards.loc[cards.mtgo_id == row['ID #'], 'stock']
            print(stockSeries.size)
            if stockSeries.get_values()[0] != row.Quantity:
                incorrectIds.append(int(row['ID #']))
        print('Seconds: ', time.time() - start)
        return incorrectIds

    def set_prices(self):
        '''Last attempt took approximately 76 seconds'''
        start = time.time()
        cards = self.get_cards()
        subset = cards[(cards.market_buy > 0) & (cards.market_sell > 0)]
        for index, row in subset.iterrows():
            cards.loc[cards.mtgo_id == row.mtgo_id, 'buy'] = round(row.market_buy, 4)
            cards.loc[cards.mtgo_id == row.mtgo_id, 'sell'] = round(row.market_sell, 3)
        print('Seconds taken: ', time.time() - start)
        return cards

    def update_market_prices(self):
        '''Last attempt took approximately 88 seconds'''
        start = time.time()
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        date = date.isoformat().replace('T',' ')
        cards = pd.read_sql('SELECT * FROM cards', self.conn)
        
        query = 'SELECT DISTINCT tbl_name FROM sqlite_master'
        for (tbl,) in sk.conn.execute(query):
            if tbl in ['cards', 'pNone']: # Skip these two
                continue 
            try:
                mtgo_id = int(tbl.lstrip('p'))
                table = 'p' + str(mtgo_id)
                query = "SELECT * FROM {} WHERE timestamp > '{}'".format(table, date)
                cardPH = pd.read_sql(query, self.conn)
                if cardPH.shape[0] > 0:
                    sma1 = cardPH.groupby('vendor').mean()
                    if sma1.columns.str.contains('buy').any():
                        # market_buy = 1-day sma
                        cards.loc[cards.mtgo_id == mtgo_id, 'market_buy'] = sma1.buy.mean()
                    if sma1.columns.str.contains('sell').any():
                        # market_sell = 1-day sma
                        cards.loc[cards.mtgo_id == mtgo_id, 'market_sell'] = sma1.sell.mean()
                else:
                    print('No data for: ', mtgo_id)
            except Exception as e:
                print(mtgo_id, e)       
        print('Seconds: ', time.time() - start)
        return cards
        
    
if __name__ == '__main__':
    conn = sqlite3.connect('mtgobot.db')
    sk = Shopkeep(conn)
