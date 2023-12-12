from typing import Dict, List


# This problem was INSANE


class Pipe:
    def __init__(self, y: int, x: int, char: str):
        self.y = y
        self.x = x
        self.connections = {
            "north": char in ["|", "L", "J"],
            "south": char in ["|", "7", "F"],
            "east": char in ["-", "L", "F"],
            "west": char in ["-", "J", "7"],
        }
        self.is_connected_to_loop = False


def parse_input(
    input: List[str]
) -> (Dict[int, Dict[int, Pipe | None | str]], int, int):
    """
    Takes the puzzle input and generates a model of the pipes.

    Returns a tuple containing 5 values:
        Dict[int, Dict[int, Pipe | None]: a nested dictionary representing the grid, where the keys are y positions and the nested keys are x positions. Nested values are pipes (Pipe) or empty (None).
        int: The grid height.
        int: The grid width.
        int: The starting y coordinate
        int: The starting x coordinate
    """
    grid = {}
    height = len(input)
    width = None
    for row_index in range(height):
        line = input[row_index].strip()
        if width is None:
            width = len(line)
        grid_line = {}
        for col_index in range(width):
            char = input[row_index][col_index]
            if char == "S":
                start_y = row_index
                start_x = col_index
                grid_line[col_index] = "S"
            elif char == ".":
                grid_line[col_index] = None
            else:
                grid_line[col_index] = Pipe(row_index, col_index, char)
        grid[row_index] = grid_line
    return grid, height, width, start_y, start_x


def get_adjacent_coordinates(start_y: int, start_x: int, direction: str) -> (int, int):
    match direction:
        case "north":
            return (
                start_y - 1,
                start_x,
            )
        case "south":
            return (start_y + 1, start_x)
        case "east":
            return (start_y, start_x + 1)
        case "west":
            return (start_y, start_x - 1)


def flip_direction(initial_direction: str) -> str:
    match initial_direction:
        case "north":
            return "south"
        case "south":
            return "north"
        case "east":
            return "west"
        case "west":
            return "east"


def rotate_direction_cw(initial_direction: str) -> str:
    """Rotate direction clockwise"""
    match initial_direction:
        case "north":
            return "east"
        case "south":
            return "west"
        case "east":
            return "south"
        case "west":
            return "north"


def rotate_direction_acw(initial_direction: str) -> str:
    """Rotate direction anti-clockwise"""
    match initial_direction:
        case "north":
            return "west"
        case "south":
            return "east"
        case "east":
            return "north"
        case "west":
            return "south"


def get_connected_pipe(
    entry_direction: str,  # From perspective of the target pipe
    target_y: int,
    target_x: int,
    grid: Dict[int, Dict[int, Pipe | None | str]],
) -> (Pipe | None, str | None):
    """
    Returns the pipe at the target location only if it has a connection in the entry direction. Also returns the next direction.
    """
    tile = grid[target_y][target_x]
    if not isinstance(tile, Pipe):
        return (None, None)
    if not tile.connections[entry_direction]:
        return (None, None)
    grid[target_y][target_x].is_connected_to_loop = True
    next_direction = [
        direction_key
        for direction_key in tile.connections.keys()
        if tile.connections[direction_key] and direction_key != entry_direction
    ][0]
    return (tile, next_direction)


def get_starting_pipe_and_direction(
    start_y: int, start_x: int, grid: Dict[int, Dict[int, Pipe | None | str]]
) -> (Pipe, int):
    adjacent_movements = [
        (direction, get_adjacent_coordinates(start_y, start_x, direction))
        for direction in ["north", "south", "east", "west"]
    ]
    parsed_adjacent_movements = [
        movement
        for movement in adjacent_movements
        if 0 <= movement[1][0] < height and 0 <= movement[1][1] < width
    ]

    connected_pipes = []
    for movement in parsed_adjacent_movements:
        connected_pipe, next_direction = get_connected_pipe(
            flip_direction(movement[0]), movement[1][0], movement[1][1], grid
        )
        if connected_pipe is not None:
            connected_pipes.append((connected_pipe, next_direction))
    return (connected_pipes[0][0], connected_pipes[0][1])


def is_tile_connected(
    tile: Pipe | None | str,
) -> bool:
    """Returns True if the tile is connected to the main loop"""
    return tile == "S" or (isinstance(tile, Pipe) and tile.is_connected_to_loop)


def count_markers(grid: Dict[int, Dict[int, Pipe | None | str]], target_char) -> int:
    """Counts markers, but also prints out the grid, for debugging purposes"""
    count = 0

    y_positions = grid.keys()
    for y in y_positions:
        x_positions = grid[y].keys()
        for x in x_positions:
            tile = grid[y][x]
            if tile == target_char:
                count += 1
            if not is_tile_connected(tile):
                if isinstance(tile, Pipe) or tile is None:
                    print(" ", end="")
                else:
                    print(tile, end="")
            else:
                print("+", end="")
        print()

    return count


