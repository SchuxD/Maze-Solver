import random
import tkinter as tk
from queue import PriorityQueue

start_id = None
end_id = None
start_point = None
end_point = None
# set up the window
root = tk.Tk()
root.title("Maze Generator")
canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# set up the maze parameters
maze_width = 20
maze_height = 20
cell_width = canvas_width // maze_width
cell_height = canvas_height // maze_height

# create a 2D array to represent the maze
maze = [[0 for j in range(maze_width)] for i in range(maze_height)]

# generate a random maze
def generate_maze():
    for i in range(maze_height):
        for j in range(maze_width):
            maze[i][j] = random.randint(0, 1)
    draw_maze()
    generate_points()

# draw the maze on the canvas
def draw_maze():
    canvas.delete("all")
    for i in range(maze_height):
        for j in range(maze_width):
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = (j + 1) * cell_width
            y2 = (i + 1) * cell_height
            if maze[i][j] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white")

# generate the start and end points
# generate the start and end points
def generate_points():
    global start_point, end_point, start_id, end_id
    # delete old rectangles
    if start_id:
        canvas.delete(start_id)
    if end_id:
        canvas.delete(end_id)
    
    # clear green squares
    for i in range(maze_height):
        for j in range(maze_width):
            if maze[i][j] == 2:
                maze[i][j] = 0
                draw_cell((j, i), "white")

    # keep generating new points until a path is found between them
    while True:
        # generate new points
        start_point = (random.randint(0, maze_width - 1), random.randint(0, maze_height - 1))
        end_point = (random.randint(0, maze_width - 1), random.randint(0, maze_height - 1))
        
        # check if the points are valid
        if start_point == end_point or maze[start_point[1]][start_point[0]] == 1 or maze[end_point[1]][end_point[0]] == 1 or start_point == (0,0) or end_point == (0,0):
            continue
        
        # check if there is a path between the points
        path = bfs(start_point, end_point)
        if path is None:
            continue
        
        # create new rectangles
        start_id = canvas.create_rectangle(start_point[0] * cell_width, start_point[1] * cell_height, (start_point[0] + 1) * cell_width, (start_point[1] + 1) * cell_height, fill="red")
        end_id = canvas.create_rectangle(end_point[0] * cell_width, end_point[1] * cell_height, (end_point[0] + 1) * cell_width, (end_point[1] + 1) * cell_height, fill="blue")
        for node in path:
            if node != start_point and node != end_point:
                draw_cell(node, "green")
        # mark the path as visited
        for node in path:
            maze[node[1]][node[0]] = 2
        return start_point, end_point

# run depth-first search algorithm to find the shortest path
# run iterative deepening depth-first search algorithm to find the shortest path
def iddfs(start, end):
    for depth in range(maze_width * maze_height):
        visited = set()
        path = []
        if iddfs_helper(start, end, visited, path, depth):
            path.append(start)
            path.reverse()
            for node in path:
                if node != start and node != end:
                    draw_cell(node, "green")
            return path
    return None

def iddfs_helper(current, end, visited, path, depth):
    if depth < 0:
        return False
    if current == end:
        path.append(current)
        return True
    visited.add(current)
    queue = PriorityQueue()
    queue.put((0, current, [current]))
    while not queue.empty():
        _, node, path_so_far = queue.get()
        if node == end:
            path.extend(path_so_far)
            return True
        for neighbor in get_neighbors(node):
            if neighbor not in visited and maze[neighbor[1]][neighbor[0]] == 0:
                cost = len(path_so_far) + 1 + manhattan_distance(neighbor, end)
                queue.put((cost, neighbor, path_so_far + [neighbor]))
    return False

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
# usage
path = iddfs(start_point, end_point)


# run breadth-first search algorithm to find the shortest path
def bfs(start, end):
    visited = set()
    queue = [(start, [start])]
    while queue:
        current, path = queue.pop(0)
        if current == end:
            for node in path:
                draw_cell(node, "green")
            return path
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor not in visited and maze[neighbor[1]][neighbor[0]] == 0:
                queue.append((neighbor, path + [neighbor]))
    return None

# draw a cell with a given color
def draw_cell(cell, color):
    x1 = cell[0] * cell_width
    y1 = cell[1] * cell_height
    x2 = (cell[0] + 1) * cell_width
    y2 = (cell[1] + 1) * cell_height
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)


# helper function to get the neighbors of a cell
def get_neighbors(cell):
    neighbors = []
    x = cell[0]
    y = cell[1]
    if x > 0:
        neighbors.append((x - 1, y))
    if x < maze_width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < maze_height - 1:
        neighbors.append((x, y + 1))
    return neighbors


# create the buttons
# create the buttons
generate_maze_button = tk.Button(root, text="Generate Maze", command=lambda: (canvas.delete("all"), generate_maze()))
generate_maze_button.pack(side="left")

generate_points_button = tk.Button(root, text="Generate Points", command=lambda: (generate_points()))
generate_points_button.pack(side="left")



root.bind("<space>", lambda event: generate_maze())
root.bind("<Return>", lambda event: iddfs(start_point, end_point))
# generate the initial maze and points
generate_maze()
start_point, end_point = generate_points()

# run the main loop
root.mainloop()
