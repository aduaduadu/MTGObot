from PIL import Image
import pyautogui as pag
import os, time, pymongo
from mtgoHelpers import * # module in cwd
import price_gen # module in cwd

# MAP for navigating mtgo collection screen
# Maybe change this? Global variables clash?
from mapTransaction import mapTransaction


# establish connection to db
conn = pymongo.MongoClient()
db = conn.card_data


# regions of areas in which screenshots will be taking place
REGIONS = {
    'YWR Quantity': (19, 946, 41, 18),
    'YWR Name': (87, 946, 400, 18),
    'YWR Shortcode': (553, 946, 57, 18),
    'OWR Quantity': (816, 946, 55, 18),
    'OWR Name': (881, 946, 400, 18),
    'OWR Shortcode': (1346, 946, 58, 18)
    }
    

# ADJUSTMENT
def vert_rest():
    '''
    Returns collection screen vertical adjustment to rest
    '''

    goto_mtgo()

    # vertical reset handle position
    Vrest = (803, 542)
    imageFolder = 'MTGO Screen Images\\Trade Screen\\Vertical Adjustment'

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
        # ERROR cupid
        print('ERROR cupid')
        print('No image found. Add another pic to database.')
        input('Hit Enter to continue...')


# ADJUSTMENT
def horz_rest_top():
    '''
    Returns trade screen horizontal adjustment top to rest
    '''

    goto_mtgo()

    # horizontal top reset handle position
    # same as for collection screen
    HrestT = (337, 334)
    imageFolder = 'MTGO Screen Images\\Trade Screen\\Horizontal Adjustment'

    # checks for all vertical adjustment images (manually obtained)
    for f in os.listdir(imageFolder):
        im = Image.open(imageFolder+'\\'+f)
        center = pag.locateCenterOnScreen(im)
        if center:
            # if y coord is in top half of screen
            if center[1] < 530:
                print('Trade Horizontal Adjustment Image: '+f)
                pag.mouseDown(center)
                # REST COORD
                pag.moveTo(HrestT,duration=1)
                pag.mouseUp()
                time.sleep(.1)
                break
    # if an image is not found
    else:
        # ERROR cupid
        print('ERROR cupid')
        print('No image found. Add another pic to database.')
        input('Hit Enter to continue...')


# ADJUSTMENT
def horz_rest_bottom():
    '''
    Returns collection screen horizontal adjustment bottom to rest
    Use after minimize_trade() has been completed (static region chosen)
    '''

    goto_mtgo()

    # horizontal bottom reset handle position
    HrestB = (805, 970)

    # manually chosen region via generate_region_box() function
    REGION = (523, 878, 505, 5)

    # black pixel color
    BLACK = (0, 0, 0)

    # take specific screenshot
    im = pag.screenshot(region=REGION)
    width, height = im.size

    # two divider lines to be ready for in horizontal scan of image
    dividerCoords = []

    for i in range(width):
        if im.getpixel((i,0)) != BLACK:
            dividerCoords.append(i)

    # x point for 2nd divider line
    x = REGION[0] + dividerCoords[1]

    # low enough to ensure horizontal adjustment cursor
    y = 970

    pag.mouseDown(x,y)
    pag.moveTo(HrestB)
    pag.mouseUp()
            

def minimize_trade():
    '''minimizes cards on mtgo trade screen for consistent screenshots'''

    goto_mtgo()

    # screen position when transaction screen cards are minimized
    minRest = (803, 874)

    # folder with vertical adjustment images
    folder = r'MTGO Screen Images\Trade Screen\Vertical Adjustment'

    # checks for all vertical adjustment images (manually obtained)
    for f in os.listdir(folder):
        im = Image.open(folder+'\\'+f)
        center = pag.locateCenterOnScreen(im)
        if center:
            print('Trade Vertical Adjustment Image: '+f)
            pag.mouseDown(center)
            pag.moveTo(minRest,duration=2)
            pag.mouseUp()
            time.sleep(.1)
            break
    # if an image is not found
    else:
        # ERROR minnie
        print('ERROR minnie')
        print('No image found. Add another pic to database.')
        input('Hit Enter to continue...')


