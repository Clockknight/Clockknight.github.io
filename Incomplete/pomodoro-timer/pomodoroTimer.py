import sys
import time
import tkinter as tk

switchStatus = 'Start'
seconds = 900

class App():
    def __init__(self):
        #Create main GUI for user
        self.root = tk.Tk()
        self.label = tk.Label(text="%H:%M:%S")
        self.label.pack()
        self.tickUpdate()
        self.root.mainloop()

        #Button to toggle timer
        switchButton = tk.Button(mainGui, text=switchStatus, width=25, command=mainGui.destroy)
        switchButton.pack() #Button Layout

    def tickUpdate(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.tickUpdate)


app = App()
