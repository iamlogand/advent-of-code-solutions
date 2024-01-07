from collections import deque
import time
from typing import List, Tuple


"""
LAVA LAGOON
This solution uses dig instructions to calculate the volume of a lava lagoon.

'Position' refers to an index in the matrix.
'Point' refers to a location in (simulated) space, measured in meters.
"""


class Instruction:
    def __init__(self, direction: str, distance: int):
        match direction:
            case "L" | "2":
                self.direction = (0, -1)
            case "U" | "3":
                self.direction = (-1, 0)
            case "R" | "0":
                self.direction = (0, 1)
            case "D" | "1":
                self.direction = (1, 0)
        self.distance = distance


class Point:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x


class Rectangle:
    def __init__(self, west: int, north: int, east: int, south: int):
        self.west = west
        self.north = north
        self.east = east
        self.south = south
        self.excavated = False
        self.area = (east - west + 1) * (south - north + 1)
        self.southern_area = east - west + 1
        self.eastern_area = south - north + 1


def parse_dig_plan(dig_plan: List[str], use_hexadecimals: bool) -> List[Instruction]:
    instructions = []
    for line in dig_plan:
        if not use_hexadecimals:
            # Part 1 uses small distances no greater than 12m
            direction, distance, _ = line.split(" ")
            distance = int(distance)
        else:
            # Part 2 uses huge distances, represented as hexadecimal numbers, which can be over 1000km
            hex = line.split(" ")[-1].strip()[2:-1]
            distance = int(hex[:-1], 16)
            direction = hex[-1]
        instruction = Instruction(direction, distance)
        instructions.append(instruction)
    return instructions


def create_matrix(
    instructions: List[Instruction],
) -> (List[List[Tuple[Point, None, List[bool]]]], Tuple[int, int]):
    """
    Returns the matrix and the matrix position where the instructions start.
    Each value in the 'finished' matrix eventually contains a point (1),
    the corresponding rectangle extending southeast (2),
    and indication of whether perimeter lines extend south and east (3).
    """
    position = (0, 0)
    vertical_positions = []
    horizontal_positions = []
    for instruction in instructions:
        position = (
            position[0] + instruction.direction[0] * instruction.distance,
            position[1] + instruction.direction[1] * instruction.distance,
        )
        if instruction.direction[0] != 0:
            vertical_positions.append(position[0])
        if instruction.direction[1] != 0:
            horizontal_positions.append(position[1])
    vertical_positions = list(set(vertical_positions))
    horizontal_positions = list(set(horizontal_positions))
    vertical_positions.sort()
    horizontal_positions.sort()
    # The value at each index in the matrix will be a tuple with a Point, a Rectangle
    # and optionally perimeter lines going South and/or East.
    matrix = [
        [(Point(y, x), None, [False, False]) for x in horizontal_positions]
        for y in vertical_positions
    ]
    start_position = (
        len([p for p in vertical_positions if p < 0]),
        len([p for p in horizontal_positions if p < 0]),
    )
    return matrix, start_position


def dig_perimeter(
    matrix: List[List[Tuple[Point, None, List[bool]]]],
    start_position: Tuple[int, int],
    instructions: List[Instruction],
):
    position = start_position
    for instruction in instructions:
        start_point = matrix[position[0]][position[1]][0]
        target_y = start_point.y + instruction.distance * instruction.direction[0]
        target_x = start_point.x + instruction.distance * instruction.direction[1]
        last_position = (position[0], position[1])
        while True:
            position = (
                position[0] + instruction.direction[0],
                position[1] + instruction.direction[1],
            )
            point = matrix[position[0]][position[1]][0]
            if instruction.direction[0] > 0:
                matrix[last_position[0]][last_position[1]][2][0] = True
            elif instruction.direction[0] < 0:
                matrix[position[0]][position[1]][2][0] = True
            elif instruction.direction[1] > 0:
                matrix[last_position[0]][last_position[1]][2][1] = True
            elif instruction.direction[1] < 0:
                matrix[position[0]][position[1]][2][1] = True
            if point.y == target_y and point.x == target_x:
                break
            last_position = position


