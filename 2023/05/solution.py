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

    @property
    def src_end(self) -> int:
        return self.src_start + self.range

    @property
    def dest_end(self) -> int:
        return self.dest_start + self.range

    def map_num(self, num: int) -> int:
        return num - self.src_start + self.dest_start


def perform_mapping(
    num_range: [int, int], this_category: str, target_category: str, maps: List[Map]
) -> int:
    matching_category_maps = [
        map for map in maps if map.src_category == this_category]
    matching_category_maps.sort(key=lambda map: map.src_start)
    try:
        next_category = matching_category_maps[0].dest_category
    except:
        return num_range[0]

    results = []
    for i in range(len(matching_category_maps)):
        map = matching_category_maps[i]

        # Check if the map has any overlap with the num range
        if map.src_start < num_range[1] and map.src_end > num_range[0]:

            # Perform mapping on num range after the last mapping but before this mapping
            if len(results) > 1:
                result_start = perform_mapping(
                    [matching_category_maps[-1].src_end, map.src_start], next_category, target_category, maps)
                results.append(result_start)

            # Perform mapping on num range before the first mapping
            if len(results) == 0 and map.src_start > num_range[0]:
                result_start = perform_mapping(
                    [num_range[0], map.src_start], next_category, target_category, maps)
                results.append(result_start)

            # Perform mapping on num range using this map
            sub_range_start = max(map.src_start, num_range[0])
            sub_range_end = min(map.src_end, num_range[1])
            result_start = perform_mapping(
                [map.map_num(sub_range_start), map.map_num(sub_range_end)], next_category, target_category, maps)
            results.append(result_start)

    if len(results) > 0:
        # Perform mapping on num range after the last mapping
        result_start = perform_mapping(
            [matching_category_maps[-1].src_end, num_range[1]], next_category, target_category, maps)
        results.append(result_start)
    else:
        # Perform mapping on entire num range if there are no overlapping mappings
        result_start = perform_mapping(
            [num_range[0], num_range[1]], next_category, target_category, maps)
        results.append(result_start)
    return min(results)


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
    current_min = 99999999999
    for seed_range in seed_ranges:
        result_start = perform_mapping(
            seed_range, "seed", "location", maps)
        if result_start < current_min:
            current_min = result_start
    return current_min


with open("2023/05/input.txt") as input:
    almanac = input.readlines()
    print("Solution for part 1: {}\n".format(
        find_lowest_location_num(almanac)))
    print("Solution for part 2: {}\n".format(
        find_lowest_location_num(almanac, True)))
