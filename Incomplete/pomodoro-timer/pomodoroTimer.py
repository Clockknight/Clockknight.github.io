import sys
import time
import datetime
import tkinter as tk

#Using time, create variable of "current" time


class App():
    now = datetime.datetime.now()
    startTime = now

    timeOver = datetime.timedelta(seconds=0)

    duration = datetime.timedelta(minutes=15)
    timeLeft = duration

    def __init__(self):
        #Create main GUI for user
        self.root = tk.Tk()
        #Timer for user to view
        self.label = tk.Label(text="")
        self.label.pack()
        #Button to toggle timer
        self.button = tk.Button(text='Start', command=self.startTimer)
        self.button.pack()

        self.tickUpdate()

        self.root.mainloop()


    def startTimer(self):
        updateNow()
        self.button.configure(text='Stop', command=self.stopTimer)

    def stopTimer(self):
        self.button.configure(text='Start', command=self.startTimer)

    def tickUpdate(self):
        #Set timer label to now
        self.label.configure(text=timeLeft)
        #Run this function again every second, if the timer isnt up
        if timeLeft != timeOver:
            self.root.after(1000, self.tickUpdate)

    def updateNow(self):
        now = datetime.datetime.now()
        startTime = now

    def timerEnd(self):
        timeLeft = duration
        app.focus()

app = App()
