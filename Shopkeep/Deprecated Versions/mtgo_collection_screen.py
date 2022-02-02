from PIL import Image
import pyautogui as pag
import sys, os, time
from mtgoHelpers import * # module in cwd

# MAP for navigating mtgo collection screen
# Maybe change this? Global variables clash?
from mapCollection import cmap


# screenshot regions for important card name locations on screen
REGIONS = {
    # bottom 1 & 2 are for the minimized bottom cards
    'T1 Quantity': (356, 184, 41, 19),
    'T1 Name': (416, 185, 289, 18),
    'T1 Shortcode': (884, 183, 52, 21),
    'T2 Quantity': (358, 207, 39, 22),
    'T2 Name': (415, 205, 322, 25),
    'T2 Shortcode': (880, 207, 55, 22),
    'B1 Quantity': (353, 949, 47, 20),
    'B1 Name': (413, 947, 357, 23),
    'B1 Shortcode': (881, 947, 60, 22),
    'B2 Quantity': (355, 970, 44, 23),
    'B2 Name': (415, 970, 369, 22),
    'B2 Shortcode': (881, 970, 60, 22)
    }

# top cards category selector menu in mtgo collection screen
topMenu = {
    'menu': (1900, 166),
    'Image': (1758, 204),
    'Quantity': (1758, 239),
    'Color': (1758, 274),
    'Name': (1758, 309),
    'Mana Cost': (1758, 344),
    'Type': (1758, 479),
    'Subtype': (1758, 514),
    'Power/Toughness': (1758, 549),
    'Set': (1758, 584),
    'Rarity': (1758, 619),
    'Text': (1758, 654),
    'Artist': (1758, 689),
    'Collector #': (1758, 724)
}

# top cards category selector menu in mtgo collection screen
# for vRest position
bottomMenu = {
    'menu': (1900, 583),
    'Image': (1758, 125),
    'Quantity': (1758, 160),
    'Color': (1758, 195),
    'Name': (1758, 230),
    'Mana Cost': (1758, 265),
    'Type': (1758, 300),
    'Subtype': (1758, 335),
    'Power/Toughness': (1758, 370),
    'Set': (1758, 405),
    'Rarity': (1758, 440),
    'Text': (1758, 475),
    'Artist': (1758, 510),
    'Collector #': (1758, 545)
}

def set_collection_bottom_menu():
    '''sets bottom menu categories to (Quantity, Name, Set, Rarity)'''

    goto_mtgo()

    # uncheck these boxes
    # maybe mtgo remembers placement of this info?
    for category in ['Color','Mana Cost','Type','Power/Toughness','Text']:
        pag.click(bottomMenu['menu'])
        time.sleep(.1)
        pag.click(bottomMenu[category])
        time.sleep(.1)
        
    # extend card name category right by 250 pixels
    pag.mouseDown((536, 581))
    pag.moveRel(250)
    pag.mouseUp()
    

# ALIGNMENT
def vert_rest():
    '''
    Returns collection screen vertical adjustment to rest
    '''

    goto_mtgo()

    # vertical reset handle position
    Vrest = (960, 529)
    imageFolder = 'MTGO Screen Images\\Collection Screen\\Vertical Adjustment'

    # checks for all vertical adjustment images (manually obtained)
    for f in os.listdir(imageFolder):
        im = Image.open(imageFolder+'\\'+f)
        center = pag.locateCenterOnScreen(im)
        if center:
            print('Collection Vertical Adjustment Image: '+f)
            pag.mouseDown(center)
            # REST COORD
            pag.moveTo(Vrest,duration=2)
            pag.mouseUp()
            time.sleep(.1)
            break
    # if an image is not found
    else:
        print('No image found. Add another vertical pic to database.')
        input('Hit Enter to continue...')


# ALIGNMENT
def horz_rest_top():
    '''
    Returns collection screen horizontal adjustment top to rest
    '''

    goto_mtgo()

    # horizontal top reset handle position
    # same as for trade screen
    HrestT = (337, 334)
    imageFolder = 'MTGO Screen Images\\Collection Screen\\Horizontal Adjustment Top'

    # checks for all vertical adjustment images (manually obtained)
    for f in os.listdir(imageFolder):
        im = Image.open(imageFolder+'\\'+f)
        center = pag.locateCenterOnScreen(im)
        if center:
            # if y coord is in top half of screen
            if center[1] < 530:
                print('Collection Horizontal Adjustment Top Image: '+f)
                pag.mouseDown(center)
                # REST COORD
                pag.moveTo(HrestT,duration=1)
                pag.mouseUp()
                time.sleep(.1)
                break
    # if an image is not found
    else:
        print('No image found. Add another horizontal top pic to database.')
        input('Hit Enter to continue...')


