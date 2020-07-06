# Multiplayer Minesweeper
Pass-and-play multiplayer minesweeper game, written entirely in Python using TKinter.

## About
This program contains a program for a setup window, minesweeper GUI, and helper functions for the GUI. The setup window gives the height, width, and number of bombs in the game as input values to the minesweeper GUI. Bombs are randomly placed in the minesweeper grid and the game runs with standard minesweeper funcitonality. The twist of "multiplayer minesweeper" is that there is a timer running throughout gameplay that controls, in cycles, which player can flag/unflag squares possibly containing bombs and clear squares on the board. There are also passing stages between players' stages in which no player can perform these actions so the mouse can be passed.

## Points System
Throughout gameplay, both players aim to win points. The following point values are awarded for the following actions:

`+1`: Correctly flagging a square (containing a bomb) \
`-1`: Unflagging a correctly flagged square (containing a bomb) \
`+5`: Unflagging an incorrectly flagged square (not containing a bomb) \
`-5`: Incorrectly flagging a square (not containing a bomb)

## Win Conditions
A player wins when:
- The other player clicks on a square containing a bomb
- The other player has fewer points when one of the following conditions is met:
  - The number of flags placed is equivalent to the number of bombs on the grid
  - Both players pass

## Notes
Bugs: Most background functionality is not separanted from the GUI program into `sweeper.py` \
Author: Andrew Feikema \
Date: Dec. 2018