# ALIGNMENT
def align_categories_ywr():
    '''
    Standardizes left/right alignment of Qty, Name, and Set categories
    Assumes transaction cards have already been minimized
    '''

    goto_mtgo()

    # dividerColor found manually by inspecting color of yellow bars in categories
    dividerColor = (235, 199, 124)
    REGION = (17, 921, 739, 13)
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
        # ERROR johnny
        print('ERROR johnny')
        print('Cannot see divider bars. Check alignment.')
        input('Hit Enter to continue...')

    # click in reverse order
    categoryAdjustments.reverse()
    
    for x, y in categoryAdjustments:
        pag.doubleClick((x,y))
        time.sleep(.1)

    # Expand Set
    pag.mouseDown((175, 928))
    pag.moveRel((20,0))
    pag.mouseUp()
    time.sleep(.1)

    # Expand Name
    pag.mouseDown((130, 927))
    pag.moveRel((400, 0))
    pag.mouseUp()
    time.sleep(.1)

    #Expand Qty.
    pag.mouseDown((64, 927))
    pag.moveRel((20, 0))
    pag.mouseUp()
    time.sleep(.1)


# ALIGNMENT
def align_categories_owr():
    '''
    Standardizes left/right alignment of Qty, Name, and Set categories
    Assumes transaction cards have already been minimized
    '''

    goto_mtgo()

    # dividerColor found manually by inspecting color of yellow bars in categories
    dividerColor = (235, 199, 124)
    REGION =(809, 921, 754, 14)
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
        # ERROR johnny
        print('ERROR johnny')
        print('Cannot see divider bars. Check alignment.')
        input('Hit Enter to continue...')

    # click in reverse order
    categoryAdjustments.reverse()
    
    for x, y in categoryAdjustments:
        pag.doubleClick((x,y))
        time.sleep(.1)

    # Expand Set
    pag.mouseDown((968, 927))
    pag.moveRel((20,0))
    pag.mouseUp()
    time.sleep(.1)

    # Expand Name
    pag.mouseDown((924, 928))
    pag.moveRel((400, 0))
    pag.mouseUp()
    time.sleep(.1)

    #Expand Qty.
    pag.mouseDown((859, 927))
    pag.moveRel((20, 0))
    pag.mouseUp()
    time.sleep(.1)


def highlight_cards(side):
    '''
    highlights cards as a function of side
    side options: ['YWR', 'OWR']
    '''

    goto_mtgo()

    ywrCards = (41, 956)
    owrCards = (832, 956)

    if side == 'OWR':
        point = owrCards
    else:
        point = ywrCards
    
    pag.click(point)
    time.sleep(1)
    pag.hotkey('ctrl','a')
    time.sleep(.1)


def tulip_shot(side):
    '''
    takes a region (from REGIONS global list) and returns a tuple
    of images (quantity,name,shortcode) for that region

    depends on crop_white_space() from mtgoHelpers module
    '''

    quantityIm = pag.screenshot(region=REGIONS[side+' Quantity'])
    quantityIm = crop_white_space(quantityIm)
    nameIm = pag.screenshot(region=REGIONS[side+' Name'])
    nameIm = crop_white_space(nameIm)
    shortcodeIm = pag.screenshot(region=REGIONS[side+' Shortcode'])
    shortcodeIm = crop_white_space(shortcodeIm)

    return quantityIm, nameIm, shortcodeIm


# TODO: cannot read lists with duplicate names ordered together yet
def pick_tulips(side):
    '''
    side options: ['YWR', 'OWR']

    returns a list of image tuples, cropped card line items from mtgo screen:
    [(quantityIm, nameIm, shortcodeIm),...]
    '''

    # initialize cardTuple list
    tulips = []

    # initialize previousNameIm to compare against current nameIm
    previousNameIm = Image.new('RGB',(10,10))

    # reads trade list until duplicate name is encountered
    # TOO FRAGILE against LAG
    while True:

        tulip = quantityIm, nameIm, shortcodeIm = tulip_shot(side)

        # if name and previousName the same, break loop
        if nameIm.tostring() == previousNameIm.tostring():
            print('duplicate encountered. breaking...')
            break

        # if not same...
        tulips.append(tulip) # append pic to picTuples
        previousNameIm = nameIm # save name for end of list detection

        # scroll down once
        pag.click(mapTransaction['OWR']['Scroll Down']['COORD'])
        time.sleep(1) ### TIME TESTING ###

    return tulips


