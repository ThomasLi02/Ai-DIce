from tkinter import *
from tkinter import font
import tkinter as tk
import random
from PIL import ImageTk, Image

import numpy
import random
import math
from scipy.special import binom, factorial


class database():
    def __init__(self):
        self.data = []
        self.gameList = []
        self.d1 = []
        self.d2 = []
        self.i1 = []
        self.i2 = []
        self.score = [0, 0]
        self.nBluff = 0
        self.call = (1,1,1)
        self.whoStart = 1

    def createGame(self, calls):
        result = []
        for call in calls:
            result.append(call)
        self.data.append(call)

    def createCall(self, who, diceNum, dicePoint):
        return who, diceNum, dicePoint


def bluff(call, playerDice):
    numCount = 0
    for i in playerDice:
        if i == call[2] or i == 1:
            numCount += 1
    if call[1] >= 6:
        return numCount < call[1] / 2.0 + 1
    else:
        return numCount < call[1] / 2.0


def callBluff(call, playerDice):
    numCount = 0
    for i in playerDice:
        if i == call[2] or i == 1:
            numCount += 1
    return numCount < call[1] / 3.0


class total():
    def __init__(self):
        self.start = [1, 2]
        self.add = [1, 2]
        self.switch = [1, 2]
        self.call = [1, 2]
        self.markov = [[1, 1], [1, 1]]

    def updateMarkov(self, game, playerDice):
        bluffList = []
        for i in range(len(game)):
            if game[i][0] == 1:
                if i == 0:
                    bluffList.append(callBluff(game[i], playerDice))
                elif i == 1:
                    if game[1][2] == game[0][2]:
                        bluffList.append(callBluff(game[i], playerDice))
                else:
                    if game[i][2] != game[i - 2][2] and game[i][2] == game[i - 1][2]:
                        bluffList.append(callBluff(game[i], playerDice))
                    else:
                        bluffList.append(bluff(game[i], playerDice))
        for i in range(len(bluffList) - 1):
            if bluffList[i] == 1:
                if bluffList[i + 1] == 1:
                    self.markov[0][0] += 1
                else:
                    self.markov[0][1] += 1
            if bluffList[i] == 0:
                if bluffList[i + 1] == 1:
                    self.markov[1][0] += 1
                else:
                    self.markov[1][1] += 1

    def printData(self):
        result = ""
        result += ("start" + str(self.start[0]) + " " + str(self.start[1]))
        result += ("\nadd" + str(self.add[0]) + " " + str(self.add[1]))
        result += ("\nswitch" + str(self.switch[0]) + " " + str(self.switch[1]))
        result += ("\ncall" + str(self.call[0]) + " " + str(self.call[1]))
        result += "\n"
        result += "\n" + str(self.markov[0][0]) + " "  + str((self.markov[0][1]))
        result += "\n" + str(self.markov[1][0])+ " " +str((self.markov[1][1]))
        return result

    def updateStart(self, game, playerDice):
        if game[0][0] == 1:
            if bluff(game[0], playerDice):
                self.start[0] += 1
                self.start[1] += 1
            else:
                self.start[1] += 1

    def updateAdd(self, game, playerDice):
        for i in range(2, len(game)):
            if game[i][0] == 1:
                if game[i][2] == game[i - 2][2]:
                    if bluff(game[i], playerDice):
                        self.add[0] += 1
                        self.add[1] += 1
                    else:
                        self.add[1] += 1

    def updateSwitch(self, game, playerDice):
        for i in range(1, len(game)):
            if i == 1:
                if game[1][0] == 1:
                    if game[1][2] != game[0][2]:
                        if bluff(game[1], playerDice):
                            self.add[0] += 1
                            self.add[1] += 1
                        else:
                            self.add[1] += 1
            else:
                if game[i][0] == 1:
                    if game[i][2] != game[i - 2][2] and game[i][2] != game[i - 1][2]:
                        if bluff(game[i], playerDice):
                            self.add[0] += 1
                            self.add[1] += 1
                        else:
                            self.add[1] += 1

    def updateCall(self, game, playerDice):
        for i in range(1, len(game)):
            if i == 1:
                if game[1][0] == 1:
                    if game[1][2] == game[0][2]:
                        if callBluff(game[i], playerDice):
                            self.add[0] += 1
                            self.add[1] += 1
                        else:
                            self.add[1] += 1
            else:
                if game[i][0] == 1:
                    if game[i][2] != game[i - 2][2] and game[i][2] == game[i - 1][2]:
                        if callBluff(game[i], playerDice):
                            self.call[0] += 1
                            self.call[1] += 1
                        else:
                            self.call[1] += 1

    def updateAll(self, game, playerDice):
        self.updateStart(game, playerDice)
        self.updateAdd(game, playerDice)
        self.updateCall(game, playerDice)
        self.updateSwitch(game, playerDice)

    def getStartBluff(self):
        return self.start[0] / (self.start[1])

    def getAddBluff(self):
        return self.add[0] / (self.add[1])

    def getSwitchBluff(self):
        return self.switch[0] / (self.switch[1])

    def getCallBluff(self):
        return self.call[0] / (self.call[1])

    def printing(self):
        print(self.add)
        print(self.switch)
        print(self.call)
        print(self.start)


