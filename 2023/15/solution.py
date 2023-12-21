def apply_step(text: str):
    result = 0
    for char in text:
        ascii_code = ord(char)
        result = (result + ascii_code) * 17 % 256
    return result


with open("2023/15/input.txt") as input:
    steps = input.read().split(",")

sum = 0
for step in steps:
    sum += apply_step(step)
print(f"Answer for part 1: {sum}")
