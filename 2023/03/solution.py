from typing import List


class Point:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x


class Symbol:
    def __init__(self, character: str, position: Point):
        self.character: str = character
        self.position: Point = position


class PartNumber:
    def __init__(self, number: int, start: Point, end: Point):
        self.number: int = number
        self.start: Point = start
        self.end: Point = end


def get_adjacent_part_numbers(
    symbol: Symbol, part_nums: List[PartNumber]
) -> (List[PartNumber], List[PartNumber]):
    matches = []
    rejects = []

    for part in part_nums:
        # check adjacency
        is_y_adjacent = part.start.y - 1 <= symbol.position.y <= part.end.y + 1
        is_x_adjacent = part.start.x - 1 <= symbol.position.x <= part.end.x + 1
        if is_y_adjacent and is_x_adjacent:
            matches.append(part)
        else:
            rejects.append(part)

    return (matches, rejects)


def parse_schematic(line: str, y: int) -> (List[PartNumber], List[Symbol]):
    part_nums = []
    symbols = []
    current_num = ""
    width = len(line)
    for i in range(width + 1):
        if i != width and line[i].isnumeric():
            current_num += line[i]
        elif current_num != "":
            start = Point(y, i - len(current_num))
            end = Point(y, i - 1)
            part_nums.append(PartNumber(int(current_num), start, end))
            current_num = ""

        if i != width and not line[i].isnumeric() and line[i] != ".":
            position = Point(y, i)
            symbols.append(Symbol(line[i], position))
    return part_nums, symbols


def solve_problem(schematic: str) -> int:
    part_nums = []
    symbols = []
    y = 0
    for line in schematic:
        new_part_nums, new_symbols = parse_schematic(line.strip(), y)
        part_nums = part_nums + new_part_nums
        symbols = symbols + new_symbols
        y += 1

    sum = 0
    for symbol in symbols:
        matching_part_nums, remaining_part_nums = get_adjacent_part_numbers(
            symbol, part_nums
        )
        for part_num in matching_part_nums:
            sum += part_num.number
        part_nums = remaining_part_nums
    return sum


with open("2023/03/input.txt") as input:
    schematic = input.readlines()

    print("Solution for part 1: {}".format(solve_problem(schematic)))