def open(d1, d2, call):
    n = call[1]
    k = call[2]
    count = 0
    for x in range(0, 5):
        if (d1[x] == k or d1[x] == 1):
            count += 1
        if (d2[x] == k or d2[x] == 1):
            count += 1
    if set(d1) == {1} or set(d1) == {k} or set(d1) == {1, k}:
        count += 1
    if set(d2) == {1} or set(d2) == {k} or set(d2) == {1, k}:
        count += 1
    return count >= n






def count(d2):
    counting = []
    for x in range(5):
        counting.append(d2.count(x + 2) + d2.count(1))
    return counting


def has4(d2):
    countList = count(d2)
    most = max(countList)
    if most >= 4:
        return countList.index(most) + 2, most
    else:
        return 0, 0


def reverse(countList):
    counting = count(countList)
    counting.reverse()
    return counting


def switch(call, computerList):
    n = call[1]
    k = call[2]
    if n == 3 and k < 6:
        k1 = first_move(call, computerList)
        return (0, n, k1)
    reversed = reverse(computerList)
    val = 6 - reversed.index(max(reversed))
    if max(reversed) >= 3:
        if(n == 3 and k == 6) or (n == 4 and k < 6 and val > k):
            return (0, 4, val)
        elif (n == 4 or (n == 5 and val > k)):
            return (0, 5, val)
    elif n == 3 and k == 6:
        return (0, 4, random.choice([2, 3, 4, 5]))
    elif n == 4 and k < 6:
        return (0, 4, random.choice(list(range(k + 1, 7))))
    return (2, n, k)


def switch2(call, computerList):
    n = call[1]
    k = call[2]
    if n == 3 and k < 6:
        k1 = first_move(call, computerList)
        return (1, n, k1)
    elif n == 3 and k == 6:
        return (1, 4, random.choice([2, 3, 4, 5]))
    elif n == 4 and k < 6:
        return (1, 4, random.choice(list(range(k + 1, 7))))
    else:
        reversed = reverse(computerList)
        val = 6 - reversed.index(max(reversed))
        if max(reversed) >= 3 and (n == 4 or (n == 5 and val > k)):
            return (0, 5, val)
        return (2, n, k)


def first_move(call, computerList):
    k = call[2]
    if 1 in computerList:
        counting = count(computerList)
        for x in range(k - 1):
            counting.pop(0)
        return counting.index(max(counting)) + k + 1
    missing = list(set(range(2, 7)) - set(computerList))
    if (len(missing)) >= 1 and random.random() <= 0.8 and missing[0] > k:
        return missing[0]
    return random.choice(list(range(k + 1, 7)))

