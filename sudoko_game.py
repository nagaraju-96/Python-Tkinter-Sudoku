import pygame
from copy import deepcopy
import random

pygame.init()

width, height = 600, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku Game")

cell_size = 60

puzzle_width = cell_size * 9
puzzle_height = cell_size * 9

start_x = (width - puzzle_width) // 2
start_y = (height - puzzle_height) // 2

font = pygame.font.Font(None, 36)
font_error = pygame.font.Font(None, 28)
font_title = pygame.font.Font(None, 48)

grid_width = 2

difficulty_page = True
selected_difficulty = None

button_width, button_height = 150, 50
easy_button_rect = pygame.Rect(width // 4 - button_width // 2, height // 2 - 50, button_width, button_height)
medium_button_rect = pygame.Rect(width // 2 - button_width // 2, height // 2 - 50, button_width, button_height)
hard_button_rect = pygame.Rect(3 * width // 4 - button_width // 2, height // 2 - 50, button_width, button_height)

def draw_difficulty_page():
    screen.fill((255, 255, 255))

    title_text = font_title.render("Choose Difficulty Level", True, (0, 0, 0))
    easy_text = font.render("Easy", True, (0, 0, 0))
    medium_text = font.render("Medium", True, (0, 0, 0))
    hard_text = font.render("Hard", True, (0, 0, 0))

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))
    pygame.draw.rect(screen, (0, 255, 0), easy_button_rect)
    pygame.draw.rect(screen, (255, 255, 0), medium_button_rect)
    pygame.draw.rect(screen, (255, 0, 0), hard_button_rect)

    screen.blit(easy_text, (easy_button_rect.centerx - easy_text.get_width() // 2, easy_button_rect.centery - easy_text.get_height() // 2))
    screen.blit(medium_text, (medium_button_rect.centerx - medium_text.get_width() // 2, medium_button_rect.centery - medium_text.get_height() // 2))
    screen.blit(hard_text, (hard_button_rect.centerx - hard_text.get_width() // 2, hard_button_rect.centery - hard_text.get_height() // 2))

def get_selected_difficulty(pos):
    if easy_button_rect.collidepoint(pos):
        return "easy"
    elif medium_button_rect.collidepoint(pos):
        return "medium"
    elif hard_button_rect.collidepoint(pos):
        return "hard"
    else:
        return None

def draw_grid(start_x, start_y, cell_size, grid_width):
    for i in range(10):
        if i % 3 == 0:
            thickness = grid_width * 2
        else:
            thickness = grid_width

        y = start_y + i * cell_size
        pygame.draw.line(screen, (0, 0, 0), (start_x, y), (start_x + puzzle_width, y), thickness)

        x = start_x + i * cell_size
        pygame.draw.line(screen, (0, 0, 0), (x, start_y), (x, start_y + puzzle_height), thickness)


def draw_numbers(grid, error_message=None):
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            original_num = grid_array[row][col]

            if num != 0:
                text_color = (0, 0, 0) if original_num == num else (0, 255, 0) 
            else:
                text_color = (255, 255, 255) 

            text = font.render(str(num), 1, text_color)
            x = start_x + col * cell_size + (cell_size - text.get_width()) // 2
            y = start_y + row * cell_size + (cell_size - text.get_height()) // 2
            screen.blit(text, (x, y))

    if error_message:
        text = font_error.render(error_message, True, (255, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height - 40))


def is_valid_move(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True


def generate_sudoku(difficulty):
    grid = [[0] * 9 for _ in range(9)]
    solve_sudoku(grid)

    puzzle = deepcopy(grid)
    num_to_remove = 0

    if difficulty == "easy":
        num_to_remove = 30  
    elif difficulty == "medium":
        num_to_remove = 40
    elif difficulty == "hard":
        num_to_remove = 50

    for _ in range(num_to_remove):
        row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0

    return puzzle


def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


def main():
    global grid_array
    global selected_difficulty
    global difficulty_page

    while difficulty_page:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_difficulty = get_selected_difficulty(pos)
                if selected_difficulty:
                    difficulty_page = False
                    grid_array = generate_sudoku(selected_difficulty)

        draw_difficulty_page()
        pygame.display.flip()

    grid = deepcopy(grid_array)
    selected_cell = None
    error_message = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    col = (pos[0] - start_x) // cell_size
                    row = (pos[1] - start_y) // cell_size
                    selected_cell = (row, col)
                    error_message = None 

            if event.type == pygame.KEYDOWN and selected_cell is not None:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    if is_valid_move(grid, *selected_cell, num):
                        grid[selected_cell[0]][selected_cell[1]] = num
                        error_message = None  
                    else:
                        error_message = "Invalid move! This number is not allowed in the current cell."

                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    grid[selected_cell[0]][selected_cell[1]] = 0
                    error_message = None

                if event.key == pygame.K_SPACE:
                    grid = deepcopy(grid_array)

        screen.fill((255, 255, 255))
        draw_grid(start_x, start_y, cell_size, grid_width)
        draw_numbers(grid, error_message)

        if selected_cell is not None:
            row, col = selected_cell
            pygame.draw.rect(screen, (255, 0, 0), (start_x + col * cell_size, start_y + row * cell_size, cell_size, cell_size), 3)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
