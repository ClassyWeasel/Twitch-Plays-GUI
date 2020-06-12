# General imports
import time
import subprocess
import ctypes
import random
import string
import keyboard
import tkinter as tk

# Twitch imports
import TwitchPlays_Connection
from TwitchPlays_AccountInfo import TWITCH_USERNAME, TWITCH_OAUTH_TOKEN

# Controller imports
import pyautogui
import pynput
from pynput.mouse import Button, Controller

SendInput = ctypes.windll.user32.SendInput

# Found at: https://stackoverflow.com/questions/53643273/how-to-keep-pynput-and-ctypes-from-clashing
# Use these to prevent conflict errors with pynput
def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Holds down a key for the specified number of seconds
def PressAndHoldKey(hexKeyCode, seconds):
    PressKeyPynput(hexKeyCode)
    time.sleep(seconds)
    ReleaseKeyPynput(hexKeyCode)

########################################################
# DIRECTX KEY CODES
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
RIGHT_SHIFT = 0x36

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
#
########################################################

PATH_TO_AUTOHOTKEY = 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'
PATH_TO_MOVEMOUSELEFT_SCRIPT = 'C:\\Users\\Douglas Wreden\\Dropbox\\Livestream Assets\\Twitch Chat Plays\\Twitch Plays - Main\\MoveMouseLeft.ahk'
PATH_TO_MOVEMOUSERIGHT_SCRIPT = 'C:\\Users\\Douglas Wreden\\Dropbox\\Livestream Assets\\Twitch Chat Plays\\Twitch Plays - Main\\MoveMouseRight.ahk'
PATH_TO_MOVEMOUSEUP_SCRIPT = 'C:\\Users\\Douglas Wreden\\Dropbox\\Livestream Assets\\Twitch Chat Plays\\Twitch Plays - Main\\MoveMouseUp.ahk'
PATH_TO_MOVEMOUSEDOWN_SCRIPT = 'C:\\Users\\Douglas Wreden\\Dropbox\\Livestream Assets\\Twitch Chat Plays\\Twitch Plays - Main\\MoveMouseDown.ahk'

# Count down to 10 before starting, so you have time to load up the game
# countdown = 5
# while countdown > 0:
#     print(countdown)
#     countdown -= 1
#     time.sleep(1)

# Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
# Login credentials are stored in "account_credentials.py"
t = TwitchPlays_Connection.Twitch();
t.twitch_connect(TWITCH_USERNAME, TWITCH_OAUTH_TOKEN);

last_time = time.time()
mouse = Controller()
b_currentlyAiming = False
b_currentlyDriving = False
b_currentlyReversing = False
time_since_last_command = 0

##################### GAME VARIABLES #####################

THROTTLE_TIME = 0.4  #Set this to 0 for no throttle

SHORT_TURN_LENGTH = 0.1
MEDIUM_TURN_LENGTH = 0.3
LONG_TURN_LENGTH = 1

MP_LIGHT_HOLD_TIME = 0.1
MP_MEDIUM_HOLD_TIME = 0.4
MP_HARD_HOLD_TIME = 1

MELEE_LIGHT_HOLD_TIME = 0.05
MELEE_MEDIUM_HOLD_TIME = 0.1
MELEE_HARD_HOLD_TIME = 0.2

firstHalfAlphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
multiplayer = False # Keeps track of whether or not we want to use multiplayer

def isPlayer1(name):
    if multiplayer:
        return (name[0] in firstHalfAlphabet)
    return True
    #return False #use for testing player 2

##################### CONTROLLER INPUTS #####################

# SNES KEYS
# Note: arrow keys do not work for some reason on SNES, use other keys
SNES_P1_UP = V
SNES_P1_DOWN = B
SNES_P1_LEFT = N
SNES_P1_RIGHT = M
SNES_P1_A = X
SNES_P1_B = Z
SNES_P1_L = Q
SNES_P1_R = E
SNES_P1_X = C
SNES_P1_Y = R
SNES_P1_START = ENTER
SNES_P1_SELECT = RIGHT_SHIFT

SNES_P2_UP = I
SNES_P2_DOWN = K
SNES_P2_LEFT = J
SNES_P2_RIGHT = L
SNES_P2_A = G
SNES_P2_B = F
SNES_P2_L = O
SNES_P2_R = P
SNES_P2_X = T
SNES_P2_Y = H
SNES_P2_START = SEMICOLON

# N64 KEYS
N64_P1_UP = UP_ARROW
N64_P1_DOWN = DOWN_ARROW
N64_P1_LEFT = LEFT_ARROW
N64_P1_RIGHT = RIGHT_ARROW
N64_P1_A = X
N64_P1_B = Z
N64_P1_L = Q
N64_P1_R = E
N64_P1_Z = V
N64_P1_START = ENTER

N64_P2_UP = I
N64_P2_DOWN = K
N64_P2_LEFT = J
N64_P2_RIGHT = L
N64_P2_A = G
N64_P2_B = F
N64_P2_L = O
N64_P2_R = P
N64_P2_Z = Y
N64_P2_START = SEMICOLON

# GAMECUBE KEYS
GC_P1_UP = UP_ARROW
GC_P1_DOWN = DOWN_ARROW
GC_P1_LEFT = LEFT_ARROW
GC_P1_RIGHT = RIGHT_ARROW
GC_P1_A = X
GC_P1_B = Z
GC_P1_L = Q
GC_P1_R = E
GC_P1_X = C
GC_P1_Y = R
GC_P1_Z = V
GC_P1_START = ENTER

GC_P2_UP = I
GC_P2_DOWN = K
GC_P2_LEFT = J
GC_P2_RIGHT = L
GC_P2_A = G
GC_P2_B = F
GC_P2_L = O
GC_P2_R = P
GC_P2_X = T
GC_P2_Y = H
GC_P2_Z = Y
GC_P2_START = SEMICOLON

####################################################################################################################
########################################## CODE BY NATHAN KILCREASE ################################################
####################################################################################################################

# Keeps track of which game you want Twitch to play
currentGame = ""

# Array of commands and descriptions (List of each Twitch command for every game)

# GTAV
GTACommandList = ["Forward/Drive", "Back/Reverse", "Stop", "Jump", "Shoot/Left Click",
                            "Fire/Right Click", "Honk", "Camera", "Rear View", "Cinematic", "Light Left", "Left",
                            "Hard Left", "Light Right", "Right", "Hard Right", "Run", "Phone/Phone Up", "Phone Down",
                            "Phone Left", "Phone Right", "Backspace", "Enter", "Eject", "Vehicle Weapon/Moltov",
                            "Speed Boost", "Look Down/LD", "Look Up/LU", "Look Right/LR", "Look Left/LL"]
GTASecondaryCommandList = [""] * len(GTACommandList)
GTADescrip = ["WIP"] * len(GTACommandList)

# Smash 64
Smash64CommandList = ["Up", "Down", "Left", "Right", "Light Left", "Light Right", "Stop", "A", "B", "L", "R", "Z",
                      "Up Smash", "Down Smash", "Left Smash", "Right Smash"]
Smash64SecondaryCommandList = [""] * len(Smash64CommandList)
Smash64Descrip = ["WIP"] * len(Smash64CommandList)

# Mario Kart 64
MK64CommandList = ["Left", "Right", "Light Left", "Light Right", "Drive", "Brake", "Stop", "A", "B", "L", "R", "Z"]
MK64SecondaryCommandList = [""] * len(MK64CommandList)
MK64Descrip = ["WIP"] * len(MK64CommandList)

# Mario Bros/Tetris
TetrisMBCommandList = ["Left", "Right", "Light Left", "Light Right", "A", "B", "L", "R", "X", "Y"]
TetrisMBSecondaryCommandList = [""] * len(TetrisMBCommandList)
TetrisMBDescrip = ["WIP"] * len(TetrisMBCommandList)

# Internet
InternetCommandList = ["Mouse Up/MU", "Mouse Down/MD", "Mouse Right/MR", "Mouse Left/ML",
                        "Mouse Up Right/MUR", "Mouse Up Left/MUL", "Mouse Down Right/MDR", "Mouse Down Left/MDL",
                        "Draw Up/DU", "Draw Down/DD", "Draw Right/DR", "Draw Left/DL", "Draw Up Right/DUR",
                        "Draw Up Left/DUL", "Draw Down Right/DDR", "Draw Down Left/DDL", "North R", "South R",
                        "East R", "West R", "North East R", "North West R", "South East R", "South West R", "Click",
                        "Select All", "Zoom In", "Zoom Out", "Type ", "Please No Uncle D ", "Enter", "Escape"]
InternetSecondaryCommandList = [""] * len(InternetCommandList)
InternetDescrip = ["WIP"] * len(InternetCommandList)

# Mario 64
Mario64CommandList = ["Light Left", "Left", "Hard Left", "Light Right", "Right", "Hard Right", "Forward", "Light Back",
                      "Back", "Hard Back", "Hold Forward", "Hold Back", "Forward Jump", "Stop", "Jump", "Kick",
                      "Pound/Z", "Camera 1", "Camera 2", "Camera 3", "Camera 4"]
Mario64SecondaryCommandList = [""] * len(Mario64CommandList)
Mario64Descrip = ["WIP"] * len(Mario64CommandList)

# Mario Kart Double Dash
MKDDCommandList = ["Light Left", "Left", "Hard Left", "Light Right", "Right", "Hard Right", "Up", "Down", "Drive",
                   "Reverse", "Stop", "Swap", "Item"]