# type-computer start = -1 after switch = 1, after call = 2, after add = 3, after start = 4
def play2(type, d2, game, total, call, curBluff):
    num, most = has4(d2)
    if num > 0 and call[1] >= 2 * most:
        return (2, call[1], call[2]), 0
    elif num > 0 and call[2] < num:
        return (0, call[1], num), 0
    elif num > 0:
        return (0, call[1] + 1, num), 0
    elif type == -1:
        return (0, 3, first_move(call, d2)), 0
    else:
        playerCall = game[len(game) - 1]
        if type == 4:
            bluff = random.random() < total.getSwitchBluff()
            if len(game) == 2:
                newBluff = bluff
            else:
                while bluff != (random.random() < total.markov[curBluff][0] / (
                        total.markov[curBluff][0] + total.markov[curBluff][1])):
                    bluff = random.random() < total.getSwitchBluff()
                newBluff = bluff
        if type == 3:
            bluff = random.random() < total.getCallBluff()
            while bluff != random.random() < total.markov[curBluff][0] / (
                    total.markov[curBluff][0] + total.markov[curBluff][1]):
                bluff = random.random() < total.getSwitchBluff()
            newBluff = bluff
        if type == 2:
            bluff = random.random() < total.getAddBluff()
            while bluff != random.random() < total.markov[curBluff][0] / (
                    total.markov[curBluff][0] + total.markov[curBluff][1]):
                bluff = random.random() < total.getSwitchBluff()
            newBluff = bluff
        if type == 1:
            bluff = random.random() < total.getStartBluff()
            newBluff = bluff
        if bluff:
            playerCount = math.ceil(playerCall[1] / 2.0) - 1
        else:
            playerCount = math.ceil(playerCall[1] / 2.0)
        myCount = 0
        for i in d2:
            if i == playerCall[2] or i == 1:
                myCount += 1
        if myCount + playerCount < playerCall[1] - 1:
            return (2, call[1], call[2]), 0
        elif myCount + playerCount < playerCall[1]:
            if random.random() < 0.3:
                return switch(call, d2), newBluff
            return (2, call[1], call[2]), 0
        elif myCount + playerCount > playerCall[1]:
            return (0, playerCall[1] + 1, playerCall[2]), newBluff
        else:
            if random.random() < 0.3:
                return (2, call[1], call[2]), 0
            return (switch(call, d2)), newBluff


def play(type, d2, game, total, call, curBluff):
    num, most = has4(d2)
    if num > 0 and call[1] >= 2 * most:
        return (2, call[1], call[2]), 0
    elif num > 0 and call[2] < num:
        return (0, call[1], num), 0
    elif num > 0:
        return (0, call[1] + 1, num), 0
    elif type == -1:
        return (0, 3, first_move(call, d2)), 0
    else:
        playerCall = game[len(game) - 1]
        if type == 4:
            bluff = random.random() < total.getSwitchBluff()
            if len(game) == 2:
                    newBluff = bluff
            else:
                bluff = random.random() < total.markov[curBluff][0] / (
                        total.markov[curBluff][0] + total.markov[curBluff][1])
                newBluff = bluff
        elif type == 3 or type == 2:
            bluff = random.random() < total.markov[curBluff][0] / (
                    total.markov[curBluff][0] + total.markov[curBluff][1])
            newBluff = bluff
        elif type == 1:
            bluff = random.random() < total.getStartBluff()
            newBluff = bluff
        else:
            bluff = False
            newBluff = bluff

        if bluff:
            playerCount = math.ceil(playerCall[1] / 2.0) - 2
        else:
            playerCount = math.ceil(playerCall[1] / 2.0)
        myCount = 0
        for i in d2:
            if i == playerCall[2] or i == 1:
                myCount += 1
        if myCount >= playerCall[1] or myCount + playerCount > playerCall[1]:
            return (0, playerCall[1] + 1, playerCall[2]), newBluff
        elif myCount + playerCount < playerCall[1] - 1:
            return (2, call[1], call[2]), 0
        if random.random() < 0.5:
            return (2, call[1], call[2]), 0
        return (switch(call, d2)), newBluff



def play3(type, d2, game, total, call, curBluff):
    num, most = has4(d2)
    if num > 0 and call[1] >= 2 * most:
        return (2, call[1], call[2]), 0
    elif num > 0 and call[2] < num:
        return (1, call[1], num), 0
    elif num > 0:
        return (1, call[1] + 1, num), 0
    elif type == -1:
        return (1, 3, first_move(call, d2)), 0
    else:
        playerCall = game[len(game) - 1]
        if type == 4:
            bluff = random.random() < total.getSwitchBluff()
            if len(game) == 2:
                newBluff = bluff
            else:
                bluff = random.random() < total.markov[curBluff][0] / (
                    total.markov[curBluff][0] + total.markov[curBluff][1])
                newBluff = bluff
        elif type == 3 or type == 2:
            bluff = random.random() < total.markov[curBluff][0] / (
                total.markov[curBluff][0] + total.markov[curBluff][1])
            newBluff = bluff
        else:
            bluff = random.random() < total.getStartBluff()
            newBluff = bluff
        if bluff:
            playerCount = math.ceil(playerCall[1] / 2.0) - 1
        else:
            playerCount = math.ceil(playerCall[1] / 2.0)
        myCount = 0
        for i in d2:
            if i == playerCall[2] or i == 1:
                myCount += 1
        if myCount + playerCount < playerCall[1] - 1:
            return (2, call[1], call[2]), 0
        elif myCount + playerCount < playerCall[1]:
            if random.random() < 0.3:
                return switch(call, d2), newBluff
            return (2, call[1], call[2]), 0
        elif myCount + playerCount > playerCall[1]:
            return (0, playerCall[1] + 1, playerCall[2]), newBluff
        else:
            if random.random() < 0.3:
                return (2, call[1], call[2]), 0
            return (switch(call, d2)), newBluff