def create_rectangles(
    matrix: List[List[Tuple[Point, None, List[bool]]]], h: int, w: int
):
    for matrix_y in range(h - 1):
        for matrix_x in range(w - 1):
            matrix_value = matrix[matrix_y][matrix_x]
            nw_point = matrix_value[0]
            se_point = matrix[matrix_y + 1][matrix_x + 1][0]
            matrix[matrix_y][matrix_x] = (
                matrix_value[0],
                Rectangle(nw_point.x, nw_point.y, se_point.x, se_point.y),
                matrix_value[2],
            )


def find_interior_rectangle(
    matrix: List[List[Tuple[Point, Rectangle, List[bool]]]], w: int
) -> int:
    """
    Finds a rectangle inside the dig perimeter and returns the x position of it's nw corner.
    It is assumed that the perimeter touches the north of the matrix (y position 0).
    """
    for matrix_x in range(w - 1):
        if matrix[0][matrix_x][2][0] and matrix[0][matrix_x][2][1]:
            return matrix_x


def dig_interior(
    matrix: List[List[Tuple[Point, Rectangle, List[bool]]]], h: int, w: int
):
    dig_queue = deque()
    dig_queue.append((0, find_interior_rectangle(matrix, w)))
    while len(dig_queue) > 0:
        # These y and x values are matrix positions
        y, x = dig_queue.popleft()
        if 0 <= y < h - 1 and 0 <= x < w - 1 and not matrix[y][x][1].excavated:
            matrix[y][x][1].excavated = True
            if not matrix[y][x][2][0]:
                dig_queue.append((y, x - 1))
            if not matrix[y][x][2][1]:
                dig_queue.append((y - 1, x))
            if not matrix[y][x + 1][2][0]:
                dig_queue.append((y, x + 1))
            if not matrix[y + 1][x][2][1]:
                dig_queue.append((y + 1, x))


def measure_volume(
    matrix: List[List[Tuple[Point, Rectangle, List[bool]]]], h: int, w: int
):
    """
    Add together the areas of all the excavated rectangles,
    the areas of the gaps between the rectangles,
    and the areas of the perimeter lines.
    
    The y and x values in this function are matrix positions.
    """
    volume = 0
    for y in range(h - 1):
        for x in range(w - 1):
            rectangle = matrix[y][x][1]
            if rectangle.excavated:
                volume += rectangle.area
                north_rectangle = west_rectangle = None
                nw_excavated = ne_excavated = False
                if y > 0:
                    north_rectangle = matrix[y - 1][x][1]
                    if not north_rectangle.excavated:
                        north_rectangle = None
                if x > 0:
                    west_rectangle = matrix[y][x - 1][1]
                    if not west_rectangle.excavated:
                        west_rectangle = None
                if y > 0 and x > 0:
                    nw_excavated = matrix[y - 1][x - 1][1].excavated
                if y > 0 and x < w - 2:
                    ne_excavated = matrix[y - 1][x + 1][1].excavated
                if north_rectangle and west_rectangle:
                    volume -= (
                        north_rectangle.southern_area + west_rectangle.eastern_area - 1
                    )
                if north_rectangle and not west_rectangle:
                    volume -= north_rectangle.southern_area
                if west_rectangle and not north_rectangle:
                    volume -= west_rectangle.eastern_area
                if nw_excavated and not west_rectangle and not north_rectangle:
                    volume -= 1
                if ne_excavated and not north_rectangle:
                    volume -= 1
    return volume


def get_lava_lagoon_volume(dig_plan: List[str], use_hexadecimals: bool = False) -> int:
    instructions = parse_dig_plan(dig_plan, use_hexadecimals)
    matrix, position = create_matrix(instructions)
    h = len(matrix)
    w = len(matrix[0])
    dig_perimeter(matrix, position, instructions)
    create_rectangles(matrix, h, w)
    dig_interior(matrix, h, w)
    return measure_volume(matrix, h, w)


with open("2023/18/input.txt") as input:
    dig_plan = input.readlines()

start_time = time.time()

print(f"Answer for part 1: {get_lava_lagoon_volume(dig_plan)}")
print(f"Answer for part 2: {get_lava_lagoon_volume(dig_plan, True)}")

end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run")
