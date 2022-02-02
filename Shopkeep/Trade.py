import time, pywinauto
from math import ceil
from operator import itemgetter
from mtgoScreens import DataScreen


class TradeRequest:
    def __init__(self, sk):
        self.start = time.time()
        self.conn = sk.conn

        '''Trade Request Controls'''
        self.mainDlg = sk.mtgo['Magic: The Gathering Online']
        self.dlg = self.mainDlg.child_window(title="Trade Request",
                                             control_type="Window")
        self.forSale = self.dlg.child_window(title="FOR SALE",
                                             auto_id="FOR SALE",
                                             control_type="RadioButton")
        self.importList = self.dlg.child_window(title="Import a Decklist",
                                                auto_id="LoadButton",
                                                control_type="Button")
        self.accept = self.dlg.child_window(title="Accept",
                                            auto_id="OkButton",
                                            control_type="Button")
        self.reject = self.dlg.child_window(title="Reject",
                                            auto_id="CancelButton",
                                            control_type="Button")

        '''Identify trade partner'''
        pTextWS = self.dlg.descendants(control_type="Text")[1]
        self.partner = pTextWS.window_text().split(' ')[0]

        '''Check to see if customer is in db already, else add'''
        query = 'SELECT * FROM mtgo_customers WHERE customer=?'
        values = (self.partner,)
        if self.conn.execute(query, values).fetchone() == None:
            query = 'INSERT INTO mtgo_customers VALUES (?,?)'
            values = (self.partner, 0.0)
            self.conn.execute(query, values)
            self.conn.commit()
        partnerTime = round(time.time() - self.start, 2)
        print('Time to find trade partner:', partnerTime)

        '''Accept trade request'''
        self.accept.click()
        requestTime = round(time.time() - self.start, 2)
        print('Trade Request Time: {}s'.format(requestTime))