def callType(gameList):
    if len(gameList) == 0:
        return -1
    elif len(gameList) == 1: #first move is player
        return 1
    elif len(gameList) == 2: # first move is ai, second move is player
        if gameList[len(gameList) - 1][2] != (gameList[len(gameList) - 2][2]): # if player switched
            return 4
        if gameList[len(gameList) - 1][2] == (gameList[len(gameList) - 2][2]): #if player called
            return 3
    elif (gameList[len(gameList) - 1][2] == gameList[len(gameList) - 3][2]):
        return 2
    elif (gameList[len(gameList) - 1][2] == gameList[len(gameList) - 2][2]
          and gameList[len(gameList) - 1][2] != gameList[len(gameList) - 3][2]):
        return 3
    elif (gameList[len(gameList) - 1][2] != gameList[len(gameList) - 2][2]
          and gameList[len(gameList) - 1][2] != gameList[len(gameList) - 3][2]):
        return 4


data = database()
total = total()

# Initialize Tkinter obj
window = tk.Tk()

# set window name
window.title("Liar's Dice Game")

# Open window fullscreen
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))

imagePath = "GUI/imgs/"

bg = ImageTk.PhotoImage(Image.open(imagePath + "background.png").resize((width, height)))

# Show Background using label
label1 = Label(window, image=bg)
label1.place(x=0, y=0)

# Create Header
headerFont = tk.font.Font(family="Comic Sans MS", size=40, weight='bold')
header = Label(window, text= " Liar's Dice Game ", font=headerFont,
               borderwidth=7, relief='solid')
header.place(relx=0.5, rely=0.1, anchor=CENTER)

# Create Rules Frame
rulesFWidth, rulesFHeight = 420, 600
rulesFrame = Frame(window, width=rulesFWidth,
                   height=rulesFHeight, bd=7, relief='solid')
rulesFrame.place(relx=0.175, rely=0.5, anchor=CENTER)

# Create Rules Header
rulesHeaderFont = tk.font.Font(family="Comic Sans MS", size=40, weight='bold')
rulesHeader = Label(rulesFrame, text=" Rules ",
                    font=rulesHeaderFont, borderwidth=4, relief='solid')
rulesHeader.place(relx=0.5, rely=0.15, anchor=CENTER)

# Create Rules Text
rule1 = "Roll the dice and guess how many pips there are in total."
rule2 = "Make a move! For example, you can say, 5x4s, or you can choose to open if you don't believe your opponent."
rule3 = "Make a move again after your opponent makes their move."
rule4 = "Good luck!"

ruleFont = tk.font.Font(family="Comic Sans MS", size=17, weight="bold")
bullet_width = ruleFont.measure("-  ")
em = ruleFont.measure("m")
text = Text(rulesFrame, font=ruleFont, height=15, width=35,
            relief='flat', bg=rulesFrame.cget('bg'), wrap=WORD)
text.tag_configure("bulleted", lmargin1=em, lmargin2=em + bullet_width)

text.insert("end", "1. " + rule1 + '\n' + '\n', "bulleted")
text.insert("end", "2. " + rule2 + '\n' + '\n', "bulleted")
text.insert("end", "3. " + rule3 + '\n' + '\n', "bulleted")
text.insert("end", "4. " + rule4, "bulleted")
text.place(relx=0.5, rely=0.6, anchor=CENTER)

# Create User Frame
uFWidth, uFHeight = 375, 100
userFrame = Frame(window, width=uFWidth, height=uFHeight, bd=4, relief='solid')
userFrame.place(relx=0.5, rely=0.225, anchor=CENTER)

# Create User Name
userNameFont = tk.font.Font(family="Comic Sans MS", size=15, weight='bold')
userName = Label(userFrame, text=" Input User: ",
                 font=userNameFont, borderwidth=2, relief='solid').place(relx=0.20, rely=0.275, anchor=CENTER)
