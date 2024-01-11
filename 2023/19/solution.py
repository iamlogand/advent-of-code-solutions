from collections import deque
import time


class Part:
    def __init__(self, desc: str):
        self.x, self.m, self.a, self.s = [
            int(rating.split("=")[1]) for rating in desc[1:-1].split(",")
        ]

    @property
    def rating_sum(self) -> int:
        return self.x + self.m + self.a + self.s


class Workflow:
    def __init__(self, desc: str):
        self.name, rules_desc = desc.strip()[:-1].split("{")
        self.rules = [Rule(rule_desc) for rule_desc in rules_desc.split(",")]

    def process_part(self, part: Part):
        for rule in self.rules:
            result = rule.apply(part)
            if result is not False:
                return result


class Rule:
    def __init__(self, desc: str):
        if ":" in desc:
            criteria_desc, self.effect = desc.split(":")
            self.criteria = Criteria(criteria_desc)
        else:
            self.criteria = None
            self.effect = desc

    def apply(self, part: Part):
        if self.criteria is None or self.criteria.check(part):
            return self.effect
        return False


class Criteria:
    def __init__(self, desc: str):
        self.rating_category = desc[0]
        self.operator = desc[1]
        self.value = int(desc[2:])

    def check(self, part: Part):
        return eval(f"{eval(f"part.{self.rating_category}")} {self.operator} {self.value}")


class WorkflowTask:
    def __init__(self, workflow: Workflow, part: Part):
        self.workflow = workflow
        self.part = part

    def execute(self) -> str:
        return self.workflow.process_part(self.part)


def process_parts():
    with open("2023/19/input.txt") as input:
        workflows_desc, parts_desc = [itemList.split(
            "\n") for itemList in input.read().split("\n\n")]

    parts = []
    for desc in parts_desc:
        parts.append(Part(desc))
    workflows = {}
    for desc in workflows_desc:
        workflow = Workflow(desc)
        workflows[workflow.name] = workflow

    task_queue = deque()
    for part in parts:
        task_queue.append(WorkflowTask(workflows["in"], part))
    accepted_parts = []
    while len(task_queue) > 0:
        task = task_queue.pop()
        result = task.execute()
        if result == "R":
            continue
        elif result == "A":
            accepted_parts.append(task.part)
        else:
            task_queue.append(WorkflowTask(workflows[result], task.part))

    accepted_part_rating_sum = 0
    for part in accepted_parts:
        accepted_part_rating_sum += part.rating_sum
    return accepted_part_rating_sum


start_time = time.time()
print(f"Answer for part 1: {process_parts()}")
end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run")