def smell_tulips(tulips):
    '''
    takes a list of tuples [(quantityIm, nameIm, shortcodeIm),...]
    and uses image recognition on each image, returns a cardList from tulips

    quantityIm only searches quantitity images
    shortcodeIm only search shortcode images

    figure out shortcode, then filter by that to reduce name images search
    maybe unnecessary if all in .tostring format
    '''

    # initialize list
    cardList = []
    for quantityIm, nameIm, shortcodeIm in tulips:

        # initialize variables for tulip
        quantity = name = shortcode = 0

        # quantity
        for f in os.listdir('Quantity Images'):
            if Image.open('Quantity Images\\'+f).tostring() == quantityIm.tostring():
                # if same, quantity = filename without extension
                quantity = int(os.path.splitext(f)[0])

        # shortcode
        for f in os.listdir('Shortcode Images'):
            if Image.open('Shortcode Images\\'+f).tostring() == shortcodeIm.tostring():
                shortcode = os.path.splitext(f)[0]

        # name
        for f in os.listdir(shortcode):        
            if Image.open(shortcode+'\\'+f).tostring() == nameIm.tostring():
                name = os.path.splitext(f)[0]

        cardList.append((quantity, name, shortcode))

    return cardList


# UTILITY function for getting name image files for one set
def get_images_for_one_set(side, shortcode):
    '''
    side options: ['YWR', 'OWR']

    shortcode examples: ['ORI', 'DTK', 'FRF', 'KTK']

    saves all name images for one set to a folder = shortcode

    assumes there is one full set in the mtgo trade screen and it has been
    sorted by name, assumes align_categories_owr has been run

    assumes there exists a shortcode.csv file in cwd for name assignment
    '''

    # set mtgo screen up for reading cards
    minimize_trade()
    highlight_cards(side)

    # make folder for images if it does not exist
    if not os.path.exists(shortcode):
        os.makedirs(shortcode)

    # generate ordered list of card names in set 'shortcode'
    f = open(shortcode+'.csv','r')
    setList = f.read().splitlines()
    setList.sort()
    f.close()

    # all except last one
    for name in setList:

        # snapshot
        tulip = quantityIm, nameIm, shortcodeIm = tulip_shot(side)
        nameIm.save(shortcode+'\\'+name+'.png','PNG')

        # scroll down once
        pag.click(mapTransaction['OWR']['Scroll Down']['COORD'])
        time.sleep(.1) ### TIME TESTING ###


# UTILITY function for getting quantity images
def get_quantity_images():

    folder = r'C:\Users\David Wilkins\Desktop\Code\MTGO Bot\Quantity Images'

    # set mtgo screen up for reading cards
    minimize_trade()
    highlight_cards('OWR')

    # initialize previousNameIm to compare against current nameIm
    previousQuantityIm = Image.new('RGB',(10,10))

    # counter for naming images
    i = 1
    while True:
        im = pag.screenshot(region=REGIONS['OWR Quantity'])
        im = crop_white_space(im)

        if im.tostring() == previousQuantityIm.tostring():
            print('duplicate encountered. breaking...')
            break

        im.save(folder+'\\'+str(i)+'.png','PNG')
        previousQuantityIm = im

        # scroll down once
        pag.click(mapTransaction['OWR']['Scroll Down']['COORD'])
        time.sleep(1) ### TIME TESTING ###

        i+=1


# UTILITY function for getting name image files for one set
def get_shortcode_images():

    folder = r'C:\Users\David Wilkins\Desktop\Code\MTGO Bot\Shortcode Images'

    # set mtgo screen up for reading cards
    minimize_trade()
    highlight_cards('OWR')

    # initialize previousShortcodeIm to compare against current shortcodeIm
    previousShortcodeIm = Image.new('RGB',(10,10))

    # counter for naming files
    i = 1
    while True:
        im = pag.screenshot(region=REGIONS['OWR Shortcode'])
        im = crop_white_space(im)

        if im.tostring() == previousShortcodeIm.tostring():
            print('duplicate encountered. breaking...')
            break

        im.save(folder+'\\'+str(i)+'.png','PNG')
        previousShortcodeIm = im

        # scroll down once
        pag.click(mapTransaction['OWR']['Scroll Down']['COORD'])
        time.sleep(1) ### TIME TESTING ###

        i+=1


def refresh():

    goto_mtgo()
    
    vert_rest()
    horz_rest_top()
    horz_rest_bottom()

    minimize_trade()

    align_categories_owr()
    align_categories_ywr()


# the whole shebang atm
def main():

    # set mtgo screen up for reading cards
    minimize_trade()
    align_categories_owr()
    highlight_cards('OWR')

    # pick tulips from trade screen
    tulips = pick_tulips('OWR')

    # decipher
    owrlist = smell_tulips(tulips)

    return owrlist
