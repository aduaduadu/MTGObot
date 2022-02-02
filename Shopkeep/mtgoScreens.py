import time, datetime, win32gui, pywinauto, cv2
import numpy as np
from operator import itemgetter


class DashScreen:
    def __init__(self, sk):
        self.mtgo = sk.mtgo
        self.dlg = self.mtgo['Magic: The Gathering Online']
        self.homeBtn = self.dlg.child_window(title="HOME",
                                             auto_id="HomeButton",
                                             control_type="Button")
        self.colBtn = self.dlg.child_window(title="COLLECTION",
                                            auto_id="CollectionButton",
                                            control_type="Button")
        self.storeBtn = self.dlg.child_window(title="STORE",
                                              auto_id="StoreButton",
                                              control_type="Button")
        self.forumBtn = self.dlg.child_window(title="TRADE",
                                              auto_id="TradeButton",
                                              control_type="Button")
        self.accountBtn = self.dlg.child_window(title="ACCOUNT",
                                                auto_id="SettingsButton",
                                                control_type="Button")

    def click(self, control):
        control.click_input()
        pywinauto.mouse.move((30,30)) # Move cursor away from screen data


class DataScreen:
    def __init__(self, sk):
        self.conn = sk.conn
        self.c = self.conn.cursor()

    def windowEnumerationHandler(self, hwnd, resultList):
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

    def enumerate_handles(self):
        top_windows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, top_windows)
        for (handle, name) in top_windows:
            if name not in ['', 'Default IME', 'MSCTFIME UI']:
                print(handle, name)

    def get_handle(self, windowTitle):
        top_windows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, top_windows)
        for (handle, name) in top_windows:
            if windowTitle in name:
                #print(name, handle)
                return handle

    def extract_name(self, s):
        '''
        Name and quantity data for each row is store in (E + QN), where:
        E = extraneous text -> ('spam eggs: ')
        Q = integer value representing both quantity of card and number
            of repetitions of N contained within s
        N = (card name pattern) + ' '
        '''
        s = s.split(': ')[1]
        i = (s+s).find(s, 1, -1)
        return s.strip() if i == -1 else s[:i].strip()

    def clean_image(self, im):
        # Get thresheld im
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        retval, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        # Get bounding box of threshold
        invert = cv2.bitwise_not(threshold)
        textCoords = cv2.findNonZero(invert) 
        x, y, w, h = cv2.boundingRect(textCoords)
        # Crop white space around im
        cleanIm = threshold[y:y+h, x:x+w]
        return cleanIm

    def expansion_ir(self, im, expRef):
        for key in expRef:
            if im.shape == expRef[key].shape:
                if (im == expRef[key]).all():
                    return key.split(' ')[0]
        print('Expansion not found in Image Recognition Dict.')
        folder = 'Expansion Images\\Unidentified\\'
        filename = time.asctime().replace(':', '-') + '.png'
        cv2.imwrite(folder+filename, im)

    def extract_data(self, listItemWrapper, expRef):
        wrapperText = listItemWrapper.window_text()
        name = self.extract_name(wrapperText)
        quantity = wrapperText.count(name)

        cells = listItemWrapper.children()
        if name == 'Event Ticket':
            expansion = 'mtgo'
        else:
            expansion = cells[self.expansionIndex].capture_as_image()
            expansion = np.array(expansion)
            expansion = self.clean_image(expansion)
            expansion = self.expansion_ir(expansion, expRef)
        premium = cells[self.premiumIndex].capture_as_image()
        premium = np.array(premium)[:, -25:]
        premium = self.clean_image(premium)
        invert = cv2.bitwise_not(premium) # if no im, np.any(invert)=>False
        premium = 'Yes' if np.any(invert) else 'No'
        mtgo_id = self.identify_id(expansion, name, premium)
        return mtgo_id, quantity, expansion, name, premium

    def data31(self, listView, expRef):
        '''Newest version of function for reading data out of listViews
        in Trade Screen. Does not work for Collection screen yet.'''
        data = []
        if len(listView.items()) > 31:
            # Reset ywr listview
            tts = listView.item_count()//len(listView.items())
            listView.scroll('up', 'page', tts)
            # Read data, then scroll page
            for i in range(tts):
                for row in listView.items():
                    line = self.extract_data(row, expRef)
                    if line[1] != None:
                        data.append(line)
                listView.scroll('down', 'page')
        else:
            data = [self.extract_data(row, expRef) for row in listView.items()]
        return list(set(data))

    def dump_expansion_images(self, listView):
        '''Saves all unique expansion images to file.
        Must be present during function execution else infinite.'''
        path = 'Expansion Images\\Dump\\'
        imList = []
        while True:
            for row in listView.items()[0:31]:
                cells = row.children()
                expansion = cells[self.expansionIndex].capture_as_image()
                expansion = np.array(expansion)
                expansion = self.clean_image(expansion)                   
                if not any((expansion == im).all() for im in imList if im.shape == expansion.shape):
                    imList.append(expansion)
                    filename = str(time.time()).replace('.', ',') + '.png'
                    cv2.imwrite(path+filename, expansion)
            listView.scroll('down', 'page')

    def identify_id(self, expansion, name, premium):
        '''Returns mtgo_id for given set of identifiers (expansion,
        name, premium)'''
        try:
            if name == 'Event Ticket':
                return 1
            query = '''SELECT mtgo_id FROM cards
                    WHERE name=? AND expansion=? AND premium=?'''
            values = (name, expansion, premium)
            self.c.execute(query, values)
            mtgo_id = self.c.fetchone()[0]
            if mtgo_id == None:
                raise Exception
            return mtgo_id
        except Exception as e:
            print('ERROR: card cannot be identified')
            print(e, expansion, name, premium)

    def identify_enp(self, mtgo_id):
        ''' Returns (expansion, name, premium) for a given mtgo_id'''
        try:
            query = '''SELECT name, expansion, premium
                    FROM cards WHERE mtgo_id=?'''
            values = (int(mtgo_id),) # Purify input, used to cause error w/o
            self.c.execute(query, values)
            n, e, p = self.c.fetchone()
            print(e, n, p)
            return (e, n, p)
        except Exception as e:
            print(mtgo_id, e)


