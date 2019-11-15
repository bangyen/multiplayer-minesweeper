"""This is not the main program. To set desired board specifications in another window before playing, run setup.py
This program sets most of the methods for the Multiplayer Minesweeper game"""

from tkinter import *
from project.sweeper import *


class GUI:
    def __init__(self, window, width, height, bombs):
        self.window = window
        self.width = int(width)
        self.height = int(height)

        # creates object for helper functions
        self.sweep = Sweeper(window, width, height, bombs)
        
        '''Creates label and options for player 1'''
        p1label = Label(window, text="Player 1", bg='#FF0000')
        p1label.grid(row=0, column=0, columnspan=2, sticky=W)
        p1scorelabel = Label(window, textvariable=self.sweep.p1scorelbl)
        p1scorelabel.grid(row=1, column=0, columnspan=3, sticky=W)
        p1pass = Button(window, text="Pass", command=self.sweep.player1pass)
        p1pass.grid(row=2, column=0, columnspan=2, sticky=W)
        p1quit = Button(window, text="Quit", command=self.window.destroy)
        p1quit.grid(row=3, column=0, columnspan=2, sticky=W)
        
        '''Creates label and options for player 2'''
        p2label = Label(window, text="Player 2", bg='#3054C6')
        p2label.grid(row=0, column=width-2, columnspan=2, sticky=E)
        p2scorelabel = Label(window, textvariable=self.sweep.p2scorelbl)
        p2scorelabel.grid(row=1, column=width-3, columnspan=3, sticky=E)
        p2pass = Button(window, text="Pass", command=self.sweep.player2pass)
        p2pass.grid(row=2, column=width-2, columnspan=2, sticky=E)
        p2quit = Button(window, text="Quit", command=self.window.destroy)
        p2quit.grid(row=3, column=width-2, columnspan=2, sticky=E)

        statuslabel1 = Label(window, text="Timer:")
        statuslabel1.grid(row=0, column=int(width/2)-3, columnspan=3, rowspan=2)
        statuslabel3 = Label(window, textvariable=self.sweep.timer)
        statuslabel3.grid(row=2, column=int(width/2)-3, columnspan=3)
        
        '''Label for number of flags yet to be placed'''
        flaglabel = Label(window, text='Flags\nleft:')
        flaglabel.grid(row=0, column=int(width/2), rowspan=2, columnspan=3)
        flagnumlabel = Label(window, textvariable=self.sweep.flagsrem)
        flagnumlabel.grid(row=2, column=int(width/2), rowspan=1, columnspan=3)
        
        '''Label for the game's turn status and the win message'''
        winlabel = Label(window, textvariable=self.sweep.status, font='arial 10')
        winlabel.grid(row=3, column=0, rowspan=2, columnspan=self.width, sticky=S)
        
        '''Creates a range of buttons for the minesweeper board'''
        for y in range(height):
            for x in range(width):
                b = Button(window, width=2, height=1, command=self.sweep.click_event, bg='#BBBBBB')
                b.bind('<Button-3>', self.sweep.flag_event)
                b.grid(row=5+y, column=x)
                self.sweep.buttonlist.append(b)
        self.sweep.click_event()

        '''runs in loop until game terminated'''
        self.sweep.changetimer()


if __name__ == '__main__':
    guiroot = Tk()
    guiroot.title('Multiplayer Minesweeper')
    a = GUI(guiroot, 16, 16, 40)
    col_count, row_count = guiroot.grid_size()
    for row in range(row_count):
        guiroot.grid_rowconfigure(row, minsize=26)
    for col in range(col_count):
        guiroot.grid_columnconfigure(col, minsize=24)
    guiroot.mainloop()
