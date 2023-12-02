# Tree represents an individual tree in a tree grid
class Tree:
    def __init__(self, x, y, h):
        self.x = x  # Position along x axis
        self.y = y  # Position along y axis
        self.h = h  # Height of tree

        # `None` means unknown
        # `True` means visible
        # `False` means hidden
        self.visibility = None

    def __str__(self):
        if self.visibility == None:
            return " "
        if self.visibility == True:
            return "O"
        if self.visibility == False:
            return "X"

    def __repr__(self):
        return str(self)


# Scan the input map and generate a list of tree objects, representing all
# the trees in the grid.
def generate_tree_grid(map):
    tree_grid = []
    y = 0
    for row in map:
        tree_grid.append([])
        x = 0
        for item in row:
            if item.isdigit():
                tree_grid[y].append(Tree(x, y, int(item)))
                x += 1
        y += 1
    return tree_grid


# Find the greatest tree height in a tree grid
def get_greatest_height(tree_grid):
    greatest_height = 0
    for row in tree_grid:
        for tree in row:
            if tree.h > greatest_height:
                greatest_height = tree.h
    return greatest_height


# Assign visibility values to trees by scanning from the perimiter
def scan_lines_from_perimiter(tree_grid, greatest_height):
    x_len = len(tree_grid[0])
    y_len = len(tree_grid)

    for y_position in range(y_len):
        scan_line(tree_grid, greatest_height, 0, y_position, 1, 0)
        scan_line(tree_grid, greatest_height, x_len - 1, y_position, -1, 0)

    for x_position in range(x_len):
        scan_line(tree_grid, greatest_height, x_position, 0, 0, 1)
        scan_line(tree_grid, greatest_height, x_position, y_len - 1, 0, -1)


# Inspect trees in a line and assign a visibility value to each
# Stop after the greatest height is reached
def scan_line(tree_grid, grid_greatest_height, x_start_position, y_start_position, x_direction, y_direction):
    depth = 0
    line_greatest_height = 0
    while True:
        x_rel_position = depth * x_direction
        y_rel_position = depth * y_direction

        x_position = x_start_position + x_rel_position
        y_position = y_start_position + y_rel_position

        try:
            tree = tree_grid[y_position][x_position]
        except:
            break

        if depth == 0 or tree.h > line_greatest_height:
            tree.visibility = True
            line_greatest_height = tree.h

            if line_greatest_height == grid_greatest_height:
                break
        else:
            if tree.visibility == None:
                tree.visibility = False
        depth += 1


# Print a tree grid (handy for debugging)
def print_grid(tree_grid):
    for row in tree_grid:
        print(row)


# Count the total number of visible trees in a grid
def get_visible_count(tree_grid):
    visible_count = 0
    for row in tree_grid:
        for tree in row:
            if tree.visibility == True:
                visible_count += 1
    return visible_count


# Get the highest scenic score in a tree grid
def get_high_score(tree_grid):
    x_len = len(tree_grid[0])
    y_len = len(tree_grid)

    high_score = 0
    for y in range(y_len):
        for x in range(x_len):
            score = score_tree(tree_grid, x, y)
            if score > high_score:
                high_score = score
    return high_score


# Get the scenic score for a tree in a tree grid
def score_tree(tree_grid, x_position, y_position):
    tree = tree_grid[y_position][x_position]
    height = tree.h

    # Score up
    u_score = score_line(tree_grid, height, x_position, y_position, 0, -1)
    # Score left
    l_score = score_line(tree_grid, height, x_position, y_position, -1, 0)
    # Score down
    d_score = score_line(tree_grid, height, x_position, y_position, 0, 1)
    # Score right
    r_score = score_line(tree_grid, height, x_position, y_position, 1, 0)

    return u_score * l_score * d_score * r_score


# Get the scenic score in one direction from a starting point in a tree grid
# Stop after the maximum height is reached
def score_line(tree_grid, max_height, x_start_position, y_start_position, x_direction, y_direction):
    distance = 0
    visible_trees = 0

    while True:
        # Calculate the position to inspect
        distance += 1
        x_rel_position = distance * x_direction
        y_rel_position = distance * y_direction
        x_position = x_start_position + x_rel_position
        y_position = y_start_position + y_rel_position

        # Figure out if there is a tree at the position
        tree_exists = None
        if x_position < 0 or y_position < 0:
            tree_exists = False
        else:
            try:
                tree = tree_grid[y_position][x_position]
                tree_exists = True
            except:
                tree_exists = False
        
        # Based on tree height, decide whether to break or continue
        if tree_exists:
            visible_trees += 1
            if tree.h < max_height:
                continue
            else:
                break
        else:
            break
        
    return visible_trees


with open('2022/08/input.txt') as file:
    map = file.readlines()

tree_grid = generate_tree_grid(map)
greatest_height = get_greatest_height(tree_grid)

scan_lines_from_perimiter(tree_grid, greatest_height)
print_grid(tree_grid)

visible_count = get_visible_count(tree_grid)
print("Visible tree count: {}".format(visible_count))

line_score = get_high_score(tree_grid)
print("Highest scenic score: {}".format(line_score))
