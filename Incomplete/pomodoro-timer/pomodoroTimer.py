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
        self.updateNow()
        self.button.configure(text='Stop', command=self.stopTimer)

    def stopTimer(self):
        self.button.configure(text='Start', command=self.startTimer)

    def tickUpdate(self):
        #Set timer label to now
        self.label.configure(text=self.timeLeft)
        #Run this function again every second, if the timer isnt up
        if self.timeLeft != self.timeOver:
            self.root.after(1000, self.tickUpdate)

    def updateNow(self):
        self.now = datetime.datetime.now()
        self.startTime = self.now

    def timerEnd(self):
        self.timeLeft = self.duration
        app.focus()

app = App()
