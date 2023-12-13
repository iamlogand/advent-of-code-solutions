from typing import List
import itertools


def generate_combinations(target, input_count, max_num=None, prefix=None):
    combinations = []
    for combination in itertools.product(range(2), repeat=input_count):
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
    unknowns = list(input_arrangement).count("?")
    total_damaged = sum(damaged_counts)
    known_damaged = list(input_arrangement).count("#")
    possible_unknowns = generate_combinations(
        total_damaged - known_damaged, unknowns)
    arrangement_count = 0
    for possible_unknown in possible_unknowns:
        candidate_arrangement = ""
        sub_index = 0
        for char in input_arrangement:
            if char == "?":
                candidate_arrangement += "#" if possible_unknown[sub_index] == 1 else "."
                sub_index += 1
            else:
                candidate_arrangement += char
        arrangement_is_valid = True
        candidate_damaged_counts = []
        parsing_group = False
        for i in range(len(candidate_arrangement)):
            expected_char = input_arrangement[i]
            if candidate_arrangement[i] != expected_char and expected_char != "?":
                arrangement_is_valid = False
                break
            if candidate_arrangement[i] == "#":
                if parsing_group:
                    candidate_damaged_counts[-1] += 1
                else:
                    parsing_group = True
                    candidate_damaged_counts.append(1)
            else:
                if parsing_group:
                    parsing_group = False
            if not parsing_group and candidate_damaged_counts != damaged_counts[:len(candidate_damaged_counts)]:
                arrangement_is_valid = False
                break
        if candidate_damaged_counts == damaged_counts and arrangement_is_valid:
            arrangement_count += 1
            print(".", end="")
    print()
    return arrangement_count


with open("2023/12/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

variant_sum = 0
for line in lines:
    input_arrangement = line.split(" ")[0]
    damaged_counts = [int(n) for n in line.split(" ")[1].split(",")]
    variant_sum += sum_variants(input_arrangement, damaged_counts)
print("Solution for part 1: {}".format(variant_sum))

variant_sum = 0
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
