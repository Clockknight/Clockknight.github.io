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
        self.okayFileTypes = {'.png', '.jpg', '.jpeg', '.gif'}
        self.moveArray = []
        self.size = 500

        #Groups of elements, will pack under either of these empty labels
        self.elemGroup1 = tk.Label()
        self.elemGroup1.place(anchor='nw')
        self.elemGroup2 = tk.Label()
        self.elemGroup2.pack(side='right')
        self.elemGroup3 = tk.Label()
        self.elemGroup3.pack(side='right')

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
        self.stopButton = tk.Button(self.elemGroup1, text='Stop Sorting', command=self.stopSorting, state='disabled')
        self.stopButton.pack()

        self.undoAllButton = tk.Button(self.elemGroup2, text='Undo ALL moves', command=self.undoAll, height=5, width=15)
        self.undoAllButton.pack()
        self.undoButton = tk.Button(self.elemGroup2, text='Undo ONE move', command=self.undo, height=5, width=15)
        self.undoButton.pack()
        self.delButton = tk.Button(self.elemGroup2, text='Delete Image', command=self.delImage, height=5, width=15)
        self.delButton.pack()
        self.nextButton = tk.Button(self.elemGroup2, text='Last Image', command=self.updateImage, height=5, state='disabled', width=15)
        self.nextButton.pack()
        self.lastButton = tk.Button(self.elemGroup2, text='Next Image', command=self.lastImage, height=5, state='disabled', width=15)
        self.lastButton.pack()
        self.shrinkButton = tk.Button(self.elemGroup2, text='Shrink by 100px', command=self.shrink, state='disabled', width=15)
        self.shrinkButton.pack()
        self.growButton = tk.Button(self.elemGroup2, text='Grow by 100px', command=self.grow, width=15)
        self.growButton.pack()
        self.sizeLabel = tk.Label(self.elemGroup2, text='Current image size: 500x500px.')
        self.sizeLabel.pack()

        self.imageLabel = tk.Label()
        self.imageLabel.pack()

        self.generateButtons()
        self.root.mainloop()

    #Function to take new directory, delete old buttons, then call generateButton
    def inputDirectory(self):
        self.dirTarget =  self.dirTextbox.get()#Change variable to textbox text
        self.dirTextbox.delete(0, len(self.dirTarget)+1)#Clear textbox text
        self.imageLabel.configure(text='')#Clear imageLabel in case it isnt already empty
        #Clear old buttons, stored in the array
        for button in self.buttonArray:
            button.destroy()

        self.generateButtons()#Generate buttons based on new directory

    def shrink(self):
        self.size -= 100
        self.growButton.configure(state='normal')

        if self.size == 500:
            self.shrinkButton.configure(state='disabled')

        self.resizeFunc()
    def grow(self):
        self.size += 100
        self.shrinkButton.configure(state='normal')

        if self.size == 1600:
            self.growButton.configure(state='disabled')

        self.resizeFunc()
    def resizeFunc(self):
        self.sizeLabel.configure(text='Current image size: ' + str(self.size) + 'x' + str(self.size) + 'px.')
        self.targetIndex -= 1
        self.updateImage()

    def undo(self):
        #x represents the file's new home, and y the file's old source
        x = len(self.moveArray) - 2
        y = x + 1


        print(self.moveArray[x])
        print(self.moveArray[y])

        shutil.move(self.moveArray[x], self.moveArray[y])

        del self.moveArray[x]
        del self.moveArray[x]

        self.targetIndex -= 1

        self.updateArray()
        self.updateImage()
    def undoAll(self):
        arrayLen = int(len(self.moveArray) / 2)#Get half of length of array (guaranteed to be an even number)

        for index in range(arrayLen):
            x = index * 2
            y = x + 1
            shutil.move(self.moveArray[x], self.moveArray[y])

        self.moveArray = []
        self.targetIndex = 0

        self.stopSorting()

    #Clears all variables and then makes buttons based on subdirectories
    def generateButtons(self):
        #Clear old variables
        self.dirArray = []
        self.buttonArray = []
        #Reset target directory label
        self.targetDirLabel.configure(text=self.dirTarget)

        #Add each subfolder to the directory array
        for directory in os.scandir(self.dirTarget):
            if directory.is_dir():
                object = directory.name
                #create button labelled with current subfolder
                self.arrayButton = tk.Button(self.elemGroup3, text=object, height=3, state='disabled', width=15)

                #Add variables to arrays
                self.dirArray.append(self.dirTarget + '\\' + object)
                self.buttonArray.append(self.arrayButton)
                self.arrayButton.pack()

        #For loop to configure all directory buttons, once they've been generated
        for index in range(0, len(self.buttonArray)):
            #Set it to call targetMove with it's label as an extra variable
            self.buttonArray[index].configure(command=lambda index=index: self.targetMove(str(self.dirArray[index])))

    def updateArray(self):
        self.imageArray = []

        #Select viable images in the directory, by first looking through all images
        for folder, dir, files in os.walk(self.dirTarget, topdown=False):
            for file in files:
                if folder == self.dirTarget:
                    #Check file type against filetypes in okayFileTypes dictionary
                    if file[-4:].lower() in self.okayFileTypes:
                        self.imageArray.append(self.dirTarget + '\\' + file)


    #Will begin opening image files on main canvas, and also enable all buttonArray buttons
    def startSorting(self):
        self.updateArray()

        #Only do the following things if the image array isn't empty
        if len(self.imageArray) > 0:
            #Disable the new directory/start sorting button while sorting images
            self.inputButton.configure(state='disabled')
            self.startButton.configure(state='disabled')

            self.stopButton.configure(state='normal')
            self.delButton.configure(state='normal')
            self.nextButton.configure(state='normal')
            self.lastButton.configure(state='normal')
            for button in self.buttonArray:
                button.configure(state='normal')

            #Select and display the first available image in the image array
            self.targetImage = self.imageArray[0]
            self.targetIndex = 0
            self.currentImage = tk.PhotoImage(file=self.targetImage)
            self.imageLabel.configure(text='', image=self.currentImage)

        else:
            self.imageLabel.configure(text='No images to sort in the given directory!')
    #Function to stop the program once everything has been sorted
    def stopSorting(self):
        self.inputButton.configure(state='normal')
        self.startButton.configure(state='normal')

        self.stopButton.configure(state='disabled')
        self.delButton.configure(state='disabled')
        self.nextButton.configure(state='disabled')
        self.lastButton.configure(state='disabled')
        for button in self.buttonArray:
            button.configure(state='disabled')

        self.imageLabel.configure(image='')
        if len(self.imageArray) == 0:
            self.imageLabel.configure(text='No more movable files in this directory!')

    #Functions that change currently displayed image
    #Should move currently selected file into button's target
    def targetMove(self, inputTarget):
        #Move image file
        inputTarget = os.path.abspath(inputTarget)
        targetFile = os.path.abspath(self.targetImage)

        #Get relevant piece of targetFile, then append all strings to moveArray
        filename = os.path.basename(targetFile)
        self.moveArray.append(inputTarget + '\\' + filename)
        self.moveArray.append(targetFile)

        shutil.move(targetFile, inputTarget)

        #Update variables and arrays
        del self.imageArray[self.targetIndex]
        self.targetIndex -= 1 #Adjusted so updateImage doesn't skip the next image



        #Update image display
        self.updateImage()

    #Reduces target index before calling updateImage
    def lastImage(self):
        self.targetIndex -= 2
        self.updateImage()
    #Deletes currently viewed image, and removes image object from the array
    def delImage(self):
        x = self.targetIndex

        filename = os.path.abspath(self.imageArray[x])
        os.remove(filename)

        del self.imageArray[x]

        self.targetIndex -= 1
        self.updateImage()

    #Updates the target index before updating the image
    def updateImage(self):
        #Update variables
        self.imageArrayMax = len(self.imageArray) - 1
        if self.targetIndex != self.imageArrayMax:
            self.targetIndex += 1
        else:
            self.targetIndex = 0

        if self.imageArrayMax != -1:
            self.targetImage = self.imageArray[self.targetIndex]
            self.targetLoad = Image.open(self.targetImage)
            self.targetLoad = self.targetLoad.resize((self.size, self.size), Image.ANTIALIAS)

            #Update imageLabel
            self.currentImage = ImageTk.PhotoImage(self.targetLoad)
            self.imageLabel.configure(image=self.currentImage)
        else:
            self.imageLabel.configure(text='No more movable files in this directory!', image='')
            self.stopSorting()

app = App()