whoStart = tk.StringVar()
whoStartFont = tk.font.Font(family="Comic Sans MS", size=15, weight='bold')
whoStartFWidth, whoStartFHeight = 375, 100
whoStartFrame = Frame(window, width = whoStartFWidth, height = whoStartFHeight, bd = 4, relief = 'solid')
whoStartFrame.place(relx = 0.5, rely = 0.225, anchor=CENTER)
whoStartLabel = Label(whoStartFrame, textvariable=whoStart, font = whoStartFont)
whoStartLabel.place(relx=0.5, rely=0.7, anchor=CENTER)
whoStart.set(" ")

# Create Dice Frame
dFWidth, dFHeight = 375, 400
diceFrame = Frame(window, width=dFWidth, height=dFHeight, bd=4, relief='solid')
diceFrame.place(relx=0.5, rely=0.525, anchor=CENTER)

imagePath = "GUI/imgs/"

diceList = []

dice1 = Image.open(imagePath + "one.png").resize((50, 50))
dice2 = Image.open(imagePath + "two.png").resize((50, 50))
dice3 = Image.open(imagePath + "three.png").resize((50, 50))
dice4 = Image.open(imagePath + "four.png").resize((50, 50))
dice5 = Image.open(imagePath + "five.png").resize((50, 50))
dice6 = Image.open(imagePath + "six.png").resize((50, 50))
diceList.append(ImageTk.PhotoImage(dice1))
diceList.append(ImageTk.PhotoImage(dice2))
diceList.append(ImageTk.PhotoImage(dice3))
diceList.append(ImageTk.PhotoImage(dice4))
diceList.append(ImageTk.PhotoImage(dice5))
diceList.append(ImageTk.PhotoImage(dice6))


# Create Roll Function

pLabelList = []
aiLabelList = []

def rollPlayerDice():
    data.i1 = []
    data.d1 = []
    data.nBluff = 0

    xVal, yVal = 0.4, 0.125
    if len(pLabelList) != 0:
        for i in range(len(pLabelList)):
            pLabelList[i].destroy()
            aiLabelList[i].destroy()
    while len(set(data.i1)) == len(data.i1):
        data.d1 = []
        data.i1 = []
        for i in range(0, 5):
            n = random.randint(1, 6)
            data.i1.append(diceList[n-1])
            data.d1.append(n)

    for i in range(5):
        randomPlayerDice = data.i1[i]
        playerDiceLabel = Label(diceFrame, image=randomPlayerDice)
        pLabelList.append(playerDiceLabel)
        playerDiceLabel.place(relx=xVal, rely=yVal, anchor=CENTER)
        if i % 2 == 0:
            xVal += 0.2
        else:
            if i != 3:
                xVal -= 0.2
            else:
                xVal -= 0.1
            yVal += 0.15
    print(data.d1)

def rollAiDice():
    data.i2 = []
    data.d2 = []
    data.call = (1, 1, 1)

    xVal, yVal = 0.25, 0.4
    if len(aiLabelList) != 0:
        for i in range(len(aiLabelList)):
            aiLabelList[i].destroy()
    while len(set(data.d2)) == len(data.d2):
        data.d2 = []
        data.i2 = []
        for i in range(0, 5):
            n = random.randint(1, 6)
            data.i2.append(diceList[n-1])
            data.d2.append(n)

    for i in range(5):
        randomAiDice = data.i2[i]
        aiDiceLabel = Label(aiDiceFrame, image=randomAiDice)
        aiLabelList.append(aiDiceLabel)
        aiDiceLabel.place(relx=xVal, rely=yVal, anchor=CENTER)
        if i % 2 == 0:
            xVal += 0.475
        else:
            if i != 3:
                xVal -= 0.475
                yVal += 0.4
            else:
                xVal -= 0.2375
                yVal -= 0.2
    if data.whoStart == 0:
        whoStart.set("Computer Start, Look at Computer Move")
        print(first_move(data.call, data.d2))
        data.call = (0, 3, first_move(data.call, data.d2))
        print(data.call)
        data.gameList.append(data.call)
        aiMove.set(data.call)
        print(aiMove.get())
    else:
        whoStart.set("You are starting, Computer is Waiting")

    print(data.d2)



