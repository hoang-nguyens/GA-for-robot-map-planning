import pygame
from solve import *
import matplotlib.pyplot as plt
pygame.init()

#  constant
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid map")

# draw grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
# draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

#draw start
def draw_start(start):
    for obstacle in start:
        pygame.draw.rect(screen, DARK_GREEN, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
#draw target
def draw_target(target):
    for obstacle in target:
        pygame.draw.rect(screen, RED, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
# save map

# draw line from center of a grid to another
def draw_line(grid1, grid2):
    center1 = (grid1[0] * GRID_SIZE + GRID_SIZE/2, grid1[1] * GRID_SIZE + GRID_SIZE/2)
    center2 = (grid2[0] * GRID_SIZE + GRID_SIZE/2, grid2[1] * GRID_SIZE + GRID_SIZE/2)

    pygame.draw.line(screen, ORANGE, center1, center2, 3)


def save_map(file_name, obstacles, start, target):
    with open(file_name, 'wb') as f:
        pickle.dump((obstacles, start, target), f)
# load map
def load_map(file_name):
    try:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return set(), set(), set()

# get map name
def get_map_name():
    map_name = ""
    typing = True
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    map_name = map_name[:-1]
                else:
                    map_name += event.unicode
        screen.fill(WHITE)
        font =pygame.font.Font(None, 36)
        text = font.render("Enter map name: " + map_name, True, BLACK)
        screen.blit(text, (10, 10))
        pygame.display.flip()
    return map_name


def main():
    line = False
    evaluate = list()
    obstacles = set()
    start = set()
    target = set()
    running = True
    dragging = False
    draw = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                line = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    filename = get_map_name() + ".pickle"
                    save_map(filename,obstacles,start, target)
                elif event.key == pygame.K_l:
                    filename_not_pickle = get_map_name()
                    filename = filename_not_pickle + ".pickle"
                    obstacles, start, target = load_map(filename)

                elif event.key == pygame.K_a:
                    filename_not_pickle = get_map_name()
                    filename = filename_not_pickle + ".pickle"
                    obstacles, start, target = load_map(filename)

                    #save_map(filename, obstacles, start, target)S
                    evaluate, run_time = solve(filename)
                    line = True
                    draw = True
                    # squares, a, b = load_map
                    squares, a, b = load_map(filename_not_pickle+ '_solve' + '.pickle')
                    squares = list(squares)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    row = event.pos[0] // GRID_SIZE
                    col = event.pos[1] // GRID_SIZE
                    if (row, col) not in obstacles and (row, col) not in target and (row, col) not in start:
                        obstacles.add((row,col))
                    else:
                        obstacles.remove((row, col))
                    dragging = True
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    row = event.pos[0] // GRID_SIZE
                    col = event.pos[1] // GRID_SIZE
                    obstacles.add((row, col))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    row = event.pos[0] // GRID_SIZE
                    col = event.pos[1] // GRID_SIZE
                    dragging = False
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if (row, col) in start:
                            start.clear()
                        else:
                            start.clear()
                            start.add((row, col))

                    elif pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                        if (row, col) in target:
                            target.clear()
                        else:
                            target.clear()
                            target.add((row, col))



        screen.fill(WHITE)
        draw_grid()
        draw_obstacles(obstacles)
        draw_start(start)
        draw_target(target)
        if line:
            for i in range(len(squares) -1):
                square1, square2 = squares[i], squares[i+1]
                draw_line(square1, square2)

        pygame.display.flip()
    pygame.quit()
    if(draw == True):
        x = list(range(len(evaluate)))

        plt.plot(x, evaluate, label='Evaluate Values', color='b')

        plt.xlabel('ith Generation')
        plt.ylabel('Fitness Values')
        plt.title('Convergence of Genetic Algorithm')
        plt.legend()

        plt.show()
        print(evaluate)
    print(obstacles)
    new_grid = [[0]*30 for i in range(30)]
    for obstacle in obstacles:
        new_grid[obstacle[0]][obstacle[1]] = 1
    print(grid)
    print()
    print(len(squares))
    print(round(run_time,2))

if __name__ == "__main__":
    main()
