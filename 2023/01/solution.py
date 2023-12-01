number_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def findDigitAtIndex(input_text: str, index: int, useLetters: bool = False) -> int:
    try:
        return int(input_text[index])
    except ValueError:
        if useLetters:
            word = ""
            i = 0
            input_len = len(input_text)
            while True:
                if index + i >= input_len:
                    break
                word += input_text[index + i]
                if len(word) > 2:
                    try:
                        return number_map[word]
                    except KeyError:
                        pass
                if len(word) > 5:
                    break
                i += 1
            raise ValueError("No integer or letters spelling an integer found at this index")
        else:
            raise ValueError("No integer found at this index")


def getCalibrationValue(input_text: str, useLetters: bool = False) -> int:
    first = None
    last = None
    for i in range(len(input_text)):
        if first is None:
            try:
                first = findDigitAtIndex(input_text, i, useLetters)
            except ValueError:
                pass

        if last is None:
            try:
                last = findDigitAtIndex(input_text, -i - 1, useLetters)
            except ValueError:
                pass

        if first is not None and last is not None:
            break

    return int(str(first) + str(last))


def getCalibrationSum(input_text: str, useLetters: bool = False) -> int:
    out = 0
    for line in input_text:
        out += getCalibrationValue(line[:-1], useLetters)
    return out


with open("2023/01/input.txt") as input:
    input_text = input.readlines()

    print("Solution for part 1: {}".format(getCalibrationSum(input_text)))
    print("Solution for part 2: {}".format(getCalibrationSum(input_text, True)))
