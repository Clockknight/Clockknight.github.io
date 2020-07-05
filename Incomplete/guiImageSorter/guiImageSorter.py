import os
import sys
import shutil
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

class App():

    def __init__(self):
        #Setting up settings about the window
        self.root = tk.Tk(className='Clockknight\'s Image Sorter')
        self.root.geometry('1280x720')

        #Setting up variables
        self.dirTarget = '.'
        self.targetImage = ''
        self.imageArray = []
        self.okayFileTypes = {'.png', '.jpg', '.gif'}

        #Groups of elements, will pack under either of these empty labels
        self.elemGroup1 = tk.Label()
        self.elemGroup1.place(anchor='nw')
        self.elemGroup2 = tk.Label()
        self.elemGroup2.pack(side='right')

        #Textbox to input duration of timer
        self.dirHeader = tk.Label(self.elemGroup1, text="\nInput target directory here:")
        self.dirHeader.pack()
        self.dirTextbox = tk.Entry(self.elemGroup1, textvariable=self.dirTarget)
        self.dirTextbox.pack()
        #Button to input time in minutes
        self.inputButton = tk.Button(self.elemGroup1, text='Input new directory to sort', command=self.inputDirectory)
        self.inputButton.pack()
        self.targetDirLabel = tk.Label(self.elemGroup1, text=self.dirTarget)
        self.targetDirLabel.pack()
        self.startButton = tk.Button(self.elemGroup1, text='Start Sorting', command=self.startSorting)
        self.startButton.pack()
        self.skipButton = tk.Button(self.elemGroup2, text='Skip Image', command=self.updateImage,height=5, state='disabled', width=15)
        self.skipButton.pack()

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
                #create button labelled with current subfolder
                self.arrayButton = tk.Button(self.elemGroup2, text=object, height=5, state='disabled', width=15)

                #Add variables to arrays
                self.dirArray.append(self.dirTarget + '\\' + object)
                self.buttonArray.append(self.arrayButton)
                self.arrayButton.pack()

        #For loop to configure all directory buttons, once they've been generated
        for index in range(0, len(self.buttonArray)):
            #Set it to call targetMove with it's label as an extra variable
            self.buttonArray[index].configure(command=lambda index=index: self.targetMove(str(self.dirArray[index])))

    #Will begin opening image files on main canvas, and also enable all buttonArray buttons
    def startSorting(self):
        #Enable each button in buttonArray
        for button in self.buttonArray:
            button.configure(state='normal')

        #Select viable images in the directory, by first looking through all images
        for root, dir, files in os.walk(self.dirTarget, topdown=False):
            for file in files:
                #Check file type against filetypes in okayFileTypes dictionary
                if file[-4:].lower() in self.okayFileTypes:
                    self.imageArray.append(self.dirTarget + '\\' + file)

        #Disable the new directory/start sorting button while sorting images
        self.inputButton.configure(state='disabled')
        self.startButton.configure(state='disabled')
        self.skipButton.configure(state='normal')

        #Select and display the first available image in the image array
        self.targetImage = self.imageArray[0]
        self.targetIndex = 0
        self.currentImage = tk.PhotoImage(file=self.targetImage)
        self.imageLabel = tk.Label(image=self.currentImage)
        self.imageLabel.pack()

    #Functions that change currently displayed image
    #Should move currently selected file into button's target
    def targetMove(self, test):
        #Move image file
        targetFile = self.targetImage
        shutil.move(targetFile, test)

        #Update variables and arrays
        del self.imageArray[self.targetIndex]
        self.targetIndex -= 1 #Adjusted so updateImage doesn't skip the next image

        #Update image display
        self.updateImage()

    def updateImage(self):
        #Update variables
        self.imageArrayMax = len(self.imageArray) - 1
        if self.targetIndex != self.imageArrayMax:
            self.targetIndex += 1
        else:
            self.targetIndex = 0

        if self.imageArrayMax != 0:
            self.targetImage = self.imageArray[self.targetIndex]
            self.targetLoad = Image.open(self.targetImage)

            #Update imageLabel
            self.currentImage = ImageTk.PhotoImage(self.targetLoad)
            self.imageLabel.configure(image=self.currentImage)
        else:

app = App()
