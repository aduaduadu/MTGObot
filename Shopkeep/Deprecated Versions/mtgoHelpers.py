import pyautogui as pag
import os, time, pyperclip
from PIL import Image


def mouse_clip():
    '''copies mouse position as tuple (x, y) to clipboard'''

    mousePosition = pag.position()
    pyperclip.copy(str(mousePosition))
    return mousePosition
    

def goto_mtgo():
    '''brings focus to mtgo client from python script via a mouse click'''
    
    pag.click((30,30))
    time.sleep(.1)


def region_shot(REGIONS,region):
    '''
    quick snapshot of REGION region and saves it for viewing
    depends on paint() utility function from mtgoHelpers module

    takes REGIONS, a list of regions, and region, str form of region to snapshot
    '''
    
    im = pag.screenshot(region=REGIONS[region])
    im = crop_white_space(im)
    paint(im)

    return im


def paint(im):
    '''takes an image file, saves it to an example folder, opens in paint, maximizes'''

    # check if temp folder is created, make if not
    if not os.path.exists('paintings'):
        os.makedirs('paintings')

    # timestamp for filename
    fp = 'paintings\\'+str(int(time.time()))+'.png'
    im.save(fp,'PNG')
    os.startfile(fp)
    time.sleep(1)

    # click magnifying glass
    pag.click((335, 122))
    # magnify image
    for i in range(10):
        pag.click((9, 178))     
    # slide scroll bar all the way left
    pag.mouseDown((238, 991))
    pag.moveRel(-10,0)
    pag.mouseUp()


def magnify_all(folder):
    '''magnifies all images in a folder for inspecting'''

    for f in os.listdir(folder):
        os.startfile(folder+'\\'+f)
        time.sleep(.5)

        '''
        for i in range(5):
            pag.click((949, 21))
            time.sleep(.1)
            pag.press(['alt','v','i'])
        '''

        # click program
        pag.click((949, 21))
        time.sleep(.1)
        # click magnifying glass
        pag.click((336, 122))
        time.sleep(.1)
        
        # magnify image
        for i in range(10):
            pag.click((9, 178))     
        # slide scroll bar all the way left
        pag.mouseDown((238, 991))
        pag.moveRel(-10,0)
        pag.mouseUp()


def stitch(im1, im2):
    '''takes two images and stitches them together, returns a new image'''

    newIm = Image.new(im1.mode,(im1.size[0]+im2.size[0], im1.size[1]))
    newIm.paste(im1,box=(0,0))
    newIm.paste(im2,box=(im1.size[0],0))

    return newIm


def read_set_list(shortcode):
    '''takes a 3-letter shortcode, reads in that csv setList, returns order list'''
    
    f = open(shortcode+'.csv','r')
    setList = f.read().splitlines()
    setList.sort()
    f.close()

    return setList


# UTILITY function for easily finding region coordinates
def generate_region_box():
    '''returns a (left, top, width, height) tuple of the desired region'''

    # get top left of region
    print('Hover mouse over top left corner of region')
    print('Recording position in...')
    for i in range(5,0,-1):
        print(i)
        time.sleep(1)

    left, top = pag.position()

    # get bottom right of region
    print('Hover mouse over bottom right corner of region')
    print('Recording position in...')
    for i in range(5,0,-1):
        print(i)
        time.sleep(1)

    right, bottom = pag.position()

    # down is +y, hence bottom - top
    height = bottom - top
    width = right - left

    # paint image to verify accuracy
    snap = pag.screenshot(region=(left, top, width, height))
    paint(snap)

    pyperclip.copy(str((left, top, width, height)))

    return left, top, width, height


def outline_region(region):
    '''
    Uses the cursor to outline a given region. For verification and visualization.
    '''


# WILL THIS BREAK FOR A COMPLETELY WHITE IMAGE? Yes.
# DIFFERENT COLOR MODES?
# standardizes images by cropping outer white space
def crop_white_space(im):
    '''takes an image im and crop out white space on all sides, returns an image'''
    
    width, height = im.size

    # this could be simpler right?
    topRow = []
    botRow = []
    rightCol = []
    leftCol = []

    # what about different color modes?
    white = (255, 255, 255)

    # find top row
    for j in range(height):
            for i in range(width):
                if im.getpixel((i,j)) != white:
                    topRow.append(j)
                    break

    # find bottom row
    # traverse backwards
    for j in range(height-1,-1,-1):
        for i in range(width):
            if im.getpixel((i,j)) != white:
                botRow.append(j)
                break

    # find leftmost column
    for i in range(width):
        for j in range(height):
            if im.getpixel((i,j)) != white:
                leftCol.append(i)
                break

    # find rightmost column
    # traverse backwards
    for i in range(width-1,-1,-1):
        for j in range(height):
            if im.getpixel((i,j)) != white:
                rightCol.append(i)
                break

    # +1s are to include the outer right and outer bottom
    croppedIm = im.crop((leftCol[0],topRow[0],rightCol[0]+1,botRow[0]+1))

    return croppedIm
