import pygame
import sys
import os
from time import sleep
from copy import deepcopy
import sudoku_generator

#functions responsible for solving the sudoku grid
#checking if the board is solved
def is_solved(board):
    for i in board:
        if 0 in i:
            return False
    return True

#finding the coordinates of the upcoming unsolved space
def find_unsolved(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i,j)

#finding out what are the possible answers(returns [] if there is no possible answer)
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
    x_square = x // 3
    y_square = y // 3
    for i in range(x_square*3, x_square*3 + 3):
        for j in range(y_square*3, y_square*3 + 3):
            if board[i][j] != 0:
                n_answers.add(board[i][j])
    for i in n_answers:
        answers.remove(i)
    return answers

#main board-solving function(backtracking included)
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

#game class with all the attributes and states...easier to code without global variables
class game:

    solving = False
    solved = False
    screen = None
    o_board = sudoku_generator.new_grid()
    s_board = solve(o_board) 
    board = o_board.copy() 
    fake_board = deepcopy(o_board)
    tries = 5
    g_state = 0
    coord = None
    running = False
    p_selected = None
    s_selected = None
    timer = 5
    n_font = None
    font = None
    
    #initializing the the library, screen variable and font
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sudoku")
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.n_font = pygame.font.Font("freesansbold.ttf", 22)
        self.running = True
            
    #intermediary function made to draw squares
    def draw_square(self, coord, length, width, color):    
        A = coord
        B = (coord[0] + length, coord[1])
        C = (coord[0], coord[1] + length)
        D = (coord[0] + length, coord[1] + length)
        pygame.draw.line(self.screen, color, A, B, width)
        pygame.draw.line(self.screen, color, A, C, width)
        pygame.draw.line(self.screen, color, D, B, width)
        pygame.draw.line(self.screen, color, D, C, width)

    #drawing the inner 9x9 grid
    def draw_grid(self):

        #drawing the grid
        self.draw_square((200, 100), 405, 5, (0, 0, 0))
        for i in range(200, 605, 45):
            for j in range(100, 505, 45):
                self.draw_square((i, j), 45, 2, (0, 0, 0))
        
        #square borders
        #column
        for i in range(335, 605, 135):
            pygame.draw.line(self.screen, (0, 0, 0), (i, 100), (i, 505), 5)
        
        #line
        for j in range(235, 505, 135):
            pygame.draw.line(self.screen, (0, 0, 0), (200, j), (605, j), 5)    

    #drawing the numbers
    def draw_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.screen.blit(self.n_font.render(str(self.board[i][j]), True, (0, 0, 0)), (200 + 45 * i + 5, 100 + 45 * j + 5))
                elif self.fake_board[i][j] != 0:
                    self.screen.blit(self.n_font.render(str(self.fake_board[i][j]), True, (0, 255, 0)), (200 + 45 * i + 25, 100 + 45 * j + 20))
    #drawing the selected space(might need some improvement for a feature)
    def draw_selected(self):
        if self.p_selected == None:
            pass
        else:
            self.draw_square((200 + self.p_selected[0] * 45, 100 + self.p_selected[1] * 45), 43, 2, (255, 0, 0))
        if self.s_selected == None:
            pass
        else:
            self.draw_square((200 + self.s_selected[0] * 45, 100 + self.s_selected[1] * 45), 43, 2, (0, 255, 0))
                
    #main drawing function(it uses all the other intermediary functions)
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
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
                pygame.display.flip()
                sleep(1)
                self.timer -= 1
            else:
                message = self.font.render("Solved! The game will close in " + str(self.timer) + " seconds...", True, (0, 0, 0))
                self.screen.blit(message, (60, 50))
                pygame.display.flip()
                sleep(1)
                self.timer -= 1

        #lose condition
        elif self.g_state == -1 and self.solved:
            message = self.font.render("You lost! The game will close in " + str(self.timer) + " seconds...", True, (0, 0, 0))
            self.screen.blit(message, (60, 50))
            pygame.display.flip()
            sleep(1)
            self.timer -= 1
        #updating the frame
        pygame.display.flip()

    def get_square(self, coord):
        #checking wether the coordonates are in the grid
        if coord[0] >= 200 and coord[0] <= 605 and coord[1] >= 100 and coord[1] <= 505:
            x_coord = (coord[0] - 200) // 45
            y_coord = (coord[1] - 100) // 45
            return [x_coord, y_coord]
        else:
            return None
    
    #quiting the game
    def quit(self):
        pygame.quit()
        self.running = False
    
    #graphic solver(to visualize the way a backtracking algorithm solves a sudoku board)
    def g_solve(self):
        if is_solved(self.board):
            self.solved = True
            self.solving = False
            self.p_selected = None
            return
        else:
            coord = find_unsolved(self.board)
            answers = find_answers(self.board, coord[0], coord[1])
            for i in answers:
                self.draw()
                self.p_selected = [coord[0], coord[1]]
                self.board[coord[0]][coord[1]] = i
                sleep(0.15)
                self.g_solve()
                if self.board == self.s_board:
                    break 
                self.board[coord[0]][coord[1]] = 0
                self.p_selected = [coord[0], coord[1]]
                self.draw()
                sleep(0.15)
        self.selected = None

