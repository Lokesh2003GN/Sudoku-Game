import numpy as np
import random
import sudoku_solver as ss
import copy
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# create complect sudoku box with full of numbers by using random values
def creat(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                nums = random.sample(range(1, 10), 9)
                for num in nums:
                    if ss.valid(i, j, num,board):
                        board[i][j] = num
                        if creat(board):
                            return True
                        board[i][j] = 0
                return False
    return True


# removes random values from give complect sudoku and give number of values to remove
def remove_nums(remove):
	removed_ind=[]
	i=0
	while i <remove:
		x=random.randint(0,8)
		y=random.randint(0,8)
		if (x,y) not in removed_ind:
			removed_ind.append((x,y))
			i+=1
	for z in removed_ind:
		board[z[0]][z[1]]=0

# verify number to the empty box with coordinates and value
def verify_num(x,y,n,board):
	if ss.valid(x,y,n,board):
		board[x][y]=n
		if ss.solve_sudoku(board):
			return True
		else:
			board[x][y]=0
			return False
	else:
		return False

# function to create complect sudoku box with some numbers removed
def creat_sudoku_board(rem):
	creat(board)
	remove_nums(rem)
	return board
	
# write number after verify to the respected box by using coordinates
def write_num(x,y,n):
	board2=copy.deepcopy(board)
	if board2[x][y]==0 and verify_num(x,y,n,board2) :
		board[x][y]=n
		return True
	else:
		return False
