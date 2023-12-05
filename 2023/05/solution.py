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


def parse_almanac(almanac: str) -> (List[int], List[Map]):
    seeds = [int(seed) for seed in almanac[0].strip().split(" ")[1:]]
    maps = parse_maps(almanac[2:])
    return (seeds, maps)


def find_lowest_location_num(almanac: str) -> int:
    seeds, maps = parse_almanac(almanac)
    locations = []
    for seed in seeds:
        locations.append(perform_mapping(seed, "seed", "location", maps))
    return min(locations)


with open("2023/05/input.txt") as input:
    almanac = input.readlines()
    print("Solution for part 1: {}\n".format(find_lowest_location_num(almanac)))
