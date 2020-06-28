import os
import sys
import tkinter as tk

class App():

    def __init__(self):
        self.root = tk.Tk(className='Clockknight\'s Image Sorter')
        self.root.geometry('1024x576')

        self.dirArray = []
        self.dirTarget = '.'

        #Textbox to input duration of timer
        self.dirHeader = tk.Label(text="\nInput target directory here:")
        self.dirHeader.pack()
        self.dirTextbox = tk.Entry(textvariable=self.dirTarget)
        self.dirTextbox.pack()
        #Button to input time in minutes
        self.inputButton = tk.Button(text='Input', command=self.inputDirectory)
        self.inputButton.pack()

        self.generateButtons()
        self.root.mainloop()

    def inputDirectory(self):
        self.dirTarget = self.dirTextbox.get()
        self.dirTextbox.delete(0, len(givenDuration)+1)

    def generateButtons(self):
        #Fill array with items
        #Clear old array
        self.dirArray = []
        for root, dir, files in os.walk(self.dirTarget, topdown=False):
            print(dir)

        #Create buttons based on those items
        print(self.dirArray)

app = App()