def main():
    sudoku = game()
    number = -1
    coord = {
        "coordinates" : None,
        "type" : None
    }

    #game loop
    while sudoku.running:

        #writing the numbers
        if number != -1:
            #it's a primary box selection
            if sudoku.p_selected != None:
        
                #checking if the square is editable
                if sudoku.o_board[sudoku.p_selected[0]][sudoku.p_selected[1]] == 0:
                    #checking if it's a valid option
                    if number == sudoku.s_board[sudoku.p_selected[0]][sudoku.p_selected[1]]:
                        sudoku.board[sudoku.p_selected[0]][sudoku.p_selected[1]] = number
                        sudoku.o_board[sudoku.p_selected[0]][sudoku.p_selected[1]] = number
                        sudoku.fake_board[sudoku.p_selected[0]][sudoku.p_selected[1]] = number
                        sudoku.p_selected = None
                    else:
                        sudoku.tries -= 1

            #it's a secondary box selection
            elif sudoku.s_selected != None:
                if sudoku.o_board[sudoku.s_selected[0]][sudoku.s_selected[1]] == 0:
                    sudoku.fake_board[sudoku.s_selected[0]][sudoku.s_selected[1]] = number
            number = -1
        
        #win condition
        if is_solved(sudoku.board) and sudoku.g_state != -1:
            sudoku.g_state = 1
            if sudoku.timer == 0:
                sleep(1)
                sudoku.quit()
                continue
        
       #lose condition
        if sudoku.tries <= 0:
            sudoku.g_state = -1
            if not sudoku.solved:
                sudoku.solving = True
                sudoku.g_solve()
                sudoku.draw()
            if sudoku.timer == 0:
                sleep(1)
                sudoku.quit()
                continue
        
        #updating the frame
        sudoku.draw()

        #getting the board coordinates from the mouse input
        if coord["coordinates"] != None:
            s_coord = sudoku.get_square(coord["coordinates"])
            if s_coord != None and sudoku.o_board[s_coord[0]][s_coord[1]] == 0:
                if coord["type"] == "primary":
                        if s_coord == sudoku.p_selected:
                            sudoku.p_selected = None
                        else:
                            sudoku.s_selected = None
                            sudoku.p_selected = s_coord
                elif coord["type"] == "secondary":
                    if s_coord == sudoku.s_selected:
                        sudoku.s_selected = None
                    else:
                        sudoku.p_selected = None
                        sudoku.s_selected = s_coord
            coord.update({"coordinates" : None})
            coord.update({"type" : None})

        #ciclying trough game events(key presses, mouse clicks, quitting the program)
        for event in pygame.event.get():

            #quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sudoku.running = False
            
            #selecting the squares
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord.update({"coordinates" : pygame.mouse.get_pos()})
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                   coord.update({"type" : "primary"})
                elif mouse[2]:
                    coord.update({"type" : "secondary"})

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
