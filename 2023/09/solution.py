from typing import List


def get_differences(nums: List[int]) -> List[int]:
    """
    Take an input sequence of numbers and return a new sequence containing
    the differences between each pair of adjacent numbers
    """
    num_count = len(nums)
    differences = []
    for first_num_index in range(num_count - 1):
        first_num = nums[first_num_index]
        second_num = nums[first_num_index + 1]
        differences.append(second_num - first_num)
    return differences


def check_all_zeros(nums: List[int]) -> bool:
    """Returns True if all numbers are 0"""
    for num in nums:
        if num != 0:
            return False
    return True


def make_history(history: List[List[int]], focus_index: int, backwards: bool) -> None:
    depth = len(history) - 1
    history[depth].append(0)
    while depth > 0:
        child = history[depth][focus_index]
        depth -= 1
        sibling = history[depth][focus_index]
        if backwards:
            extrapolated_value = sibling - child
            history[depth].insert(0, extrapolated_value)
        else:
            extrapolated_value = child + sibling
            history[depth].append(extrapolated_value)


def sum_extrapolations(lines: List[str], backwards: bool = False) -> int:
    sum = 0
    focus_index = 0 if backwards else -1
    for line in lines:
        history = [[int(item) for item in line.strip().split(" ")]]
        current_sequence = history[0]
        target_length = len(current_sequence) + 1
        while not check_all_zeros(current_sequence):
            current_sequence = get_differences(current_sequence)
            history.append(current_sequence)
        while len(history[0]) < target_length:
            make_history(history, focus_index, backwards)
        sum += history[0][focus_index]
    return sum


with open("2023/09/input.txt") as input:
    lines = input.readlines()
print("Solution for part 1: {}".format(sum_extrapolations(lines)))
print("Solution for part 2: {}".format(sum_extrapolations(lines, backwards=True)))
