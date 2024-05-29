import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title("pack1")
        self.geometry('300x300')

        ttk.Button(self,text="大家排隊").pack()
        ttk.Button(self,text="A1").pack()
        ttk.Button(self,text="A2").pack()
        ttk.Button(self,text="A3").pack()
        ttk.Button(self,text="A4").pack()



if __name__ == '__main__':
    window:Window = Window()
    window.mainloop()