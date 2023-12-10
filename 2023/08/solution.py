import re
from math import lcm
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


def count_steps_along_route(map: str, start_pattern: str, end_pattern: str) -> int:
    instructions, nodes = parse_map(map)
    step = 0
    instruction_count = len(instructions)
    current_node = [
        nodes[key] for key in nodes.keys() if re.match(start_pattern, key) is not None
    ][0]
    while True:
        instruction_step = step % instruction_count
        instruction = instructions[instruction_step]
        next_key = current_node.left if instruction else current_node.right
        current_node = nodes[next_key]
        step += 1
        if re.match(end_pattern, next_key) is not None:
            break
    return step


with open("2023/08/input1.txt") as input:
    map1 = input.readlines()
step_count = count_steps_along_route(map1, start_pattern="AAA", end_pattern="ZZZ")
print("Solution for part 1: {}".format(step_count))

with open("2023/08/input2.txt") as input:
    map2 = input.readlines()
nodes = parse_map(map2)[1]
starting_keys = [key for key in nodes.keys() if re.match("..A", key) is not None]
step_counts = []
for key in starting_keys:
    step_count = count_steps_along_route(map2, start_pattern=key, end_pattern="..Z")
    step_counts.append(step_count)
multiple = step_counts[0]
for i in range(1, len(step_counts)):
    multiple = lcm(multiple, step_counts[i])
print("Solution for part 2: {}".format(multiple))
