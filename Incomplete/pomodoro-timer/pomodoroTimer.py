import sys
import time
import tkinter as tk

#Using time, create variable of "current" time
duration = '00:15:00'
timeLeft = '00:15:00'
now = time.strftime("%H:%M:%S")
startTime = now

class App():

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
        test()
        self.button.configure(text='Stop', command=self.stopTimer)

    def stopTimer(self):
        self.button.configure(text='Start', command=self.startTimer)


    def tickUpdate(self):
        #Set timer label to now
        self.label.configure(text=timeLeft)
        #Run this function again every second

        self.root.after(1000, self.tickUpdate)

def test():
    now = time.strftime("%H:%M:%S")
    startTime = now

def timerEnd():
    timeLeft = duration
    app.focus()

app = App()
