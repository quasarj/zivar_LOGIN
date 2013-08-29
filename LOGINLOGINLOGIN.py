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
    im.save('save.png', 'PNG')
    #return im

def isError1017():
    im = screenGrab()
    # test to see if it's an error message

    reference_code = (239, 194, 53)
    reference_background = (16, 16, 16)

    error_code_pixels = [
        im.getpixel((728, 646)),
        im.getpixel((746, 647)),
        im.getpixel((746, 652)),
    ]

    box_background_pixels = [
        im.getpixel((681, 620)),
        im.getpixel((379, 636)),
    ]

    for p in error_code_pixels:
        if p != reference_code:
            return False

    for p in box_background_pixels:
        if p != reference_background:
            return False

    return True

def isCharSelectScreen():
    im = screenGrab()
    # white char box and realm square
    white_stuff = [
        im.getpixel((587, 92)),
        im.getpixel((661, 92)),
        im.getpixel((709, 117)),
        im.getpixel((580, 149)),
        im.getpixel((676, 163)),

        # character name, gaurantees loaded
        im.getpixel((632, 179)),
        im.getpixel((664, 177)),
        im.getpixel((616, 177)),
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


exit()


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





