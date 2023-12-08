from typing import Dict


class Node:
    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right


def parse_map(map: str) -> (str, Dict[str, Node], str):
    instructions = map[0].strip()
    nodes = {}
    for line in map[2:]:
        key = line.split(" ")[0]
        left, right = line.strip().split("(")[1][:-1].split(", ")
        nodes[key] = Node(left, right)
    return instructions, nodes


def solve_problem(map: str) -> int:
    instructions, nodes = parse_map(map)
    step = 0
    instruction_count = len(instructions)
    current_node = nodes["AAA"]
    while True:
        instruction_step = step % instruction_count
        instruction = instructions[instruction_step]
        next_key = current_node.left if instruction == "L" else current_node.right
        current_node = nodes[next_key]
        step += 1
        if next_key == "ZZZ":
            break
    return step


with open("2023/08/input.txt") as input:
    map = input.readlines()
    print("Solution for part 1: {}".format(solve_problem(map)))
