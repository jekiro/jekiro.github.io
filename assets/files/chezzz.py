#!/usr/bin/env python

from z3 import *
import sys

# Can't have too many nasty pieces on the board
MAX_PAWNS = 0
MAX_ROOKS = 4
MAX_KNIGHTS = 0
MAX_BISHOPS = 0
MAX_QUEENS = 2
MAX_KINGS = 2

# Initialize z3 solver
s = Solver()

# Setup the board
board = [[Int('board_%i_%i' % (i, j)) for j in range(8)] for i in range(8)]

def restrict_number(value, ma):
    s.add(Sum([If(board[i][j] == value, 1, 0)
               for j in range(8) for i in range(8)]) <= ma)

var_2 = lambda i: 8 - i
var_3 = lambda j: j + 9

def get_value(value):
    if value == 6:
        return "_"
    elif value == 5:
        return "P"
    elif value == 4:
        return "R"
    elif value == 3:
        return "N"
    elif value == 2:
        return "B"
    elif value == 1:
        return "Q"
    elif value == 0:
        return "K"

# Make it so that each piece can only be a value from 0 to 6 (6 being empty)
for row in board:
    for piece in row:
        s.add(piece >= 0, piece <= 6)

# Restrict the number of each piece
restrict_number(5, MAX_PAWNS)
restrict_number(4, MAX_ROOKS)
restrict_number(3, MAX_KNIGHTS)
restrict_number(2, MAX_BISHOPS)
restrict_number(1, MAX_QUEENS)
restrict_number(0, MAX_KINGS)

# Add constraint where pawns cannot be on the first or last row
for j in range(8):
    s.add(board[0][j] != 5)
    s.add(board[7][j] != 5)

# The kings are unmovable
s.add(board[0][4] == 0)
s.add(board[7][4] == 0)

# Add the restrictions for each type of piece
# God please forgive me for what I have done
s.add(Sum([
    If(board[i][j] == 5, var_2(i) - var_3(j),
       If(board[i][j] == 4, 256 - var_2(i) - var_3(j),
          If(board[i][j] == 3, var_3(j) % var_2(i),
             If(board[i][j] == 2, 2*(var_2(i) + var_3(j)),
                If(board[i][j] == 1, var_2(i) * var_3(j),
                   If(board[i][j] == 0, var_2(i) + var_3(j),
                      0))))))
    for j in range(8)
    for i in range(8)]) == 467)

if s.check() == sat:
    modl = s.model()

    for i in range(8):
        for j in range(8):
            value = modl[board[i][j]].as_long()

            value = get_value(value)
            sys.stdout.write(value + " ")

        sys.stdout.write("\n")
    sys.stdout.flush()
