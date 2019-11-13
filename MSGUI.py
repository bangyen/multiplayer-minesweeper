"""This is not the main program. To set desired board specifications in another window before playing, run setup.py
This program sets most of the methods for the Multiplayer Minesweeper game"""

from tkinter import *
from project.sweeper import *


class GUI:
    def __init__(self, window, width, height, bombs):
        self.window = window

        # creates object for helper functions
        self.sweep = Sweeper(width, height, bombs)
        
        self.status = StringVar()
        self.timer = IntVar()
        self.flagsrem = IntVar()
        self.flagsrem.set(bombs)
        
        self.firstclickstatus = True
        self.done = False
        self.player1passed = False
        self.player2passed = False
        self.firstturn = True
        
        self.width = int(width)
        self.height = int(height)

        self.p1scorelbl = StringVar()
        self.p2scorelbl = StringVar()        
        self.p1score = 0
        self.tempp1score = 0
        self.p2score = 0
        self.tempp2score = 0
        
        self.p1scorelbl.set("Score: 0")
        self.p2scorelbl.set("Score: 0")
        
        '''Creates label and options for player 1'''
        p1label = Label(window, text="Player 1", bg='#FF0000')
        p1label.grid(row=0, column=0, columnspan=2, sticky=W)
        p1scorelabel = Label(window, textvariable=self.p1scorelbl)
        p1scorelabel.grid(row=1, column=0, columnspan=3, sticky=W)
        p1pass = Button(window, text="Pass", command=self.player1pass)
        p1pass.grid(row=2, column=0, columnspan=2, sticky=W)
        p1quit = Button(window, text="Quit", command=self.window.destroy)
        p1quit.grid(row=3, column=0, columnspan=2, sticky=W)
        
        '''Creates label and options for player 2'''
        p2label = Label(window, text="Player 2", bg='#3054C6')
        p2label.grid(row=0, column=width-2, columnspan=2, sticky=E)
        p2scorelabel = Label(window, textvariable=self.p2scorelbl)
        p2scorelabel.grid(row=1, column=width-3, columnspan=3, sticky=E)
        p2pass = Button(window, text="Pass", command=self.player2pass)
        p2pass.grid(row=2, column=width-2, columnspan=2, sticky=E)
        p2quit = Button(window, text="Quit", command=self.window.destroy)
        p2quit.grid(row=3, column=width-2, columnspan=2, sticky=E)

        '''Starts the timer and sets the status label'''
        self.timer.set(5)
        self.status.set("Pass to Player 1:")
        statuslabel1 = Label(window, text="Timer:")
        statuslabel1.grid(row=0, column=int(width/2)-3, columnspan=3, rowspan=2)
        statuslabel3 = Label(window, textvariable=self.timer)
        statuslabel3.grid(row=2, column=int(width/2)-3, columnspan=3)
        self.changetimer()
        
        '''Label for number of flags yet to be placed'''
        flaglabel = Label(window, text='Flags\nleft:')
        flaglabel.grid(row=0, column=int(width/2), rowspan=2, columnspan=3)
        flagnumlabel = Label(window, textvariable=self.flagsrem)
        flagnumlabel.grid(row=2, column=int(width/2), rowspan=1, columnspan=3)
        
        '''Label for the game's turn status and the win message'''
        winlabel = Label(window, textvariable=self.status, font='arial 10')
        winlabel.grid(row=3, column=0, rowspan=2, columnspan=self.width, sticky=S)
        
        '''Creates a range of buttons for the minesweeper board'''
        for y in range(height):
            for x in range(width):
                b = Button(window, width=2, command=self.click_event, bg='#BBBBBB')
                b.bind('<Button-3>', self.flag_event)
                b.grid(row=5+y, column=x)
                self.sweep.buttonlist.append(b)
        self.click_event()
    
    def changetimer(self):
        """Controls the time status of each turn in the cycle
        The status that this program changes cyclically controls many of the game's methods"""
        # Stops timer if the game has been won
        self.timer.set(self.timer.get() - 1)
        if self.done:
            return None
        self.window.after(1000, self.changetimer)
        # Once the time for a status elapses, the status is changed
        if self.timer.get() == 0:
            if self.status.get() == "Pass to Player 1:":
                self.player1passed = False
                self.timer.set(16)
                # sets the first turn to half a regular turn to enforce fairness
                if self.firstturn:
                    self.timer.set(8)
                    self.firstturn = False
                self.status.set("Player 1's turn")
            elif self.status.get() == "Player 1's turn":
                self.timer.set(8)
                """as a turn progresses, points are won and lost by placing and removing flags. Positive point values 
                result from correct choices, negative values from incorrect choices to prevent the determination of flag
                placement using the score, the score is compiled and written at the end of each turn."""
                self.p1score += self.tempp1score
                self.tempp1score = 0
                self.p1scorelbl.set("Score: "+str(self.p1score))
                self.status.set("Pass to Player 2:")
            elif self.status.get() == "Pass to Player 2:":
                self.player2passed = False
                self.timer.set(16)
                self.status.set("Player 2's turn")
            elif self.status.get() == "Player 2's turn":
                self.timer.set(8)
                self.p2score += self.tempp2score
                self.tempp2score = 0
                self.p2scorelbl.set("Score: "+str(self.p2score))
                self.status.set("Pass to Player 1:")

    def click_event(self):
        """sets the first click to a random open square to prevent the first player from losing unfairly in the first
        click"""
        if self.firstclickstatus:
            position = self.sweep.firstclick(self.width, self.height)
            self.firstclickstatus = False
        else:
            if self.status.get() == "Pass to Player 1:" or self.status.get() == "Pass to Player 2:":
                return None
            # finds the position of the cursor upon click
            x = self.window.winfo_pointerx() - self.window.winfo_rootx()
            y = self.window.winfo_pointery() - self.window.winfo_rooty()
            # calculates cell based on cursor position
            cellx = x//24
            celly = (y-130)//26
            position = cellx + celly*self.width
        
        # removes clicked cell from grid
        self.sweep.buttonlist[position].grid_forget()
        
        statnum = self.sweep.data[position][0]
        color = self.sweep.setcolor(statnum)
        # creates new label for clicked cell
        d = Label(self.window, width=2, bg='white', text=statnum, height=1, border=3, pady=2, font='arial 9 bold',
                  fg=color)
        d.grid(row=5 + position // self.width, column=position % self.width)
        # triggers a loss for clicking on a button above a bomb
        if statnum == "*":
            self.win("Bomb")
        self.sweep.clickedlist.append(position)
        self.clearing_loop(position)
        
    def clearing_loop(self, pos):
        """Recursive program that clears all the cells surrounding a cell with no surrounding bombs. It then tests those
         cells and repeats"""
        statnum = self.sweep.data[pos][0]
        if statnum == ' ':
            for u in self.sweep.findneighbors(pos, self.width, self.width*self.height):
                # if the button is not clicked or flagged:
                if u not in self.sweep.clickedlist and self.sweep.flagbuttonlist[u] == '':
                    # changes the button to a label
                    self.sweep.clickedlist.append(u)
                    self.sweep.buttonlist[u].grid_forget()
                    statnum = self.sweep.data[u][0]
                    color = self.sweep.setcolor(statnum)
                    d = Label(self.window, width=2, bg='white', text=statnum, height=1, border=3, font='arial 9 bold',
                              fg=color)
                    d.grid(row=5 + u // self.width, column=u % self.width)
                    self.clearing_loop(u)
    
    def flag_event(self, event):
        """finds the position of the cursor"""
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        cellx = x//24
        celly = (y-130)//26
        position = cellx + celly*self.width
        
        # sets different flagging effects for different turn status
        if self.status.get() == "Player 1's turn":
            self.flagsrem.set(self.flagsrem.get()-1)
            bgcol = '#FF0000'
            if self.sweep.data[position][0] == "*":
                # 1 point for correctly placed flag
                self.tempp1score += 1
            else:
                # -5 points for incorrectly plaged flag
                self.tempp1score -= 5
        
        elif self.status.get() == "Player 2's turn":
            self.flagsrem.set(self.flagsrem.get()-1)
            bgcol = '#3054C6'
            if self.sweep.data[position][0] == "*":    
                self.tempp2score += 1
            else:
                self.tempp2score -= 5
        # stops program if clicking happens during a passing status
        else:
            return None
        
        # forgets the old button in the position
        self.sweep.buttonlist[position].grid_forget()
        b = Button(self.window, width=2, bg=bgcol)
        # adds the new button in the position
        b.bind('<Button-3>', self.unflag_event)
        b.grid(row=5+celly, column=cellx)
        # adds the new button to the list of flag buttons to be accessed for unflagging
        self.sweep.flagbuttonlist.pop(position)
        self.sweep.flagbuttonlist.insert(position, b)
        # checks if there are no more flags. In that case, the game is won
        if self.flagsrem.get() == 0:
            self.win('Zero flags')
            
    def unflag_event(self, event):
        """Removes the flag from a button if right-clicked"""
        # Finds position of cell clicked
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        cellx = x//24
        celly = (y-130)//26
        position = cellx + celly*self.width
        
        if self.status.get() == "Player 1's turn":
            self.flagsrem.set(self.flagsrem.get()+1)
            if self.sweep.data[position][0] == "*":
                # -1 point for removing a correctly placed flag
                self.tempp1score -= 1
            else:
                # 5 points for removing an incorrectly placed flag
                self.tempp1score += 5
        elif self.status.get() == "Player 2's turn":
            self.flagsrem.set(self.flagsrem.get()+1)
            if self.sweep.data[position][0] == "*":    
                self.tempp2score -= 1
            else:
                self.tempp2score += 5
        else:
            return None
        # forgets flag button and restores unflagged button to grid
        self.sweep.flagbuttonlist[position].grid_forget()
        self.sweep.buttonlist[position].grid(row=5+celly, column=cellx)
    
    def player1pass(self):
        """Passes player 1's turn and updates score"""
        if self.status.get() == "Player 1's turn":
            self.player1passed = True
            self.timer.set(8)
            self.p1score += self.tempp1score
            self.tempp1score = 0
            self.p1scorelbl.set("Score: "+str(self.p1score))            
            self.status.set("Pass to Player 2:")
            # ends game in case of double pass
            if self.player2passed:
                self.win("Double pass")
    
    def player2pass(self):
        if self.status.get() == "Player 2's turn":
            self.player2passed = True
            self.timer.set(8)
            self.p2score += self.tempp2score
            self.tempp2score = 0
            self.p2scorelbl.set("Score: "+str(self.p2score))
            self.status.set("Pass to Player 1:")
            if self.player1passed:
                self.win('Double pass')
    
    def win(self, cause):
        """ends game given a cause"""
        # updates scores
        self.p1score += self.tempp1score
        self.p2score += self.tempp2score
        self.p1scorelbl.set("Score: " + str(self.p1score))
        self.p2scorelbl.set("Score: " + str(self.p2score))
        # sets boolean value to stop timer
        self.done = True
        if cause == 'Bomb':
            if self.status.get() == "Player 1's turn" or self.status.get() == "Pass to Player 2":
                self.status.set("Player 2 wins by explosion")
            if self.status.get() == "Player 2's turn" or self.status.get() == "Pass to Player 1":
                self.status.set("Player 1 wins by explosion!")
        elif cause == 'Zero flags' or cause == 'Double pass':
            if self.p1score > self.p2score:
                self.status.set("{}. Player 1 wins! Score: {} - {}".format(cause, self.p1score, self.p2score))
            elif self.p2score > self.p1score:
                self.status.set("{}. Player 2 wins! Score: {} - {}".format(cause, self.p1score, self.p2score))
            else:
                self.status.set("{}. Tie game at {} - {}".format(cause, self.p1score, self.p2score))
        
        for child in self.window.winfo_children():
            '''Disables all buttons except for the quit buttons at index 3 and 7'''
            if child.winfo_class() == 'Button' and child != self.window.winfo_children()[3] and child != \
                    self.window.winfo_children()[7]:
                child.configure(state='disable')
                child.unbind('<Button-3>')


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
