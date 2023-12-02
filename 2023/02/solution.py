limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def getHandfuls(game_result: str) -> int:
    id_end_position = game_result.find(":")
    game_results = game_result[id_end_position + 2 :]
    return game_results.split("; ")


def getCubeCounts(handful: str) -> (int, int, int):
    red_count = green_count = blue_count = 0
    for color in handful.split(", "):
        count, name = color.split(" ")
        match name:
            case "red":
                red_count = int(count)
            case "green":
                green_count = int(count)
            case "blue":
                blue_count = int(count)
    return red_count, green_count, blue_count


def getMinGamePower(game_result: str) -> int:
    """
    Returns the power of the minimum number of cubes of each color required
    for the handfuls in the game to be possible,
    with the 'power' being the count for each color multiplied together.
    """

    min_red = min_green = min_blue = 0
    handfuls = getHandfuls(game_result)
    for handful in handfuls:
        candidate_min_red, candidate_min_green, candidate_min_blue = getCubeCounts(
            handful
        )
        min_red = max(min_red, candidate_min_red)
        min_green = max(min_green, candidate_min_green)
        min_blue = max(min_blue, candidate_min_blue)
    return min_red * min_green * min_blue


def sumMinGamePowers(input_text: str) -> int:
    out = 0
    for line in input_text:
        out += getMinGamePower(line.strip())
    return out


def validateHandful(handful: str) -> bool:
    for color in handful.split(", "):
        count, name = color.split(" ")
        if int(count) > limits[name]:
            return False
    return True


def getGameId(game_result: str) -> int:
    id_end_position = game_result.find(":")
    return int(game_result[5:id_end_position])


def validateGameResult(game_result: str) -> int:
    """
    Returns game ID number if the game was possible otherwise returns 0.
    """

    handfuls = getHandfuls(game_result)

    handful_is_valid = True
    for handful in handfuls:
        if not validateHandful(handful):
            handful_is_valid = False
    return getGameId(game_result) if handful_is_valid else 0


def sumPossibleGameIds(input_text: str) -> int:
    out = 0
    for line in input_text:
        out += validateGameResult(line.strip())
    return out


with open("2023/02/input.txt") as input:
    input_text = input.readlines()

    print("Solution for part 1: {}".format(sumPossibleGameIds(input_text)))
    print("Solution for part 2: {}".format(sumMinGamePowers(input_text)))
