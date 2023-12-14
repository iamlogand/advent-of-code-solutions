from typing import List


def validate_candidate(candidate: str, expected_damaged: List[int], input_arrangement: str) -> bool:
    damage_count = 0
    for char in candidate:
        if char == "#":
            damage_count += 1
    expected_damage_count = sum(expected_damaged)
    remaining = len(input_arrangement) - len(candidate)
    if damage_count + remaining < expected_damage_count or damage_count > expected_damage_count:
        return False
    candidate_damaged_counts = []
    parsing_group = False
    for i in range(len(candidate)):
        expected_char = input_arrangement[i]
        if candidate[i] != expected_char and expected_char != "?":
            return False
        if candidate[i] == "#":
            if parsing_group:
                candidate_damaged_counts[-1] += 1
            else:
                parsing_group = True
                candidate_damaged_counts.append(1)
        else:
            if parsing_group:
                parsing_group = False
        if not parsing_group and candidate_damaged_counts != expected_damaged[:len(candidate_damaged_counts)]:
            return False
    if len(candidate) == len(input_arrangement) and candidate_damaged_counts != expected_damaged:
        return False
    return True


def guess_answer(input_arrangement: str, candidates: List[str], expected_damaged: List[int], this_candidate: str = "", char_index: int = 0) -> List[str]:
    candidate_is_valid = validate_candidate(
        this_candidate, expected_damaged, input_arrangement)
    if not candidate_is_valid:
        return
    if char_index >= len(input_arrangement):
        candidates.append(this_candidate)
        return
    this_char = input_arrangement[char_index]
    if this_char == ".":
        guess_answer(
            input_arrangement, candidates, expected_damaged,
            this_candidate + ".", char_index + 1)
        return
    elif this_char == "#":
        guess_answer(
            input_arrangement, candidates, expected_damaged,
            this_candidate + "#", char_index + 1)
        return
    else:
        guess_answer(
            input_arrangement, candidates, expected_damaged,
            this_candidate + ".", char_index + 1)
        guess_answer(
            input_arrangement, candidates, expected_damaged,
            this_candidate + "#", char_index + 1)
        return


def sum_variants(input_arrangement: str, expected_damaged: List[int]) -> int:
    candidates = []
    guess_answer(input_arrangement, candidates, expected_damaged)
    return len(candidates)


with open("2023/12/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

print("SOLVING PART 1\n")
variant_sum = 0
for line in lines:
    input_arrangement = line.split(" ")[0]
    expected_damaged = [int(n) for n in line.split(" ")[1].split(",")]
    variant_sum += sum_variants(input_arrangement, expected_damaged)
print("Solution for part 1: {}".format(variant_sum))

print("\nSOLVING PART 2\n")
variant_sum = 0
for line_index in range(len(lines)):
    print(f"Solving line {line_index + 1} of {len(lines)}")
    line = lines[line_index]
    split_input_arrangement = [line.split(" ")[0]] * 5
    input_arrangement = ""
    for i in range(len(split_input_arrangement)):
        if i != 0:
            input_arrangement += "?"
        input_arrangement += split_input_arrangement[i]
    damaged_counts = [int(n) for n in line.split(" ")[1].split(",")] * 5
    variant_sum += sum_variants(input_arrangement, damaged_counts)
print("\nSolution for part 2: {}".format(variant_sum))
