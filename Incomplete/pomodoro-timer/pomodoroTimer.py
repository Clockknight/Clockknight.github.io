import sys
import time
import datetime
import tkinter as tk

#Using time, create variable of "current" time


class App():


    def __init__(self):
        #Initializing variables for apps
        self.now = datetime.datetime.now()
        self.startTime = self.now

        self.timeOver = datetime.timedelta(seconds=0)

        self.duration = datetime.timedelta(minutes=15)
        self.timeLeft = self.duration

        self.timerActive = False

        #Create main GUI for user
        self.root = tk.Tk()
        #Timer for user to view
        self.label = tk.Label(text="")
        self.label.pack()
        #Button to toggle timer
        self.button = tk.Button(text='Start', command=self.startTimer)
        self.button.pack()
        #Button to reset timer
        self.resetButton = tk.Button(text='Reset', command=self.resetNow)
        self.button.pack()
        #Textbox to input duration of timer
        self.durationTextbox = tk.Entry(self)
        self.durationTextbox.pack()

        self.tickUpdate()

        self.root.mainloop()

    #Timer label functions
    def startTimer(self):
        self.updateNow()
        self.timerActive = True
        self.button.configure(text='Stop', command=self.stopTimer)

    def stopTimer(self):
        self.timerActive = False
        self.button.configure(text='Start', command=self.startTimer)

    def timerEnd(self):
        self.timeLeft = self.duration
        self.timerActive = False
        self.button.configure(text='Stop Timer', command=self.stopTimer)
        app.focus()

    #Variable update functions
    def tickUpdate(self):
        #Set timer label to now
        self.label.configure(text=self.timeLeft)
        if self.timerActive == True:
            self.timeLeft -= datetime.timedelta(seconds=1)
        #Run this function again every second, if the timer isnt up
        if self.timeLeft != self.timeOver:
            self.root.after(1000, self.tickUpdate)
        else:
            self.timerEnd()

    def updateNow(self):
        self.now = datetime.datetime.now()
        self.startTime = self.now

    def resetDuration(self):
        self.duration = datetime.timedelta(minutes=15)


app = App()
