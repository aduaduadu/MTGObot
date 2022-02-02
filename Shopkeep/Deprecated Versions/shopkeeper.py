import pyautogui as pag
import pyperclip
from PIL import Image
import os

# dictionary with (x, y) coordinates of mtgo client link locations
COORD = {
'Client': (30, 30),
'Home': (115, 75),
'Collection': (245, 75),
'Play Lobby': (415, 75),
'Store': (555, 75),
'Trade': (660, 75),
'My Post: Message': (100, 900),
'Submit': (1540, 985),
'Remove Post': (1675, 985),
'Cancel Changes': (1825, 985),
'Account': (780, 75),
'Account Settings': (95, 225),
'Edit Default Addresses': (720, 800),
'First name': (1140, 390),
'Save Changes': (1185, 740),
'Help': (890, 75),
'Chat': (1795, 75)
}

# function for navigating around the mtgo client
def goto(name):
        # move cursor to 'name' coordinate, click, reset mouse position
	pag.click(COORD[name])
	pag.moveTo(COORD['Client'])

# quick function for clearing text
def clear_text():
        pag.hotkey('ctrl','a')
        pag.press('backspace')

def change_address_to_home():
        # navigate to 'Edit Default Addresses' in 'Account' tab
        pag.moveTo(COORD['Client'])
        goto('Account')
        goto('Account Settings')
        goto('Edit Default Addresses')

        pag.click(COORD['First name'])
        clear_text()

        # unfinished

def address_test_emilie():
        # start with mtgo client just behind this main window for this function
        
        # changes shipping address to:
        # Emilie Samuelsen
        # 2384 McKinley St
        # Ypsilanti, MI 48197
        
        pag.click(COORD['Client'])
        pag.click(COORD['Edit Default Addresses'])
        pag.click(COORD['First name'])
        clear_text()

        pag.typewrite('Emilie')
        pag.press('tab')
        pag.typewrite('Samuelsen')
        pag.press('tab')
        pag.typewrite('2384 McKinley St')
        pag.press('tab')
        pag.press('tab')
        pag.typewrite('Ypsilanti')
        pag.press('tab')
        pag.typewrite('MI')
        pag.press('tab')
        pag.press('tab')
        pag.typewrite('48197')
        pag.moveTo(COORD['Save Changes'])
        pag.click()

def address_test_david():
        # start with mtgo client just behind this main window for this function
        
        # changes shipping address to:
        # David Wilkins
        # 2384 McKinley St
        # Ypsilanti, MI 48197
        
        pag.click(COORD['Client'])
        pag.click(COORD['Edit Default Addresses'])
        pag.click(COORD['First name'])
        clear_text()

        pag.typewrite('David')
        pag.press('tab')
        pag.typewrite('Wilkins')
        pag.press('tab')
        pag.typewrite('2384 McKinley St')
        pag.press('tab')
        pag.press('tab')
        pag.typewrite('Ypsilanti')
        pag.press('tab')
        pag.typewrite('MI')
        pag.press('tab')
        pag.press('tab')
        pag.typewrite('48197')
        pag.moveTo(COORD['Save Changes'])
        pag.click()

def address_test_customer():
        # start with mtgo client just behind this main window for this function
        
        # changes shipping address to:
        # Customer X
        # 1234 Elsewhere
        # Somewhere, MI 12345
        
        pag.click(COORD['Client'])
        pag.click(COORD['Edit Default Addresses'])
        pag.click(COORD['First name'])
        clear_text()

        pag.typewrite('Customer')
        pag.press('tab')
        pag.typewrite('X')
        pag.press('tab')
        pag.typewrite('1234 Elsewhere')
        pag.press('tab')
        pag.press('tab')
        pag.typewrite('Somewhere')
        pag.press('tab')
        pag.typewrite('MI')
        pag.press('tab')
        pag.press('tab')
        pag.typewrite('12345')
        pag.moveTo(COORD['Save Changes'])
        pag.click()

# generates 'Contact Buyer' message for each eBay sale
# copies message string to clipboard
def contact_buyer_message():
        MESSAGE = '''Thank you for your purchase of a __ Complete Set
with Mythics! Your order will be processed Wednesday, October 14
and shipped soon after. Please allow 1 to 3 weeks from that date for
delivery.\n\nI will upload tracking information as soon as your order is
shipped.'''
        pyperclip.copy(MESSAGE)
