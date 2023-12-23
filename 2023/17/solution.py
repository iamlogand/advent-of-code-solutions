from functools import cache
from typing import List, Tuple
import time


def get_movements(y: int, x: int, direction: int, matrix: List[str]) -> List[Tuple[int, int, int, int]]:
    """
    Gets a list of possible movements, where each movement contains a new y, a new x, a new direction
    and list of coordinates that were passed through for each
    """
    if direction in [0, 2]:
        next_directions = [1, 3]
    else:
        next_directions = [0, 2]
    movements = []
    x_dir = y_dir = 0
    match direction:
        case 0:
            x_dir = -1
        case 1:
            y_dir = -1
        case 2:
            x_dir = 1
        case 3:
            y_dir = 1
    for next_direction in next_directions:
        for distance in range(1, 4):
            loss_increase = 0
            for i in range(1, distance + 1):
                try:
                    loss_increase += int(matrix[y + y_dir * i][x + x_dir * i])
                except IndexError:
                    pass
            movements.append(
                (y + y_dir * distance, x + x_dir * distance, next_direction, loss_increase))
    return movements


def find_best_path(matrix: List[str], target_y: int, target_x: int, base_loss: int) -> int:
    h = len(matrix)
    w = len(matrix[0])
    half_circumference = h + w - 1

    def custom_sort(movement: (int, int, int, List[Tuple[int, int]])):
        match movement[2]:
            case 2 | 3:
                return 0
            case 0 | 1:
                return 1

    @cache
    def find_path(y: int, x: int, direction: int, loss: int, min_loss: int) -> int:
        """
        Returns minimum loss.
        """
        if loss >= abs(min_loss) or loss + half_circumference - y - x > abs(min_loss):
            return min_loss
        if y == target_y and x == target_x:
            print("New lowest loss:", loss)
            return loss
        movements = get_movements(y, x, direction, matrix)
        movements.sort(key=custom_sort)
        for movement in movements:
            this_loss = loss + movement[3]
            if 0 <= y < h and 0 <= x < w:
                min_loss = find_path(
                    movement[0], movement[1], movement[2], this_loss, min_loss)
        return min_loss

    return find_path(0, 0, 2, 0, base_loss)


start_time = time.time()

with open("2023/17/input.txt") as input:
    matrix = [line.strip() for line in input.readlines()]

BASE_LOSS = 1000

min_loss = find_best_path(
    matrix, len(matrix) - 1, len(matrix[0]) - 1, BASE_LOSS)
print(f"Answer for part 1: {min_loss}")

end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run")
