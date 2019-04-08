import curses
import time
import threading

class SuperTyper:

    def __init__(self):
        self.screen = curses.initscr()
        self.screen.keypad(1)
        curses.noecho()
        self.height, self.width = self.screen.getmaxyx()
        self.pad = curses.newpad(self.height, self.width)
        self.text = ""
        self.my_msg = ""
        self.stop = False
        threading._start_new_thread(self.startDrawingThread, ())
        self.hintWord   = ""
        self.levelWord  = ""
        self.remainWord = ""
        self.titleWord  = ""
        self.answers    = []
    
    def getTime(self):
        return None

    def drawFrame(self, title):

        for y in range(1, self.height-1):
            self.pad.addch(y, 1, "|")
            self.pad.addch(y, self.width-2, "|")

        for x in range(1, self.width-1):
            self.pad.addch(1, x, "=")
            self.pad.addch(self.height-2, x, "=")

        start = self.width // 2 - len(title) // 2
        for w in range(len(title)):
            self.pad.addch(1, w + start, title[w])

    def updateTimer(self, percentageFunc):
        percentage = percentageFunc()
        if percentage == None:
            for x in range(2, self.width-2):
                self.pad.addch(self.height-4, x, " ")
        else:
            if percentage < 0:
                percentage = 0
            if percentage > 100:
                percentage = 100
            currentPercentage = ("%3d" % percentage) + "%"
            availableWidth = (self.width-8-7+1) * percentage // 100
            self.pad.addch(self.height-4, 4, "[")
            self.pad.addch(self.height-4, self.width-9, "]")
            for x in range(4):
                self.pad.addch(self.height-4, self.width-8 + x, currentPercentage[x])
            for x in range(availableWidth):
                self.pad.addch(self.height-4, 5+x, "=")
    
    def showLine(self, lineNum, line):
        lineLimit = self.width - 10
        lineStart = 5
        estLineNum = len(line) // lineLimit
        if len(line) % lineLimit:
            estLineNum += 1
        for y in range(estLineNum):
            for x in range(2, self.width-2):
                self.pad.addch(y+lineNum, x, " ")
            for x in range(lineLimit):
                if x+y*lineLimit >= len(line):
                    break
                self.pad.addch(y+lineNum, x+5, line[x+y*lineLimit])
        return lineNum + estLineNum

    def setQuestion(self, hint, level, remain, title, answers):
        self.hintWord   = hint
        self.levelWord  = "Current Level: %s." % level
        self.remainWord = "You Have %s Chances to Get Help." % remain
        self.titleWord  = "Q: %s?" % title
        self.answers    = answers
        
        self.drawQuestion()
        

    def drawQuestion(self):
        line = 3
        line = 1 + self.showLine(line, self.hintWord)
        line = self.showLine(line, self.levelWord)
        line = 1 + self.showLine(line, self.remainWord)
        line = 1 + self.showLine(line, self.titleWord)

        for q in self.answers:
            line = self.showLine(line, q)

    def goCursur(self):
        for x in range(2, self.width-2):
            self.pad.addch(self.height-6, x, " ")
        self.pad.addch(self.height-6, 4, ">")
        self.pad.addch(self.height-6, 5, " ")
        for x in range(len(self.text)):
            self.pad.addch(self.height-6, 6+x, self.text[x])

    def clear(self):
        self.screen.clear()
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.pad.addch(y, x, " ")

    def startDrawingThread(self):
        while True:
            if self.stop:
                break
            self.clear()
            self.drawFrame("    Conqueroring Finance    ")
            self.updateTimer(self.getTime)
            self.drawQuestion()
            self.goCursur()
            self.pad.refresh(0, 0, 0, 0, self.height, self.width)
            time.sleep(0.01)

    def fetchMessage(self):
        tempMsg = self.my_msg
        self.my_msg = ""
        return tempMsg

    def run(self):
        while True:
            if self.stop:
                break
            theInput = self.screen.getch()
            if (theInput >= ord('A') and theInput <= ord('Z')) or (theInput >= ord('a') and theInput <= ord('z')) or (theInput >= ord('0') and theInput <= ord('9')):
                self.text += chr(theInput)
            elif theInput == 10:
                self.my_msg = self.text
                self.text = ""
            elif theInput == 127:
                self.text = self.text[:-1]
            # else:
            #     self.text += str(theInput)
            time.sleep(0.01)
            
        curses.echo()
        curses.endwin()
    
    def stop():
        self.stop = True

if __name__ == "__main__":
    
    def addTime():
        global currentTime
        while True:
            if currentTime < 100:
                currentTime += 1
            time.sleep(1)

    threading._start_new_thread(addTime, ())

    typer = SuperTyper()
    typer.setQuestion("Please Choose One Question (Type next to switch to another Question,  go to choose current Question) QwQ:", 1, 3, "Is CS Better Than Fanance?", ["A: Yes, Definitely", "B: Well, Maybe Yes", "C: Oh, Yes!"])

    typer.run()

