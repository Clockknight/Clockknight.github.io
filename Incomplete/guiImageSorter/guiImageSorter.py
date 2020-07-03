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
        self.startButton = tk.Button(text='Start Sorting', command=self.startSorting)
        self.startButton.pack()
        self.targetDirLabel = tk.Label(text=self.dirTarget)
        self.targetDirLabel.pack()

        self.generateButtons()
        self.root.mainloop()

    #Function to take new directory, delete old buttons, then call generateButton
    def inputDirectory(self):
        newTarget = self.dirTextbox.get()
        self.dirTarget = newTarget
        self.dirTextbox.delete(0, len(self.dirTarget)+1)

        #Clear old buttons
        for button in self.buttonArray:
            button.destroy()
        self.generateButtons()

    #Clears all variables and then makes buttons based on subdirectories
    def generateButtons(self):
        #Clear old variables
        self.dirArray = []
        self.buttonArray = []
        #Reset target directory label
        self.targetDirLabel.configure(text=self.dirTarget)

        #Add each subfolder to the directory array
        for root, dir, files in os.walk(self.dirTarget, topdown=False):
            for object in dir:
                #Add variables to arrays
                self.dirArray.append(object)
                #create button labelled with current subfolder
                self.arrayButton = tk.Button(text=object, height=5, width=15)
                self.buttonArray.append(self.arrayButton)
                self.arrayButton.pack()

        #For loop to configure all directory buttons, once they've been generated
        for index in range(0, len(self.buttonArray)):
            #Set it to call targetMove with it's label as an extra variable
            self.buttonArray[index].configure(command=lambda index=index: self.targetMove(str(self.dirArray[index])))

    #Should move currently selected file into button's target
    def targetMove(self, test):
        print(test)
        #Create buttons based on those items

    #Will begin opening image files on main canvas, and also enable all buttonArray buttons
    def startSorting(self):
        for button in self.buttonArray:

            print('null')

app = App()
