import os
import time
import sys
import ImageGrab

import ImageOps

import win32api
import win32gui
import win32con



def windowEnumerationHandler(hwnd, resultList):
    """Callback"""
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
    box = (0, 0, 1024, 768)
    im = ImageGrab.grab(box)
    #im.save('save.png', 'PNG')
    return im

def isError1017():
    im = screenGrab()
    # test to see if it's an error message

    reference_code = (239, 194, 53)

    error_code_pixels = [
        im.getpixel((728, 464)),
        im.getpixel((746, 468)),
        im.getpixel((746, 472)),
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
        im.getpixel((611, 54)),
        im.getpixel((666, 55)),
        im.getpixel((623, 76)),
        im.getpixel((588, 105)),
    ]

    print white_stuff

    for p in white_stuff:
        if p != (255, 255, 255):
            return False

    return True


def send0():
    sendKeys(handle)
    time.sleep(0.75)



# setup stuff

handle = get_handle()

# Move the window to 0,0 and resize it
# make sure the game is in borderless windowed mode!
win32gui.MoveWindow(handle, 0, 0, 1024, 768, True)


#screenGrab()
#exit()


print "waiting 2 seconds"
time.sleep(2)

# assume we're at the login screen, start with two 0's
send0()
send0()

while True:
    # wait for the character screen
    while not isCharSelectScreen():
        print("Waiting for character screen to load...")
        time.sleep(1)
    print("Detected character screen!")

    send0()
    send0()

    # now find the error screen
    while not isError1017():
        print("Waiting for error screen to load...")
        time.sleep(1)

    print("Detected error screen. Sorry, you didn't make it this time :(")

    send0()
    send0()





