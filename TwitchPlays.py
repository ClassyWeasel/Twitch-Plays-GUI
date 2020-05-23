# Written by DougDoug (DougDoug on Youtube, DougDougW on Twitch)

# The source code primarily comes from:
    # Wituz's "Twitch Plays" tutorial: http://www.wituz.com/make-your-own-twitch-plays-stream.html
    # PythonProgramming's "Python Plays GTA V" tutorial: https://pythonprogramming.net/direct-input-game-python-plays-gta-v/

# There are 2 other files needed to run this code:
    # TwitchPlays_AccountInfo.py is where you put your Twitch username and OAuth token. This is to keep your account details separated from the main source code.
    # TwitchPlays_Connection.py is the code that actually connects to Twitch. You should not modify this file.

# Disclaimer: 
    # This code is NOT optimized or well-organized. I am not a Python programmer.
    # I created a simple version that works quickly, and I'm sharing it for educational purposes.

###############################################
# Import and define our functions / key codes to send key commands

# General imports
import time
import tkinter as tk
from tkinter import ttk
import subprocess
import ctypes
import random
import string

# Twitch imports
import TwitchPlays_Connection
from TwitchPlays_AccountInfo import TWITCH_USERNAME, TWITCH_OAUTH_TOKEN

# Controller imports
import pyautogui
import pynput
from pynput.mouse import Button, Controller

SendInput = ctypes.windll.user32.SendInput

# KEY PRESS NOTES
# The standard "Twitch Plays" tutorial key commands do NOT work in DirectX games (they only work in general windows applications)
# Instead, we use DirectX key codes and input functions below.
# This DirectX code is partially sourced from: https://stackoverflow.com/questions/53643273/how-to-keep-pynput-and-ctypes-from-clashing

# Presses and permanently holds down a keyboard key
def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Releases a keyboard key if it is currently pressed down
def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Helper function. Holds down a key for the specified number of seconds, then releases it.
def PressAndHoldKey(hexKeyCode, seconds):
    PressKeyPynput(hexKeyCode)
    time.sleep(seconds)
    ReleaseKeyPynput(hexKeyCode)

# Mouse Controller, using pynput
    # pynput.mouse functions are found at: https://pypi.org/project/pynput/
    # NOTE: pyautogui's click() function permanently holds down in DirectX, so I used pynput instead for mouse instead.
mouse = Controller()

###################### Written by ClassyWeasel #########################

# Array of commands (List of each Twitch command for GTAV)
commandList = ["Left", "Right", "Drive", "Reverse", "Stop", "Brake", "Shoot", "Drag Mouse Up", "Drag Mouse Down", "Select All", "Type "]
secondaryCommandList = [""] * len(commandList)

# Array of descriptions for each command
descrip = ["If the chat message is 'left', then hold down the A key for 2 seconds", "If the chat message is 'right', then hold down the D key for 2 seconds",
            "If message is 'drive', then permanently hold down the W key", "If message is 'reverse', then permanently hold down the S key", "Release both the 'drive' and 'reverse' keys",
            "Press the spacebar for 0.7 seconds", "Presses the left mouse button down for 1 second, then releases it", "Clicks and drags the mouse upwards",
            "Clicks and drags the mouse downwards", "First holds down the LEFT_CONTROL key, then presses the A key for 0.1 seconds,\n then releases the LEFT_CONTROL key.",
            "Here, if a chat message says 'type ...', it will type out their text."]

# Array of values which keep track of which commands are turned on or off in chat
OnOrOff = [1] * len(commandList)
# Keeps track of whether or not we have paused Twitch Plays
TwitchActive = False

