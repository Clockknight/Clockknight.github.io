import sys
import time
import datetime
import tkinter

switchStatus = 'Start'
seconds = 900

def test():
    print('test')

#Create main GUI for user
mainGui = tkinter.Tk(screenName=None,  baseName=None,  className='Tk',  useTk=1)
mainGui.title('Pomodoro Timer')

#Button to toggle timer
switchButton = tkinter.Button(mainGui, text=switchStatus, width=25, command=test())
switchButton.pack() #Button Layout

#Keep GUI from closing as soon as it starts
mainGui.mainloop()
