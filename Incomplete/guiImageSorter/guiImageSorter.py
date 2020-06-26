import os
import sys
import tkinter as tk

class App():

    def __init__(self):
        self.root = tk.Tk(className='Clockknight\'s Image Sorter')
        self.root.geometry('1024x576')

        self.dirArray = []
        self.dirTarget = '.'

        self.generateButtons()
        self.root.mainloop()

    def generateButtons(self):
        #Fill array with items
        #Clear old array
        self.dirArray = []
        for root, dir, files in os.walk(self.dirTarget, topdown=False):
            print(dir[0])

        #Create buttons based on those items
        print(self.dirArray)

app = App()
