from collections import deque
from typing import List, Tuple


class Instruction:
    def __init__(self, direction: str, distance: str, color: str):
        match direction:
            case "L":
                self.direction = (0, -1)
            case "U":
                self.direction = (-1, 0)
            case "R":
                self.direction = (0, 1)
            case "D":
                self.direction = (1, 0)
        self.distance = int(distance)


def parse_dig_plan(dig_plan: List[str]) -> List[Instruction]:
    instructions = []
    for line in dig_plan:
        direction, distance, color = line.split(" ")
        instruction = Instruction(direction, distance, color)
        instructions.append(instruction)
    return instructions


def create_matrix(
    instructions: List[Instruction],
) -> (List[List[bool]], Tuple[int, int]):
    """Returns the matrix and the relative position where the instructions start."""
    position = (0, 0)
    north = west = 0
    south = east = 1
    for instruction in instructions:
        position = (
            position[0] + instruction.direction[0] * instruction.distance,
            position[1] + instruction.direction[1] * instruction.distance,
        )
        if position[0] + 1 < north:
            north = position[0] + 1
        elif position[0] + 1 > south:
            south = position[0] + 1
        elif position[1] + 1 < east:
            east = position[1] + 1
        elif position[1] + 1 > west:
            west = position[1] + 1
    matrix = [
        [False for _ in range(west + abs(east) + 1)]
        for _ in range(south + abs(north) + 1)
    ]
    start_position = (abs(north) + 1, abs(east) + 1)
    return matrix, start_position


def dig_perimeter(
    matrix: List[List[bool]],
    start_position: Tuple[int, int],
    instructions: List[Instruction],
):
    position = start_position
    for instruction in instructions:
        for _ in range(instruction.distance):
            position = (
                position[0] + instruction.direction[0],
                position[1] + instruction.direction[1],
            )
            matrix[position[0]][position[1]] = True


def find_interior_position(matrix: List[List[bool]], h: int, w: int):
    """
    Finds a position inside the dig perimeter.
    
    This position is the 3rd position in a ".#." pattern,
    which is not proceeded by a "##" pattern on the same row,
    where a "#" represents a perimeter position
    and "." represents a non-perimeter position.
    """
    for y in range(h):
        for x in range(w):
            if matrix[y][x] and x + 1 < w and matrix[y][x + 1]:
                break
            if (
                not matrix[y][x]
                and x + 2 < w
                and matrix[y][x + 1]
                and not matrix[y][x + 2]
            ):
                return (y, x + 2)


def dig_interior(matrix: List[List[bool]], h: int, w: int):
    dig_queue = deque()
    dig_queue.append(find_interior_position(matrix, h, w))
    while len(dig_queue) > 0:
        y, x = dig_queue.popleft()
        if 0 < y < h and 0 < x < w and not matrix[y][x]:
            matrix[y][x] = 1
            dig_queue.append((y, x - 1))
            dig_queue.append((y - 1, x))
            dig_queue.append((y, x + 1))
            dig_queue.append((y + 1, x))


def measure_volume(matrix: List[List[bool]], h: int, w: int):
    volume = 0
    for y in range(h):
        for x in range(w):
            if matrix[y][x]:
                volume += 1
    return volume


def get_lava_lagoon_volume(dig_plan: List[str]) -> int:
    instructions = parse_dig_plan(dig_plan)
    matrix, position = create_matrix(instructions)
    h = len(matrix)
    w = len(matrix[0])
    dig_perimeter(matrix, position, instructions)
    dig_interior(matrix, h, w)
    return measure_volume(matrix, h, w)


with open("2023/18/input.txt") as input:
    dig_plan = input.readlines()

print(f"Answer for part 1: {get_lava_lagoon_volume(dig_plan)}")
