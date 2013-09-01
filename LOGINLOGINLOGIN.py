import os
import time
import sys

from PIL import ImageGrab
from PIL import ImageOps

import win32api
import win32gui
import win32con


def window_callback(hwnd, resultList):
    """Callback to handle enumerate"""
    resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def sendkey(handle):
    """Send the key to the window, identified by handle"""
    print("Sending NUMPAD0...")
    win32api.SendMessage(handle, win32con.WM_KEYDOWN, 0x60, 0)
    win32api.SendMessage(handle, win32con.WM_KEYUP, 0x60, 0)

def get_handle():
    """Find the running zivar and get it's handle"""
    topWindows = []
    win32gui.EnumWindows(window_callback, topWindows)

    handle = None
    for wnd,title in topWindows:
        if title == "FINAL FANTASY XIV: A Realm Reborn":
            handle = wnd
            print("Found the window. Everything looks good.")

    if handle is None:
        raise Exception("Zivar window not found. Is it running?")

    return handle

def grab_game_window():
    """Capture the game window as a PIL image"""
    box = (0, 0, 1024, 768)
    im = ImageGrab.grab(box)
    #im.save('save.png', 'PNG')
    return im

def is_1017():
    """Test to see if the 1017 error is currently displayed"""
    im = grab_game_window()

    reference_code = (238, 190, 48)

    error_code_pixels = [
            #im.getpixel((728, 464)),
        im.getpixel((746, 468)),
        im.getpixel((746, 472)),
    ]

    print(error_code_pixels)

    for p in error_code_pixels:
        if p != reference_code:
            return False

    return True

def is_char_screen():
    """Test to see if the character screen has loaded"""
    im = grab_game_window()

    white_stuff = [
        im.getpixel((611, 54)),
        im.getpixel((666, 55)),
        im.getpixel((623, 76)),
        im.getpixel((588, 105)),
    ]

    print(white_stuff)

    for p in white_stuff:
        if p != (255, 255, 255):
            return False

    return True


def send_0():
    """Send key, and wait a bit"""
    sendkey(handle)
    time.sleep(1)


# setup stuff

handle = get_handle()

# Move the window to 0,0 and resize it
# make sure the game is in borderless windowed mode!
win32gui.MoveWindow(handle, 0, 0, 1024, 768, True)

#grab_game_window()
#exit()

print("Waiting 2 seconds for you to get your shit straight...")
time.sleep(2)

# assume we're at the login screen, start with two 0's
send_0()
send_0()

# loop forever (becuase this is gonna take a while)
while True:
    # wait for the character screen
    while not is_char_screen():
        print("Waiting for character screen to load...")
        time.sleep(1)
    print("Detected character screen!")

    # send two 0's to login.
    send_0()
    send_0()

    # wait for the error screen (or if we're lucky, it will never appaer!)
    while not is_1017():
        print("Waiting for error screen to load...")
        time.sleep(1)

    print("Detected error screen. Sorry, you didn't make it this time :(")

    # send two 0's to cancel the error screen, then select start
    send_0()
    send_0()
