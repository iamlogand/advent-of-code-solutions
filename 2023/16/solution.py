from collections import deque
import copy
from typing import List


class Tile:
    def __init__(self, y: int, x: int, mirror: str | None = None):
        self.y = y
        self.x = x
        self.mirror = mirror
        self.beam_left = False
        self.beam_up = False
        self.beam_right = False
        self.beam_down = False
        self.energized = False

    def add_beam(self, direction: str) -> bool:
        new_energized = False
        new_direction = False
        match direction:
            case "left":
                if not self.beam_left:
                    self.beam_left = True
                    new_direction = True
            case "up":
                if not self.beam_up:
                    self.beam_up = True
                    new_direction = True
            case "right":
                if not self.beam_right:
                    self.beam_right = True
                    new_direction = True
            case "down":
                if not self.beam_down:
                    self.beam_down = True
                    new_direction = True
        if not self.energized:
            self.energized = True
            new_energized = True
        return new_energized, new_direction


def get_adjacent_coordinates(y: int, x: int, direction: str) -> (int, int):
    match direction:
        case "left":
            return y, x - 1
        case "up":
            return y - 1, x
        case "right":
            return y, x + 1
        case "down":
            return y + 1, x


def get_reflected_directions(mirror: str, direction: str) -> List[str]:
    new_directions = []
    if (
        (mirror == "-" and (
            direction == "left" or direction == "up" or direction == "down"))
        or (mirror == "/" and direction == "down")
        or (mirror == "\\" and direction == "up")
    ):
        new_directions.append("left")
    if (
        (mirror == "|" and (
            direction == "left" or direction == "up" or direction == "right"))
        or (mirror == "/" and direction == "right")
        or (mirror == "\\" and direction == "left")
    ):
        new_directions.append("up")
    if (
        (mirror == "-" and (
            direction == "up" or direction == "right" or direction == "down"))
        or (mirror == "/" and direction == "up")
        or (mirror == "\\" and direction == "down")
    ):
        new_directions.append("right")
    if (
        (mirror == "|" and (
            direction == "left" or direction == "right" or direction == "down"))
        or (mirror == "/" and direction == "left")
        or (mirror == "\\" and direction == "right")
    ):
        new_directions.append("down")
    return new_directions


def get_total_energized(matrix, entry_direction: str, position: int, height: int, width: int):
    if entry_direction == "left":
        y, x = position, width - 1
    if entry_direction == "up":
        y, x = height - 1, position
    if entry_direction == "right":
        y, x = position, 0
    if entry_direction == "down":
        y, x = 0, position
    matrix = copy.deepcopy(matrix)
    pending_beams = deque([[y, x, entry_direction]])
    energized_count = 0
    while len(pending_beams) > 0:
        beam_y, beam_x, beam_direction = pending_beams.pop()
        if beam_y < 0 or beam_y >= height or beam_x < 0 or beam_x >= width:
            continue
        tile = matrix[beam_y][beam_x]
        new_energized, new_direction = tile.add_beam(beam_direction)
        if new_energized:
            energized_count += 1
        if new_direction:
            mirror = tile.mirror
            if mirror is None:
                next_y, next_x = get_adjacent_coordinates(
                    beam_y, beam_x, beam_direction)
                pending_beams.append([next_y, next_x, beam_direction])
            else:
                reflected_directions = get_reflected_directions(
                    mirror, beam_direction)
                for direction in reflected_directions:
                    next_y, next_x = get_adjacent_coordinates(
                        beam_y, beam_x, direction)
                    pending_beams.append([next_y, next_x, direction])
    return energized_count


with open("2023/16/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

rows = []
height = len(lines)
width = len(lines[0])
matrix = []
for row_index in range(height):
    row = []
    for col_index in range(width):
        char = lines[row_index][col_index]
        tile = Tile(
            row_index, col_index, char if char in [
                "|", "-", "/", "\\"] else None
        )
        row.append(tile)
    matrix.append(row)

total = get_total_energized(matrix, "right", 0, height, width)
print(f"Answer for part 1: {total}")

largest_total = 0
for y in range(height):
    largest_total = max(largest_total, get_total_energized(
        matrix, "left", y, height, width), get_total_energized(matrix, "right", y, height, width))
for x in range(width):
    largest_total = max(largest_total, get_total_energized(
        matrix, "up", x, height, width), get_total_energized(matrix, "down", x, height, width))
print(f"Answer for part 2: {largest_total}")
