from random import shuffle, randint
from copy import deepcopy
#a grid generator for sudoku(I'm spending way more time on this than I should)
counter = 0

def is_completed(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (False, i, j)
    return (True, None, None)


def get_answers(board, row, col):
    n_answers = set()
    numbers = list(range(1,10))
    #checking the column
    for i in range(9):
        if board[i][col] != 0:
            n_answers.add(board[i][col])
    #checking the row
    for j in range(9):
        if board[row][j] != 0:
            n_answers.add(board[row][j])
    #checking numbers on the 3x3 square
    x_square = row // 3
    y_square = col // 3
    for i in range(x_square*3 , x_square*3 + 3):
        for j in range(y_square*3, y_square*3 + 3):
            if board[i][j] != 0:
                n_answers.add(board[i][j])
    #removing impossible answers
    for i in n_answers:
        numbers.remove(i)
    return numbers


def get_board(o_board):
    board = deepcopy(o_board)
    is_solved, x_coord, y_coord = is_completed(board)
    if is_solved:
        return board
    else:
        answers = get_answers(board, x_coord, y_coord)
        shuffle(answers)
        for i in answers:
            board[x_coord][y_coord] = i
            n_board = get_board(board)
            if n_board != None:
                return n_board
            board[x_coord][y_coord] = 0


def solve_board(o_board):
    board = deepcopy(o_board)
    global counter
    is_solved, x_coord, y_coord = is_completed(board)
    if is_solved:
        counter += 1
        return board
    else:
        answers = get_answers(board, x_coord, y_coord)
        for i in answers:
            board[x_coord][y_coord] = i
            n_board = solve_board(board)
            if n_board != None:
                return n_board
            board[x_coord][y_coord] = 0

#function that returns a random uncompleted grid
def new_grid():
    global counter
    board = []
    for i in range(9):
        board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board = get_board(board)
    i = 0
    while i<42:
        counter = 0
        x_coord = randint(0,8)
        y_coord = randint(0,8)
        aux = board[x_coord][y_coord]
        board[x_coord][y_coord] = 0
        solve_board(board)
        if counter > 1:
            board[x_coord][y_coord] = aux
            continue
        i += 1
    return board

#this is just for testing(leaving it here for the memories)
def main():
    global counter
    board = []
    for i in range(9):
        board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    board = get_board(board)
    i = 0
    while i<42:
        counter = 0
        x_coord = randint(0,8)
        y_coord = randint(0,8)
        aux = board[x_coord][y_coord]
        board[x_coord][y_coord] = 0
        solve_board(board)
        if counter > 1:
            board[x_coord][y_coord] = aux
            continue
        i += 1
    
if __name__ == "__main__":
    main()