MKDDSecondaryCommandList = [""] * len(MKDDCommandList)
MKDDDescrip = ["WIP"] * len(MKDDCommandList)

# Mario Party 7
MP7CommandList = ["Light Left", "Left", "Hard Left", "Light Right", "Right", "Hard Right", "Light Up", "Up", "Hard Up",
                  "Light Down", "Down", "Hard Down", "A", "Hold A", "B", "X", "Y", "Z", "L", "R"]
MP7SecondaryCommandList = [""] * len(MP7CommandList)
MP7Descrip = ["WIP"] * len(MP7CommandList)

# Smash Bros Melee
SBMeleeCommandList = ["Light Left", "Left", "Hard Left", "Light Right", "Right", "Hard Right", "Up", "Down", "Stop",
                      "A/A button", "B/B button", "Jump", "Right Jump/Rump", "Left Jump/Lump", "Grab/Z", "Shield/L",
                      "R", "Left Smash/Lash", "Right Smash/Rash", "Up Smash/Uash", "Down Smash/Dash", "Left B",
                      "Right B", "Up B", "Down B", "Left Dash Attack/LDA", "Right Dash Attack/RDA"]
SBMeleeSecondaryCommandList = [""] * len(SBMeleeCommandList)
SBMeleeDescrip = ["WIP"] * len(SBMeleeCommandList)

# Minecraft
MinecraftCommandList = ["Forward", "Back", "Left", "Right", "Jump", "Left Click", "Right Click", "Inventory", "Run",
                        "Crouch"]
MinecraftSecondaryCommandList = [""] * len(MinecraftCommandList)
MinecraftDescrip = ["WIP"] * len(MinecraftCommandList)

# Outlast
OutlastCommandList = ["Forward", "Back", "Left", "Right", "Jump", "Use", "Camera", "Run", "Crouch", "Lean Left",
                      "Lean Right", "NightVision", "420"]
OutlastSecondaryCommandList = [""] * len(OutlastCommandList)
OutlastDescrip = ["WIP"] * len(OutlastCommandList)

# Super Mario World
SMWorldCommandList = ["Right", "Left", "Tap Right", "Stop", "Light Jump", "Crouch", "Spin Jump", "Jump", "Run"]
SMWorldSecondaryCommandList = [""] * len(SMWorldCommandList)
SMWorldDescrip = ["WIP"] * len(SMWorldCommandList)

# Team Fortress 2
TF2CommandList = ["Forward", "Back", "Left", "Right", "Stop", "Jump", "Crouch", "Shoot/Left Click/LC", "Right Click/RC",
                  "Weapon 1/1", "Weapon 2/2", "Weapon 3/3", "Weapon 4/4", "Taunt/420"]
TF2SecondaryCommandList = [""] * len(TF2CommandList)
TF2Descrip = ["WIP"] * len(TF2CommandList)

# SSX Tricky
SSXTCommandList = ["Light Left", "Left", "Light Right", "Right", "Forward", "Back", "Jump", "Boost", "Trick",
                   "ONLY FOR ONE PLAYER: Shove Left/SL", "ONLY FOR ONE PLAYER: Shove Right/SR"]
SSXTSecondaryCommandList = [""] * len(SSXTCommandList)
SSXTDescrip = ["WIP"] * len(SSXTCommandList)

# Spelunky
SpelunkyCommandList = ["Light Left", "Left", "Hard Left", "Light Right", "Right", "Hard Right", "Jump",
                       "Right Jump/Rump", "Left Jump/Lump", "Up", "Down", "Run", "Whip/Shoot", "Bomb", "Rope", "Door",
                       "Pick Up", "Stop"]
SpelunkySecondaryCommandList = [""] * len(SpelunkyCommandList)
SpelunkyDescrip = ["WIP"] * len(SpelunkyCommandList)

# Generic game
# NormalCommandList = ["Left", "Right", "Up", "Down", "Start", "Drag Mouse Up", "Drag Mouse Down", "Select All", "Type "]
# NormalSecondaryCommandList = [""] * (len(NormalCommandList)-1) + ["type "]
# NormalDescrip = ["If the chat message is 'left', then hold down the A key for 2 seconds", "If the chat message is 'right', then hold down the D key for 2 seconds",
#             "If message is 'up', then hold down the W key for 2 seconds", "If message is 'down', then hold down the S key for 2 seconds", "If message is 'start', then press Enter once", "Clicks and drags the mouse upwards",
#             "Clicks and drags the mouse downwards", "First holds down the LEFT_CONTROL key, then presses the A key for 0.1 seconds,\n then releases the LEFT_CONTROL key.",
#             "Here, if a chat message says 'type ...', it will type out their text."]




# List of games that this code supports
gameList = ["GTA", "Skyrim (does not work atm)", "Smash64", "MK64", "TetrisMB", "Internet", "Mario64", "MKDD", "MP7", "SBMelee", "Minecraft", "Outlast", "SMWorld", "TF2", "SSXT", "Spelunky"]

# Initial window for choosing your game
class chooseGame():

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(300, 100)
        self.root.title("Please choose a game")
        self.root.config(bg="gray28")

        # Global variables
        global gameList

        for i in range(0, len(gameList)):
            globals()['%sBtn' % gameList[i]] = tk.Button(self.root, text=gameList[i], bg='grey57', height=1, width=20, command=lambda num=i: self.press(num))
            globals()['%sBtn' % gameList[i]].pack() # grid(sticky='EW', column=0, row=i)

        self.root.mainloop()

    def press(self, num):
        global currentGame
        global gameList

        currentGame = gameList[num]
        self.root.destroy()


# Main GUI code
class App(tk.Tk):


    def __init__(self, master=None):

        # Setup self
        bgColor = "gray28"
        tk.Tk.__init__(self)
        self.minsize(500, 200)
        self.title("Twitch Plays")
        self.config(bg=bgColor)

        #Global variables
        global commandList
        global secondaryCommandList
        global OnOrOff
        global descrip

        # Creating all our rows of commands (buttons, entry boxes, label, etc.)
        for i in range(0, len(commandList)):
            globals()['Label %s' % i] = tk.Label(self, text=f"{commandList[i]}", fg='SeaGreen1', bg='dark green', font=20)
            globals()['Label %s' % i].grid(sticky="WE", column=0, row=i+1, columnspan=1)
            globals()['Label2 %s' % i] = tk.Label(self, text=f"              ", fg='coral1', bg=bgColor, font=20)
            globals()['Label2 %s' % i].grid(sticky="W", column=3, row=i + 1)
            globals()['ActBtn %s' % i] = tk.Button(self, text="Deactivate", bg='grey57', command=lambda commandNum=i: self.activate(commandNum))
            globals()['ActBtn %s' % i].grid(sticky="W", column=4, row=i + 1)
            globals()['Descr %s' % i] = tk.Button(self, text="Description", bg='sea green', command=lambda commandNum=i: self.pop_up(commandList[commandNum], descrip[commandNum]))
            globals()['Descr %s' % i].grid(sticky="W", column=5, row=i + 1)
            globals()['name %s' % i] = tk.StringVar()
            globals()['name %s' % i].set(commandList[i])
            globals()['txtBox %s' % i] = tk.Entry(self, width=25, bg='LightSkyBlue1', textvariable=globals()['name %s' % i])
            globals()['txtBox %s' % i].grid(column=2, row=i + 1)
            globals()['ChaBtn %s' % i] = tk.Button(self, text="Change name", bg='SkyBlue1', command=lambda command=i: self.changeName(command))
            globals()['ChaBtn %s' % i].grid(sticky="E", column=1, row=i + 1)

        # Pause button:
        self.pause_btn = tk.Button(self, text="Click Here to Start Twitch Plays!", bg='ivory2', font=('Helvetica', 13, 'bold'), command=self.pause)
        self.pause_btn.grid(sticky='NSEW', column=0, row=0, columnspan=6)

    # Function that changes the Twitch chat name of a command (i.e. changes 'drive' to 'forward' or what have you)
    def changeName(self, commandNum):
        secondaryCommandList[commandNum] = globals()['name %s' % commandNum].get().lower()
        globals()['Label %s' % commandNum].config(text=f"{commandList[commandNum]} (or {globals()['name %s' % commandNum].get()})")


    # Function that turns a given key on or off when the corresponding button is pressed (Green means on, Red means off)
    def activate(self, commandNum):
        if OnOrOff[commandNum] == 0:
            OnOrOff[commandNum] = 1
            globals()['Label %s' % commandNum].config(fg='SeaGreen1', bg='dark green')
            globals()['ActBtn %s' % commandNum].config(text='Deactivate')
        else:
            OnOrOff[commandNum] = 0
            globals()['Label %s' % commandNum].config(fg='gray84', bg='OrangeRed2')
            globals()['ActBtn %s' % commandNum].config(text='Activate')


    # Function that pauses Twitch Plays
    def pause(self, event=None):
        global TwitchActive
        if TwitchActive == True:
            TwitchActive = False
            self.pause_btn.config(text="Click Here to Start Twitch Plays!")
        else:
            self.countdown(5)
            TwitchActive = True
            self.pause_btn.config(text="Click Here to Pause Twitch Plays")


    # Pop up self when clicking on the description of each Twitch command
    def pop_up(self, title, message):
        root = tk.Tk()
        root.title(title)
        root.minsize(200, 110)
        w = tk.Label(root, text=message, width=0, height=4)
        w.pack()
        b = tk.Button(root, text="OK", command=root.destroy, width=10)
        b.pack()
        root.geometry('+%d+%d' % (self.winfo_x(), self.winfo_y()))
        root.mainloop()


    def countdown(self, count):
        while count > 0:
            self.title(f"Twitch Plays will start in {count}")
            time.sleep(1)
            count -= 1
        self.title("Twitch Plays")