class CollectionScreen(DashScreen, DataScreen): 
    def __init__(self, sk):
        DashScreen.__init__(self, sk)
        DataScreen.__init__(self, sk)
        self.EXPbinder = sk.EXPbinder
        # Indices specific to Collection Screen
        self.expansionIndex = 7
        self.premiumIndex = 2
        self.tbinders = self.dlg.child_window(title="Trade Binders",
                                              control_type="Custom").children()
        self.binder = self.dlg.descendants(control_type='DataGrid')[1]
        #self.change_binder(5) # Seeded with FOR SALE

    def change_binder(self, index):
        '''
        Index: Binder Name
        2: Full Trade List
        3: Wish List
        4: Active Trade
        5: trade2
        '''
        self.click(self.tbinders[index])
        self.binderTitle = self.dlg.child_window(auto_id="DeckTotalCardsText", control_type="Text").wrapper_object()
        self.binderName = self.binderTitle.window_text().split(': ')[0]
        self.cardTotal = int(self.binderTitle.window_text().split(': ')[1])

    def read_binder(self):
        pywinauto.mouse.move((30,30))
        return self.data31(self.binder, self.EXPbinder)

    def print_binder(self):
        for row in sorted(self.read_binder()): print(row)


class StoreScreen(DashScreen):
    def __init__(self, sk):
        DashScreen.__init__(self, sk)

class ForumScreen(DashScreen):
    def __init__(self, sk):
        DashScreen.__init__(self, sk)
        self.adEdit = self.dlg.child_window(auto_id="MyPostMessageTextArea",
                                            control_type="Edit")
        self.submit = self.dlg.child_window(title="Submit",
                                            control_type="Button")
        self.removePost = self.dlg.child_window(title="Remove Post",
                                                control_type="Button")
        self.ok = self.dlg.child_window(title="Remove Post",
                                         auto_id="OkButton",
                                         control_type="Button")

    def update_message(self, m):
        '''If a message greater than 250 char in len in posted then
        mtgo breaks and is forced to restart'''
        m = m[:250] if len(m) > 250 else m
        self.adEdit.set_text(m)
        self.submit.click()

    def remove_message(self):
        self.removePost.click()
        self.ok.click()


class AccountScreen(DashScreen):
    def __init__(self, sk):
        DashScreen.__init__(self, sk)
        self.name = 'Account'
        self.accountSettings = self.dlg.child_window(title="Account Settings",
                                                     control_type="Text")
        self.editDefault = self.dlg.child_window(title="Edit Default Addresses",
                                                 auto_id="EditAddresses",
                                                 control_type="Button")

    def change_address(self, address):
        self.click(self.accountSettings)  
        self.click(self.editDefault)
        editDlg = self.dlg.child_window(title="Edit Addresses",
                                        control_type="Window")
        sameAsBilling = editDlg.child_window(title="Same as Billing",
                                               auto_id="CopyBoxOne",
                                               control_type="CheckBox")
        checkbox = sameAsBilling.wrapper_object()
        if checkbox.get_toggle_state():
            self.click(checkbox)
        # Edit address fields
        for i, edit in enumerate(editDlg.descendants(control_type='Edit')[9:]):
            edit.set_text(address[i])
        # Save changes
        self.click(editDlg.child_window(title="Save Changes",
                                        auto_id="SaveButton",
                                        control_type="Button"))

    def reset_address(self):
        self.click(self.accountSettings)
        self.click(self.editDefault)
        editDlg = self.dlg.child_window(title="Edit Addresses",
                                        control_type="Window")
        sameAsBilling = editDlg.child_window(title="Same as Billing",
                                             auto_id="CopyBoxOne",
                                             control_type="CheckBox")
        saveChanges = editDlg.child_window(title="Save Changes",
                                           auto_id="SaveButton",
                                           control_type="Button")
        self.click(sameAsBilling)
        self.click(saveChanges)