# Create Roll Button
btn = Button(diceFrame, text='Roll Dice!', bd='10', command=lambda: [resetDisplays(),rollPlayerDice(), rollAiDice()])
btn.place(relx=0.5, rely=0.55, anchor=CENTER)

# Create User Game input
userGInputFont = tk.font.Font(family="Comic Sans MS", size=15, weight='bold')
userGInput = Label(diceFrame, text=" What's Your Move?: ",
                   font=userGInputFont, borderwidth=3, relief='solid').place(relx=0.5, rely=0.675, anchor=CENTER)




# Create AI Frame
aiFWidth, aiFHeight = 375, 100
aiFrame = Frame(window, width=aiFWidth, height=aiFHeight, bd=4, relief='solid')
aiFrame.place(relx=0.5, rely=0.825, anchor=CENTER)

# Create AI Move Header
aiHeaderFont = tk.font.Font(family="Comic Sans MS", size=15, weight='bold')
aiHeader = Label(aiFrame, text=" Computer's Move: ",
                 font=aiHeaderFont, borderwidth=3, relief='solid')
aiHeader.place(relx=0.5, rely=0.275, anchor=CENTER)

# Create AI Move Entry
aiMove = tk.StringVar()
aiMoveLabel = Label(aiFrame, textvariable=aiMove, font=aiHeaderFont)
aiMoveLabel.place(relx=0.5, rely=0.7, anchor=CENTER)
aiMove.set(" ")

# Create Results Frame
resultsFWidth, resultsFHeight = 325, 400
resultsFrame = Frame(window, width=resultsFWidth,
                     height=resultsFHeight, bd=7, relief='solid')
resultsFrame.place(relx=0.825, rely=0.275, anchor=CENTER)

# Create Score Header
scoreHeaderFont = tk.font.Font(family="Comic Sans MS", size=40, weight='bold')
scoreBLabel = Label(resultsFrame, text=" Results ",
                    font=scoreHeaderFont, borderwidth=4, relief='solid')
scoreBLabel.place(relx=0.5, rely=0.125, anchor=CENTER)

# Create Score Label
scoreB = tk.StringVar()
scoreBLabel = Label(resultsFrame, textvariable=scoreB, font=aiHeaderFont)
scoreBLabel.place(relx=0.5, rely=0.3, anchor=CENTER)
scoreB.set(" ")

# Create Win/Lose Label
winLose = tk.StringVar()
winLoseLabel = Label(resultsFrame, textvariable=winLose, font=aiHeaderFont)
winLoseLabel.place(relx=0.5, rely=0.45, anchor=CENTER)
winLose.set(" ")

# Create Ai Dice Frame
aiDiceFWidth, aiDiceFHeight = 275, 175
aiDiceFrame = Frame(resultsFrame, width=aiDiceFWidth,
                     height=aiDiceFHeight, bd=4, relief='solid')
aiDiceFrame.place(relx=0.5, rely=0.75, anchor=CENTER)

# Create Computer Dice Header
aiDiceHeaderFont = tk.font.Font(family="Comic Sans MS", size=15, weight='bold')
aiDiceLabel = Label(aiDiceFrame, text=" Computer's Dice: ",
                    font=aiDiceHeaderFont, borderwidth=2, relief='solid')
aiDiceLabel.place(relx=0.05, rely=0.125, anchor=W)

# Create Database Display Frame
dataB = tk.StringVar()
dataBFWidth, dataBFHeight = 325, 200
dataBFrame = Frame(window, width=dataBFWidth,
                   height=dataBFHeight, bd=4, relief='solid')
dataBFrame.place(relx=0.825, rely=0.8, anchor=CENTER)
dataBLabel = Label(dataBFrame, textvariable=dataB, font=aiHeaderFont)
dataBLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
dataB.set(" ")

# Create Reset Function for New Game
def resetDisplays():
    aiMove.set(" ")
    winLose.set(" ")
    dataB.set(" ")
    inputCheck.set(" ")
    aiDiceFrame.place_forget()
    setEntryEmpty(userGInputEntry)

# Create Set Entry Box as Empty Function
def setEntryEmpty(entry):
    entry.delete(0, END)
    entry.insert(0, "")



inputCheck = tk.StringVar()
inputCheckWidth, inputCheckHeight = 325, 100
inputCheckFrame = Frame(window, width = inputCheckWidth, height = inputCheckHeight, bd = 4, relief = 'solid')
inputCheckFrame.place(relx = 0.825, rely = 0.6, anchor=CENTER)
inputCheckLabel = Label(inputCheckFrame, textvariable=inputCheck, font = aiHeaderFont, wraplength= 240)
inputCheckLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
inputCheck.set(" ")

