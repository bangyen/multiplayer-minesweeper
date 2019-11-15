"""This program contains all the helper functions for MSGUI.py"""
import random
from tkinter import Label, StringVar, IntVar, Button


class Sweeper:
    def __init__(self, window, width, height, bombnum):
        self.window = window
        self.width = width
        self.height = height

        self.flagsrem = IntVar(value=bombnum)

        # one of 4 turn statuses
        self.status = StringVar()
        self.status.set("Pass to Player 1:")

        '''Starts the Timer and sets the status label'''
        self.timer = IntVar(value=5)

        self.p1score = 0
        self.temp1score = 0
        self.p2score = 0
        self.temp2score = 0

        self.p1scorelbl = StringVar(value="Score: 0")
        self.p2scorelbl = StringVar(value="Score: 0")

        # Initializes lists of clicked buttons, un-clicked buttons, and flagged buttons
        self.clickedlist = []
        self.buttonlist = []
        self.flagbuttonlist = [None]*(height*width)

        self.firstturn = True
        self.firstclickstatus = True
        self.done = False
        self.player1passed = False
        self.player2passed = False

        """initializes and writes the bomb status or neighbor status of each cell"""
        squarenum = width * height

        '''Writes to status.txt a specified count of bombs randomly'''
        file = open('status.txt', 'w')
        for x in range(squarenum):
            '''Compares a random float between 0 and 1 to the probability of bomb placement in each cell'''
            if random.random() > bombnum / squarenum:
                file.write("0\n")
                squarenum -= 1
            else:
                file.write("*\n")
                squarenum -= 1
                bombnum -= 1
        file.close()
        squarenum = width * height

        '''Writes the list of bomb placements to a list'''
        with open('status.txt', 'r') as file:
            data = file.readlines()

        '''Places the number of bombs surrounding each cell in a list, in order of position'''
        for x in range(squarenum):
            if data[x] != '*\n':
                for y in self.findneighbors(x, width, squarenum):
                    if data[y] == '*\n':
                        data[x] = str(int(data[x][0]) + 1) + '\n'

        '''status.txt now serves as a reference file'''
        with open('status.txt', 'w') as file:
            file.writelines(data)

        '''Changes the zeros to blank spaces to be written on the main board's labels'''
        data = [w.replace('0\n', ' \n') for w in data]
        self.data = data
    
    @staticmethod
    def setcolor(statnum):
        """Returns the color associated with the number of bombs surrounding a minesweeper cell"""
        col = 'black'
        if statnum == '1':
            col = 'blue'
        elif statnum == '2':
            col = 'green'
        elif statnum == '3':
            col = 'red'
        elif statnum == '4':
            col = 'purple'
        elif statnum == '5':
            col = 'maroon'
        elif statnum == '6':
            col = 'turquoise'
        elif statnum == '8':
            col = 'gray'
        return col
    
    @staticmethod
    def findneighbors(x, width, squarenum):
        """Finds the position in status.txt associated with the neighbors of a given cell, eliminating neighbors if on
        an edge or corner"""
        neighbors = [x - 1 - width, x - width, x + 1 - width, x - 1, x + 1, x - 1 + width, x + width, x + 1 + width]
        if x / width < 1:
            neighbors.remove(x - 1 - width)
            neighbors.remove(x - width)
            neighbors.remove(x + 1 - width)
            if x == 0:
                neighbors.remove(x - 1)
                neighbors.remove(x - 1 + width)
            if x == width - 1:
                neighbors.remove(x + 1)
                neighbors.remove(x + 1 + width)
        elif x + width >= squarenum:
            neighbors.remove(x + width - 1)
            neighbors.remove(x + width)
            neighbors.remove(x + width + 1)
            if x % width == 0:
                neighbors.remove(x - 1 - width)
                neighbors.remove(x - 1)
            if x == squarenum - 1:
                neighbors.remove(x + 1 - width)
                neighbors.remove(x + 1)
        elif (x + 1) % width == 0:
            neighbors.remove(x + 1 - width)
            neighbors.remove(x + 1)
            neighbors.remove(x + 1 + width)
        elif x % width == 0:
            neighbors.remove(x - 1 - width)
            neighbors.remove(x - 1)
            neighbors.remove(x - 1 + width)
        return neighbors

    def firstclick(self, width, height):
        """Finds a blank position for the first click"""
        pos = random.randint(0, width * height - 1)
        while self.data[pos][0] != ' ':
            pos = random.randint(0, width * height - 1)
        return pos

    def clearing_loop(self, pos):
        """Recursive program that clears all the cells surrounding a cell with no surrounding bombs. It then tests those
         cells and repeats"""
        statnum = self.data[pos][0]
        if statnum == ' ':
            for u in self.findneighbors(pos, self.width, self.width * self.height):
                # if the button is not clicked or flagged:
                if u not in self.clickedlist and not self.flagbuttonlist[u]:
                    # changes the button to a label
                    self.clickedlist.append(u)
                    self.buttonlist[u].grid_forget()
                    statnum = self.data[u][0]
                    color = self.setcolor(statnum)
                    d = Label(self.window, width=2, bg='white', text=statnum, height=1, border=3, font='arial 9 bold',
                              fg=color)
                    d.grid(row=5 + u // self.width, column=u % self.width)
                    self.clearing_loop(u)

    def click_event(self):
        """sets the first click to a random open square to prevent the first player from losing unfairly in the first
        click"""
        if self.firstclickstatus:
            position = self.firstclick(self.width, self.height)
            self.firstclickstatus = False
        else:
            if self.status.get() == "Pass to Player 1:" or self.status.get() == "Pass to Player 2:":
                return None
            # finds the position of the cursor upon click
            x = self.window.winfo_pointerx() - self.window.winfo_rootx()
            y = self.window.winfo_pointery() - self.window.winfo_rooty()
            # calculates cell based on cursor position
            cellx = x // 24
            celly = (y - 94) // 26
            position = cellx + celly * self.width

        # removes clicked cell from grid
        self.buttonlist[position].grid_forget()

        statnum = self.data[position][0]
        # color for revealed number indicating neighboring bombs
        color = self.setcolor(statnum)
        # creates new label for clicked cell
        d = Label(self.window, width=2, bg='white', text=statnum, height=1, border=3, pady=2, font='arial 9 bold',
                  fg=color)
        d.grid(row=5 + position // self.width, column=position % self.width)
        # triggers a loss for clicking on a button above a bomb
        if statnum == "*":
            self.win("Bomb")
        self.clickedlist.append(position)
        self.clearing_loop(position)

    def flag_event(self, event):
            """finds the position of the cursor"""
            x = self.window.winfo_pointerx() - self.window.winfo_rootx()
            y = self.window.winfo_pointery() - self.window.winfo_rooty()
            cellx = x // 24
            celly = (y - 94) // 26
            position = cellx + celly * self.width

            # sets different flagging effects for different turn status
            if self.status.get() == "Player 1's turn":
                self.flagsrem.set(self.flagsrem.get() - 1)
                bgcol = '#FF0000'
                if self.data[position][0] == "*":
                    # 1 point for correctly placed flag
                    self.temp1score += 1
                else:
                    # -5 points for incorrectly placed flag
                    self.temp1score -= 5

            elif self.status.get() == "Player 2's turn":
                self.flagsrem.set(self.flagsrem.get() - 1)
                bgcol = '#3054C6'
                if self.data[position][0] == "*":
                    self.temp2score += 1
                else:
                    self.temp2score -= 5
            # stops program if clicking happens during a passing status
            else:
                return None

            # forgets the old button in the position
            self.buttonlist[position].grid_forget()
            b = Button(self.window, width=2, bg=bgcol)
            # adds the new button in the position
            b.bind('<Button-3>', self.unflag_event)
            b.grid(row=5 + celly, column=cellx)
            # adds the new button to the list of flag buttons to be accessed for unflagging
            self.flagbuttonlist.pop(position)
            self.flagbuttonlist.insert(position, b)
            # checks if there are no more flags. In that case, the game is won
            if self.flagsrem.get() == 0:
                self.win('Zero flags')
        
    def unflag_event(self, event):
        """Removes the flag from a button if right-clicked"""
        # Finds position of cell clicked
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        cellx = x // 24
        celly = (y - 94) // 26
        position = cellx + celly * self.width

        if self.status.get() == "Player 1's turn":
            self.flagsrem.set(self.flagsrem.get() + 1)
            if self.data[position][0] == "*":
                # -1 point for removing a correctly placed flag
                self.temp1score -= 1
            else:
                # 5 points for removing an incorrectly placed flag
                self.temp1score += 5
        elif self.status.get() == "Player 2's turn":
            self.flagsrem.set(self.flagsrem.get() + 1)
            if self.data[position][0] == "*":
                self.temp2score -= 1
            else:
                self.temp2score += 5
        else:
            return None
        # forgets flag button and restores unflagged button to grid
        self.flagbuttonlist[position].grid_forget()
        self.buttonlist[position].grid(row=5 + celly, column=cellx)
    
    def changetimer(self):
        """Controls the time status of each turn in the cycle
        The status that this program changes cyclically controls many of the game's methods"""
        # Stops sweep.timer if the game has been won
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
                placement using the score, the score is compounded and written at the end of each turn."""
                self.p1score += self.temp1score
                self.temp1score = 0
                self.p1scorelbl.set("Score: "+str(self.p1score))
                self.status.set("Pass to Player 2:")
            elif self.status.get() == "Pass to Player 2:":
                self.player2passed = False
                self.timer.set(16)
                self.status.set("Player 2's turn")
            elif self.status.get() == "Player 2's turn":
                self.timer.set(8)
                self.p2score += self.temp2score
                self.temp2score = 0
                self.p2scorelbl.set("Score: "+str(self.p2score))
                self.status.set("Pass to Player 1:")

    def player1pass(self):
        """Passes player 1's turn and updates score"""
        if self.status.get() == "Player 1's turn":
            self.player1passed = True
            self.timer.set(8)
            self.p1score += self.temp1score
            self.temp1score = 0
            self.p1scorelbl.set("Score: " + str(self.p1score))
            self.status.set("Pass to Player 2:")
            # ends game in case of double pass
            if self.player2passed:
                self.win("Double pass")

    def player2pass(self):
        if self.status.get() == "Player 2's turn":
            self.player2passed = True
            self.timer.set(8)
            self.p2score += self.temp2score
            self.temp2score = 0
            self.p2scorelbl.set("Score: " + str(self.p2score))
            self.status.set("Pass to Player 1:")
            if self.player1passed:
                self.win('Double pass')

    def win(self, cause):
        """ends game given a cause"""
        # updates scores
        self.p1score += self.temp1score
        self.p2score += self.temp2score
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