# ALIGNMENT
def horz_rest_bottom():
    '''
    Returns collection screen horizontal adjustment bottom to rest
    '''

    goto_mtgo()

    # horizontal top reset handle position
    HrestB = (337, 782)
    imageFolder = 'MTGO Screen Images\\Collection Screen\\Horizontal Adjustment Bottom'

    # checks for all vertical adjustment images (manually obtained)
    for f in os.listdir(imageFolder):
        im = Image.open(imageFolder+'\\'+f)
        center = pag.locateCenterOnScreen(im)
        if center:
            # if y coord is in bottom half of screen
            if center[1] > 530:
                print('Collection Horizontal Adjustment Bottom Image: '+f)
                pag.mouseDown(center)
                # REST COORD
                pag.moveTo(HrestB,duration=1)
                pag.mouseUp()
                time.sleep(.1)
                break
    # if an image is not found
    else:
        print('No image found. Add another horizontal bottom pic to database.')
        input('Hit Enter to continue...')


# ALIGNMENT
def close_binders_tab():
    '''
    Closes any open tab in the Decks & Binders section of the collection screen
    Only works for initial realignment, because one is highlighted after closing
    '''

    goto_mtgo()

    imageFolder = r'MTGO Screen Images\Decks & Binders Tabs'

    # checks for all horizontal adjustment images (manually obtained)
    for f in os.listdir(imageFolder):
        # open image and see if it is on screen
        im = Image.open(imageFolder+'\\'+f)
        center = pag.locateCenterOnScreen(im)
        if center:
            pag.click(center)
            time.sleep(.1)
            break
        
    else:
        print('No image found. Add another pic to database.')
        input('Hit Enter to continue...')


# ALIGNMENT
def align_categories_top():
    '''
    Standardizes left/right alignment of Qty, Name, and Set categories
    Assumes vertAdjust has been reset already
    '''

    goto_mtgo()

    # dividerColor found manually by inspecting color of yellow bars in categories
    dividerColor = (235, 199, 124)
    REGION = (345, 158, 1531, 9)
    im = pag.screenshot(region=REGION)
    
    categoryAdjustments = []
    
    i = 0
    while i < im.size[0]:
        if im.getpixel((i,0)) == dividerColor:
            categoryAdjustments.append((REGION[0] + i, REGION[1]))

            # skip 5 pixels over divider
            i += 5
        else:
            i += 1

    # makeshift error net
    if len(categoryAdjustments) < 2:
        print('Cannot see divider bars. Check alignment.')
        input('Hit Enter to continue...')

    # click in reverse order
    categoryAdjustments.reverse()
    
    for x, y in categoryAdjustments:
        pag.doubleClick((x,y))
        time.sleep(.1)

    # Expand Set
    pag.mouseDown((504, 165))
    pag.moveRel((20,0))
    pag.mouseUp()
    time.sleep(.1)

    # Expand Name
    pag.mouseDown((457, 165))
    pag.moveRel((400, 0))
    pag.mouseUp()
    time.sleep(.1)

    #Expand Qty.
    pag.mouseDown((393, 166))
    pag.moveRel((20, 0))
    pag.mouseUp()
    time.sleep(.1)
    

# ALIGNMENT
def align_categories_bottom():
    '''
    Standardizes left/right alignment of Qty, Name, and Set categories
    Assumes vertAdjust has been reset already
    '''

    goto_mtgo()
    
    # dividerColor found manually by inspecting color of yellow bars in categories
    dividerColor = (235, 199, 124)
    REGION = (344, 570, 1535, 22)
    im = pag.screenshot(region=REGION)
    
    categoryAdjustments = []
    
    i = 0
    while i < im.size[0]:
        if im.getpixel((i,0)) == dividerColor:
            categoryAdjustments.append((REGION[0] + i, REGION[1]))

            # skip 5 pixels over divider
            i += 5
        else:
            i += 1

    # makeshift error net
    if len(categoryAdjustments) < 2:
        print('Cannot see divider bars. Check alignment.')
        input('Hit Enter to continue...')

    # click in reverse order
    categoryAdjustments.reverse()
    
    for x, y in categoryAdjustments:
        pag.doubleClick((x,y))
        time.sleep(.1)

    # Expand Set
    pag.mouseDown((504, 581))
    pag.moveRel((20,0))
    pag.mouseUp()
    time.sleep(.1)

    # Expand Name
    pag.mouseDown((458, 580))
    pag.moveRel((400, 0))
    pag.mouseUp()
    time.sleep(.1)

    #Expand Qty.
    pag.mouseDown((393, 580))
    pag.moveRel((20, 0))
    pag.mouseUp()
    time.sleep(.1)


# Complete Initial Realignment
def refresh():
    '''
    Resets the alignment for the collection screen
    '''
    
    # reset alignments
    vert_rest()
    horz_rest_top()
    horz_rest_bottom()
    
    close_binders_tab()

    # Switch to (Active) For Trade binder
    pag.click(mapCollection['Decks & Binders']['Binders']['COORD'])
    time.sleep(.5)
    pag.click(mapCollection['Decks & Binders']['Binders']['(Active) For Trade']['COORD'])
    time.sleep(.5)

    # Switch top cards to List View
    pag.click(mapCollection['Cards']['Display']['COORD'])
    time.sleep(.5)
    pag.click(mapCollection['Cards']['Display']['List View']['COORD'])
    time.sleep(.5)

    # Switch bottom cards to List View
    pag.click(mapCollection['Binder']['Display']['COORD'])
    time.sleep(.5)
    pag.click(mapCollection['Binder']['Display']['List View']['COORD'])
    time.sleep(.5)
    
    align_categories_top()
    align_categories_bottom()

