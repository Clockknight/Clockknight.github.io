import os
import sys
import tkinter as tk
import numpy as np

class App():

    def __init__(self):
        self.root = tk.Tk(className='Clockknight\'s Image Sorter')
        self.root.geometry('1024x576')

        self.dirTarget = '.'

        #Textbox to input duration of timer
        self.dirHeader = tk.Label(text="\nInput target directory here:")
        self.dirHeader.pack()
        self.dirTextbox = tk.Entry(textvariable=self.dirTarget)
        self.dirTextbox.pack()
        #Button to input time in minutes
        self.inputButton = tk.Button(text='Input', command=self.inputDirectory)
        self.inputButton.pack()
        self.targetDirLabel = tk.Label(text=self.dirTarget)
        self.targetDirLabel.pack()

        self.generateButtons()
        self.root.mainloop()

    def inputDirectory(self):
        newTarget = self.dirTextbox.get()
        self.dirTarget = newTarget
        self.dirTextbox.delete(0, len(self.dirTarget)+1)
        self.generateButtons()

    def generateButtons(self):
        #Fill array with items
        #Clear old variables
        self.dirArray = []
        self.dirDict = {}
        self.dirIndex = 0
        #Reset target directory label
        self.targetDirLabel.configure(text=self.dirTarget)

        #Add each subfolder to the directory array
        for root, dir, files in os.walk(self.dirTarget, topdown=False):
            for object in dir:
                self.dirArray.append(object)
                self.arrayButton = tk.Button(text=object, command=self.buttonTest)
                self.arrayButton.pack()
                self.dirIndex += 1


    def buttonTest(self):
        print('text')

        #Create buttons based on those items
        print(self.dirArray)

app = App()
