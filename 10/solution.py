import re


class Process:

    x = 1
    objects = []

    @classmethod
    def execute_first(cls):
        if cls.objects:
            cls.objects[0].execute()

    def __init__(self, remaining_cycles, task=None):
        self.remaining_cycles = remaining_cycles
        self.task = task
        Process.objects.append(self)

    def execute(self):
        self.remaining_cycles -= 1
        if self.remaining_cycles == 0: 
            if self.task != None:
                Process.x += int(self.task)
            self.remove_object()

    def remove_object(self):
        process_list = Process.objects
        for i in range(len(process_list)):
            if self == process_list[i]:
                del process_list[i]
                break


with open('10/input.txt') as input:
    program = input.readlines()

instruction_index = 1
sum = 0
interesting_cycles = [20, 60, 100, 140, 180, 220]

while True:
    if instruction_index < len(program):
        instructions = program[instruction_index]
        steps = re.split(" ", instructions)
        if steps[0] == "addx":
            Process(2, steps[1])
        elif steps[0] == "noop":
            Process(1)
    elif len(Process.objects) == 0:
        break

    Process.execute_first()

    print("instruction={}, x={}, process_count={}".format(instruction_index, Process.x, len(Process.objects)))

    if instruction_index in interesting_cycles:
        for cycle in interesting_cycles:
            if cycle == instruction_index:
                print("adding {} x {}".format(cycle, Process.x))
                sum += cycle * Process.x

    instruction_index += 1

print(sum)