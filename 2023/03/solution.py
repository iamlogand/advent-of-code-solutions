from typing import List


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class PartNumber:
    def __init__(self, number: int, zone_start: Point, zone_end: Point):
        self.number: int = number

        # The "zone" is the area around the part number where a symbol would be considered adjacent.
        # These are represented by start (top left) and end (bottom right) coordinates.
        self.zone_start: Point = zone_start
        self.zone_end: Point = zone_end


def check_for_symbol(schematic, zone_start: (int, int), zone_end: (int, int)):
    max_y = len(schematic) - 1
    max_x = len(schematic[0]) - 1

    for y in range(zone_start.y, zone_end.y + 1):
        for x in range(zone_start.x, zone_end.x + 1):
            if y < 0 or x < 0 or y >= max_y or x >= max_x:
                continue
            char = schematic[y][x]
            if not char.isnumeric() and char != ".":
                return True
    return False


def get_part_numbers(line: str, y: int) -> List[PartNumber]:
    part_nums = []
    current_num = ""
    width = len(line)
    for i in range(width + 1):
        if i != width and line[i] in "1234567890":
            current_num += line[i]
        elif current_num != "":
            zone_start = Point(i - len(current_num) - 1, y - 1)
            zone_end = Point(i, y + 1)
            part_nums.append(PartNumber(int(current_num), zone_start, zone_end))
            current_num = ""
    return part_nums


def sum_all_part_numbers(schematic: str) -> int:
    part_nums = []
    y = 0
    for line in schematic:
        part_nums += get_part_numbers(line.strip(), y)
        y += 1

    sum = 0
    for part_num in part_nums:
        is_near_symbol = check_for_symbol(
            schematic, part_num.zone_start, part_num.zone_end
        )
        if is_near_symbol:
            sum += part_num.number

        # print(
        #     part_num.number,
        #     (part_num.zone_start.x, part_num.zone_start.y),
        #     (part_num.zone_end.x, part_num.zone_end.y),
        #     is_near_symbol,
        # )
    return sum


with open("2023/03/input.txt") as input:
    schematic = input.readlines()

    print("Solution for part 1: {}".format(sum_all_part_numbers(schematic)))