class Trade(DataScreen):
    def __init__(self, sk, partner):
        self.start = time.time()
        self.completed = False # Whether trade has been completed yet
        DataScreen.__init__(self, sk)
        # determine partner credit
        self.partner = partner
        query = 'SELECT credit FROM mtgo_customers WHERE customer=?'
        values = (self.partner,)
        self.credit = self.conn.execute(query, values).fetchone()[0]
        # Image recognition reference dicts
        self.EXPywr = sk.EXPywr
        self.EXPpwr = sk.EXPpwr
        # Indices specific to Transaction Screen       
        self.expansionIndex = 2
        self.premiumIndex = 1

        #References and window specification objects to various controls
        self.mtgo = sk.mtgo
        self.mainDlg = sk.mtgo['Magic: The Gathering Online']
        self.dlg = self.mtgo.window(handle=sk.get_handle('Trade:'))
        self.submitBtn = self.dlg.child_window(title="Submit",
                                               control_type="Button")
        self.cancelBtn = self.dlg.child_window(title="Cancel Trade",
                                               control_type="Button")
        self.chat = self.dlg.child_window(title="Shiny.Chat.ViewModels.PrivateChatSessionViewModel",
                                          control_type="TabItem")
        self.chatEdit = self.chat.child_window(auto_id="ChatSendEditBox",
                                               control_type="Edit")
        self.sendBtn = self.chat.child_window(title="Send",
                                              auto_id="ChatSendButton",
                                              control_type="Button")
        self.chatClose = self.chat.child_window(auto_id="CloseButton",
                                                control_type="Button")
        self.searchTools = self.dlg.child_window(title="Search Tools",
                                                 control_type="Button")
        self.importDeck = self.dlg.child_window(title="Import Deck",
                                                control_type="Button")

        # These are the 2 ListView controls representing YWR & PWR
        self.ywr = self.dlg.descendants(control_type="DataGrid")[1]
        self.pwr = self.dlg.descendants(control_type="DataGrid")[2]
        # Virtual carts for reference after data read from screen
        self.ywrCart = []
        self.pwrCart = []
        # mtgo_ids of any cards that populated these lists during trade
        self.ywrHistory = []
        self.pwrHistory = []

        #self.mainloop()

    def close(self):
        '''Incomplete. Breaks on chat.close(). Needs to log trade report
        as trade is closing.'''
        self.dlg.close()
        chat = self.mainDlg.child_window(title="Shiny.Chat.ViewModels.PrivateChatSessionViewModel",
                                         control_type="TabItem")
        chat.close()

    def update_ywrCart(self):
        self.ywrCart = self.data31(self.ywr, self.EXPywr)

    def update_pwrCart(self):
        self.pwrCart = self.data31(self.pwr, self.EXPpwr)

    def empty_ywr(self):
        start = time.time()
        self.remove_tix()
        while len(self.ywr.items()) > 0:
            self.ywr.items()[0].double_click_input()
        pywinauto.mouse.move((30,30)) # Reset cursor
        print('Empty Cart Time: {}s'.format(round(time.time() - start, 2)))

    def remove_tix(self):
        '''Removes all Event Tickets from ywr.'''
        if self.ywr.item_count() > 0:
            firstName = self.extract_name(self.ywr.items()[0].window_text())
            if firstName == 'Event Ticket':  
                self.ywr.items()[0].click_input('right')
                removeAllPattern = '{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{ENTER}'
                pywinauto.keyboard.SendKeys(removeAllPattern)
                pywinauto.mouse.move((30,30)) # Reset cursor
            else: print('no tickets')
        else: print('no tix')
                
    def grab_tix(self, num):
        self.remove_tix()
        
        # determine event tickets in stock on mtgo account
        query = 'SELECT stock FROM cards WHERE name = "Event Ticket"'
        tixStock = self.conn.execute(query).fetchone()[0]
        num = num + tixStock

        # .dek file format (xml?)
        tixStr = '''<?xml version="1.0" encoding="utf-8"?>
<Deck xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NetDeckID>0</NetDeckID>
  <PreconstructedDeckID>0</PreconstructedDeckID>
  <Cards CatID="1" Quantity="{}" Sideboard="false" Name="Event Ticket" /> 
</Deck>'''.format(num)

        # create .dek file for mtgo to read and load list
        with open('TIX.DEK','w') as f:
            f.write(tixStr)
        self.load_list('TIX.DEK')
        self.update_ywrCart()
        
    def load_list(self, dekFile):
        start = time.time()
        self.searchTools.click()
        self.importDeck.click()
        time.sleep(.5)
        pywinauto.keyboard.SendKeys(dekFile)
        pywinauto.keyboard.SendKeys('{ENTER}')
        try:
            warnStart = time.time()
            warningDlg = self.dlg.child_window(title="Warning",
                                               control_type="Window")
            ok = warningDlg.child_window(auto_id="TitleBarCloseButton",
                                         control_type="Button")
            ok.click()
        except Exception as e:
            print('no warning dialog')

        # Timers
        span = round(time.time() - start, 2)
        print('Load Buylist Time: {}s'.format(span))
        span = round(time.time() - warnStart, 2)
        print('Warn Check Wait Time: {}s'.format(span))

    def send_message(self, m):
        '''Sends chat message to customer. Breaks messages longer than
        500 characters into chunks [len: 500].'''
        start = time.time()        
        while len(m) > 0:
            chunk = m[0:500]
            m = m.replace(chunk,'')
            self.chatEdit.set_edit_text(chunk)
            pywinauto.keyboard.SendKeys('{LEFT}') # reset 'Send Button', else inactive sometimes
            self.sendBtn.click()
            time.sleep(.5)
        span = round(time.time() - start, 2)
        print('Message Time: {}s'.format(span))

    def customer_input_check(self):
        start = time.time()
        chatBox = self.chat.child_window(auto_id="ChatItemsControl",
                                         control_type="List")
        lastMessage = chatBox.items()[-1].texts()[0]
        p = self.partner + ': ' # create chat specific partner id str
        
        if p in lastMessage:
            # Respond to different customer inputs
            content = lastMessage.split(p)[1].strip().lower()
            if content == 'done':
                print('customer is done! GASP!')
            elif content == 'remove all':
                self.empty_ywr()
                self.update_ywrCart()
                self.tally_order()
            elif content == 'grab tix':
                pass
            else:
                print('customer input:', content)
        else:
            span = round(time.time() - start, 2)
            print('Customer Input Check: {}s'.format(span))

    def tally_order(self):
        # YWR
        lineItems = []
        message = ''
        for i, (mtgo_id, qty, exp, name, prem) in enumerate(self.ywrCart):
            query = '''SELECT buy FROM cards
                    WHERE mtgo_id == {}'''.format(mtgo_id)
            price = self.c.execute(query).fetchone()[0]
            lineItems.append((qty, price))
            message += '{}:{}x {}({}) '.format(i, qty, name, price)
        self.ywrCartValue = round(sum([q*p for q, p in lineItems]), 4)
        message += '${}$'.format(self.ywrCartValue)
        self.send_message(message)
        
        # PWR
        lineItems = []
        message = ''
        for mtgo_id, qty, exp, name, prem in self.pwrCart:
            query = '''SELECT sell FROM cards
                    WHERE mtgo_id == {}'''.format(mtgo_id)
            price = self.c.execute(query).fetchone()[0]
            lineItems.append((qty, price))
            message += '{}x {}({}) '.format(name, qty, price)
        self.pwrCartValue = round(sum([q*p for q, p in lineItems]), 4)
        message += '${}$'.format(self.pwrCartValue)
        self.send_message(message)


