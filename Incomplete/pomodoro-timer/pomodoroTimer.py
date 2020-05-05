import sys
import time
import tkinter

switchStatus = 'Start'
seconds = 900

#Create main GUI for user
mainGui = tkinter.Tk(screenName=None,  baseName=None,  className='Tk',  useTk=1)
mainGui.title('Pomodoro Timer')

#Button to toggle timer
switchButton = tkinter.Button(mainGui, text=switchStatus, width=25, command=mainGui.destroy)
switchButton.pack() #Button Layout

#Keep GUI from closing as soon as it starts
mainGui.mainloop()
