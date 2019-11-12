"""This program contains all the helper functions for MSGUI.py"""
import random


class Sweeper:
    def __init__(self):
        if __name__ == '__main__':    
            self.start_game(8, 8, 10)
        
    def create_game(self, width, height, bombnum):
        """initializes and writes the bomb status or neighbor status of each cell"""
        squarenum = width*height
        
        '''Writes to status.txt a specified count of bombs randomly'''
        file = open('status.txt', 'w')
        for x in range(squarenum):
            '''Compares a random float between 0 and 1 to the probability of bomb placement in each cell'''
            if random.random() > bombnum/squarenum:
                file.write("0\n")
                squarenum -= 1
            else:
                file.write("*\n")
                squarenum -= 1
                bombnum -= 1
        file.close()    
        squarenum = width*height
        
        '''Writes the list of bomb placements to a list'''
        with open('status.txt', 'r') as file:
            data = file.readlines()
        
        '''Places the number of bombs surrounding each cell in a list, in order of position'''
        for x in range(squarenum):
            if data[x] != '*\n':
                for y in self.findneighbors(x, width, squarenum):
                    if data[y] == '*\n':
                        data[x] = str(int(data[x][0])+1) + '\n'
        
        '''status.txt now serves as a reference file'''            
        with open('status.txt', 'w') as file:
            file.writelines(data)
        
        '''Changes the zeros to blank spaces to be written on the main board's labels'''
        data = [w.replace('0\n', ' \n') for w in data]
        self.data = data
        
    def findneighbors(self, x, width, squarenum):
        """Finds the position in status.txt associated with the neighbors of a given cell, eliminating neighbors if on
        an edge or corner"""
        neighbors = [x-1-width, x-width, x+1-width, x-1, x+1, x-1+width, x+width, x+1+width]
        if x / width < 1:
            neighbors.remove(x-1-width)
            neighbors.remove(x-width)
            neighbors.remove(x+1-width)
            if x == 0:
                neighbors.remove(x-1)
                neighbors.remove(x-1+width)
            if x == width-1:
                neighbors.remove(x+1)
                neighbors.remove(x+1+width)
        elif x+width >= squarenum:
            neighbors.remove(x+width-1)
            neighbors.remove(x+width)
            neighbors.remove(x+width+1)
            if x % width == 0:
                neighbors.remove(x-1-width)
                neighbors.remove(x-1)
            if x == squarenum-1:
                neighbors.remove(x+1-width)
                neighbors.remove(x+1)
        elif (x+1) % width == 0:
            neighbors.remove(x+1-width)
            neighbors.remove(x+1)
            neighbors.remove(x+1+width)
        elif x % width == 0:
            neighbors.remove(x-1-width)
            neighbors.remove(x-1)
            neighbors.remove(x-1+width)
        return neighbors
    
    def firstclick(self, width, height):
        """Finds a blank position for the first click"""
        pos = random.randint(0, width*height-1)
        while self.data[pos][0] != ' ':
            pos = random.randint(0, width*height-1)
            if self.data[pos][0] == ' ':
                break
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
