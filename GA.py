import random
import pickle
from collections import deque
import math
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
GRID_WIDTH = 30

direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]# ,(1,1),(1,-1),(-1,-1),(-1,1)]
second_level_direction = [(-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (2, -2), (1, -2), (0, -2), (-1, -2),
                          (-2, -2), (-2, -1), (-2, 0), (-2, 1)]
#obstacles = [(2, 1), (5, 4), (6, 7), (5, 3)]
grid = [[0] * GRID_WIDTH for _ in range(GRID_WIDTH)]
sp = 0.05  # path weigh
sfl = 0.05  # safety first level weight
ssl = 0.01  # safety second level weight

'''
for obstacle in obstacles:
    x, y = obstacle[0], obstacle[1]
    grid[x][y] = 1
start = (1, 1)
end = (9, 9)
'''

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
# use random walk to find path

obstacles_set, start_set, end_set = load_map("someone's map.pickle")

start = start_set.pop()
end = end_set.pop()
obstacles_set.remove(start)
obstacles_set.remove(end)
obstacles = list(obstacles_set)
for obstacle in obstacles:
    x, y = obstacle
    grid[x][y] = 1

def random_walk(grid, start, end):
    n, m = len(grid), len(grid[0])
    cur = start
    path = [cur]

    while cur != end:
        x, y = cur
        neighbor = []
        ban_list = set()
        for dr, dc in direction:
            new_x, new_y = x + dr, y + dc
            if 0 <= new_x < n and 0 <= new_y < m and grid[new_x][new_y] == 0 and (new_x, new_y) not in ban_list:
                neighbor.append((new_x, new_y))
        if neighbor:
            cur = random.choice(neighbor)
            path.append(cur)
        else:
            if len(path) == 1:
                return None
            else:

                path.pop()
                cur = path[-1]
        ban_list.add(cur)
    return path


# print( random_walk(grid, start, end))

#  bfs
def bfs(grid, start, end):
    n, m = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for dx, dy in direction:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < n and 0 <= new_y < m and grid[new_x][new_y] == 0 and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))
    return None
def unknown_bfs(grid, start, end):
    new_grid = grid
    for i in range(GRID_WIDTH):
        for j in range(GRID_WIDTH):
            if grid[i][j] == 1 and (i,j)!= start and (i,j) != end:
                n = random.random()
                if n > 0.8:
                    new_grid[i][j] = 0

    n, m = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for dx, dy in direction:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < n and 0 <= new_y < m and new_grid[new_x][new_y] == 0 and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))


def random_grid_path(grid, start, end):
    n, m = len(grid), len(grid[0])

    # Find a random non-obstacle grid cell
    non_obstacle_cells = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == 0 and (i,j)!= start and (i,j) != end]
    random_number = random.randrange(2, len(non_obstacle_cells) -2)
    random_grid_cell = non_obstacle_cells[random_number]

    # Find path from start to the random grid cell
    path_start_to_grid = bfs(grid, start, random_grid_cell)

    # Find path from the random grid cell to end
    path_grid_to_end = bfs(grid, random_grid_cell, end)

    # Combine paths
    path = path_start_to_grid + path_grid_to_end[1:]

    return path

def unknown_find_path(grid, start, end):
    n, m = len(grid), len(grid[0])

    # Find a random non-obstacle grid cell
    non_obstacle_cells = [(i, j) for i in range(n) for j in range(m) if
                          grid[i][j] == 0 and (i, j) != start and (i, j) != end]
    random_number = random.randrange(2, len(non_obstacle_cells) - 2)
    random_grid_cell = non_obstacle_cells[random_number]

    # Find path from start to the random grid cell
    path_start_to_grid = unknown_bfs(grid, start, random_grid_cell)

    # Find path from the random grid cell to end
    path_grid_to_end = bfs(grid, random_grid_cell, end)

    # Combine paths
    path = path_start_to_grid + path_grid_to_end[1:]
    return path

def is_valid_point(grid, point):
    x, y = point
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

# Function to generate a random point in the grid
def random_point(grid):
    x = random.randint(0, len(grid) - 1)
    y = random.randint(0, len(grid[0]) - 1)
    return (x, y)

# Function to find the nearest node in the tree to a given point
def nearest_node(tree, point):
    min_dist = float('inf')
    nearest = None
    for node in tree:
        dist = math.sqrt((point[0] - node[0])**2 + (point[1] - node[1])**2)
        if dist < min_dist:
            min_dist = dist
            nearest = node
    return nearest

# Function to extend the tree from a given node towards a point
def extend_tree(grid, node, target):
    step_size = 1
    dx = target[0] - node[0]
    dy = target[1] - node[1]
    dist = math.sqrt(dx**2 + dy**2)
    if dist == 0:
        return None
    dx /= dist
    dy /= dist
    new_point = (int(node[0] + step_size * dx), int(node[1] + step_size * dy))
    if is_valid_point(grid, new_point):
        return new_point
    else:
        return None

# RRT function to find a path in a grid map
def rrt(grid, start, goal, max_iter=300):
    tree = [start]
    path_found = False
    for _ in range(max_iter):
        rand_point = random_point(grid)
        nearest = nearest_node(tree, rand_point)
        new_node = extend_tree(grid, nearest, rand_point)
        if new_node:
            tree.append(new_node)
            if new_node == goal:
                path_found = True
                break
    if path_found:
        path = [goal]
        current_node = goal
        while current_node != start:
            for node in tree:
                if node == start:
                    path.append(start)
                    break
                if node == current_node:
                    path.append(node)
                    current_node = node
                    break
        return path[::-1]  # Reverse the path to start from the start point
    else:
        return None
