import copy
from typing import List


class SuperBreak(Exception):
    """ Used to break nested for loops. """
    pass


def slide_rocks_one_step(row: List[int]) -> (List[int], bool):
    """ Slides rocks towards the start of the list by one step. """
    l = len(row)
    has_changed = False
    for first_item_index in range(0, l - 1):
        if row[first_item_index] == "." and row[first_item_index + 1] == "O":
            has_changed = True
            row[first_item_index], row[first_item_index + 1] = "O", "."
    return row, has_changed


def slide_rocks(row: List[int]) -> List[int]:
    """ Slides rocks towards the start of the list until they stop. """
    has_changed = True
    while has_changed:
        row, has_changed = slide_rocks_one_step(row)
    return row


def rotate_matrix_cw(matrix: List[List[int]], turns: int = 1) -> List[List[int]]:
    """ Rotate a 2 dimensional matrix clockwise by 90 degrees. """
    for i in range(turns):
        h = len(matrix)
        w = len(matrix[0])
        new_matrix = []
        for row_index in range(w):
            row = []
            for col_index in range(h):
                row.append(matrix[h - col_index - 1][row_index])
            new_matrix.append(row)
        matrix = new_matrix
    return new_matrix


def score_matrix(matrix: List[List[int]]) -> int:
    """ Get the total load on the North support beams, assuming default orientation. """
    score_level = len(matrix)
    score = 0
    for line in matrix:
        for char in line:
            if char == "O":
                score += score_level
        score_level -= 1
    return score


with open("2023/14/input.txt") as input:
    lines = input.readlines()

original_matrix = [[char for char in line.strip()] for line in lines]
matrix = rotate_matrix_cw(original_matrix, 3)
for row in matrix:
    row = slide_rocks(row)
matrix = rotate_matrix_cw(matrix)
print(f"Answer for part 1: {score_matrix(matrix)}")

CYCLE_COUNT = 1000000000
matrix = rotate_matrix_cw(original_matrix, 3)
saved_arrangements = []
start = end = None
try:
    for i in range(CYCLE_COUNT):
        for j in range(4):
            for row in matrix:
                row = slide_rocks(row)
            matrix = rotate_matrix_cw(matrix)
        if matrix not in saved_arrangements:
            saved_arrangements.append(matrix)
            matrix = copy.deepcopy(matrix)
        else:
            for k in range(len(saved_arrangements)):
                if saved_arrangements[k] == matrix:
                    start, end = (k, i)
                    raise SuperBreak
except SuperBreak:
    pass
target_iteration_index = (CYCLE_COUNT - 1 - start) % (end - start) + start
matrix = rotate_matrix_cw(saved_arrangements[target_iteration_index])
print(f"Answer for part 2: {score_matrix(matrix)}")
