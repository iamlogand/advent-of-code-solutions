def get_reflection_summary(pattern):
    for reflection_y in range(1, len(pattern)):
        top_matrix = pattern[:reflection_y]
        bottom_matrix = pattern[reflection_y:]
        scope_h = min(len(top_matrix), len(bottom_matrix))
        if scope_h < 1:
            continue
        scoped_top_matrix = top_matrix[-scope_h:]
        scoped_bottom_matrix = bottom_matrix[:scope_h]
        if scoped_top_matrix == scoped_bottom_matrix[::-1]:
            return reflection_y * 100
    for reflection_x in range(1, len(pattern[0])):
        left_matrix = [row[:reflection_x] for row in pattern]
        right_matrix = [row[reflection_x:] for row in pattern]
        scope_w = min(len(left_matrix[0]), len(right_matrix[0]))
        if scope_w < 1:
            continue
        scoped_left_matrix = [row[-scope_w:] for row in left_matrix]
        scoped_right_matrix = [row[:scope_w] for row in right_matrix]
        if scoped_left_matrix == [row[::-1] for row in scoped_right_matrix]:
            return reflection_x


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