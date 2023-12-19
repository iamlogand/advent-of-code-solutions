import copy


def get_reflection_summary(pattern, smudge_y=None, smudge_x=None, invalid_result=None):
    h = len(pattern)
    for reflection_y in range(1, h):
        if smudge_y is not None and (
            smudge_y > reflection_y * 2 or smudge_y < h - (h - reflection_y) * 2
        ):
            continue
        top_matrix = pattern[:reflection_y]
        bottom_matrix = pattern[reflection_y:]
        scope_h = min(len(top_matrix), len(bottom_matrix))
        if scope_h < 1:
            continue
        scoped_top_matrix = top_matrix[-scope_h:]
        scoped_bottom_matrix = bottom_matrix[:scope_h]
        if (
            scoped_top_matrix == scoped_bottom_matrix[::-1]
            and invalid_result != reflection_y * 100
        ):
            return reflection_y * 100
    w = len(pattern[0])
    for reflection_x in range(1, w):
        if smudge_x is not None and (
            smudge_x > reflection_x * 2 or smudge_x < w - (w - reflection_x) * 2
        ):
            continue
        left_matrix = [row[:reflection_x] for row in pattern]
        right_matrix = [row[reflection_x:] for row in pattern]
        scope_w = min(len(left_matrix[0]), len(right_matrix[0]))
        if scope_w < 1:
            continue
        scoped_left_matrix = [row[-scope_w:] for row in left_matrix]
        scoped_right_matrix = [row[:scope_w] for row in right_matrix]
        if (
            scoped_left_matrix == [row[::-1] for row in scoped_right_matrix]
            and invalid_result != reflection_x
        ):
            return reflection_x
    return None


def summarize_smudged_mirror(pattern):
    invalid_result = get_reflection_summary(pattern)
    for row_index in range(len(pattern)):
        for col_index in range(len(pattern[0])):
            candidate = copy.deepcopy(pattern)
            candidate[row_index][col_index] = not candidate[row_index][col_index]
            result = get_reflection_summary(
                candidate, row_index, col_index, invalid_result
            )
            if result is not None:
                return result


with open("2023/13/input.txt") as input:
    lines = [line.strip() for line in input.readlines()]

patterns = []
row_index = 0
current_pattern = []
for line in lines:
    if len(line) == 0:
        row_index = 0
    else:
        if row_index == 0:
            current_pattern = []
            patterns.append(current_pattern)
        current_pattern.append([char == "#" for char in line])
        row_index += 1

sum = 0
for pattern in patterns:
    sum += get_reflection_summary(pattern)
print("Answer for part 1: {}".format(sum))


sum = 0
for pattern in patterns:
    sum += summarize_smudged_mirror(pattern)
print("Answer for part 2: {}".format(sum))
