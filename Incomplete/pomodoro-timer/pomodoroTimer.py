import sys
import time
import tkinter as tk

#Using time, create variable of "current" time
now = time.strftime("%H:%M:%S")

class App():



    def __init__(self):
        #Create main GUI for user
        self.root = tk.Tk()
        #Timer for user to view
        self.label = tk.Label(text="")
        self.label.pack()
        #Button to toggle timer
        self.button = tk.Button(text='Start', command=self.root.destroy)#Change command after things work
        self.button.pack()
        self.tickUpdate()
        self.root.mainloop()

    def tickUpdate(self):
        #Set timer label to now
        self.label.configure(text=now)
        #Run this function again every second
        self.root.after(1000, self.tickUpdate)


app = App()
