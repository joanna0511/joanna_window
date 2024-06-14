from tkinter import Tk, Canvas, Frame, BOTH

class Example(Frame):
    
    def __init__(self,master):
        super().__init__(master)
        self.initUI()
        self.master.title("Lines")
        self.pack(fill=BOTH,expand=1)

    def initUI(self):
        canvas=Canvas(self)
        canvas.create_line(15,30,200,30)
        canvas.create_line(55,85,155,85,105,180,55,85)
        canvas.pack(fill=BOTH,expand=1)

def main():

    root=Tk()
    ex=Example(root)
    root.geometry("400X250+300+300")
    root.mainloop()

if __name__=="main__":
    main()
