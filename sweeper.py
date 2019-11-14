"""This program contains all the helper functions for MSGUI.py"""
import random
from tkinter import Label, StringVar, IntVar


class Sweeper:
    def __init__(self, window, width, height, bombnum):
        self.window = window
        self.width = width
        self.height = height

        self.status = StringVar()
        self.timer = IntVar()

        self.p1score = 0
        self.tempp1score = 0
        self.p2score = 0
        self.tempp2score = 0

        self.p1scorelbl = StringVar()
        self.p2scorelbl = StringVar()
        self.p1scorelbl.set("Score: 0")
        self.p2scorelbl.set("Score: 0")

        # Initializes lists of clicked buttons, un-clicked buttons, and flagged buttons
        self.clickedlist = []
        self.buttonlist = []
        self.flagbuttonlist = []
        for x in range(height * width):
            self.flagbuttonlist.append('')

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

    def findneighbors(self, x, width, squarenum):
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

    def setcolor(self, statnum):
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

    def clearing_loop(self, pos):
        """Recursive program that clears all the cells surrounding a cell with no surrounding bombs. It then tests those
         cells and repeats"""
        statnum = self.data[pos][0]
        if statnum == ' ':
            for u in self.findneighbors(pos, self.width, self.width * self.height):
                # if the button is not clicked or flagged:
                if u not in self.clickedlist and self.flagbuttonlist[u] == '':
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

    def player1pass(self):
        """Passes player 1's turn and updates score"""
        if self.status.get() == "Player 1's turn":
            self.player1passed = True
            self.timer.set(8)
            self.p1score += self.tempp1score
            self.tempp1score = 0
            self.p1scorelbl.set("Score: " + str(self.p1score))
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
            self.p2scorelbl.set("Score: " + str(self.p2score))
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
