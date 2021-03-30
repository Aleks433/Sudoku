import pygame
import sys
import os
from time import sleep
from copy import deepcopy
import sudoku_generator

#functions responsible for solving the sudoku grid
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


class game:

    solving = False
    solved = False
    screen = None
    o_board = sudoku_generator.new_grid()
    s_board = solve(o_board) 
    board = o_board.copy() 
    tries = 5
    g_state = 0
    coord = None
    running = False
    images = []
    selected = -1
    timer = 5
    font = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sudoku")
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        for i in range(1,10):
            self.images.append(pygame.image.load(os.path.join('Images', 'Number ' + str(i) + '.png')))
            self.images[-1] = pygame.transform.scale(self.images[-1], (30,30))
        self.running = True
            
    def draw_square(self, coord, length, width, color):    
        A = coord
        B = (coord[0] + length,coord[1])
        C = (coord[0], coord[1]+length)
        D = (coord[0] + length,coord[1] + length)
        pygame.draw.line(self.screen, color, A, B, width)
        pygame.draw.line(self.screen, color, A, C, width)
        pygame.draw.line(self.screen, color, D, B, width)
        pygame.draw.line(self.screen, color, D, C, width)

    def draw_grid(self):

        #drawing the grid
        self.draw_square((200, 100), 405, 5, (0, 0, 0))
        for i in range(200, 605, 45):
            for j in range(100, 505, 45):
                self.draw_square((i,j), 45, 2, (0,0,0))
        
        #square borders
        #column
        for i in range(335, 605, 135):
            pygame.draw.line(self.screen, (0,0,0), (i,100), (i,505), 5)
        
        #line
        for j in range(235,505,135):
            pygame.draw.line(self.screen,(0,0,0), (200,j), (605,j), 5)    

    def draw_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.screen.blit(self.images[self.board[i][j] - 1], (200 + 45*i + 5, 100 + 45*j + 5))

    def draw_selected(self, color = (255, 0, 0)):
        try:
            self.draw_square((200 + self.selected[0] * 45, 100 + self.selected[1] * 45), 43, 2, color)
        except:
            pass
        
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        if self.solving and self.g_state != -1:
            self.draw_selected((0, 255, 0))
        else:
            self.draw_selected()
        self.draw_board()
        message = self.font.render("Mistakes: ", True, (0, 0, 0))
        cross = self.font.render("X", True, (255, 0, 0))
        self.screen.blit(message, (30, 530))
        for i in range(5 - self.tries):
            self.screen.blit(cross, (30 + 130 + ((i+1) * 25), 532))

        #win condition
        if self.g_state == 1:
            if not self.solved:
                message = self.font.render("You win! The game will close in " + str(self.timer) + " seconds...", True, (0, 0, 0))
                self.screen.blit(message, (60, 50))
                sleep(1)
                self.timer -= 1
            else:
                message = self.font.render("Solved! the game will close in " + str(self.timer) + " seconds...", True, (0, 0, 0))
                self.screen.blit(message, (60, 50))
                sleep(1)
                self.timer -= 1

        #lose condition
        elif self.g_state == -1 and not self.solving:
            self.solving = True
            self.g_solve()
            message = self.font.render("You lost! The game will close in " + str(self.timer) + " seconds...", True, (0, 0, 0))
            self.screen.blit(message, (60, 50))
            sleep(1)
            self.timer -= 1
        pygame.display.flip()

    def get_square(self, coord):
        #checking wether the coordonates are in the grid
        if coord[0] >= 200 and coord[0] <= 605 and coord[1] >= 100 and coord[1] <= 505:
            x_coord = (coord[0] - 200)//45
            y_coord = (coord[1] - 100)//45
            return [x_coord, y_coord]
        else:
            return None

    def quit(self):
        pygame.quit()
        self.running = False

    def g_solve(self):
        if is_solved(self.board):
            self.solving = False
            self.solved = True
            return
        else:
            coord = find_unsolved(self.board)
            answers = find_answers(self.board, coord[0], coord[1])
            for i in answers:
                self.draw()
                self.selected = [coord[0], coord[1]]
                self.board[coord[0]][coord[1]] = i
                sleep(0.15)
                self.g_solve()
                if self.board == self.s_board:
                    break 
                self.board[coord[0]][coord[1]] = 0
                self.selected = [coord[0], coord[1]]
                self.draw()
                sleep(0.15)
        self.selected = None

def main():
    sudoku = game()
    number = -1
    coord = None
    while sudoku.running:
        #writing the numbers
        if number != -1:
            if sudoku.selected != None:
                
                #checking if the square is editable
                if sudoku.o_board[sudoku.selected[0]][sudoku.selected[1]] == 0:

                    #checking if it's a valid option
                    if number == sudoku.s_board[sudoku.selected[0]][sudoku.selected[1]]:
                        sudoku.board[sudoku.selected[0]][sudoku.selected[1]] = number
                        sudoku.o_board[sudoku.selected[0]][sudoku.selected[1]] = number
                        sudoku.selected = None
                    else:
                        sudoku.tries -= 1
                number = -1
        sudoku.draw()
        
        #win condition
        if is_solved(sudoku.board):
            sudoku.g_state = 1
            if sudoku.timer == 0:
                sleep(1)
                sudoku.quit()
                continue
        
       #lose condition
        if sudoku.tries <= 0:
           sudoku.g_state = -1
           if sudoku.timer == 0:
                sleep(1)
                sudoku.quit()
                continue

        if coord !=None:
            s_coord = sudoku.get_square(coord)
            if s_coord != None and sudoku.o_board[s_coord[0]][s_coord[1]] == 0:
                if s_coord == sudoku.selected:
                    sudoku.selected = None
                else:
                    sudoku.selected = s_coord
                coord = None
        for event in pygame.event.get():

            #quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sudoku.running = False
            
            #selecting the squares
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()

            #getting the number input
            if event.type == pygame.KEYDOWN:
                if event.key - pygame.K_0 <= 9 and event.key - pygame.K_0 >= 1:
                    number = event.key - pygame.K_0
                elif event.key - pygame.K_KP0 <= 9 and event.key - pygame.K_KP0 >= 1:
                    number = event.key - pygame.K_KP0
                elif event.key == pygame.K_SPACE:
                    sudoku.solving = True
                    sudoku.g_solve()
                else:
                    pass

if __name__=="__main__":
    main()