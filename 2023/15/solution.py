from typing import List, Optional, Tuple


def get_box_number(text: str) -> int:
    result = 0
    for char in text:
        ascii_code = ord(char)
        result = (result + ascii_code) * 17 % 256
    return result


def find_lens(box: List[Tuple[str, int]], label: str) -> (Optional[Tuple[str, int]], Optional[int]):
    for i in range(len(box)):
        lens = box[i]
        if lens[0] == label:
            return lens, i
    return None, None


with open("2023/15/input.txt") as input:
    steps = input.read().split(",")

sum = 0
for step in steps:
    sum += get_box_number(step)
print(f"Answer for part 1: {sum}")

boxes = {}
for step in steps:
    label = step.split("-")[0].split("=")[0]
    box_number = get_box_number(label)
    if "=" in step:
        focal_length = int(step.split("=")[1])
        if box_number in boxes.keys():
            box = boxes[box_number]
            lens, lens_index = find_lens(box, label)
            if lens is None:
                box.append((label, focal_length))
            else:
                box[lens_index] = (label, focal_length)
        else:
            box = [(label, focal_length)]
            boxes[box_number] = box
    elif box_number in boxes.keys():
        box = boxes[box_number]
        lens, lens_index = find_lens(box, label)
        if lens is not None:
            del box[lens_index]

focusing_power = 0
for box_number in boxes.keys():
    box = boxes[box_number]
    for i in range(len(box)):
        focal_length = box[i][1]
        focusing_power += (box_number + 1) * (i + 1) * focal_length

print(f"Answer for part 2: {focusing_power}")
