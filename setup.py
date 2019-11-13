"""This program displays the first window that sets up the minesweeper game and runs the animation for the main game
window"""

from tkinter import *
from project.MSGUI import GUI


class Settings:
    def __init__(self, window):
        
        self.window = window
        self.widthnum = StringVar()
        self.heightnum = StringVar()
        self.bombnum = StringVar()
        self.err = StringVar()
        
        label1 = Label(window, text="Welcome to Multiplayer Minesweeper!")
        label1.grid(row=0, column=0, columnspan=3, sticky=W, padx=20)
        label2 = Label(window, text="Input your desired settings.")
        label2.grid(row=1, column=0, columnspan=3, sticky=W, padx=20)
        
        width_label = Label(window, text="Board Width:")
        width_label.grid(row=2, column=0, sticky=E, padx=10)
        length_label = Label(window, text="Board Length:")
        length_label.grid(row=3, column=0, sticky=E, padx=10)
        bomb_label = Label(window, text="Bomb Count:")
        bomb_label.grid(row=4, column=0, sticky=E, padx=10)
        
        # entries for width, height, and bomb count
        width_entry = Entry(window, width=6, textvariable=self.widthnum)
        width_entry.grid(row=2, column=1, sticky=W)
        height_entry = Entry(window, width=6, textvariable=self.heightnum)
        height_entry.grid(row=3, column=1, sticky=W)
        bomb_entry = Entry(window, width=6, textvariable=self.bombnum)
        bomb_entry.grid(row=4, column=1, sticky=W)

        defaultbutton = Button(window, text="Set defaults", command=self.setdefault)
        defaultbutton.grid(row=3, column=3, sticky=W, padx=10)
       
        startbutton = Button(window, text="Start game!", command=self.startgame)
        startbutton.grid(row=4, column=3, sticky=W, padx=10)
        
        errormsg = Label(window, textvariable=self.err)
        errormsg.grid(row=5, column=0, columnspan=3)

    def startgame(self):
        """Tests for all possible issues and displays error message on window if issue is found"""
        try:
            self.widthnum.set(int(self.widthnum.get()))
            self.heightnum.set(int(self.heightnum.get()))
            self.bombnum.set(int(self.bombnum.get()))
        except ValueError:
            self.err.set("Invalid entry, try again.")
        if int(self.widthnum.get()) < 10:
            self.err.set("Width lower than 10, try again.")
            raise ValueError("Width lower than 10, try again.")
        elif int(self.widthnum.get()) > 30:
            self.err.set("Width greater than 30, try again.")
            raise ValueError("Width greater than 30, try again.")
        elif int(self.heightnum.get()) < 10:
            self.err.set("Height lower than 10, try again.")
            raise ValueError("Height lower than 10, try again.")
        elif int(self.heightnum.get()) > 30:
            self.err.set("Height greater than 30, try again.")
            raise ValueError("Height greater than 30, try again.")
        elif int(self.bombnum.get()) < 5:
            self.err.set("Bomb count lower than 5, try again.")
            raise ValueError("Bomb count lower than 5, try again.")
        elif int(self.bombnum.get())/int(self.heightnum.get())/int(self.widthnum.get()) > .3:
            raise ValueError("Too many bombs set to board, try again.")
        else:
            '''Destroys setup window and runs the main window with the given inputs'''
            root.destroy()
            guiroot = Tk()
            print(self.bombnum.get())
            guiroot.title('Multiplayer Minesweeper')
            guiroot = GUI(guiroot, int(self.widthnum.get()), int(self.heightnum.get()), int(self.bombnum.get()))

    def setdefault(self):
        self.widthnum.set(16)
        self.heightnum.set(16)
        self.bombnum.set(40)


if __name__ == '__main__':
    root = Tk()
    app = Settings(root)
    root.title('Multiplayer Minesweeper Setup')
    root.mainloop()
