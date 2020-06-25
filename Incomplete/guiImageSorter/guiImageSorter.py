import os
import sys
import tkinter as tk

class App():

    def __init__(self):
        self.root = tk.Tk(className='Clockknight\'s Image Sorter')
        self.root.geometry('1024x576')

        self.dirArray = []
        self.dirTarget = '\\testDirectory'
        self.root.mainloop()

    def generateButtons(self):
        #Fill array with items
        #Clear old array
        self.dirArray = []
        for root, dir, files in os.walk(self.dirTarget):
            print(root)

        #Create buttons based on those items
        print('filler')


app = App()
