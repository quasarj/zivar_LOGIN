import os
import time
import sys
import ImageGrab

import ImageOps

import win32api
import win32gui
import win32con



def windowEnumerationHandler(hwnd, resultList):

    '''Pass to win32gui.EnumWindows() to generate list of window handle, window text tuples.'''

    resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def sendKeys(handle):
    print "Sending NUMPAD0..."
    win32api.SendMessage(handle, win32con.WM_KEYDOWN, 0x60, 0)
    win32api.SendMessage(handle, win32con.WM_KEYUP, 0x60, 0)

def get_handle():
    topWindows = []
    win32gui.EnumWindows(windowEnumerationHandler, topWindows)

    handle = None
    for wnd,title in topWindows:
        if title == "FINAL FANTASY XIV: A Realm Reborn":
            handle = wnd
            print "Found the window. Everything looks good."

    if handle is None:
        print "WoW window not found. Is it running?"
        sys.exit(1)

    return handle

def screenGrab():
    box = (0, 0, 1024, 1080)
    im = ImageGrab.grab(box)
    # im.save('save.png', 'PNG')
    return im

def isError1017():
    im = screenGrab()
    # test to see if it's an error message

    reference_code = (239, 194, 53)

    error_code_pixels = [
        im.getpixel((728, 466)),
        im.getpixel((736, 465)),
        im.getpixel((739, 470)),
    ]

    print error_code_pixels

    for p in error_code_pixels:
        if p != reference_code:
            return False

    return True

def isCharSelectScreen():
    im = screenGrab()
    # white char box and realm square
    white_stuff = [
        im.getpixel((596, 82)),
        im.getpixel((740, 82)),
        im.getpixel((737, 102)),
        im.getpixel((590, 102)),
    ]

    print white_stuff

    for p in white_stuff:
        if p != (255, 255, 255):
            return False

    return True


def send0():
    sendKeys(handle)
    time.sleep(0.5)


im = screenGrab()
# print isCharSelectScreen()
# print isError1017()



handle = get_handle()

# Move the window to 0,0 so measurements are accurate
win32gui.MoveWindow(handle, 0, 0, 0, 0, True)


#exit()


print "waiting 2 seconds"
time.sleep(2)

# assume we're at the login screen, start with two 0's
send0()
send0()

while True:
    # wait for the character screen
    while not isCharSelectScreen():
        print "Character not loading?"
        time.sleep(1)

    send0()
    send0()

    # now find the error screen
    while not isError1017():
        print "Error not loading?"
        time.sleep(1)


    send0()
    send0()





