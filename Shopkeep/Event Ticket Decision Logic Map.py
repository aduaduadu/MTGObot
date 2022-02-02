        '''Logic for telling customer to select tickets if needed'''
        if self.ywrCartValue >= self.pwrCartValue:
            d = round(self.ywrCartValue - self.pwrCartValue, 4)
            if d < 1:
                finalMessage = '''Please type 'done' to finish the trade.
You will store {} credits.'''.format(d)
            else:
                finalMessage = '''Please take {} tickets. You will store {}
credits.'''.format(int(d//1), d%1)
                
            self.send_message(finalMessage)
                
        elif self.pwrCartValue > self.ywrCartValue:
            d = round(self.pwrCartValue - self.ywrCartValue, 4)
            self.grab_tix(int(d+1))


case 1:
    situation: i take cards, customer just wants to sell
    cart values: ywr = X, pwr = 0
    procedure: bot tells customer to take X tix, where x is value of cards bot has taken

case 2:
    situation: i do not take any cards, customer buys cards
    cart values: ywr = 0, pwr = Y
    procedure: bot takes Y tix

case 3:
    situation: bot takes cards, customer takes cards
    notes: If this is to be done dynamically, I need to account for current tix in each cart.
        X and Y would be value of just cards in the cart. Event Tickets represented as Tx and Ty
    cart values: ywr = X, pwr = Y
    procedure:
        if X > Y:
            tell customer to take [floor(X - Y)] tix and bot saves remainder [(X - Y)%1] in credit
        if Y > X:
            bot takes [ceil(Y - X)] tix and saves overage [(Y - X)%1] in credit
    
    