class SampleApp(tk.Tk):

    def __init__(window):

        # Setup window
        bgColor = "gray28"
        tk.Tk.__init__(window)
        window.minsize(560, 300)
        window.title("Twitch Plays")
        window.config(bg=bgColor)

        #Global variables
        global commandList
        global secondaryCommandList
        global OnOrOff
        global descrip

        # Creating all our rows of commands (buttons, entry boxes, label, etc.)
        for i in range(0, len(commandList)):
            globals()['Label %s' % i] = tk.Label(window, text=f"{commandList[i]}", fg='SeaGreen1', bg='dark green', font=20)
            globals()['Label %s' % i].grid(sticky="WE", column=0, row=i+1, columnspan=1)
            globals()['Label2 %s' % i] = tk.Label(window, text=f"              ", fg='coral1', bg=bgColor, font=20)
            globals()['Label2 %s' % i].grid(sticky="W", column=3, row=i + 1)
            globals()['ActBtn %s' % i] = tk.Button(window, text="Deactivate", bg='grey57', command=lambda commandNum=i: window.activate(commandNum))
            globals()['ActBtn %s' % i].grid(sticky="W", column=4, row=i + 1)
            globals()['Descr %s' % i] = tk.Button(window, text="Description", bg='sea green', command=lambda commandNum=i: window.pop_up(commandList[commandNum], descrip[commandNum]))
            globals()['Descr %s' % i].grid(sticky="W", column=5, row=i + 1)
            globals()['name %s' % i] = tk.StringVar()
            globals()['name %s' % i].set(commandList[i])
            globals()['txtBox %s' % i] = tk.Entry(window, width=25, bg='LightSkyBlue1', textvariable=globals()['name %s' % i])
            globals()['txtBox %s' % i].grid(column=2, row=i + 1)
            globals()['ChaBtn %s' % i] = tk.Button(window, text="Change name", bg='SkyBlue1', command=lambda command=i: window.changeName(command))
            globals()['ChaBtn %s' % i].grid(sticky="E", column=1, row=i + 1)

        # Pause button:
        window.pause_btn = tk.Button(window, text="Click Here to Start Twitch Plays!", bg='ivory2', font=('Helvetica', 13, 'bold'), command=window.pause)
        window.pause_btn.grid(sticky='NSEW', column=0, row=0, columnspan=6)

    # Function that changes the Twitch chat name of a command (i.e. changes 'drive' to 'forward' or what have you)
    def changeName(window, commandNum):
        secondaryCommandList[commandNum] = globals()['name %s' % commandNum].get().lower()
        globals()['Label %s' % commandNum].config(text=f"{commandList[commandNum]} (or {globals()['name %s' % commandNum].get()})")


    # Function that turns a given key on or off when the corresponding button is pressed (Green means on, Red means off)
    def activate(window, commandNum):
        if OnOrOff[commandNum] == 0:
            OnOrOff[commandNum] = 1
            globals()['Label %s' % commandNum].config(fg='SeaGreen1', bg='dark green')
            globals()['ActBtn %s' % commandNum].config(text='Deactivate')
        else:
            OnOrOff[commandNum] = 0
            globals()['Label %s' % commandNum].config(fg='gray84', bg='OrangeRed2')
            globals()['ActBtn %s' % commandNum].config(text='Activate')


    # Function that pauses Twitch Plays
    def pause(window):
        global TwitchActive
        if TwitchActive == True:
            TwitchActive = False
            window.pause_btn.config(text="Click Here to Start Twitch Plays!")
        else:
            TwitchActive = True
            window.pause_btn.config(text="Click Here to Pause Twitch Plays")

    # Pop up window when clicking on the description of each Twitch command
    def pop_up(window, title, message):
        root = tk.Tk()
        root.title(title)
        root.minsize(200, 110)
        w = tk.Label(root, text=message, width=0, height=4)
        w.pack()
        b = tk.Button(root, text="OK", command=root.destroy, width=10)
        b.pack()
        root.geometry('+%d+%d' % (window.winfo_x(), window.winfo_y()))
        root.mainloop()


###############################################

# DIRECTX KEY CODES
# These codes identify each key on the keyboard.
# Note that DirectX's key codes (or "scan codes") are NOT the same as Windows virtual hex key codes. 
#   DirectX codes are found at: https://docs.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-6.0/aa299374(v=vs.60)
Q = 0x10
W = 0x11
E = 0x12
R = 0x13
T = 0x14
Y = 0x15
U = 0x16
I = 0x17
O = 0x18
P = 0x19
A = 0x1E
S = 0x1F
D = 0x20
F = 0x21
G = 0x22
H = 0x23
J = 0x24
K = 0x25
L = 0x26
Z = 0x2C
X = 0x2D
C = 0x2E
V = 0x2F
B = 0x30
N = 0x31
M = 0x32
ESC = 0x01
ONE = 0x02
TWO = 0x03
THREE = 0x04
FOUR = 0x05
FIVE = 0x06
SIX = 0x07
SEVEN = 0x08
EIGHT = 0x09
NINE = 0x0A
ZERO = 0x0B
MINUS = 0x0C
EQUALS = 0x0D
BACKSPACE = 0x0E
SEMICOLON = 0x27
TAB = 0x0F
CAPS = 0x3A
ENTER = 0x1C
LEFT_CONTROL = 0x1D
LEFT_ALT = 0x38
LEFT_SHIFT = 0x2A
SPACE = 0x39
DELETE = 0x53
COMMA = 0x33
PERIOD = 0x34
BACKSLASH = 0x35
NUMPAD_0 = 0x52
NUMPAD_1 = 0x4F
NUMPAD_2 = 0x50
NUMPAD_3 = 0x51
NUMPAD_4 = 0x4B
NUMPAD_5 = 0x4C
NUMPAD_6 = 0x4D
NUMPAD_7 = 0x47
NUMPAD_8 = 0x48
NUMPAD_9 = 0x49
NUMPAD_PLUS = 0x4E
NUMPAD_MINUS = 0x4A
LEFT_ARROW = 0xCB
RIGHT_ARROW = 0xCD
UP_ARROW = 0xC8
DOWN_ARROW = 0xD0
LEFT_MOUSE = 0x100
RIGHT_MOUSE = 0x101
MIDDLE_MOUSE = 0x102
MOUSE3 = 0x103
MOUSE4 = 0x104
MOUSE5 = 0x105
MOUSE6 = 0x106
MOUSE7 = 0x107
MOUSE_WHEEL_UP = 0x108
MOUSE_WHEEL_DOWN = 0x109
########################################################