##        '''Logic for telling customer to select tickets if needed'''
##        if self.ywrCartValue >= self.pwrCartValue:
##            d = round(self.ywrCartValue - self.pwrCartValue, 4)
##            if d < 1:
##                finalMessage = '''Please type 'done' to finish the trade.
##You will store {} credits.'''.format(d)
##            else:
##                finalMessage = '''Please take {} tickets. You will store {}
##credits.'''.format(int(d//1), d%1)
##                
##            self.send_message(finalMessage)
##                
##        elif self.pwrCartValue > self.ywrCartValue:
##            d = round(self.pwrCartValue - self.ywrCartValue, 4)
##            self.grab_tix(int(d+1))
    
    def mainloop(self):
        try:
            welcome = '''Welcome {}! You have {} credit.
 Checking your items now...'''.format(self.partner, self.credit)
            self.send_message(welcome)

            '''Maximize visible ListView window space'''
            adjust = self.dlg.descendants(control_type='Thumb',
                                         class_name='GridSplitter')[2]
            if adjust.rectangle().top > 156: # Max vert height
                adjust.drag_mouse_input(dst=(0,0))

            '''Order ywr by set to move Event Tickets into first slot'''
            control = self.dlg.descendants(title="Set",
                                           control_type="HeaderItem")[1]
            control.double_click_input()

            '''Grab all applicable cards to buy from partner'''
            self.load_list('BUY.DEK')
                
            '''Tally cards to buy and send total price'''
            self.update_ywrCart()
            self.tally_order()
            waitTime = round(time.time() - self.start, 2)
            print('Customer Wait Time: {}s'.format(waitTime))
        except Exception as e:
            #self.dlg.close()
            print('error before main loop', e)
            print('Duration: {} s'.format(round(time.time() - self.start, 2)))

        while self.get_handle('Trade:'):
            self.customer_input_check()
            self.lastCart = self.pwrCart
            self.update_pwrCart()
            if self.pwrCart != self.lastCart:
                self.tally_order()
                '''update cart history'''
                for mtgo_id, qty, exp, name, prem in self.pwr:
                    if mtgo_id not in self.pwrHistory:
                        self.pwrHistory.append(mtgo_id)
        else:
            print('TRADE REPORT:')
            print('Completed: {}'.format(self.completed))
            print('Length: {}s'.format(round(time.time()-self.start, 2)))
            print('Partner cart history:')
            for i in self.pwrHistory:
                print(i)
