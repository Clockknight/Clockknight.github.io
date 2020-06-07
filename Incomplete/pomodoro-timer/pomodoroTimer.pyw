import sys
import time
import datetime
import tkinter as tk
from tkinter import StringVar

#Using time, create variable of "current" time


class App():

    def __init__(self):
        #Create main GUI for user
        self.root = tk.Tk()
        self.inputVariable = tk.StringVar()

        #Initializing variables for apps
        self.timeOver = datetime.timedelta(seconds=0)
        self.duration = datetime.timedelta(minutes=15)
        self.timeLeft = self.duration

        self.timerActive = False

        #Timer for user to view
        self.HEADER1 = tk.Label(text="Time Left")
        self.HEADER1.pack()
        self.label = tk.Label(text="")
        self.label.pack()
        #Button to toggle timer
        self.button = tk.Button(text='Start', command=self.startTimer)
        self.button.pack()
        #Button to reset timer
        self.resetButton = tk.Button(text='Reset', command=self.resetTimeLeft)
        self.resetButton.pack()

        #Textbox to input duration of timer
        self.HEADER2 = tk.Label(text="\nInput time in minutes here:")
        self.HEADER2.pack()
        self.durationTextbox = tk.Entry(textvariable=self.inputVariable)
        self.durationTextbox.pack()
        #Button to input time in minutes
        self.inputButton = tk.Button(text='Input', command=self.inputDuration)
        self.inputButton.pack()

        self.tickUpdate()
        self.root.mainloop()

    #Timer label functions
    def startTimer(self):
        self.timerActive = True
        self.button.configure(text='Stop', command=self.stopTimer)

    def stopTimer(self):
        self.timerActive = False
        self.button.configure(text='Start', command=self.startTimer)

    def timerEnd(self):
        self.timeLeft = self.duration
        self.timerActive = False
        self.button.configure(text='Start', command=self.startTimer)
        self.focus()

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

    #Reset time left to duration
    def resetTimeLeft(self):
        self.timeLeft = self.duration

    #Change duration based on input
    def inputDuration(self):
        givenDuration = self.durationTextbox.get()
        self.durationTextbox.delete(0, len(givenDuration)+1)
        if givenDuration.isnumeric():
            print('s')
            self.timerEnd()
        else:
            self.durationTextbox.insert(0, 'Non-numerical input.')

app = App()
