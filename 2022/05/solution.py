import re, copy


# Build a matrix to represent the stacks of crates
def convert_arrangement_string_to_matrix(arrangement_string):
    matrix = [[],[],[],[],[],[],[],[],[]]
    for line in arrangement_string:
        for stack in range(9):  # Starting arrangement has stacks 1 to 9
            crate_position = stack * 4 + 1
            matrix[stack].append(line[crate_position])
    return matrix

'''
Remove whitespace cells from the arrangement.
Assumes that input arrangement crates are ordered from bottom to top.
Also assumes that no crates are 'floating' above empty space.
'''
def clean_whitespace_from_arrangement(arrangement):
    for stack in range(9):
        for crate in range(8):  # The highest stack in the starting arrangement is 8 crates tall
            if arrangement[stack][crate] == " ":
                arrangement[stack] = arrangement[stack][0:crate]
                break
    return arrangement

def print_arrangement(arrangement):
    for stack in arrangement:
        print(stack)

def rearrange_crates(arrangement, instructions, model_number):
    
    for instruction in instructions:

        # Get the quantity, origin and target from the instruction sentence
        split_instruction = re.split(" ", instruction)
        quantity = int(split_instruction[1])
        origin = int(split_instruction[3]) - 1
        target = int(split_instruction[5]) - 1

        # Add crates to the target stack
        crates_to_move = arrangement[origin][-quantity:]
        if model_number < 9001:
            crates_to_move.reverse()
        arrangement[target].extend(crates_to_move)

        # Remove crates from the origin stack
        del arrangement[origin][-quantity:]

    return arrangement

def get_top_crates(arrangement):
    top_crates = ''
    for stack in arrangement:
        top_crates += stack[-1]
    return top_crates

def print_report(arrangement, model_number):
    print("Predicted rearrangement outcome using the CrateMover {}:".format(model_number))
    print_arrangement(arrangement)
    print("Top crates: {}".format(get_top_crates(arrangement)))


with open('2022/05/input.txt') as file:
    inputLines = file.readlines()

# Convert the starting arrangement input string to a matrix
starting_arrangement = convert_arrangement_string_to_matrix(inputLines[0:8])

# Reverse the order of crates to suit my personal preference (from bottom to top)
for stack in starting_arrangement:
    stack.reverse()

# Remove whitespace cells from the arrangement
starting_arrangement = clean_whitespace_from_arrangement(starting_arrangement)

# Part 1 - rearrange crates using the CrateMover 9000
part1_arrangement = rearrange_crates(copy.deepcopy(starting_arrangement), inputLines[10:], 9000)
print_report(part1_arrangement, 9000)

print()

# Part 2 - rearrange crates using the CrateMover 9001
part2_arrangement = rearrange_crates(copy.deepcopy(starting_arrangement), inputLines[10:], 9001)
print_report(part2_arrangement, 9001)
