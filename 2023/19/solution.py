from collections import deque
import time
import copy
from typing import Dict, List


class Part:
    def __init__(self, desc: str):
        self.x, self.m, self.a, self.s = [
            int(rating.split("=")[1]) for rating in desc[1:-1].split(",")
        ]

    @property
    def rating_sum(self) -> int:
        return self.x + self.m + self.a + self.s


class PartRange:
    def __init__(self, min_x: int, max_x: int, min_m: int, max_m: int, min_a: int, max_a: int, min_s: int, max_s: int):
        self.min_values = {"x": min_x, "m": min_m, "a": min_a, "s": min_s}
        self.max_values = {"x": max_x, "m": max_m, "a": max_a, "s": max_s}

    @property
    def rating_combination_count(self):
        base_count = 1
        for category in ["x", "m", "a", "s"]:
            min = self.min_values[category]
            max = self.max_values[category]
            base_count *= max - min + 1
        return base_count


class Workflow:
    def __init__(self, desc: str):
        self.name, rules_desc = desc.strip()[:-1].split("{")
        self.rules = [Rule(rule_desc) for rule_desc in rules_desc.split(",")]

    def process_part(self, part: Part) -> str:
        for rule in self.rules:
            result = rule.apply(part)
            if result is not False:
                return result

    def process_range(self, root_range: PartRange, all_workflows: List["Workflow"]) -> (List["WorkflowRangeTask"], List[PartRange]):
        current_range = root_range
        new_tasks = []
        approved_ranges = []
        for rule in self.rules:
            if rule.criteria is None:
                new_range = current_range
            else:
                new_range, current_range = rule.split_range(current_range)
            if rule.effect == "A":
                approved_ranges.append(new_range)
            elif rule.effect != "R":
                new_tasks.append(WorkflowRangeTask(
                    all_workflows[rule.effect], new_range))
        return new_tasks, approved_ranges


class Rule:
    def __init__(self, desc: str):
        if ":" in desc:
            criteria_desc, self.effect = desc.split(":")
            self.criteria = Criteria(criteria_desc)
        else:
            self.criteria = None
            self.effect = desc

    def apply(self, part: Part) -> bool | str:
        if self.criteria is None or self.criteria.check(part):
            return self.effect
        return False

    def split_range(self, root_part_range: PartRange) -> (PartRange, PartRange):
        lesser_range_max, greater_range_min = self.criteria.get_max_and_min()
        outer_min = root_part_range.min_values[self.criteria.rating_category]
        outer_max = root_part_range.max_values[self.criteria.rating_category]
        lesser_range = greater_range = None
        if outer_min <= lesser_range_max:
            lesser_range = copy.deepcopy(root_part_range)
            lesser_range.max_values[self.criteria.rating_category] = lesser_range_max
        else:
            lesser_range = None
        if outer_max >= greater_range_min:
            greater_range = copy.deepcopy(root_part_range)
            greater_range.min_values[self.criteria.rating_category] = greater_range_min
        else:
            greater_range = None
        return (lesser_range, greater_range) if self.criteria.operator == "<" else (greater_range, lesser_range)


class Criteria:
    def __init__(self, desc: str):
        self.rating_category = desc[0]
        self.operator = desc[1]
        self.value = int(desc[2:])

    def check(self, part: Part) -> bool:
        """Do not remove the `part` argument because it is used by the inner `eval` call."""
        return eval(f"{eval(f"part.{self.rating_category}")} {self.operator} {self.value}")

    def get_max_and_min(self) -> (int, int):
        if self.operator == "<":
            return self.value - 1, self.value
        else:  # ">"
            return self.value, self.value + 1


class WorkflowPartTask:
    def __init__(self, workflow: Workflow, part: Part):
        self.workflow = workflow
        self.part = part

    def execute(self) -> str:
        return self.workflow.process_part(self.part)


class WorkflowRangeTask:
    def __init__(self, workflow: Workflow, part_range: PartRange):
        self.workflow = workflow
        self.part_range = part_range

    def execute(self, all_workflows: List[Workflow]) -> (List["WorkflowRangeTask"], List[PartRange]):
        return self.workflow.process_range(self.part_range, all_workflows)


def parse_workflows(workflows_desc: str) -> List[Workflow]:
    workflows = {}
    for desc in workflows_desc:
        workflow = Workflow(desc)
        workflows[workflow.name] = workflow
    return workflows


def process_individual_parts(workflows: Dict[str, Workflow], parts_desc: str):
    parts = []
    for desc in parts_desc:
        parts.append(Part(desc))

    task_queue = deque()
    for part in parts:
        task_queue.append(WorkflowPartTask(workflows["in"], part))
    accepted_parts = []
    while len(task_queue) > 0:
        task = task_queue.pop()
        result = task.execute()
        if result == "R":
            continue
        elif result == "A":
            accepted_parts.append(task.part)
        else:
            task_queue.append(WorkflowPartTask(workflows[result], task.part))

    accepted_part_rating_sum = 0
    for part in accepted_parts:
        accepted_part_rating_sum += part.rating_sum
    return accepted_part_rating_sum


def process_part_ranges(workflows: Dict[str, Workflow]):
    task_queue = deque()
    accepted_ranges = []
    root_range = PartRange(1, 4000, 1, 4000, 1, 4000, 1, 4000)
    initial_workflow_range_task = WorkflowRangeTask(
        workflows["in"], root_range)
    task_queue.append(initial_workflow_range_task)
    while len(task_queue) > 0:
        task = task_queue.pop()
        new_tasks, new_accepted_ranges = task.execute(workflows)
        task_queue += new_tasks
        accepted_ranges += new_accepted_ranges
    accepted_rating_combination_count = 0
    for part_range in accepted_ranges:
        accepted_rating_combination_count += part_range.rating_combination_count
    return accepted_rating_combination_count


start_time = time.time()

with open("2023/19/input.txt") as input:
    workflows_desc, parts_desc = [
        itemList.split("\n") for itemList in input.read().split("\n\n")
    ]

workflows = parse_workflows(workflows_desc)
accepted_parts_rating_sum = process_individual_parts(workflows, parts_desc)
print(f"Answer for part 1: {accepted_parts_rating_sum}")
accepted_rating_combination_count = process_part_ranges(workflows)
print(f"Answer for part 2: {accepted_rating_combination_count}")

end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run")