stats = 0
opened = False

def check(call, n, k):
    if n not in range(3, 14) or k not in range(2, 7):
        inputCheck.set("Out of range or wrong type of data.")
        print("x")
        print(inputCheck.get())
        return False
    #TODO
    elif call[1] > n:
        inputCheck.set("The number must be larger or equal the one in the previous round.")
        print("x")
        print(inputCheck.get())
        return False
    elif call[1] == n and call[2] >= k:
        inputCheck.set("The value must be larger than the one in the previous round if the number keeps the same.")
        print("x")
        print(inputCheck.get())
        return False
    else:
        inputCheck.set("Your input is valid")
        return True

def fin():
    if len(data.gameList) == 0:
        return None
    aiDiceFrame.place(relx=0.5, rely=0.75, anchor=CENTER)
    if open(data.d1, data.d2, data.gameList[len(data.gameList) - 1]) == 0:
        winLose.set("You Opened, You Win!")
        data.whoStart = 0
        data.score[0] += 1
        scoreB.set(
            "Player: " + str(data.score[0]) + "     Computer: " + str(data.score[1]))
        data.data.append(data.gameList)
        total.updateAll(data.gameList, data.d1)
        total.updateMarkov(data.gameList,data.d1)

        dataB.set(total.printData())
        data.gameList = []
        ''' computerDice = ""
        for i in range(len(data.d2)):
            computerDice += str(data.d2[i])
        compDice.set(computerDice) '''
    else:
        winLose.set("You Opened, You Lose.")
        data.score[1] += 1
        data.whoStart = 1
        scoreB.set(
            "Player: " + str(data.score[0]) + "     Computer: " + str(data.score[1]))
        dataB.set(total.printData())
        data.data.append(data.gameList)
        total.updateAll(data.gameList, data.d1)
        total.updateMarkov(data.gameList, data.d1)
        data.gameList = []


def do(inputcheck):
    text = userGInputEntry.get()
    if ' ' in text:
        a, b = text.split()
    else:
        inputcheck.set("Need two values seperated by a space")
        return None
    num = int(a)
    val = int(b)
    if not check(data.call, num, val):
        return None

    data.call = (1, num, val)
    data.gameList.append(data.call)
    data.call, data.nBluff = play(callType(data.gameList), data.d2, data.gameList, total, data.call, data.nBluff)
    if data.call[0] == 2:
        aiMove.set("Computer Opened You!")
    else:
        aiMove.set(data.call)
    data.gameList.append(data.call)
    if data.call[0] == 2:
        aiDiceFrame.place(relx=0.5, rely=0.75, anchor=CENTER)
        if open(data.d1, data.d2, data.call):
            winLose.set("You Win!")
            data.whoStart = 0
            data.score[0] += 1
            scoreB.set(
                "Player: " + str(data.score[0]) + "     Computer: " + str(data.score[1]))
            data.data.append(data.gameList)
            total.updateAll(data.gameList, data.d1)
            total.updateMarkov(data.gameList, data.d1)
            dataB.set(total.printData())
            data.gameList = []
        else:
            winLose.set("You Lose.")
            data.whoStart = 1
            print(data.whoStart)
            data.score[1] += 1
            scoreB.set(
                "Player: " + str(data.score[0]) + "     Computer: " + str(data.score[1]))
            data.data.append(data.gameList)
            total.updateAll(data.gameList, data.d1)
            total.updateMarkov(data.gameList, data.d1)
            dataB.set(total.printData())
            data.gameList = []
            

def openBtn():
    openB = Button(diceFrame, text='Open', bd='10', command= fin)
    openB.place(relx=0.75, rely=0.875, anchor=CENTER)


openBtn()

userGInputEntry = Entry(diceFrame)
userGInputEntry.place(relx=0.5, rely=0.775, anchor=CENTER)

def getUserInput():
    print(userGInputEntry.get())
    return userGInputEntry.get()

# Create Confirm Input Button
def confirmInput():
    btn = Button(diceFrame, text='Confirm Move', bd='10', command=lambda: do(inputCheck))
    btn.place(relx=0.3, rely=0.875, anchor=CENTER)


confirmInput()

print("x")


# window.update()
window.mainloop()
