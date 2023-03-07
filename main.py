from sudoku_solver_class import *
import timeit
import pygame

ZERO=48
NINE=58

LEFT_MOUSE_CLICK=1

WHITE= (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0,0,0)
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 360

GRID_HEIGHT=380

sudoku1=[[9,1,7,2,5,4,0,0,0],[4,0,2,0,8,0,0,0,0],[6,5,0,0,0,3,4,0,0],[0,0,3,0,9,0,2,5,6],[5,0,0,7,0,0,3,0,9],[2,0,0,0,0,5,0,7,1],[0,2,0,5,3,0,7,6,0],[3,7,0,1,6,0,0,9,8],[0,0,0,0,0,0,0,3,0]]
sudoku2=[[0,0,9,5,8,6,0,0,0],[0,0,0,0,2,0,0,0,0],[4,0,0,0,0,0,6,8,3],[9,0,0,6,5,0,0,3,2],[0,6,0,7,0,0,0,9,8],[0,3,0,2,0,0,7,0,4],[0,0,3,0,0,0,0,0,0],[6,2,0,0,1,5,0,4,0],[0,0,0,4,0,0,0,5,0]]
sudoku3=[[1,0,0,0,0,8,0,0,9],[8,7,0,0,0,1,3,0,0],[5,0,0,0,0,7,0,0,6],[0,0,4,5,0,0,9,0,0],[3,0,0,2,0,0,0,0,4],[0,9,8,0,0,0,0,0,0],[4,0,0,0,0,5,0,1,0],[0,0,0,0,0,0,0,0,0],[7,0,0,6,0,0,0,0,3]]

def main():
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    sudokuSolver=sudoku_solver(matrix)
    initialize_user_interface()

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
                col = pos[0] // blockSize
                row = (pos[1]+20) // blockSize  - 1
                if(solve_button.collidepoint(pos)):
                    sudokuSolver.set_matrix(matrix)
                    t_0 = timeit.default_timer()
                    solved_sudoku=sudokuSolver.solve()
                    t_1 = timeit.default_timer()
                    elapsed_time = round((t_1 - t_0) * 10 ** 3, 3)
                    print(f"Elapsed time: {elapsed_time} mili seconds")
                    for row in range(HEIGHT):
                        for col in range(WIDTH):
                            if(solved_sudoku[row][col]!=0):
                                put_num_in_grid(solved_sudoku[row][col],row,col)
                                pygame.display.flip()


                elif(load_sudoku1.collidepoint(pos)):
                    matrix = deepcopy(sudoku1)
                    draw_matrix(matrix)

                elif (load_sudoku2.collidepoint(pos)):
                    matrix = deepcopy(sudoku2)
                    draw_matrix(matrix)

                elif (load_sudoku3.collidepoint(pos)):
                    matrix = deepcopy(sudoku3)
                    draw_matrix(matrix)

            if(event.type==pygame.KEYDOWN):
                if(event.key>ZERO and event.key<NINE):
                    matrix[row][col]=event.key-ZERO
                    put_num_in_grid(event.key-ZERO,row,col)
                    pygame.display.flip()


def draw_matrix(matrix):
    clear_grid()
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if (matrix[row][col] != 0):
                put_num_in_grid(matrix[row][col], row, col)
                pygame.display.flip()
def initialize_user_interface():

    global SCREEN, blockSize, solve_button, load_sudoku1, load_sudoku2, load_sudoku3

    blockSize = 40
    pygame.init()
    text_font = pygame.font.SysFont(None, 16)
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Sudoku Solver')

    SCREEN.fill(WHITE)

    solve_button = pygame.Rect(160, 0, 40, 20)
    load_sudoku1 = pygame.Rect(10, 440, 90, 25)
    load_sudoku2 = pygame.Rect(110, 440, 90, 25)
    load_sudoku3 = pygame.Rect(210, 440, 90, 25)

    text_image = text_font.render("Solve", True, BLACK, WHITE)
    pygame.draw.rect(SCREEN, GRAY, solve_button, 1)
    pygame.draw.rect(SCREEN, GRAY, load_sudoku1, 1)
    pygame.draw.rect(SCREEN, GRAY, load_sudoku2, 1)
    pygame.draw.rect(SCREEN, GRAY, load_sudoku3, 1)
    # Draw the text image
    SCREEN.blit(text_image, (165, 5))

    text_image = text_font.render("Load Sudoku 1", True, BLACK, WHITE)
    SCREEN.blit(text_image, (15, 448))

    text_image = text_font.render("Load Sudoku 2", True, BLACK, WHITE)
    SCREEN.blit(text_image, (115, 448))

    text_image = text_font.render("Load Sudoku 3", True, BLACK, WHITE)
    SCREEN.blit(text_image, (215, 448))

    instruction_txt = "Click on a square and then enter the number which you want there."
    instruction_txt2 = "If you dont want to do that,  you can also load sudokus "
    instruction_txt3 = "automatically by pressing the buttons below"

    instruction_image = text_font.render(instruction_txt, True, BLACK, WHITE)
    SCREEN.blit(instruction_image, (0, 385))

    instruction_image = text_font.render(instruction_txt2, True, BLACK, WHITE)
    SCREEN.blit(instruction_image, (0, 405))

    instruction_image = text_font.render(instruction_txt3, True, BLACK, WHITE)
    SCREEN.blit(instruction_image, (0, 425))

    drawGrid()
    pygame.display.update()


def clear_grid():
    for row in range(HEIGHT):
        for column in range(WIDTH):
            put_num_in_grid("   ", row, column)

def put_num_in_grid(number,row,col):
    number_font = pygame.font.SysFont(None, 16)
    number_text = ""
    if(number!=0):
        number_text=str(number)
    number_image = number_font.render(number_text, True, BLACK, WHITE)
    row=row*blockSize+20
    col=col*blockSize
    # centre the image in the cell by calculating the margin-distance
    margin_x = (blockSize - 1 - number_image.get_width()) // 2
    margin_y = (blockSize - 1 - number_image.get_height()) // 2

    # Draw the number image
    SCREEN.blit(number_image, (col + 2 + margin_x, row + 2 + margin_y))

def drawGrid():

    for col in range(0, WINDOW_WIDTH, blockSize):
        for row in range(20, GRID_HEIGHT, blockSize):
            rect = pygame.Rect(col, row, blockSize, blockSize)
            pygame.draw.rect(SCREEN, GRAY, rect, 1)



    pygame.draw.line(SCREEN, BLACK, (0, 140), (360, 140))
    pygame.draw.line(SCREEN, BLACK, (0, 260), (360, 260))
    pygame.draw.line(SCREEN, BLACK, (120, 20), (120, 380))
    pygame.draw.line(SCREEN, BLACK, (240, 20), (240, 380))



if __name__ == '__main__':
    main()




