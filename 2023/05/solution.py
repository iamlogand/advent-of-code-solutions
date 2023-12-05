from typing import List


class Map:
    def __init__(
        self,
        src_category: str,
        dest_category: str,
        src_start: int,
        dest_start: int,
        range: int,
    ):
        self.src_category = src_category
        self.dest_category = dest_category
        self.src_start = src_start
        self.dest_start = dest_start
        self.range = range

    def check_in_range(self, num: int) -> bool:
        return self.src_start <= num < (self.src_start + self.range)

    def map_num(self, num: int) -> int:
        return num - self.src_start + self.dest_start


def perform_mapping(
    src_num: int, src_category: str, dest_category: str, maps: List[Map]
) -> int:
    matching_category_maps = [map for map in maps if map.src_category == src_category]
    matching_maps = [
        map for map in matching_category_maps if map.check_in_range(src_num)
    ]

    if len(matching_maps) > 0:
        selected_map = matching_maps[0]
        next_num = selected_map.map_num(src_num)
        next_category = selected_map.dest_category
    else:
        selected_map = matching_category_maps[0]
        next_num = src_num
        next_category = selected_map.dest_category

    if next_category == dest_category:
        return next_num
    else:
        return perform_mapping(next_num, next_category, dest_category, maps)


def parse_maps(lines: List[str]) -> List[Map]:
    maps = []
    lines.append("\n")
    for line in lines:
        if ":" in line:
            categories = line.split(" ")[0].split("-")
        elif line != "\n":
            map_nums = line.strip().split(" ")
            maps.append(
                Map(
                    categories[0],
                    categories[2],
                    int(map_nums[1]),
                    int(map_nums[0]),
                    int(map_nums[2]),
                )
            )
    return maps


def parse_seed_ranges(seeds_text: str) -> List[int]:
    range_values = seeds_text.strip().split(" ")[1:]
    i = 0
    ranges = []
    last_val = 0
    for value in range_values:
        if i % 2 == 0:
            last_val = int(value)
        else:
            ranges.append([last_val, last_val + int(value)])
        i += 1
    return ranges


def parse_almanac(
    almanac: str, input_has_seed_ranges: bool
) -> (List[List[int]], List[Map]):
    if input_has_seed_ranges:
        seed_ranges = parse_seed_ranges(almanac[0])
    else:
        seed_ranges = [
            [int(seed), int(seed) + 1] for seed in almanac[0].strip().split(" ")[1:]
        ]
    maps = parse_maps(almanac[2:])
    return (seed_ranges, maps)


def find_lowest_location_num(almanac: str, input_has_seed_ranges: bool = False) -> int:
    seed_ranges, maps = parse_almanac(almanac, input_has_seed_ranges)
    current_min = 999999999999
    for seed_range in seed_ranges:
        print("Processing:", seed_range)
        for s in range(seed_range[0], seed_range[1]):
            result = perform_mapping(s, "seed", "location", maps)
            if result % 100000 == 0:
                print(result)
            if result < current_min:
                current_min = result
                print(current_min, "<<< NEW MIN")
    return current_min


with open("2023/05/input.txt") as input:
    almanac = input.readlines()
    print("Solution for part 1: {}\n".format(find_lowest_location_num(almanac)))
    print("Solution for part 2: {}\n".format(find_lowest_location_num(almanac, True)))
