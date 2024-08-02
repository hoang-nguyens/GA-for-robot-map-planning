from GA import *
import pickle
import time
import matplotlib.pyplot as plt

GRID_WIDTH = 30
grid = [[0] * GRID_WIDTH for _ in range(GRID_WIDTH)]

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


def solve(filename):
    obstacles_set, start_set, end_set = load_map(filename)

    start = start_set.pop()
    end = end_set.pop()
    obstacles_set.remove(start)
    obstacles_set.remove(end)
    obstacles = list(obstacles_set)
    for obstacle in obstacles:

        x, y = obstacle[0], obstacle[1]
        if x < GRID_WIDTH and y < GRID_WIDTH:
            grid[x][y] = 1
    time_start = time.time()
    best, evaluate = genetic_algorithm(grid, start, end, 200, 5000)
    time_end = time.time()
    run_time = time_end - time_start
    filename_without_pickle = filename.replace('.pickle', '')
    solve_filename = filename_without_pickle + '_solve' + '.pickle'
    save_map(solve_filename, best, start, end)
    return evaluate, run_time


# plot hàm fit( khi nào hàm fitness hội tụ đủ thì dừng lại, sử dụng epslion
# các phương pháp đánh giá thuật toán metaheuristic