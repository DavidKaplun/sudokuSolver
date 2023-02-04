from sudoku_solver_class import *

import pygame

ZERO=48
NINE=58

LEFT_MOUSE_CLICK=1

WHITE= (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0,0,0)
WINDOW_HEIGHT = 380
WINDOW_WIDTH = 360
#sudoku_solver().solve()
#sudoku1=[[9,1,7,2,5,4,0,0,0],[4,0,2,0,8,0,0,0,0],[6,5,0,0,0,3,4,0,0],[0,0,3,0,9,0,2,5,6],[5,0,0,7,0,0,3,0,9],[2,0,0,0,0,5,0,7,1],[0,2,0,5,3,0,7,6,0],[3,7,0,1,6,0,0,9,8],[0,0,0,0,0,0,0,3,0]]
#sudoku2=[[0,0,9,5,8,6,0,0,0],[0,0,0,0,2,0,0,0,0],[4,0,0,0,0,0,6,8,3],[9,0,0,6,5,0,0,3,2],[0,6,0,7,0,0,0,9,8],[0,3,0,2,0,0,7,0,4],[0,0,3,0,0,0,0,0,0],[6,2,0,0,1,5,0,4,0],[0,0,0,4,0,0,0,5,0]]
def main():
    matrix=[[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]

    global SCREEN,blockSize
    blockSize=40
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(WHITE)

    solve_button = pygame.Rect(160, 0, 40, 20)
    text_font = pygame.font.SysFont(None, 16)
    text_image = text_font.render("Solve", True, BLACK, WHITE)
    pygame.draw.rect(SCREEN, GRAY, solve_button, 1)
    # Draw the text image
    SCREEN.blit(text_image, (165,5))


    drawGrid(matrix)
    pygame.display.update()
    running = True
    pos=(0,0)
    row=0
    col=0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK:
                pos = pygame.mouse.get_pos()
                col = pos[0] // 40
                row = (pos[1]+20) // 40  - 1
                if(solve_button.collidepoint(pos)):
                    matrix=sudoku_solver([[0,0,9,5,8,6,0,0,0],[0,0,0,0,2,0,0,0,0],[4,0,0,0,0,0,6,8,3],[9,0,0,6,5,0,0,3,2],[0,6,0,7,0,0,0,9,8],[0,3,0,2,0,0,7,0,4],[0,0,3,0,0,0,0,0,0],[6,2,0,0,1,5,0,4,0],[0,0,0,4,0,0,0,5,0]]).solve()
                    for row in range(HEIGHT):
                        for col in range(WIDTH):
                            if(matrix[row][col]!=0):
                                put_num_in_grid(matrix[row][col],row,col)
                                pygame.display.flip()
            if(event.type==pygame.KEYDOWN):
                if(event.key>ZERO and event.key<NINE):
                    matrix[row][col]=event.key-ZERO
                    put_num_in_grid(event.key-ZERO,row,col)
                    pygame.display.flip()


def put_num_in_grid(number,row,col):
    number_font = pygame.font.SysFont(None, 16)
    number_text=str(number)
    number_image = number_font.render(number_text, True, BLACK, WHITE)
    row=row*blockSize+20
    col=col*blockSize
    # centre the image in the cell by calculating the margin-distance
    margin_x = (blockSize - 1 - number_image.get_width()) // 2
    margin_y = (blockSize - 1 - number_image.get_height()) // 2

    # Draw the number image
    SCREEN.blit(number_image, (col + 2 + margin_x, row + 2 + margin_y))

def drawGrid(matrix):

    for col in range(0, WINDOW_WIDTH, blockSize):
        for row in range(20, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(col, row, blockSize, blockSize)
            pygame.draw.rect(SCREEN, GRAY, rect, 1)



    pygame.draw.line(SCREEN, BLACK, (0, 140), (360, 140))
    pygame.draw.line(SCREEN, BLACK, (0, 260), (360, 260))
    pygame.draw.line(SCREEN, BLACK, (120, 20), (120, 380))
    pygame.draw.line(SCREEN, BLACK, (240, 20), (240, 380))



if __name__ == '__main__':
    main()


