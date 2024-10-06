import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Set up display
GRID_SIZE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 10 * GRID_SIZE, 20 * GRID_SIZE
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris Game')

# Shapes
shapes = [
    # T shape (4 orientations)
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1],
        [1, 1],
        [0, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 1],
        [1, 0]
    ],
    # I shape (2 orientations)
    [
        [1, 1, 1, 1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ],
    # O shape (1 orientation)
    [
        [1, 1],
        [1, 1]
    ],
    # J shape (4 orientations)
    [
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [1, 1],
        [1, 0],
        [1, 0]
    ],
    [
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 1],
        [0, 1],
        [1, 1]
    ],
    # L shape (4 orientations)
    [
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    [
        [1, 1, 1],
        [1, 0, 0]
    ],
    [
        [1, 1],
        [0, 1],
        [0, 1]
    ],
    # S shape (2 orientations)
    [
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 0],
        [1, 1],
        [0, 1]
    ],
    # Z shape (2 orientations)
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1],
        [1, 1],
        [1, 0]
    ]
]

# Draw shape on the display
def draw_shape(display, shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(display, red, (position[0] + x * GRID_SIZE, position[1] + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Check collision of the shape
def check_collision(shape, position, grid):
    shape_height = len(shape)
    shape_width = len(shape[0])
    
    for y in range(shape_height):
        for x in range(shape_width):
            if shape[y][x]:
                if position[0] + x * GRID_SIZE < 0 or position[0] + (x + 1) * GRID_SIZE > SCREEN_WIDTH:
                    return True
                if position[1] + (y + 1) * GRID_SIZE > SCREEN_HEIGHT:
                    return True
                if grid[(position[1] // GRID_SIZE) + y][(position[0] // GRID_SIZE) + x]:
                    return True
    return False

# Drawing the grid for the screen
def draw_grid(display):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(display, white, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(display, white, (0, y), (SCREEN_WIDTH, y))

# Convert shape to grid
def convert_shape_to_grid(shape, position, grid):
    shape_height = len(shape)
    shape_width = len(shape[0])
    
    for y in range(shape_height):
        for x in range(shape_width):
            if shape[y][x]:
                grid[(position[1] // GRID_SIZE) + y][(position[0] // GRID_SIZE) + x] = 1

# Clear full lines and update score
def clear_lines(grid):
    full_lines = 0
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    full_lines = len(grid) - len(new_grid)
    new_grid = [[0 for _ in range(SCREEN_WIDTH // GRID_SIZE)] for _ in range(full_lines)] + new_grid
    return new_grid, full_lines * 10

# Draw landed shapes
def draw_landed_shapes(display, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(display, blue, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Display Game Over Screen
def game_over(display, score):
    display.fill(black)
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render('Game Over!', True, white)
    display.blit(game_over_text, [SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2])
    
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f'Score: {score}', True, white)
    display.blit(score_text, [SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2])
    
    play_again_text = font.render('Press P to Play Again or Q to Quit', True, white)
    display.blit(play_again_text, [SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()])
    
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main loop
def main():
    clock = pygame.time.Clock()
    run = True
    current_shape = random.choice(shapes)
    current_position = [SCREEN_WIDTH // 2 - GRID_SIZE, 0]
    score = 0

    grid = [[0 for _ in range(SCREEN_WIDTH // GRID_SIZE)] for _ in range(SCREEN_HEIGHT // GRID_SIZE)]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_position[0] -= GRID_SIZE
                    if check_collision(current_shape, current_position, grid):
                        current_position[0] += GRID_SIZE
                if event.key == pygame.K_RIGHT:
                    current_position[0] += GRID_SIZE
                    if check_collision(current_shape, current_position, grid):
                        current_position[0] -= GRID_SIZE
                if event.key == pygame.K_DOWN:
                    current_position[1] += GRID_SIZE
                    if check_collision(current_shape, current_position, grid):
                        current_position[1] -= GRID_SIZE
                if event.key == pygame.K_UP:
                    current_shape = rotate_shape(current_shape)
                    if check_collision(current_shape, current_position, grid):
                        current_shape = rotate_shape(current_shape, reverse=True)

        current_position[1] += GRID_SIZE
        if check_collision(current_shape, current_position, grid):
            current_position[1] -= GRID_SIZE
            convert_shape_to_grid(current_shape, current_position, grid)
            grid, points = clear_lines(grid)
            score += points
            current_shape = random.choice(shapes)
            current_position = [SCREEN_WIDTH // 2 - GRID_SIZE, 0]
            if check_collision(current_shape, current_position, grid):
                run = False

        display.fill(black)
        draw_grid(display)
        draw_shape(display, current_shape, current_position)
        draw_landed_shapes(display, grid)
        
        # Display score
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f'Score: {score}', True, white)
        display.blit(score_text, [10, 10])
        
        pygame.display.update()
        clock.tick(5)
    
    game_over(display, score)

def rotate_shape(shape, reverse=False):
    if reverse:
        return [list(row) for row in zip(*shape[::-1])]  # Rotate counterclockwise
    return [list(row)[::-1] for row in zip(*shape)]  # Rotate clockwise

if __name__ == "__main__":
    main()