def generate_population(POPULATION_SIZE, grid, start, end):

    paths =  [rrt(grid, start, end) for _ in range(POPULATION_SIZE)]
    for i in range(len(paths)):
        if paths[i] == None:
            paths[i] = bfs(grid, start, end)#random_grid_path(grid, start, end)
    return paths


#population = generate_population(30, grid, start, end)

def square_safety(grid, path):
    for i in range(1, len(path)):
        x1, y1 = path[i-1]
        x2, y2 = path[i]
        if x1 < x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if x1-x2 == 1 and y1-y2 == 1:
            if grid[x1][y1+1] == 1 or grid[x1 + 1][y2] == 1:
                return False
    return True

def safety_first_level(grid, path):
    dangerous = 0
    for node in path:
        x, y = node
        for dr, dc in direction:
            nx, ny = x + dr, y + dc
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                dangerous += 1
                break
    return dangerous


def safety_second_level(grid, path):
    dangerous = 0
    for node in path:
        x, y = node
        for dr, dc in second_level_direction:
            nx, ny = x + dr, y + dc
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                dangerous += 1
                break
    return dangerous


def check_continuous(grid1, grid2):
    x1, y1 = grid1
    x2, y2 = grid2
    if (abs(x1 - x2) == 1 and y1 == y2) or (x1 == x2 and abs(y1 - y2) == 1):
        return True
    else:
        return False

def check_obstacle(grid, path):

    for i in range(2, len(path) - 2):
        x, y = path[i]
        if(grid[x][y] == 1):
            return 0
    return 1
def fitness(path):
    sp = 0.05  # path weigh
    sfl = 0.05  # safety first level weight
    ssl = 0.01  # safety second level weight
    if not square_safety(grid, path):
        return 0
    if(check_obstacle(grid,path) == 0):
       return 0.01
    for i in range(len(path) - 1):
        grid1 = path[i]
        grid2 = path[i + 1]
        if check_continuous(grid1, grid2) == False:
            return 0
    return 1 / (sp * len(path) + sfl * safety_first_level(grid, path) + ssl * safety_second_level(grid, path))


def select_parent(population, percentage=0.1):  # elitist method
    sort_population = sorted(population, key=fitness, reverse=True)
    top_parents = int(percentage * len(population))
    elite_parents = sort_population[:top_parents]
    parent1_index, parent2_index = random.randint(0, top_parents - 1), random.randint(0, top_parents - 1)
    parent1, parent2 = elite_parents[parent1_index], elite_parents[parent2_index]
    return sort_population[:len(population) // 2], parent1, parent2


def crossover(population):
    elite_parents, parent1, parent2 = select_parent(population, 0.1)
    length_path1 = len(parent1)
    length_path2 = len(parent2)

    offspring = []
    for i in range(2, length_path1 - 1):
        for j in range(2, length_path2 - 1):
            if parent1[i] == parent2[j]:
                offspring1 = parent1[:i] + parent2[j:]
                offspring2 = parent2[:j] + parent1[i:]
                offspring.append(offspring1)
                offspring.append(offspring2)
                if len(offspring) > len(population):
                    i = length_path1
                    break

    offspring = sorted(offspring, key=fitness, reverse=True)
    return offspring[:len(offspring) // 2]


#offspring = crossover(population)


def mutation(path):
    random_index = random.randint(3, len(path) - 3)
    x, y = path[random_index]
    random_direct = random.randint(0, len(direction))
    dr, dc = direction[random_direct]
    nx, ny = x + dr, y + dc
    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
        path[random_index] = (nx, ny)
    return path

def population_cost(top_population):
    #return fitness(top_population[0])
    return sum([fitness(gen) for gen in top_population])


def genetic_algorithm(grid, start, end, population_size=10, max_generation=100):
    evaluate = list()
    evaluate.append(0)
    stop = 0
    population = generate_population(population_size, grid, start, end)

    for _ in range(max_generation):
        elite_parents, parent1, parent2 = select_parent(population, 0.25)

        top_population = elite_parents[:]
        generation_evaluate = population_cost(elite_parents)
        last_generation_evaluate = evaluate[-1]
        if(abs(last_generation_evaluate - generation_evaluate)  < 0.00001):
            stop +=1
        else:
            stop = 0
        if(stop > 50):
            break
        offspring = crossover(population)
        new_population = elite_parents + offspring
        new_population = new_population[:population_size]
        population = new_population

        evaluate.append(generation_evaluate)
    return population[0], evaluate


#best, evaluate = genetic_algorithm(grid, start, end, 10, 100)
#print(best)


#save_map("someone's map solve.pickle", best, start, end)




#save_map("solve_hic.pickle", best, start, end)
# print(best)
'''

obstacles_set, start_set, end_set = load_map("hic.pickle")

#
start = start_set.pop()
end = end_set.pop()
obstacles_set.remove(start)
obstacles_set.remove(end)
obstacles = list(obstacles_set)
print(obstacles)
print(start)
print(end)
#obstacles = [(1, 2), (3, 5), (7, 6), (4, 5)]
#start = (1, 1)
#end = (9, 9)
for obstacle in obstacles:
    x, y = obstacle
    grid[x][y] = 1
population = generate_population(30, grid, start, end)
offspring = crossover(population)


best = genetic_algorithm(grid, start, end, 30, 1000)
best = set(best)
save_map("solve_hic.pickle", best, start, end)
print(best)
#print(grid)
'''