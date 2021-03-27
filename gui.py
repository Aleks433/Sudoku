import pygame
import sys
import os
from time import sleep
import sys
from copy import deepcopy
import sudoku_generator
#just in case
sys.setrecursionlimit(1500)


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


#global stuff(don't judge me)
o_board = sudoku_generator.new_grid()
board = o_board.copy()
s_board = solve(board)
selected = None
tries = 5
global timer
timer=5

def draw_square(screen, coord, length, width, color):
    A = coord
    B = (coord[0] + length,coord[1])
    C = (coord[0], coord[1]+length)
    D = (coord[0] + length,coord[1] + length)
    pygame.draw.line(screen, color, A, B, width)
    pygame.draw.line(screen, color, A, C, width)
    pygame.draw.line(screen, color, D, B, width)
    pygame.draw.line(screen, color, D, C, width)


def draw_grid(screen):
        
    #drawing the grid
    draw_square(screen,(200, 100), 405, 5, (0, 0, 0))
    for i in range(200, 605, 45):
        for j in range(100, 505, 45):
            draw_square(screen, (i,j), 45, 2, (0,0,0))
    
    #square borders
    
    #column
    for i in range(335, 605, 135):
        pygame.draw.line(screen, (0,0,0), (i,100), (i,505), 5)
    
    #line
    for j in range(235,505,135):
        pygame.draw.line(screen,(0,0,0), (200,j), (605,j), 5)


def draw_board(screen, images):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                screen.blit(images[board[i][j] - 1], (200 + 45*i + 5, 100 + 45*j + 5))


def draw_selected(screen, selected):
    try:
        draw_square(screen,(200 + selected[0]*45, 100 + selected[1]*45), 43, 2, (255,0,0))
    except:
        pass


def draw(screen, images, font, g_state=0):
    screen.fill((255,255,255))
    draw_grid(screen)
    draw_selected(screen, selected)
    draw_board(screen,images)
    message = font.render("Mistakes: ", True, (0,0,0))
    cross = font.render("X", True, (255, 0, 0))
    screen.blit(message, (30,530))
    for i in range(5 - tries):
        screen.blit(cross, (30 + 130 + ((i + 1) * 25), 532))
    global timer
    if g_state == 1:
        message = font.render("You win! The game will close in " + str(timer) + " seconds...", True, (0, 0, 0))
        screen.blit(message, (60, 50))
        sleep(1)
        timer-=1
        
    elif g_state == -1:
        message = font.render("You lost! The game will close in " + str(timer) + " seconds...", True, (0,0,0))
        screen.blit(message, (60,50))
        sleep(1)
        timer-=1

    pygame.display.flip()



def gui_innit():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Sudoku")
    return screen


def load_images():
    images = []
    for i in range(1, 10):
        images.append(pygame.image.load(os.path.join('Images','Number ' + str(i) + '.png')))
        images[-1] = pygame.transform.scale(images[-1], (30,30))
    return images


def get_square(coord):
    
    #checking wether the coordonates are in the grid
    if coord[0] >= 200 and coord[0] <= 605 and coord[1] >= 100 and coord[1] <= 505:
        x_coord = (coord[0] - 200)//45
        y_coord = (coord[1] - 100)//45
        return [x_coord, y_coord]
    else:
        return None
    

def innit_font():
    return pygame.font.Font("freesansbold.ttf", 32)

def main():

    #innit stuff
    game_condition=0
    screen = gui_innit()
    running = True
    coord = None
    images = load_images()
    number = -1
    font = innit_font()
    global tries
    global selected

    #game loop
    while running:
        
        #writing the numbers
        if number != -1:
            if selected != None:

                #checking if the square is editable
                if o_board[selected[0]][selected[1]] == 0:
                
                    #checking if it's a valid option
                    if number == s_board[selected[0]][selected[1]]:
                        board[selected[0]][selected[1]] = number
                        o_board[selected[0]][selected[1]] = number
                        selected = None
                    else:
                        tries -= 1
                number = -1
        draw(screen,images,font,game_condition)

        
        #win condition
        if is_solved(board):
            game_condition=1
            if timer==0:
                pygame.quit()
                running=False
                continue

        #lose condition
        if tries <= 0:
            game_condition=-1
            if timer==0:
                pygame.quit()
                running=False
                continue
        
        #selecting the squares
        if coord != None:
            s_coord = get_square(coord)
            if s_coord != None and o_board[s_coord[0]][s_coord[1]] == 0:
                if s_coord == selected:
                    selected = None
                else:
                    selected = s_coord
                coord = None

        for event in pygame.event.get():
            
            #quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            #selecting the squares
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()

            #getting the number input
            if event.type == pygame.KEYDOWN:
                if event.key - pygame.K_0 <=9 and event.key - pygame.K_0 >= 1:
                    number = event.key - pygame.K_0
                elif event.key - pygame.K_KP0 <= 9 and event.key - pygame.K_KP0 >= 1:
                    number = event.key - pygame.K_KP0
                else:
                    pass

if __name__ == "__main__":
    main()