from typing import Dict, List


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


def parse_input(input: List[str]) -> (Dict[int, Dict[int, Pipe | None]], int, int):
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
                grid_line[col_index] = None
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


def get_connected_pipe(
    entry_direction: str,  # From perspective of the target pipe
    target_y: int,
    target_x: int,
    grid: Dict[int, Dict[int, Pipe | None]],
) -> (Pipe | None, str | None):
    """
    Returns the pipe at the target location only if it has a connection in the entry direction. Also returns the next direction.
    """
    tile = grid[target_y][target_x]
    if not isinstance(tile, Pipe):
        return (None, None)
    if not tile.connections[entry_direction]:
        return (None, None)
    next_direction = [
        direction_key
        for direction_key in tile.connections.keys()
        if tile.connections[direction_key] and direction_key != entry_direction
    ][0]
    return (tile, next_direction)


def get_starting_pipe_and_direction(
    start_y: int, start_x: int, grid: Dict[int, Dict[int, Pipe | None]]
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


with open("2023/10/input.txt") as input:
    grid, height, width, start_y, start_x = parse_input(input.readlines())

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
