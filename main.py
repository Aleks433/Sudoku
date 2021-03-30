import pygame
import sys
import os
from time import sleep
from copy import deepcopy
import sudoku_generator
import sudoku_solve

class game:
    screen = None
    o_board = sudoku_generator.new_grid()
    s_board = sudoku_solve.solve(o_board) 
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
    def draw_selected(self):
        try:
            self.draw_square((200 + self.selected[0] * 45, 100 + self.selected[1] * 45), 43, 2, (255, 0, 0))
        except:
            pass
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
            message = self.font.render("You win! The game will close in " + str(self.timer) + " seconds...", True, (0, 0, 0))
            self.screen.blit(message, (60, 50))
            sleep(1)
            self.timer -= 1

        #lose condition
        elif self.g_state == -1:
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
        if sudoku_solve.is_solved(sudoku.board):
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
                else:
                    pass

if __name__=="__main__":
    main()