# Multiplayer Minesweeper
Pass-and-play Multiplayer Minesweeper Game

Written entirely in Python Using TKinter library for the GUI-

This program contains a program for a setup window, minesweeper GUI, and helper functions for the GUI. The setup window gives the height, width, and number of bombs in the game as input values to the minesweeper GUI. Bombs are randomly placed in the minesweeper grid and the game runs with standard minesweeper funcitonality. The twist of "multiplayer minesweeper" is that there is a timer running throughout gameplay that controls, in cycles, which player can flag/unflag squares possibly containing bombs and clear squares on the board. There are also passing stages between players' stages in which no player can perform these actions so the mouse can be passed.

Throughout gameplay, both players aim to win points. The following point values are awarded for the following actions:

  1:  correctly flagging a square (containing a bomb)
  
  -1: unflagging a correctly flagged square (containing a bomb)
  
  5:  unflagging an incorrectly flagged square (not containing a bomb)
  
  -5: flagging an incorrectly flagged square (not containing a bomb)
  
  
  
A player wins when:

  1: the other player clicks on a square containing a bomb
  
  2: the player has more points that the other when:
  
    a. both players pass
  
    b. the number of flags placed is equivalent to the number of bombs on the grid

Bugs: Most background functionality is not separanted from the GUI program into sweeper.py


Author: Andrew Feikema

Date: Dec. 2018
