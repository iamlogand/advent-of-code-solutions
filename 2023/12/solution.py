from typing import List
import itertools


def generate_combinations(target, input_count, max_num=None, prefix=None):
    combinations = []
    for combination in itertools.product(range(target + 1), repeat=input_count):
        if sum(combination) == target:
            combinations.append(combination)
    return combinations


def generate_arrangement(damaged_counts: List[int], padding: List[int] = []) -> str:
    possible_arrangement = ""
    first = True
    for i in range(len(damaged_counts)):
        count = damaged_counts[i]
        if not first:
            possible_arrangement += "."
        if i < len(padding):
            possible_arrangement += "." * padding[i]
        first = False
        possible_arrangement += "#" * count
        if i + 1 == len(damaged_counts) and i + 2 == len(padding):
            possible_arrangement += "." * padding[i + 1]
    return possible_arrangement


def sum_variants(input_arrangement: str, damaged_counts: List[int]):
    basic_arrangement = generate_arrangement(damaged_counts)
    spaces = len(damaged_counts) + 1
    padding_sum = len(input_arrangement) - len(basic_arrangement)
    if padding_sum == 0:
        return 1
    else:
        padding_combinations = generate_combinations(padding_sum, spaces)
        arrangement_count = 0
        for padding_combination in padding_combinations:
            candidate_arrangement = generate_arrangement(
                damaged_counts, padding_combination
            )
            arrangement_is_valid = True
            for i in range(len(candidate_arrangement)):
                expected_char = input_arrangement[i]
                if candidate_arrangement[i] != expected_char and expected_char != "?":
                    arrangement_is_valid = False
                    break
            if arrangement_is_valid:
                arrangement_count += 1
        return arrangement_count


with open("2023/12/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

variant_sum = 0
for line in lines:
    input_arrangement = line.split(" ")[0]
    damaged_counts = [int(n) for n in line.split(" ")[1].split(",")]
    variant_sum += sum_variants(input_arrangement, damaged_counts)
print("Solution for part 1: {}".format(variant_sum))

for line_index in range(len(lines)):
    line = lines[line_index]
    split_input_arrangement = [line.split(" ")[0]] * 5
    input_arrangement = ""
    for i in range(len(split_input_arrangement)):
        if i != 0:
            input_arrangement += "?"
        input_arrangement += split_input_arrangement[i]
    damaged_counts = [int(n) for n in line.split(" ")[1].split(",")] * 5
    variant_sum += sum_variants(input_arrangement, damaged_counts)
    print(f"Solved line {line_index + 1} of {len(lines)}")
print("Solution for part 2: {}".format(variant_sum))
