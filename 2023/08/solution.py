from typing import Dict


class Node:
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right


def parse_map(map: str) -> (str, Dict[str, Node], str):
    instructions = [char == "L" for char in map[0].strip()]
    nodes = {}
    for line in map[2:]:
        key = line.split(" ")[0]
        left, right = line.strip().split("(")[1][:-1].split(", ")
        nodes[key] = Node(left, right)
    return instructions, nodes


def solve_part_1(map: str) -> int:
    instructions, nodes = parse_map(map)
    step = 0
    instruction_count = len(instructions)
    current_node = nodes["AAA"]
    while True:
        instruction_step = step % instruction_count
        instruction = instructions[instruction_step]
        next_key = current_node.left if instruction else current_node.right
        current_node = nodes[next_key]
        step += 1
        if next_key == "ZZZ":
            break
    return step


def solve_part_2(map: str) -> int:
    instructions, nodes = parse_map(map)
    step = 0
    instruction_count = len(instructions)
    current_nodes = [nodes[key] for key in nodes.keys() if key[-1] == "A"]
    ghost_count = len(current_nodes)
    while True:
        instruction_step = step % instruction_count
        instruction = instructions[instruction_step]
        all_keys_end_in_Z = True
        for i in range(ghost_count):
            current_node = current_nodes[i]
            next_key = current_node.left if instruction else current_node.right
            if all_keys_end_in_Z and next_key[-1] != "Z":
                all_keys_end_in_Z = False
            current_nodes[i] = nodes[next_key]
        step += 1
        if all_keys_end_in_Z:
            break
    return step


with open("2023/08/input1.txt") as input:
    map = input.readlines()
    print("Solution for part 1: {}".format(solve_part_1(map)))

with open("2023/08/input2.txt") as input:
    map = input.readlines()
    print("Solution for part 2: {}".format(solve_part_2(map)))
