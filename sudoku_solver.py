import numpy as np
import random
import random 

# check the given number is valid to respected position or not
def valid(row, column, num,board2):
    for i in range(9):
        if board2[row][i] == num:
            return False
    for j in range(9):
        if board2[j][column] == num:
            return False
    r0 = (row // 3) * 3
    c0 = (column // 3) * 3
    for i in range(r0,r0+3):
            for j in range(c0,c0+3):
                if board2[i][j] == num:
                	return False
    return True

# finding complect solution for the given sudoku
# this returns weather the given sudoku has solution or not
def solve_sudoku(board2):
    for i in range(9):
        for j in range(9):
            if board2[i][j] == 0:
                for num in range(1,10):
                    if valid(i, j, num, board2):
                        board2[i][j] = num
                        if solve_sudoku(board2):
                            return True
                        board2[i][j] = 0 
                return False
    return True