def send_markers(
    current_direction: str,
    current_pipe: Pipe,
    grid: Dict[int, Dict[int, Pipe | None | str]],
    height: int,
    width: int,
    next_pipe: Pipe,
    next_direction: str,
) -> (str, str):
    outer_results = []
    # Left
    left_direction = rotate_direction_acw(current_direction)
    tile_y, tile_x = get_adjacent_coordinates(
        current_pipe.y, current_pipe.x, left_direction
    )
    outer_result = lay_next_marker(
        "L", left_direction, tile_y, tile_x, grid, height, width
    )
    if outer_result is not None:
        outer_results.append(outer_result)
    # Forward left if movement is turning right
    if next_direction == rotate_direction_cw(current_direction):
        tile_y, tile_x = get_adjacent_coordinates(
            next_pipe.y, next_pipe.x, left_direction
        )
        outer_result = lay_next_marker(
            "L", left_direction, tile_y, tile_x, grid, height, width
        )
        if outer_result is not None:
            outer_results.append(outer_result)
    # Right
    right_direction = rotate_direction_cw(current_direction)
    tile_y, tile_x = get_adjacent_coordinates(
        current_pipe.y, current_pipe.x, right_direction
    )
    outer_result = lay_next_marker(
        "R", right_direction, tile_y, tile_x, grid, height, width
    )
    if outer_result is not None:
        outer_results.append(outer_result)
    # Forward right if movement is turning left
    if next_direction == rotate_direction_acw(current_direction):
        tile_y, tile_x = get_adjacent_coordinates(
            next_pipe.y, next_pipe.x, right_direction
        )
        outer_result = lay_next_marker(
            "R", right_direction, tile_y, tile_x, grid, height, width
        )
        if outer_result is not None:
            outer_results.append(outer_result)
    return outer_results


def lay_next_marker(
    side: str,
    current_direction: str,
    current_y: int,
    current_x: int,
    grid: Dict[int, Dict[int, Pipe | None | str]],
    height: int,
    width: int,
    recursion_depth: int = 0,
) -> str:
    if (
        current_y < -1
        or current_y > height + 1
        or current_x < -1
        or current_x > width + 1
    ):
        return
    try:
        current_tile = grid[current_y][current_x]
    except KeyError:
        return side
    if (
        not is_tile_connected(current_tile)
        and (current_tile not in ["L", "R"])
        and recursion_depth < 400
    ):
        grid[current_y][current_x] = side
        # Split off to left
        left_direction = rotate_direction_acw(current_direction)
        next_left_y, next_left_x = get_adjacent_coordinates(
            current_y, current_x, left_direction
        )
        lay_next_marker(
            side,
            left_direction,
            next_left_y,
            next_left_x,
            grid,
            height,
            width,
            recursion_depth + 1,
        )
        # Split off to right
        right_direction = rotate_direction_cw(current_direction)
        next_left_y, next_left_x = get_adjacent_coordinates(
            current_y, current_x, right_direction
        )
        lay_next_marker(
            side,
            right_direction,
            next_left_y,
            next_left_x,
            grid,
            height,
            width,
            recursion_depth + 1,
        )
        # Continue straight
        next_y, next_x = get_adjacent_coordinates(
            current_y, current_x, current_direction
        )
        return lay_next_marker(
            side,
            current_direction,
            next_y,
            next_x,
            grid,
            height,
            width,
            recursion_depth + 1,
        )


with open("2023/10/input.txt") as input:
    grid, height, width, start_y, start_x = parse_input(input.readlines())

# First pass counts steps along loop and works out if pipes are connected
current_pipe, current_direction = get_starting_pipe_and_direction(
    start_y, start_x, grid
)

step_count = 1
while True:
    next_pipe_y, next_pipe_x = get_adjacent_coordinates(
        current_pipe.y, current_pipe.x, current_direction
    )
    next_pipe, next_direction = get_connected_pipe(
        flip_direction(current_direction), next_pipe_y, next_pipe_x, grid
    )
    if next_pipe is None:
        break
    current_pipe = next_pipe
    current_direction = next_direction
    step_count += 1

steps_to_furthest_point = int((step_count + 1) / 2)
print("Solution for part 1: {}".format(steps_to_furthest_point))

# Second pass lays markers to count spaces inside and outside main loop
current_pipe, current_direction = get_starting_pipe_and_direction(
    start_y, start_x, grid
)

step_count = 1
all_outer_results = []
while True:
    next_pipe_y, next_pipe_x = get_adjacent_coordinates(
        current_pipe.y, current_pipe.x, current_direction
    )
    next_pipe, next_direction = get_connected_pipe(
        flip_direction(current_direction), next_pipe_y, next_pipe_x, grid
    )
    if next_pipe is None:
        break
    outer_results = send_markers(
        current_direction, current_pipe, grid, height, width, next_pipe, next_direction
    )
    if len(outer_results) > 0:
        all_outer_results = all_outer_results + outer_results
    current_pipe = next_pipe
    current_direction = next_direction
    step_count += 1

outer_left_count = all_outer_results.count("L")
outer_right_count = all_outer_results.count("R")
if outer_left_count > outer_right_count:
    inner_side = "R"
else:
    inner_side = "L"


inner_tile_count = count_markers(grid, inner_side)

print("Solution for part 2: {}".format(inner_tile_count))
