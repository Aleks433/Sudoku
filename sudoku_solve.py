from copy import deepcopy


def is_solved(board):
    for i in board:
        if 0 in i:
            return False
    return True


def find_unsolved(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i,j)


def find_answers(board, x, y):
    answers = list(range(1, 10))
    n_answers = set()
    #checking what numbers are upwards
    i = x
    while i > 0:
        i -= 1
        if board[i][y] != 0:
            n_answers.add(board[i][y])
    #checking what numbers are downwards
    i = x
    while i < 8:
        i += 1
        if board[i][y] != 0:
            n_answers.add(board[i][y])
    #checking what numbers are on the left
    j = y
    while j > 0:
        j -= 1
        if board[x][j] != 0:
            n_answers.add(board[x][j])
    #checking what numbers are on the right
    j = y
    while j < 8:
        j += 1
        if board[x][j] != 0:
            n_answers.add(board[x][j])
    #checking what numbers are in the square
    x_square = x//3
    y_square = y//3
    for i in range(x_square*3, x_square*3 + 3):
        for j in range(y_square*3, y_square*3 + 3):
            if board[i][j] != 0:
                n_answers.add(board[i][j])
    for i in n_answers:
        answers.remove(i)
    return answers


def solve(o_board):
    board = deepcopy(o_board)
    if is_solved(board):
        return board
    else:
        coord = find_unsolved(board)
        answers = find_answers(board, coord[0], coord[1])
        for i in answers:
            board[coord[0]][coord[1]] = i
            n_board = solve(board)
            if n_board != None:
                return n_board
            board[coord[0]][coord[1]] = 0