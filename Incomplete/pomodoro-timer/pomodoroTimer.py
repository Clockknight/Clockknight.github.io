import sys
import time
import tkinter

switchStatus = 'Start'
seconds = 900

#Create main GUI for user
mainGui = tkinter.Tk(screenName=None,  baseName=None,  className='Tk',  useTk=1)
mainGui.title('Pomodoro Timer')

switchButton = tkinter.Button(mainGui, text=switchStatus, width=25, command=mainGui.destroy)
switchButton.pack() #Selecting the layout of the button

mainGui = Label(master, option=str(seconds))

#Keep GUI from closing as soon as it starts
mainGui.mainloop()