##########################################################
##########################################################

gameWindow = chooseGame()
print(currentGame)

commandList = globals()['%sCommandList' % currentGame]
secondaryCommandList = globals()['%sSecondaryCommandList' % currentGame]
descrip = globals()['%sDescrip' % currentGame]

# Array of values which keep track of which commands are turned on or off in chat
OnOrOff = [1] * len(commandList)
# Keeps track of whether or not we have paused Twitch Plays
TwitchActive = False

window = App()

def task():
    global TwitchActive
    global secondaryCommandList

    if TwitchActive:
    
        # If user presses Shift+Backspace, automatically end the program
        if keyboard.is_pressed('shift+backspace'):
            exit()

        #Check for new mesasages
        new_messages = t.twitch_recieve_messages();

        if not new_messages:
            msg = ""
        else:
            try:
                for message in new_messages:
                    # We got a message. Let's extract some details from it
                    msg = message['message'].lower()
                    username = message['username'].lower()
                    #print(username + ": " + msg);

                    # Throttling. Check if enough time has passed since the last executed command
                    # time_since_last_command = time.time() - last_time
                    # if (time_since_last_command > THROTTLE_TIME):
                    #     # Enough time has passed. Execute the command, and reset timer
                    #     last_time = time.time()
                    # else:
                    #     continue


                    ########################################################################
                    # GTA 5 BLOCK
                    ########################################################################

                    if currentGame == gameList[0]:

                        if isPlayer1(username):

                            if (msg == "drive" or msg == "forward" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                ReleaseKeyPynput(S) #release brake command first
                                PressKeyPynput(W) #start permanently driving

                            if (msg == "reverse" or msg == "back" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                ReleaseKeyPynput(W) #release brake command first
                                PressKeyPynput(S)

                            if (msg == "stop" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                ReleaseKeyPynput(W)
                                ReleaseKeyPynput(S)

                            if (msg == "jump" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(SPACE, 0.7)

                            if (msg == "shoot" or msg == "left click" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                mouse.press(Button.left)
                                time.sleep(1)
                                mouse.release(Button.left)

                            if (msg == "fire" or msg == "right click" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                mouse.press(Button.right)
                                time.sleep(1)
                                mouse.release(Button.right)
                                # If we're not aiming, press aim key. If we're already aiming, release aim key
                                # if not b_currentlyAiming:
                                #     mouse.press(Button.right)
                                # else:
                                #     mouse.release(Button.right)
                                # b_currentlyAiming = not b_currentlyAiming

                            if (msg == "honk" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(E, 0.5)

                            if (msg == "camera" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(V, 0.1)

                            if (msg == "rear view" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                PressAndHoldKey(C, 1)

                            if (msg == "cinematic" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(R, 0.1)

                            ####### TURNING ########
                            if (msg == "light left" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(A, SHORT_TURN_LENGTH)

                            if (msg == "left" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(A, MEDIUM_TURN_LENGTH)

                            if (msg == "hard left" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressAndHoldKey(A, LONG_TURN_LENGTH)

                            if (msg == "light right" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                                PressAndHoldKey(D, SHORT_TURN_LENGTH)

                            if (msg == "right" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                                PressAndHoldKey(D, MEDIUM_TURN_LENGTH)

                            if (msg == "hard right" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                                PressAndHoldKey(D, LONG_TURN_LENGTH)

                            ## EXTRAS ##

                            if (msg == "run" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                                PressAndHoldKey(LEFT_SHIFT, 3)

                            if (msg == "phone" or msg == "phone up" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                                PressAndHoldKey(UP_ARROW, 0.2)

                            if (msg == "phone down" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                                PressAndHoldKey(DOWN_ARROW, 0.2)

                            if (msg == "phone left" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                                PressAndHoldKey(LEFT_ARROW, 0.2)

                            if (msg == "phone right" or msg == secondaryCommandList[20]) and OnOrOff[20] == 1:
                                PressAndHoldKey(RIGHT_ARROW, 0.2)

                            if (msg == "backspace" or msg == secondaryCommandList[21]) and OnOrOff[21] == 1:
                                PressAndHoldKey(BACKSPACE, 0.2)

                            if (msg == "enter" or msg == secondaryCommandList[22]) and OnOrOff[22] == 1:
                                PressAndHoldKey(ENTER, 0.2)

                            if (msg == 'eject' or msg == "420" or msg == secondaryCommandList[23]) and OnOrOff[23] == 1:
                                if (random.randint(1,1000) == 42):
                                    ReleaseKeyPynput(W)
                                    ReleaseKeyPynput(S)
                                    PressAndHoldKey(F, 1)
                                    time.sleep(6)
                                    print(username + " DID IT, OH MY GOSH!!!!!")

                            if (msg == "vehicle weapon" or msg == "molotov" or msg == secondaryCommandList[24]) and OnOrOff[24] == 1:
                                PressAndHoldKey(NUMPAD_PLUS, 0.7)

                            if (msg == "speed boost" or msg == secondaryCommandList[25]) and OnOrOff[25] == 1:
                                PressAndHoldKey(NUMPAD_9, 0.75)

                            if (msg == "look down" or msg == "ld" or msg == secondaryCommandList[26]) and OnOrOff[26] == 1:
                                PressAndHoldKey(NUMPAD_8, 2)

                            if (msg == "look up" or msg == "lu" or msg == secondaryCommandList[27]) and OnOrOff[27] == 1:
                                PressAndHoldKey(NUMPAD_5, 2)

                            if (msg == "look right" or msg == "lr" or msg == secondaryCommandList[28]) and OnOrOff[28] == 1:
                                PressAndHoldKey(NUMPAD_6, 0.5)

                            if (msg == "look left" or msg == "ll" or msg == secondaryCommandList[29]) and OnOrOff[29] == 1:
                                PressAndHoldKey(NUMPAD_4, 0.5)

                    ####################################
                    ####################################


                    ########################################################################
                    # SKYRIM BLOCK
                    ########################################################################
                    # if currentGame == gameList[1]:
                        # if msg == "forward":
                        #     ReleaseKeyPynput(S)
                        #     PressAndHoldKey(W, 2)

                        # if msg == "back":
                        #     ReleaseKeyPynput(W)
                        #     PressAndHoldKey(S, 0.5)

                        # if msg == "left":
                        #     PressAndHoldKey(A, 0.5)

                        # if msg == "right":
                        #     PressAndHoldKey(D, 0.5)

                        # if msg == "stop":
                        #     ReleaseKeyPynput(W)
                        #     ReleaseKeyPynput(S)
                        #     ReleaseKeyPynput(A)
                        #     ReleaseKeyPynput(D)

                        # if msg == "jump":
                        #     PressAndHoldKey(SPACE, 0.7)

                        # if msg == "heal left" or msg == "left click":
                        #     mouse.press(Button.left)
                        #     time.sleep(2)
                        #     mouse.release(Button.left)

                        # if msg == "heal right" or msg == "right click":
                        #     mouse.press(Button.right)
                        #     time.sleep(2)
                        #     mouse.release(Button.right)

                        # if msg == "molotov" or msg == "honk":
                        #     PressAndHoldKey(Z, 1)

                        # if msg == "door":
                        #     PressAndHoldKey(E, 0.1)

                        # if msg == "camera":
                        #     PressAndHoldKey(F, 0.1)

                        # if msg == "walk":
                        #     PressAndHoldKey(CAPS, 0.1)

                        # if msg == "sprint":
                        #     PressAndHoldKey(LEFT_ALT, 1)

                        # if msg == "crouch":
                        #     PressAndHoldKey(LEFT_CONTROL, 1)

                        # if msg == "look left":
                        #     # if (random.randint(1,5) == 4):
                        #     subprocess.call([PATH_TO_AUTOHOTKEY, PATH_TO_MOVEMOUSELEFT_SCRIPT])

                        # if msg == "look right":
                        #     # if (random.randint(1,5) == 4):
                        #     subprocess.call([PATH_TO_AUTOHOTKEY, PATH_TO_MOVEMOUSERIGHT_SCRIPT])

                        # if msg == "look up":
                        #     subprocess.call([PATH_TO_AUTOHOTKEY, PATH_TO_MOVEMOUSEUP_SCRIPT])

                        # if msg == "look down":
                        #     subprocess.call([PATH_TO_AUTOHOTKEY, PATH_TO_MOVEMOUSEDOWN_SCRIPT])

                    ####################################
                    ####################################


                    #####################################################################
                    # Smash 64 Block
                    ########################################################################
                    if currentGame == gameList[2]:

                        if (msg == "up" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_UP, 0.3)
                            else:
                                PressAndHoldKey(N64_P2_UP, 0.3)

                        if (msg == "down" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_DOWN, 0.3)
                            else:
                                PressAndHoldKey(N64_P2_DOWN, 0.3)

                        if (msg == "left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_LEFT, 0.3)
                            else:
                                PressAndHoldKey(N64_P2_LEFT, 0.3)

                        if (msg == "right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_RIGHT, 0.3)
                            else:
                                PressAndHoldKey(N64_P2_RIGHT, 0.3)

                        if (msg == "light left" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_LEFT, 0.1)
                            else:
                                PressAndHoldKey(N64_P2_LEFT, 0.1)

                        if (msg == "light right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_RIGHT, 0.1)
                            else:
                                PressAndHoldKey(N64_P2_RIGHT, 0.1)

                        if (msg == "stop" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            if isPlayer1(username):
                                ReleaseKeyPynput(N64_P1_UP)
                                ReleaseKeyPynput(N64_P1_DOWN)
                                ReleaseKeyPynput(N64_P1_LEFT)
                                ReleaseKeyPynput(N64_P1_RIGHT)
                            else:
                                ReleaseKeyPynput(N64_P2_UP)
                                ReleaseKeyPynput(N64_P2_DOWN)
                                ReleaseKeyPynput(N64_P2_LEFT)
                                ReleaseKeyPynput(N64_P2_RIGHT)

                        if (msg == "a" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_A, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_A, 0.2)

                        if (msg == "b" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_B, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_B, 0.2)

                        if (msg == "l" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_L, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_L, 0.2)

                        if (msg == "r" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_R, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_R, 0.2)

                        if (msg == "z" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_Z, 0.5)
                            else:
                                PressAndHoldKey(N64_P2_Z, 0.5)

                        if (msg == "up smash" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                            if isPlayer1(username):
                                PressKeyPynput(N64_P1_UP)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P1_A, 0.3)
                                ReleaseKeyPynput(N64_P1_UP)
                            else:
                                PressKeyPynput(N64_P2_UP)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P2_A, 0.3)
                                ReleaseKeyPynput(N64_P2_UP)

                        if (msg == "down smash" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                            if isPlayer1(username):
                                PressKeyPynput(N64_P1_DOWN)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P1_A, 0.3)
                                ReleaseKeyPynput(N64_P1_DOWN)
                            else:
                                PressKeyPynput(N64_P2_DOWN)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P2_A, 0.3)
                                ReleaseKeyPynput(N64_P2_DOWN)

                        if (msg == "left smash" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                            if isPlayer1(username):
                                PressKeyPynput(N64_P1_LEFT)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P1_A, 0.3)
                                ReleaseKeyPynput(N64_P1_LEFT)
                            else:
                                PressKeyPynput(N64_P2_LEFT)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P2_A, 0.3)
                                ReleaseKeyPynput(N64_P2_LEFT)

                        if (msg == "right smash" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                            if isPlayer1(username):
                                PressKeyPynput(N64_P1_RIGHT)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P1_A, 0.3)
                                ReleaseKeyPynput(N64_P1_RIGHT)
                            else:
                                PressKeyPynput(N64_P2_RIGHT)
                                time.sleep(0.05)
                                PressAndHoldKey(N64_P2_A, 0.3)
                                ReleaseKeyPynput(N64_P2_RIGHT)



                    #####################################################################
                    # Mario Kart 64 Block
                    ########################################################################

                    if currentGame == gameList[3]:

                        if (msg == "left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_LEFT, 0.5)
                            else:
                                PressAndHoldKey(N64_P2_LEFT, 0.5)

                        if (msg == "right" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_RIGHT, 0.5)
                            else:
                                PressAndHoldKey(N64_P2_RIGHT, 0.5)

                        if (msg == "light left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_LEFT, 0.3)
                            else:
                                PressAndHoldKey(N64_P2_LEFT, 0.3)

                        if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_RIGHT, 0.3)
                            else:
                                PressAndHoldKey(N64_P2_RIGHT, 0.3)

                        if (msg == "drive" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            if isPlayer1(username):
                                ReleaseKeyPynput(N64_P1_B)
                                PressKeyPynput(N64_P1_A)
                            else:
                                ReleaseKeyPynput(N64_P2_B)
                                PressKeyPynput(N64_P2_A)

                        if (msg == "brake" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            if isPlayer1(username):
                                ReleaseKeyPynput(N64_P1_A)
                                PressKeyPynput(N64_P1_B)
                                PressAndHoldKey(N64_P1_DOWN, 1)
                            else:
                                ReleaseKeyPynput(N64_P2_A)
                                PressKeyPynput(N64_P2_B)
                                PressAndHoldKey(N64_P2_DOWN, 1)

                        if (msg == "stop" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            if isPlayer1(username):
                                ReleaseKeyPynput(N64_P1_A)
                                ReleaseKeyPynput(N64_P1_B)
                            else:
                                ReleaseKeyPynput(N64_P2_A)
                                ReleaseKeyPynput(N64_P2_B)

                        if (msg == "a" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_A, 1)
                            else:
                                PressAndHoldKey(N64_P2_A, 1)

                        if (msg == "b" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_B, 1)
                            else:
                                PressAndHoldKey(N64_P2_B, 1)

                        if (msg == "l" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_L, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_L, 0.2)

                        if (msg == "r" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_R, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_R, 0.2)

                        if (msg == "z" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(N64_P1_Z, 0.2)
                            else:
                                PressAndHoldKey(N64_P2_Z, 0.2)


                    #####################################################################
                    # Mario Bros / Tetris
                    ########################################################################
                    if currentGame == gameList[4]:

                        if (msg == "left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_LEFT, 0.4)
                            else:
                                PressAndHoldKey(SNES_P2_LEFT, 0.4)

                        if (msg == "right" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_RIGHT, 0.4)
                            else:
                                PressAndHoldKey(SNES_P2_RIGHT, 0.4)

                        if (msg == "light left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_LEFT, 0.1)
                            else:
                                PressAndHoldKey(SNES_P2_LEFT, 0.1)

                        if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_RIGHT, 0.1)
                            else:
                                PressAndHoldKey(SNES_P2_RIGHT, 0.1)

                        if (msg == "a" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_A, 0.2)
                            else:
                                PressAndHoldKey(SNES_P2_A, 0.2)

                        if (msg == "b" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_B, 0.2)
                            else:
                                PressAndHoldKey(SNES_P2_B, 0.2)

                        if (msg == "l" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_L, 0.2)
                            else:
                                PressAndHoldKey(SNES_P2_L, 0.2)

                        if (msg == "r" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_R, 0.2)
                            else:
                                PressAndHoldKey(SNES_P2_R, 0.2)

                        if (msg == "x" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_X, 0.2)
                            else:
                                PressAndHoldKey(SNES_P2_X, 0.2)

                        if (msg == "y" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            if isPlayer1(username):
                                PressAndHoldKey(SNES_P1_X, 0.2)
                            else:
                                PressAndHoldKey(SNES_P2_X, 0.2)


                    ########################################################################
                    # INTERNET BLOCK
                    ########################################################################

                    if currentGame == gameList[5]:

                        moveDistance = 20
                        negMoveDistance = -20

                        if (msg == "mouse up" or msg == "mu" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            pyautogui.drag(0, negMoveDistance)
                        if (msg == "mouse down" or msg == "md" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            pyautogui.drag(0, moveDistance)
                        if (msg == "mouse right" or msg == "mr" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            pyautogui.drag(moveDistance, 0)
                        if (msg == "mouse left" or msg == "ml" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            pyautogui.drag(negMoveDistance, 0)
                        if (msg == "mouse up right" or msg == "mur" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            pyautogui.drag(moveDistance, negMoveDistance)
                        if (msg == "mouse up left" or msg == "mul" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            pyautogui.drag(negMoveDistance, negMoveDistance)
                        if (msg == "mouse down right" or msg == "mdr" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            pyautogui.drag(moveDistance, moveDistance)
                        if (msg == "mouse down left" or msg == "mdl" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            pyautogui.drag(negMoveDistance, moveDistance)

                        if (msg == "draw up" or msg == "du" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            pyautogui.drag(0, negMoveDistance, 0.25, button='left')

                        if (msg == "draw down" or msg == "dd" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            pyautogui.drag(0, moveDistance, 0.25, button='left')

                        if (msg == "draw right" or msg == "dr" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                            pyautogui.drag(moveDistance, 0, 0.25, button='left')

                        if (msg == "draw left" or msg == "dl" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                            pyautogui.drag(negMoveDistance, 0, 0.25, button='left')

                        if (msg == "draw up right" or msg == "dur" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                            pyautogui.drag(moveDistance, negMoveDistance, 0.25, button='left')

                        if (msg == "draw up left" or msg == "dul" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                            pyautogui.drag(negMoveDistance, negMoveDistance, 0.25, button='left')

                        if (msg == "draw down right" or msg == "ddr" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                            pyautogui.drag(moveDistance, moveDistance, 0.25, button='left')

                        if (msg == "draw down left" or msg == "ddl" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                            pyautogui.drag(negMoveDistance, moveDistance, 0.25, button='left')

                        # RIGHT CLICKING
                        if (msg == "north r" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                            pyautogui.drag(0, -50, 0.25, button='right')
                        if (msg == "south r" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                            pyautogui.drag(0, 50, 0.25, button='right')
                        if (msg == "east r" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                            pyautogui.drag(50, 0, 0.25, button='right')
                        if (msg == "west r" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                            pyautogui.drag(-50, 0, 0.25, button='right')
                        if (msg == "north east r" or msg == secondaryCommandList[20]) and OnOrOff[20] == 1:
                            pyautogui.drag(50, -50, 0.25, button='right')
                        if (msg == "north west r" or msg == secondaryCommandList[21]) and OnOrOff[21] == 1:
                            pyautogui.drag(-50, -50, 0.25, button='right')
                        if (msg == "south east r" or msg == secondaryCommandList[22]) and OnOrOff[22] == 1:
                            pyautogui.drag(50, 50, 0.25, button='right')
                        if (msg == "south west r" or msg == secondaryCommandList[23]) and OnOrOff[23] == 1:
                            pyautogui.drag(-50, 50, 0.25, button='right')

                        if (msg == "click" or msg == secondaryCommandList[24]) and OnOrOff[24] == 1:
                            pyautogui.click()

                        if (msg == "select all" or msg == secondaryCommandList[25]) and OnOrOff[25] == 1:
                            PressKeyPynput(LEFT_CONTROL)
                            PressAndHoldKey(A, 0.1)
                            ReleaseKeyPynput(LEFT_CONTROL)

                        if (msg == "zoom in" or msg == secondaryCommandList[26]) and OnOrOff[26] == 1:
                            for x in range(0,1):
                                PressKeyPynput(LEFT_CONTROL)
                                PressAndHoldKey(NUMPAD_PLUS, 0.1)
                                ReleaseKeyPynput(LEFT_CONTROL)

                        if (msg == "zoom out" or msg == secondaryCommandList[27]) and OnOrOff[27] == 1:
                            for x in range(0,1):
                                PressKeyPynput(LEFT_CONTROL)
                                PressAndHoldKey(NUMPAD_MINUS, 0.1)
                                ReleaseKeyPynput(LEFT_CONTROL)

                        # if username[0] in firstHalfAlphabet: #(random.randint(1,300) == 42):
                        #     firstLetter = msg[0]
                        #     pyautogui.typewrite(firstLetter)

                        if (msg.startswith("type ") or msg.startswith(secondaryCommandList[28])) and OnOrOff[28] == 1:
                            if (random.randint(1,200) == 42):
                                try:
                                    typeMsg = msg[5:]
                                    pyautogui.typewrite(typeMsg + " ")
                                    #typeMsg = typeMsg.replace('g', '')
                                except:
                                    print("this message didn't work: " + msg)

                        if (msg.startswith("pls no uncle d ") or msg.startswith(secondaryCommandList[29])) and OnOrOff[29] == 1:
                            if (random.randint(1,100) == 42):
                                try:
                                    typeMsg = msg[15:]
                                    pyautogui.typewrite(typeMsg + " ")
                                    #typeMsg = typeMsg.replace('g', '')
                                except:
                                    print("this message didn't work: " + msg)

                        if (msg == "enter" or msg == secondaryCommandList[30]) and OnOrOff[30] == 1:
                            PressAndHoldKey(ENTER, 0.1)

                        if (msg == "escape" or msg == secondaryCommandList[31]) and OnOrOff[31] == 1:
                            PressAndHoldKey(ESC, 0.1)

                    ####################################
                    ####################################


                    ########################################################################
                    # MARIO 64 BLOCK
                    ########################################################################
                    if currentGame == gameList[6]:

                        if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            PressAndHoldKey(LEFT_ARROW, 0.1)

                        if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            PressAndHoldKey(LEFT_ARROW, 0.3)

                        if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            PressAndHoldKey(LEFT_ARROW, 0.5)

                        if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            PressAndHoldKey(RIGHT_ARROW, 0.1)

                        if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            PressAndHoldKey(RIGHT_ARROW, 0.2)

                        if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            PressAndHoldKey(RIGHT_ARROW, 0.5)

                        if (msg == "forward" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            ReleaseKeyPynput(DOWN_ARROW)
                            PressAndHoldKey(UP_ARROW, 0.3)

                        if (msg == "light back" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            ReleaseKeyPynput(UP_ARROW)
                            PressAndHoldKey(DOWN_ARROW, 0.25)

                        if (msg == "back" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            ReleaseKeyPynput(UP_ARROW)
                            PressAndHoldKey(DOWN_ARROW, 0.4)

                        if (msg == "hard back" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            ReleaseKeyPynput(UP_ARROW)
                            PressAndHoldKey(DOWN_ARROW, 0.75)

                        if (msg == "hold forward" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                            ReleaseKeyPynput(DOWN_ARROW)
                            PressKeyPynput(UP_ARROW)

                        if (msg == "hold back" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                            ReleaseKeyPynput(UP_ARROW)
                            PressKeyPynput(DOWN_ARROW)

                        if (msg == "forward jump" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                            ReleaseKeyPynput(DOWN_ARROW)
                            PressAndHoldKey(X, 0.3)
                            PressKeyPynput(UP_ARROW)

                        if (msg == "stop" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                            ReleaseKeyPynput(UP_ARROW)
                            ReleaseKeyPynput(DOWN_ARROW)

                        if (msg == "jump" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                            PressAndHoldKey(X, 0.5)

                        if (msg == "kick" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                            PressAndHoldKey(Z, 0.1)

                        if (msg == "z" or msg == "pound" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                            PressAndHoldKey(V, 0.3)

                        if (msg == "camera 1" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                            PressAndHoldKey(W, 0.1)

                        if (msg == "camera 2" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                            PressAndHoldKey(A, 0.1)

                        if (msg == "camera 3" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                            PressAndHoldKey(S, 0.1)

                        if (msg == "camera 4" or msg == secondaryCommandList[20]) and OnOrOff[20] == 1:
                            PressAndHoldKey(D, 0.1)

                    ####################################
                    ####################################


                    ########################################################################
                    # MARIO KART DOUBLE DASH BLOCK
                    ########################################################################
                    if currentGame == gameList[7]:

                        if username[0] in firstHalfAlphabet:

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P1_LEFT, 0.1)

                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P1_LEFT, 0.3)

                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P1_LEFT, 0.7)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, 0.1)

                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, 0.3)

                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, 0.7)

                            if (msg == "up" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P1_UP, 0.1)
                            if (msg == "down" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P1_DOWN, 0.1)

                            if (msg == "drive" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                ReleaseKeyPynput(GC_P1_B)
                                PressKeyPynput(GC_P1_A)

                            if (msg == "reverse" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                ReleaseKeyPynput(GC_P1_A)
                                PressKeyPynput(GC_P1_B)

                            if (msg == "stop" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                ReleaseKeyPynput(GC_P1_A)
                                ReleaseKeyPynput(GC_P1_B)

                            if (msg == "swap" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                # PressKeyPynput(Y) # Optional: swap player 2 as well (used for 2-player 1-kart mode)
                                PressAndHoldKey(GC_P1_Z, 0.1)
                                # ReleaseKeyPynput(Y) # Now release player 2's swap key

                            if (msg == "item" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressAndHoldKey(GC_P1_X, 0.1)

                        else:

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P2_LEFT, 0.1)

                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P2_LEFT, 0.3)

                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P2_LEFT, 0.7)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, 0.1)

                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, 0.3)

                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, 0.7)

                            if (msg == "up" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P2_UP, 0.1)
                            if (msg == "down" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P2_DOWN, 0.1)

                            if (msg == "drive" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                ReleaseKeyPynput(GC_P2_B)
                                PressKeyPynput(GC_P2_A)

                            if (msg == "reverse" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                ReleaseKeyPynput(GC_P2_A)
                                PressKeyPynput(GC_P2_B)

                            if (msg == "stop" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                ReleaseKeyPynput(GC_P2_A)
                                ReleaseKeyPynput(GC_P2_B)

                            if (msg == "swap" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(GC_P2_Z, 0.1)

                            if (msg == "item" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressAndHoldKey(GC_P2_X, 0.1)

                    ####################################
                    ####################################



                    ########################################################################
                    # MARIO PARTY 7 BLOCK
                    ########################################################################
                    if currentGame == gameList[8]:

                        if username[0] in firstHalfAlphabet:

                            ##########################
                            ######## PLAYER 1 ########

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P1_LEFT, MP_LIGHT_HOLD_TIME)
                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P1_LEFT, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P1_LEFT, MP_HARD_HOLD_TIME)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, MP_LIGHT_HOLD_TIME)
                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, MP_HARD_HOLD_TIME)

                            if (msg == "light up" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P1_UP, MP_LIGHT_HOLD_TIME)
                            if (msg == "up" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P1_UP, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard up" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                PressAndHoldKey(GC_P1_UP, MP_HARD_HOLD_TIME)

                            if (msg == "light down" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(GC_P1_DOWN, MP_LIGHT_HOLD_TIME)
                            if (msg == "down" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(GC_P1_DOWN, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard down" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(GC_P1_DOWN, MP_HARD_HOLD_TIME)

                            if (msg == "a" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressAndHoldKey(GC_P1_A, 0.3)
                            if (msg == "hold a" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                                PressAndHoldKey(GC_P1_A, 3)

                            if (msg == "b" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                                PressAndHoldKey(GC_P1_B, 0.1)
                            if (msg == "x" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                                PressAndHoldKey(GC_P1_X, 0.1)
                            if (msg == "y" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                                PressAndHoldKey(GC_P1_Y, 0.1)
                            if (msg == "z" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                                PressAndHoldKey(GC_P1_Z, 0.1)
                            if (msg == "l" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                                PressAndHoldKey(GC_P1_L, 0.1)
                            if (msg == "r" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                                PressAndHoldKey(GC_P1_R, 0.1)

                        else:

                            ##########################
                            ######## PLAYER 2 ########

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P2_LEFT, MP_LIGHT_HOLD_TIME)
                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P2_LEFT, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P2_LEFT, MP_HARD_HOLD_TIME)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, MP_LIGHT_HOLD_TIME)
                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, MP_HARD_HOLD_TIME)

                            if (msg == "light up" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P2_UP, MP_LIGHT_HOLD_TIME)
                            if (msg == "up" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P2_UP, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard up" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                PressAndHoldKey(GC_P2_UP, MP_HARD_HOLD_TIME)

                            if (msg == "light down" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(GC_P2_DOWN, MP_LIGHT_HOLD_TIME)
                            if (msg == "down" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(GC_P2_DOWN, MP_MEDIUM_HOLD_TIME)
                            if (msg == "hard down" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(GC_P2_DOWN, MP_HARD_HOLD_TIME)

                            if (msg == "a" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressAndHoldKey(GC_P2_A, 0.3)
                            if (msg == "hold a" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                                PressAndHoldKey(GC_P2_A, 3)

                            if (msg == "b" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                                PressAndHoldKey(GC_P2_B, 0.1)
                            if (msg == "x" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                                PressAndHoldKey(GC_P2_X, 0.1)
                            if (msg == "y" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                                PressAndHoldKey(GC_P2_Y, 0.1)
                            if (msg == "z" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                                PressAndHoldKey(GC_P2_Z, 0.1)
                            if (msg == "l" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                                PressAndHoldKey(GC_P2_L, 0.1)
                            if (msg == "r" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                                PressAndHoldKey(GC_P2_R, 0.1)


                    ####################################
                    ####################################




                    ########################################################################
                    # SMASH BROS MELEE BLOCK
                    ########################################################################

                    if currentGame == gameList[9]:

                        if username[0] in firstHalfAlphabet:

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P1_LEFT, MELEE_LIGHT_HOLD_TIME)
                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P1_LEFT, MELEE_MEDIUM_HOLD_TIME)
                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P1_LEFT, MELEE_HARD_HOLD_TIME)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, MELEE_LIGHT_HOLD_TIME)
                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, MELEE_MEDIUM_HOLD_TIME)
                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, MELEE_HARD_HOLD_TIME)

                            if (msg == "up" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P1_UP, 0.1)
                            if (msg == "down" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P1_DOWN, 0.1)

                            if (msg == "stop" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                ReleaseKeyPynput(GC_P1_RIGHT)
                                ReleaseKeyPynput(GC_P1_LEFT)
                                ReleaseKeyPynput(GC_P1_UP)
                                ReleaseKeyPynput(GC_P1_DOWN)

                            if (msg == "a" or msg == "a button" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(GC_P1_A, 0.1)
                            if (msg == "b" or msg == "b button" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(GC_P1_B, 0.1)

                            if (msg == "jump" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(GC_P1_X, 0.3)

                            if (msg == "rump" or msg == "right jump" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressKeyPynput(GC_P1_RIGHT)
                                PressAndHoldKey(GC_P1_X, 0.3)
                                ReleaseKeyPynput(GC_P1_RIGHT)

                            if (msg == "lump" or msg == "left jump" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                                PressKeyPynput(GC_P1_LEFT)
                                PressAndHoldKey(GC_P1_X, 0.3)
                                ReleaseKeyPynput(GC_P1_LEFT)

                            if (msg == "z" or msg == "grab" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                                PressAndHoldKey(GC_P1_Z, 0.1)
                            if (msg == "l" or msg == "shield" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                                PressAndHoldKey(GC_P1_L, 0.5)
                            if (msg == "r" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                                PressAndHoldKey(GC_P1_R, 0.5)

                            if (msg == "left smash" or msg == "lash" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                                PressKeyPynput(GC_P1_LEFT)
                                PressAndHoldKey(GC_P1_A, 0.2)
                                ReleaseKeyPynput(GC_P1_LEFT)

                            if (msg == "right smash" or msg == "rash" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                                PressKeyPynput(GC_P1_RIGHT)
                                PressAndHoldKey(GC_P1_A, 0.2)
                                ReleaseKeyPynput(GC_P1_RIGHT)

                            if (msg == "up smash" or msg == "uash" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                                PressKeyPynput(GC_P1_UP)
                                PressAndHoldKey(GC_P1_A, 0.2)
                                ReleaseKeyPynput(GC_P1_UP)

                            if (msg == "down smash" or msg == "dash" or msg == secondaryCommandList[20]) and OnOrOff[20] == 1:
                                PressKeyPynput(GC_P1_DOWN)
                                PressAndHoldKey(GC_P1_A, 0.2)
                                ReleaseKeyPynput(GC_P1_DOWN)

                            if (msg == "left b" or msg == secondaryCommandList[21]) and OnOrOff[21] == 1:
                                PressKeyPynput(GC_P1_LEFT)
                                PressAndHoldKey(GC_P1_B, 0.2)
                                ReleaseKeyPynput(GC_P1_LEFT)

                            if (msg == "right b" or msg == secondaryCommandList[22]) and OnOrOff[22] == 1:
                                PressKeyPynput(GC_P1_RIGHT)
                                PressAndHoldKey(GC_P1_B, 0.2)
                                ReleaseKeyPynput(GC_P1_RIGHT)

                            if (msg == "up b" or msg == secondaryCommandList[23]) and OnOrOff[23] == 1:
                                PressKeyPynput(GC_P1_UP)
                                PressAndHoldKey(GC_P1_B, 0.2)
                                ReleaseKeyPynput(GC_P1_UP)

                            if (msg == "down b" or msg == secondaryCommandList[24]) and OnOrOff[24] == 1:
                                PressKeyPynput(GC_P1_DOWN)
                                PressAndHoldKey(GC_P1_B, 0.2)
                                ReleaseKeyPynput(GC_P1_DOWN)

                            if (msg == "left dash attack" or msg == "lda" or msg == secondaryCommandList[25]) and OnOrOff[25] == 1:
                                PressAndHoldKey(GC_P1_LEFT, 0.1)
                                PressAndHoldKey(GC_P1_A, 0.1)

                            if (msg == "right dash attack" or msg == "rda" or msg == secondaryCommandList[26]) and OnOrOff[26] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, 0.1)
                                PressAndHoldKey(GC_P1_A, 0.1)

                        else:

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P2_LEFT, MELEE_LIGHT_HOLD_TIME)
                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P2_LEFT, MELEE_MEDIUM_HOLD_TIME)
                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P2_LEFT, MELEE_HARD_HOLD_TIME)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, MELEE_LIGHT_HOLD_TIME)
                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, MELEE_MEDIUM_HOLD_TIME)
                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, MELEE_HARD_HOLD_TIME)

                            if (msg == "up" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P2_UP, 0.1)
                            if (msg == "down" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P2_DOWN, 0.1)

                            if (msg == "stop" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                ReleaseKeyPynput(GC_P2_RIGHT)
                                ReleaseKeyPynput(GC_P2_LEFT)
                                ReleaseKeyPynput(GC_P2_UP)
                                ReleaseKeyPynput(GC_P2_DOWN)

                            if (msg == "a" or msg == "a button" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(GC_P2_A, 0.1)
                            if (msg == "b" or msg == "b button" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(GC_P2_B, 0.1)

                            if (msg == "jump" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(GC_P2_X, 0.3)

                            if (msg == "rump" or msg == "right jump" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressKeyPynput(GC_P2_RIGHT)
                                PressAndHoldKey(GC_P2_X, 0.3)
                                ReleaseKeyPynput(GC_P2_RIGHT)

                            if (msg == "lump" or msg == "left jump" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                                PressKeyPynput(GC_P2_LEFT)
                                PressAndHoldKey(GC_P2_X, 0.3)
                                ReleaseKeyPynput(GC_P2_LEFT)

                            if (msg == "z" or msg == "grab" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                                PressAndHoldKey(GC_P2_Z, 0.1)
                            if (msg == "l" or msg == "shield" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                                PressAndHoldKey(GC_P2_L, 0.5)
                            if (msg == "r" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                                PressAndHoldKey(GC_P2_R, 0.5)

                            if (msg == "left smash" or msg == "lash" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                                PressKeyPynput(GC_P2_LEFT)
                                PressAndHoldKey(GC_P2_A, 0.2)
                                ReleaseKeyPynput(GC_P2_LEFT)

                            if (msg == "right smash" or msg == "rash" or msg == secondaryCommandList[18]) and OnOrOff[18] == 1:
                                PressKeyPynput(GC_P2_RIGHT)
                                PressAndHoldKey(GC_P2_A, 0.2)
                                ReleaseKeyPynput(GC_P2_RIGHT)

                            if (msg == "up smash" or msg == "uash" or msg == secondaryCommandList[19]) and OnOrOff[19] == 1:
                                PressKeyPynput(GC_P2_UP)
                                PressAndHoldKey(GC_P2_A, 0.2)
                                ReleaseKeyPynput(GC_P2_UP)

                            if (msg == "down smash" or msg == "dash" or msg == secondaryCommandList[20]) and OnOrOff[20] == 1:
                                PressKeyPynput(GC_P2_DOWN)
                                PressAndHoldKey(GC_P2_A, 0.2)
                                ReleaseKeyPynput(GC_P2_DOWN)

                            if (msg == "left b" or msg == secondaryCommandList[21]) and OnOrOff[21] == 1:
                                PressKeyPynput(GC_P2_LEFT)
                                PressAndHoldKey(GC_P2_B, 0.2)
                                ReleaseKeyPynput(GC_P2_LEFT)

                            if (msg == "right b" or msg == secondaryCommandList[22]) and OnOrOff[22] == 1:
                                PressKeyPynput(GC_P2_RIGHT)
                                PressAndHoldKey(GC_P2_B, 0.2)
                                ReleaseKeyPynput(GC_P2_RIGHT)

                            if (msg == "up b" or msg == secondaryCommandList[23]) and OnOrOff[23] == 1:
                                PressKeyPynput(GC_P2_UP)
                                PressAndHoldKey(GC_P2_B, 0.2)
                                ReleaseKeyPynput(GC_P2_UP)

                            if (msg == "down b" or msg == secondaryCommandList[24]) and OnOrOff[24] == 1:
                                PressKeyPynput(GC_P2_DOWN)
                                PressAndHoldKey(GC_P2_B, 0.2)
                                ReleaseKeyPynput(GC_P2_DOWN)

                            if (msg == "left dash attack" or msg == "lda" or msg == secondaryCommandList[25]) and OnOrOff[25] == 1:
                                PressAndHoldKey(GC_P2_LEFT, 0.1)
                                PressAndHoldKey(GC_P2_A, 0.1)

                            if (msg == "right dash attack" or msg == "rda" or msg == secondaryCommandList[26]) and OnOrOff[26] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, 0.1)
                                PressAndHoldKey(GC_P2_A, 0.1)


                        # else:
                        #     ##########################
                        #     ######## PLAYER 3 ########
                        #
                        #     # Throttling. Check if enough time has passed since the last executed command
                        #     # In this case, we are throttling to allow P1 more chances at a command
                        #     # time_since_last_command = time.time() - last_time
                        #     # if (time_since_last_command > THROTTLE_TIME):
                        #     #     # Enough time has passed. Execute the command, and reset timer
                        #     #     last_time = time.time()
                        #     # else:
                        #     #     continue
                        #
                        #     if msg == "light left":
                        #         PressAndHoldKey(NUMPAD_4, MELEE_LIGHT_HOLD_TIME)
                        #     if msg == "left":
                        #         PressAndHoldKey(NUMPAD_4, MELEE_MEDIUM_HOLD_TIME)
                        #     if msg == "hard left":
                        #         PressAndHoldKey(NUMPAD_4, MELEE_HARD_HOLD_TIME)
                        #
                        #     if msg == "light right":
                        #         PressAndHoldKey(NUMPAD_6, MELEE_LIGHT_HOLD_TIME)
                        #     if msg == "right":
                        #         PressAndHoldKey(NUMPAD_6, MELEE_MEDIUM_HOLD_TIME)
                        #     if msg == "hard right":
                        #         PressAndHoldKey(NUMPAD_6, MELEE_HARD_HOLD_TIME)
                        #
                        #     if msg == "up":
                        #         PressAndHoldKey(NUMPAD_8, 0.05)
                        #     if msg == "down":
                        #         PressAndHoldKey(NUMPAD_5, 0.05)
                        #
                        #     if msg == "a":
                        #         PressAndHoldKey(NUMPAD_2, 0.1)
                        #     if msg == "b":
                        #         PressAndHoldKey(NUMPAD_1, 0.1)
                        #     if msg == "jump":
                        #         PressAndHoldKey(NUMPAD_7, 0.2)
                        #     if msg == "z" or msg == "grab":
                        #         PressAndHoldKey(NUMPAD_3, 0.1)
                        #     if msg == "l" or msg == "shield":
                        #         PressAndHoldKey(COMMA, 0.5)
                        #     if msg == "r":
                        #         PressAndHoldKey(PERIOD, 0.5)
                        #
                        #     if msg == "left smash":
                        #         PressKeyPynput(NUMPAD_4)
                        #         PressAndHoldKey(NUMPAD_2, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_4)
                        #
                        #     if msg == "right smash":
                        #         PressKeyPynput(NUMPAD_6)
                        #         PressAndHoldKey(NUMPAD_2, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_6)
                        #
                        #     if msg == "up smash":
                        #         PressKeyPynput(NUMPAD_8)
                        #         PressAndHoldKey(NUMPAD_2, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_8)
                        #
                        #     if msg == "down smash":
                        #         PressKeyPynput(NUMPAD_5)
                        #         PressAndHoldKey(NUMPAD_2, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_5)
                        #
                        #     if msg == "left b":
                        #         PressKeyPynput(NUMPAD_4)
                        #         PressAndHoldKey(NUMPAD_1, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_4)
                        #
                        #     if msg == "right b":
                        #         PressKeyPynput(NUMPAD_6)
                        #         PressAndHoldKey(NUMPAD_1, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_6)
                        #
                        #     if msg == "up b":
                        #         PressKeyPynput(NUMPAD_8)
                        #         PressAndHoldKey(NUMPAD_1, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_8)
                        #
                        #     if msg == "down b":
                        #         PressKeyPynput(NUMPAD_5)
                        #         PressAndHoldKey(NUMPAD_1, 0.2)
                        #         ReleaseKeyPynput(NUMPAD_5)
                        #
                        #     if msg == "left dash attack" or msg == "lda":
                        #         PressAndHoldKey(NUMPAD_4, 0.1)
                        #         PressAndHoldKey(NUMPAD_2, 0.1)
                        #
                        #     if msg == "right dash attack" or msg == "rda":
                        #         PressAndHoldKey(NUMPAD_6, 0.1)
                        #         PressAndHoldKey(NUMPAD_2, 0.1)

                    ####################################
                    ####################################

                    ########################################################################
                    # MINECRAFT BLOCK
                    ########################################################################

                    if currentGame == gameList[10]:

                        if (msg == "forward" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            ReleaseKeyPynput(S)
                            PressAndHoldKey(W, 1.0)

                        if (msg == "back" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            ReleaseKeyPynput(W)
                            PressAndHoldKey(S, 1.0)

                        if (msg == "left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            ReleaseKeyPynput(D)
                            PressAndHoldKey(A, 0.7)

                        if (msg == "right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            ReleaseKeyPynput(A)
                            PressAndHoldKey(D, 0.7)

                        if (msg == "jump" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            PressAndHoldKey(SPACE, 0.3)

                        if (msg == "left click" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            mouse.press(Button.left)
                            time.sleep(0.3)
                            mouse.release(Button.left)

                        if (msg == "right click" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            mouse.press(Button.right)
                            time.sleep(0.3)
                            mouse.release(Button.right)

                        if (msg == "inventory" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            PressAndHoldKey(E, 0.1)

                        if (msg == "run" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            PressAndHoldKey(LEFT_CONTROL, 1.5)

                        if (msg == "crouch" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            PressAndHoldKey(LEFT_SHIFT, 0.7)


                    ########################################################################
                    # OUTLAST BLOCK
                    ########################################################################

                    if currentGame == gameList[11]:

                        if (msg == "forward" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            ReleaseKeyPynput(S)
                            PressAndHoldKey(W, 0.8)

                        if (msg == "back" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            ReleaseKeyPynput(W)
                            PressAndHoldKey(S, 0.8)

                        if (msg == "left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            ReleaseKeyPynput(D)
                            PressAndHoldKey(A, 0.5)

                        if (msg == "right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            ReleaseKeyPynput(A)
                            PressAndHoldKey(D, 0.5)

                        if (msg == "jump" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            PressAndHoldKey(SPACE, 0.3)

                        if (msg == "use" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            mouse.press(Button.left)
                            time.sleep(0.1)
                            mouse.release(Button.left)

                        if (msg == "camera" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            mouse.press(Button.right)
                            time.sleep(0.1)
                            mouse.release(Button.right)

                        if (msg == "run" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            PressAndHoldKey(LEFT_SHIFT, 1)

                        if (msg == "crouch" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            PressAndHoldKey(LEFT_CONTROL, 0.1)

                        if (msg == "lean left" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            PressAndHoldKey(Q, 0.75)

                        if (msg == "lean right" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                            PressAndHoldKey(E, 0.75)

                        if (msg == "nightvision" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                            PressAndHoldKey(F, 0.1)

                        if (msg == '420' or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                            if (random.randint(1,50) == 42):
                                PressAndHoldKey(F, 1)

                    ####################################
                    ####################################

                    #####################################################################
                    # SUPER MARIO WORLD BLOCK
                    ########################################################################

                    if currentGame == gameList[12]:

                        if (msg == "right" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            ReleaseKeyPynput(A)
                            PressKeyPynput(D)

                        if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            ReleaseKeyPynput(D)
                            PressKeyPynput(A)

                        if (msg == "tap right" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            ReleaseKeyPynput(D)
                            ReleaseKeyPynput(A)
                            PressAndHoldKey(D, 0.3)

                        if (msg == "stop" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            ReleaseKeyPynput(D)
                            ReleaseKeyPynput(A)

                        if (msg == "light jump" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            PressAndHoldKey(J, 0.3)

                        if (msg == "crouch" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            PressAndHoldKey(S, 0.5)

                        if (msg == "spin jump" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            PressAndHoldKey(K, 1)

                        if (msg == "jump" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            PressAndHoldKey(J, 1)

                        if (msg == "run" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            PressAndHoldKey(H, 1)



                    ########################################################################
                    # TF2 BLOCK
                    ########################################################################

                    if currentGame == gameList[13]:

                        if (msg == "forward" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                            ReleaseKeyPynput(S) #release brake command first
                            PressKeyPynput(W) #start permanently driving

                        if (msg == "back" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                            ReleaseKeyPynput(W) #release brake command first
                            PressKeyPynput(S)

                        if (msg == "left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                            ReleaseKeyPynput(D)
                            PressAndHoldKey(A, 0.7)

                        if (msg == "right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                            ReleaseKeyPynput(A)
                            PressAndHoldKey(D, 0.7)

                        if (msg == "stop" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                            ReleaseKeyPynput(W)
                            ReleaseKeyPynput(S)

                        if (msg == "jump" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                            print("****I got a jump command!****")
                            PressAndHoldKey(SPACE, 0.3)

                        if (msg == "crouch" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                            PressAndHoldKey(LEFT_CONTROL, 0.7)

                        if (msg == "shoot" or msg == "left click" or msg == "lc" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                            mouse.press(Button.left)
                            time.sleep(0.2)
                            mouse.release(Button.left)

                        if (msg == "right click" or msg == "rc" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                            mouse.press(Button.right)
                            time.sleep(0.2)
                            mouse.release(Button.right)

                        if (msg == "weapon 1" or msg == "1" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                            PressAndHoldKey(ONE, 0.2)

                        if (msg == "weapon 2" or msg == "2" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                            PressAndHoldKey(TWO, 0.2)

                        if (msg == "weapon 3" or msg == "3" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                            PressAndHoldKey(THREE, 0.2)

                        if (msg == "weapon 4" or msg == "4" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                            PressAndHoldKey(FOUR, 0.2)

                        if (msg == 'taunt' or msg == "420" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                            if (random.randint(1,500) == 42):
                                PressAndHoldKey(G, 1)
                                print(username + " DID IT, OH MY GOSH!!!!!")

                    ####################################
                    ####################################


                    ########################################################################
                    # SSX TRICKY BLOCK
                    ########################################################################

                    if currentGame == gameList[14]:

                        if isPlayer1(username):

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P1_LEFT, 0.3)

                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P1_LEFT, 0.5)

                            if (msg == "light right" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, 0.3)

                            if (msg == "right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P1_RIGHT, 0.5)

                            if (msg == "forward" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P1_UP, 1)

                            if (msg == "back" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P1_DOWN, 0.25)

                            if (msg == "jump" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P1_A, 0.5)

                            if (msg == "boost" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P1_B, 0.5)

                            if (msg == "trick" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                PressAndHoldKey(GC_P1_Z, 0.5)

                            if (msg == "shove left" or msg == "sl" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(A, 0.1)

                            if (msg == "shove right" or msg == "sr" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(D, 0.1)

                        else:

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(GC_P2_LEFT, 0.1)

                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(GC_P2_LEFT, 0.3)

                            if (msg == "light right" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, 0.1)

                            if (msg == "right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(GC_P2_RIGHT, 0.3)

                            if (msg == "forward" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(GC_P2_UP, 1)

                            if (msg == "back" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(GC_P2_DOWN, 0.25)

                            if (msg == "jump" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(GC_P2_A, 0.5)

                            if (msg == "boost" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressAndHoldKey(GC_P2_B, 0.5)

                            if (msg == "trick" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                PressAndHoldKey(GC_P2_Z, 0.5)


                    ####
                    # # ONLY FOR 1 PLAYER
                    # if msg == "pogchamp" or msg == "pog champ":
                    #     randomNum = random.randint(1,4)
                    #     if (randomNum == 1):
                    #         PressAndHoldKey(J, 0.5)
                    #     elif (randomNum == 2):
                    #         PressAndHoldKey(L, 0.5)



                    ########################################################################
                    # SPELUNKY BLOCK
                    ########################################################################

                    if currentGame == gameList[15]:

                        if isPlayer1(username):

                            if (msg == "light left" or msg == secondaryCommandList[0]) and OnOrOff[0] == 1:
                                PressAndHoldKey(LEFT_ARROW, 0.1)
                            if (msg == "left" or msg == secondaryCommandList[1]) and OnOrOff[1] == 1:
                                PressAndHoldKey(LEFT_ARROW, 0.4)
                            if (msg == "hard left" or msg == secondaryCommandList[2]) and OnOrOff[2] == 1:
                                PressAndHoldKey(LEFT_ARROW, 0.7)

                            if (msg == "light right" or msg == secondaryCommandList[3]) and OnOrOff[3] == 1:
                                PressAndHoldKey(RIGHT_ARROW, 0.1)
                            if (msg == "right" or msg == secondaryCommandList[4]) and OnOrOff[4] == 1:
                                PressAndHoldKey(RIGHT_ARROW, 0.4)
                            if (msg == "hard right" or msg == secondaryCommandList[5]) and OnOrOff[5] == 1:
                                PressAndHoldKey(RIGHT_ARROW, 0.7)

                            if (msg == "jump" or msg == secondaryCommandList[6]) and OnOrOff[6] == 1:
                                PressAndHoldKey(Z, 0.8)

                            if (msg == "right jump" or msg == "rump" or msg == secondaryCommandList[7]) and OnOrOff[7] == 1:
                                PressKeyPynput(RIGHT_ARROW)
                                PressAndHoldKey(Z, 0.5)
                                ReleaseKeyPynput(RIGHT_ARROW)

                            if (msg == "left jump" or msg == "lump" or msg == secondaryCommandList[8]) and OnOrOff[8] == 1:
                                PressKeyPynput(LEFT_ARROW)
                                PressAndHoldKey(Z, 0.5)
                                ReleaseKeyPynput(LEFT_ARROW)

                            if (msg == "up" or msg == secondaryCommandList[9]) and OnOrOff[9] == 1:
                                PressAndHoldKey(UP_ARROW, 1)
                            if (msg == "down" or msg == secondaryCommandList[10]) and OnOrOff[10] == 1:
                                PressAndHoldKey(DOWN_ARROW, 1)

                            if (msg == "run" or msg == secondaryCommandList[11]) and OnOrOff[11] == 1:
                                PressAndHoldKey(LEFT_SHIFT, 1)

                            if (msg == "whip" or msg == "shoot" or msg == secondaryCommandList[12]) and OnOrOff[12] == 1:
                                PressAndHoldKey(X, 0.1)

                            if (msg == "bomb" or msg == secondaryCommandList[13]) and OnOrOff[13] == 1:
                                if (random.randint(1,50) == 5):
                                    PressAndHoldKey(S, 0.1)

                            if (msg == "rope" or msg == secondaryCommandList[14]) and OnOrOff[14] == 1:
                                if (random.randint(1,10) == 5):
                                    PressAndHoldKey(A, 0.1)

                            if (msg == "door" or msg == secondaryCommandList[15]) and OnOrOff[15] == 1:
                                PressAndHoldKey(SPACE, 0.1)

                            if (msg == "pick up" or msg == secondaryCommandList[16]) and OnOrOff[16] == 1:
                                PressAndHoldKey(DOWN_ARROW, 0.1)
                                PressAndHoldKey(X, 0.1)

                            if (msg == "stop" or msg == secondaryCommandList[17]) and OnOrOff[17] == 1:
                                ReleaseKeyPynput(DOWN_ARROW)
                                ReleaseKeyPynput(UP_ARROW)
                                ReleaseKeyPynput(RIGHT_ARROW)
                                ReleaseKeyPynput(LEFT_ARROW)


            except:
                print('Encountered an exception while reading chat. Moving on to next messages')

                    ####################################
                    # DWREDEN - NOTES ON INPUT COMMANDS

                    # KEY PRESSES
                    # The standard "Twitch Plays" tutorial commands do NOT work in DirectX games (they work in general windows apps though)
                    # Instead, we use DirectX key codes and input functions from in directkeys.py
                    # This code is taken from: https://stackoverflow.com/questions/53643273/how-to-keep-pynput-and-ctypes-from-clashing
                    # Original version is from the GTA Python tutorial: https://pythonprogramming.net/direct-input-game-python-plays-gta-v/
                    # Note: DirectX's hex key codes are NOT the same as Windows virtual hex key codes.
                    #   DirectX codes are found at: https://docs.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-6.0/aa299374(v=vs.60)

                    # MOUSE CLICK
                    #   Use pynput.mouse functions: https://pypi.org/project/pynput/
                    #   NOTE: pyautogui's click() function permanently holds down in DirectX, so using pynput here instead

                    # MOUSE MOVEMENT
                    #   Run a "AutoHotkey" script, which issues Windows commands to move mouse by specified amount
                    #   AutoHotkey documentation: https://www.autohotkey.com/docs/Tutorial.htm#s12
                    #       Call it using: subprocess.call([PATH_TO_AUTOHOTKEY, PATH_TO_MOVEMOUSERIGHT_SCRIPT])
                    #       Paths to each ahk script is defined above, e.g. 'C:\\Program Files\\AutoHotkey\\AutoHotkey.exe'
                    #   Mouse emulation alternatives like NeatMouse don't respond to key-presses sent by python (only to physical keyboard presses).
                    #   Alternatives:
                    #       pyautogui.moveRel(X,Y,duration=Z) works for non-DirectX applications. However, cannot get mouse movement working in DirectX
                    #       I tried following direct input code from this tutorial, but does not work:
                    #       https://pythonprogramming.net/acquiring-vehicle-python-plays-gta-v/?completed=/finding-vehicle-python-plays-gta-v/

                    # TEXT TYPING
                    #   pyautogui.typewrite() types out text where the cursor currently is
                    #   It does NOT work inside DirectX games
                    #   NOTE: I could hack a workaround for DirectX by looping thru and pressing every individual key in a string
                    #
                    ####################################

    window.after(int(THROTTLE_TIME*1000), task)


window.after(int(THROTTLE_TIME*1000), task)
window.mainloop()
