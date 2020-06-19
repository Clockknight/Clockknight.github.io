import sys
import time
import datetime
import simpleaudio
import tkinter as tk
from tkinter import StringVar

class App():

    def __init__(self):
        #Create main GUI for user
        self.root = tk.Tk(className='Clockknight\'s Pomodoro Timer')
        self.root.geometry('400x250')
        self.inputVariable = tk.StringVar()

        #Initializing variables for apps
        self.timeOver = datetime.timedelta(seconds=0)
        self.duration = datetime.timedelta(minutes=15)
        self.timeLeft = self.duration

        self.timerActive = False

        #Timer for user to view
        self.HEADER1 = tk.Label(text="Time Left")
        self.HEADER1.pack()
        self.label = tk.Label(text=self.timeLeft)
        self.label.pack()
        #Button to toggle timer
        self.button = tk.Button(text='Start', command=self.startTimer)
        self.button.pack()
        #Button to reset timer
        self.resetButton = tk.Button(text='Reset', command=self.endTimer)
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
    #Timer begins, working with whatever time is left
    def startTimer(self):
        self.timerActive = True
        self.button.configure(text='Stop', command=self.stopTimer)

    #Timer is paused, freezing on some time
    def stopTimer(self):
        self.timerActive = False
        self.button.configure(text='Start', command=self.startTimer)

    #Timer ends, and resets time left
    def endTimer(self):
        self.resetTimeLeft()
        self.label.configure(text=self.timeLeft)
        self.timerActive = False
        self.button.configure(text='Start', command=self.startTimer)


    #Update timeleft and the timer
    def tickUpdate(self):
        #Set timer label to now
        if self.timerActive == True:
            if self.timeLeft > datetime.timedelta(seconds=0):
                self.timeLeft -= datetime.timedelta(seconds=1)
        self.label.configure(text=self.timeLeft)
        #Run this function again every second, if the timer isnt up
        if self.timeLeft == self.timeOver:
            self.button.configure(command=self.endTimer)
        self.root.after(1000, self.tickUpdate)

#Variable update functions
    #Reset time left to match duration
    def resetTimeLeft(self):
        self.timeLeft = self.duration

    #Change duration based on input
    def inputDuration(self):
        givenDuration = self.durationTextbox.get()
        self.duration = datetime.timedelta(minutes=int(givenDuration))
        self.durationTextbox.delete(0, len(givenDuration)+1)

        if givenDuration.isnumeric():
            self.endTimer()

        else:
            self.durationTextbox.insert(0, 'Non-numerical input.')

app = App()