# Connects to your twitch chat, using your username and OAuth token.
# TODO: make sure that your Twitch username and OAuth token are added to the "TwitchPlays_AccountInfo.py" file
t = TwitchPlays_Connection.Twitch();
t.twitch_connect(TWITCH_USERNAME, TWITCH_OAUTH_TOKEN);

##########################################################

window = SampleApp()

def task():
    global secondaryCommandList

    if TwitchActive:
        # Check for new chat messages
        new_messages = t.twitch_recieve_messages();
        if not new_messages:
            msg = ""
        else:
            try:
                for message in new_messages:
                    # We got a new message! Get the message and the username.
                    msg = message['message'].lower()
                    username = message['username'].lower()

                    ###################################
                    # Example GTA V Code
                    ###################################


                    # If the chat message is "left", then hold down the A key for 2 seconds
                    if (msg == "left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                        PressAndHoldKey(A, 2)

                    # If the chat message is "right", then hold down the D key for 2 seconds
                    if (msg == "right" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                        PressAndHoldKey(D, 2)

                    # If message is "drive", then permanently hold down the W key
                    if (msg == "drive" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                        ReleaseKeyPynput(S) #release brake key first
                        PressKeyPynput(W) #start permanently driving

                    # If message is "reverse", then permanently hold down the S key
                    if (msg == "reverse" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                        ReleaseKeyPynput(W) #release drive key first
                        PressKeyPynput(S) #start permanently reversing

                    # Release both the "drive" and "reverse" keys
                    if (msg == "stop" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                        ReleaseKeyPynput(W)
                        ReleaseKeyPynput(S)

                    # Press the spacebar for 0.7 seconds
                    if (msg == "brake" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                        PressAndHoldKey(SPACE, 0.7)

                    # Presses the left mouse button down for 1 second, then releases it
                    if (msg == "shoot" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                        mouse.press(Button.left)
                        time.sleep(1)
                        mouse.release(Button.left)

                    ###################################
                    # Example Miscellaneous Code
                    ###################################

                    # Clicks and drags the mouse upwards, using the Pyautogui commands.
                    # NOTE: unfortunately, Pyautogui does not work in DirectX games like GTA V. It will work in all other environments (e.g. on your desktop)
                    # If anyone finds a reliable way to move the mouse in DirectX games, please let me know!
                    if (msg == "drag mouse up" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                        pyautogui.drag(0, -50, 0.25, button='left')

                    # Clicks and drags the mouse downwards, using the Pyautogui commands
                    if (msg == "drag mouse down" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                        pyautogui.drag(0, 50, 0.25, button='left')

                    # An example of pressing 2 keys at once.
                    # First holds down the LEFT_CONTROL key, then presses the A key for 0.1 seconds, then releases the LEFT_CONTROL key.
                    if (msg == "select all" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                        PressKeyPynput(LEFT_CONTROL)
                        PressAndHoldKey(A, 0.1)
                        ReleaseKeyPynput(LEFT_CONTROL)

                    # Can use pyautogui.typewrite() to type messages from chat into the keyboard.
                    # Here, if a chat message says "type ...", it will type out their text.
                    if (msg.startswith("type ") or msg.startswith(secondaryCommandList[0])) and OnOrOff[10] == 1:
                        try:
                            typeMsg = msg[5:] # Ignore the "type " portion of the message
                            pyautogui.typewrite(typeMsg)
                        except:
                            # There was some issue typing the msg. Print it out, and move on.
                            print("Typing this particular message didn't work: " + msg)

                    ####################################
                    ####################################

            except:
                # There was some error trying to process this chat message. Simply move on to the next message.
                print('Encountered an exception while reading chat.')

    window.after(500, task)


window.after(500, task)
window.mainloop()
