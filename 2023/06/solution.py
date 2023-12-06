from typing import List


def parse_input(race_stats: str) -> List[object]:
    records = []
    for line_index in range(len(race_stats)):
        line = race_stats[line_index]
        nums = [i for i in line[9:].strip().split(" ") if len(i) > 0]
        for num_index in range(len(nums)):
            num = int(nums[num_index])
            if line_index == 0:
                records.append({"time": num})
            else:
                records[num_index]["distance"] = num
    return records


def parse_input_as_one_race(race_stats: str) -> object:
    record = {}
    for line_index in range(len(race_stats)):
        line = race_stats[line_index]
        num_elements = [i for i in line[9:].strip().split(" ") if len(i) > 0]
        num = ""
        for elem_index in range(len(num_elements)):
            num += num_elements[elem_index]
        num_value = int(num)
        if line_index == 0:
            record["time"] = num_value
        else:
            record["distance"] = num_value
    return record


def solve_problem(race_stats: str, one_race: bool = False) -> int:
    if one_race:
        records = [parse_input_as_one_race(race_stats)]
    else:
        records = parse_input(race_stats)

    product = None
    for record in records:
        winning_strategy_count = 0
        for hold_time in range(0, record["time"]):
            distance = (record["time"] - hold_time) * hold_time
            if distance > record["distance"]:
                winning_strategy_count += 1
        product = (
            winning_strategy_count
            if product is None
            else product * winning_strategy_count
        )

    return product


with open("2023/06/input.txt") as input:
    race_stats = input.readlines()
    print("Solution for part 1: {}".format(solve_problem(race_stats)))
    print("Solution for part 2: {}".format(solve_problem(race_stats, True)))
