from functools import cache
import time
from typing import List


"""
I couldn't solve the problem myself - my solution is based on another solution I found online,
and this is my first exposure to dynamic programming.

This solution uses a dynamic programming. The problem is broken down into sub-problems,
where each sub-problem is solved by the `sum_variants` function once.
The function has been setup to take repeatable arguments
and it uses memoization to cache results for a specific combination of arguments.
This approach prevents the same sub-problem from being solved more than once,
which saves loads of time.
"""


def sum_variants_for_line(input_arrangement: str, expected_damaged: List[int]) -> int:
    @cache
    def sum_variants(index: int = 0, damaged_index: int = 0, variant_count: int = 0):
        """
        Counts the number of valid combinations that can be formed based on the input arrangement,
        expected damaged, current indices and the variant count.

        Arguments:
            index (int): the current index in input_arrangement.
            damaged_index (int): the current index in expected_damaged.
            variant_count (int): counter for valid combinations that have been found.

        Returns:
            int: the passed variant count plus the number of new valid combinations found.
        """

        if index == len(input_arrangement):
            # End has been reached (returns True if valid)
            return damaged_index == len(expected_damaged)

        if input_arrangement[index] in [".", "?"]:
            # Path for the next character being "."
            variant_count += sum_variants(index + 1, damaged_index)

        if damaged_index < len(expected_damaged):
            damaged_end_index = index + expected_damaged[damaged_index]

            # Check if it's possible to place a "#" character
            # at the current index considering the current damaged index
            if (
                "." not in input_arrangement[index:damaged_end_index]
                and damaged_end_index < len(input_arrangement)
                and "#" not in input_arrangement[damaged_end_index]
            ):
                # Path for the next character being "#"
                variant_count += sum_variants(damaged_end_index + 1, damaged_index + 1)

        return variant_count

    return sum_variants()


start_time = time.time()

with open("2023/12/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

sum = 0
for line in lines:
    input_arrangement = line.split(" ")[0] + "."
    expected_damaged = [int(i) for i in line.split(" ")[1].split(",")]
    sum += sum_variants_for_line(input_arrangement, expected_damaged)
print("Answer for part 1: {}".format(sum))

sum = 0
for line in lines:
    input_arrangement = (line.split(" ")[0] + "?") * 5
    expected_damaged = [int(i) for i in line.split(" ")[1].split(",")] * 5
    sum += sum_variants_for_line(input_arrangement, expected_damaged)
print("Answer for part 2: {}".format(sum))

end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run")
