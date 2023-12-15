from typing import List
import time


def guess_answer(
    remaining_input: str,
    candidates: int,
    remaining_damaged: List[int],
    completed_damaged: List[int] = [],
    current_group_index: int = 0,
    this_candidate: str = "",
) -> List[str]:
    if remaining_input == "":
        return candidates + 1
    this_char = remaining_input[0]
    remaining_input = remaining_input[1:]
    if this_char == "?":
        allow_path_1 = allow_path_2 = True

        # If there are no remaining damaged
        # then force write of .s
        if allow_path_2 and remaining_damaged == []:
            allow_path_2 = False

        # If the current group is greater than or equal to the first remaining damaged
        # then force write of .s
        if allow_path_2 and current_group_index >= remaining_damaged[0]:
            allow_path_2 = False

        # If remaining space is less than the minimum space required for damaged groups
        # then force write of #s
        if (
            allow_path_1
            and current_group_index < 1
            and len(remaining_input)
            < sum(remaining_damaged) + max(len(remaining_damaged) - 1, 0)
        ):
            allow_path_1 = False

        # If part way through writing a damaged group and the end has not been reached
        # then force write of #s
        if (
            allow_path_1
            and current_group_index > 0
            and current_group_index < remaining_damaged[0]
        ):
            allow_path_1 = False

        # Path 1 - write a . (non-damaged spring)
        if allow_path_1:
            if current_group_index > 0:
                path_1_completed = completed_damaged + [remaining_damaged[0]]
                path_1_remaining = remaining_damaged[1:]
            else:
                path_1_completed = completed_damaged
                path_1_remaining = remaining_damaged
            candidates = guess_answer(
                remaining_input,
                candidates,
                path_1_remaining,
                path_1_completed,
                -1 if current_group_index > 0 else current_group_index - 1,
                this_candidate + ".",
            )
        # Path 2 - write a # (damaged spring)
        if allow_path_2:
            candidates = guess_answer(
                remaining_input,
                candidates,
                remaining_damaged,
                completed_damaged,
                1 if current_group_index < 0 else current_group_index + 1,
                this_candidate + "#",
            )
        return candidates
    else:
        if remaining_damaged == [] and "#" in remaining_input:
            return candidates
        if this_char == ".":
            if current_group_index > 0 and current_group_index < remaining_damaged[0]:
                return candidates
            candidates = guess_answer(
                remaining_input,
                candidates,
                remaining_damaged[1:] if current_group_index > 0 else remaining_damaged,
                completed_damaged + [remaining_damaged[0]]
                if current_group_index > 0
                else completed_damaged,
                -1 if current_group_index > 0 else current_group_index - 1,
                this_candidate + ".",
            )
            return candidates
        else:
            if (
                len(remaining_damaged) == 0
                or current_group_index >= remaining_damaged[0]
            ):
                return candidates
            candidates = guess_answer(
                remaining_input,
                candidates,
                remaining_damaged,
                completed_damaged,
                1 if current_group_index < 0 else current_group_index + 1,
                this_candidate + "#",
            )
            return candidates


def sum_variants(input_arrangement: str, expected_damaged: List[int]) -> int:
    candidates = guess_answer(input_arrangement, 0, expected_damaged)
    return candidates


start_time = time.time()
with open("2023/12/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

print("SOLVING PART 1")
variant_sum = 0
for line in lines:
    input_arrangement = line.split(" ")[0]
    expected_damaged = [int(n) for n in line.split(" ")[1].split(",")]
    variant_sum += sum_variants(input_arrangement, expected_damaged)
print("Answer for part 1: {}".format(variant_sum))

print("\nSOLVING PART 2")
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
print("Answer for part 2: {}".format(variant_sum))

end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run.")
