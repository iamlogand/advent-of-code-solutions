import time
from collections import deque
from typing import Dict, List


BASE_LOSS = 1000


def find_best_path(
    matrix: List[str],
    target_y: int,
    target_x: int,
    min_distance: int = 1,
    max_distance: int = 3,
) -> int:
    h = len(matrix)
    w = len(matrix[0])
    queued_paths = deque()
    queued_paths.append(
        {
            "y": 0,
            "x": 0,
            "direction": 2,
            "loss": 0,
        }
    )
    cached_losses = [
        [[BASE_LOSS for _ in range(0, 4)] for _ in range(w)] for _ in range(h)
    ]
    min_loss = BASE_LOSS

    def get_possible_movements(
        y: int, x: int, direction: int, loss: int
    ) -> List[Dict[str, int]]:
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
            for distance in range(min_distance, max_distance + 1):
                new_loss = loss
                out_of_bounds = False
                for i in range(1, distance + 1):
                    try:
                        new_loss += int(matrix[y + y_dir * i][x + x_dir * i])
                    except IndexError:
                        out_of_bounds = True
                if out_of_bounds:
                    continue
                new_y = y + y_dir * distance
                new_x = x + x_dir * distance
                if 0 <= new_y < h and 0 <= new_x < w:
                    movements.append(
                        {
                            "y": new_y,
                            "x": new_x,
                            "direction": next_direction,
                            "loss": new_loss,
                        }
                    )
        return movements

    def find_path(y: int, x: int, direction: int, loss: int):
        """
        Returns minimum loss.
        """
        nonlocal min_loss
        movements = get_possible_movements(y, x, direction, loss)
        for movement in movements:
            if (
                cached_losses[movement["y"]][movement["x"]][movement["direction"]]
                > movement["loss"]
            ):
                cached_losses[movement["y"]][movement["x"]][
                    movement["direction"]
                ] = movement["loss"]
                queued_paths.append(
                    {
                        "y": movement["y"],
                        "x": movement["x"],
                        "direction": movement["direction"],
                        "loss": movement["loss"],
                    }
                )
            if (
                movement["y"] == target_y
                and movement["x"] == target_x
                and movement["loss"] < min_loss
            ):
                min_loss = movement["loss"]

    counter = 0
    while len(queued_paths) > 0:
        this_path = queued_paths.popleft()
        find_path(
            this_path["y"], this_path["x"], this_path["direction"], this_path["loss"]
        )
        counter += 1
    return min_loss


start_time = time.time()

with open("2023/17/input.txt") as input:
    matrix = [line.strip() for line in input.readlines()]

min_loss = find_best_path(matrix, len(matrix) - 1, len(matrix[0]) - 1)
print(f"Answer for part 1: {min_loss}")

min_loss = find_best_path(matrix, len(matrix) - 1, len(matrix[0]) - 1, 4, 10)
print(f"Answer for part 2: {min_loss}")

end_time = time.time()
execution_time = int((end_time - start_time) * 1000)
print(f"The script took {execution_time} ms to run")
