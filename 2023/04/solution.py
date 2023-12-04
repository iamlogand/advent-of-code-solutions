from typing import List


class Card:
    def __init__(self, id: int, winning_nums: List[int], our_nums: List[int]):
        self.id = id
        self.winning_nums = winning_nums
        self.our_nums = our_nums


def count_points(card: Card) -> int:
    points = 0
    for num in card.our_nums:
        if num in card.winning_nums:
            points = points * 2 if points > 0 else 1
    return points


def count_total_points(cards: List[Card]) -> int:
    total_points = 0
    for card in cards:
        total_points += count_points(card)
    return total_points


def create_card_objects(scratchcards: str) -> List[Card]:
    cards = []
    for card in scratchcards:
        text = card.strip()
        title, nums = text.split(": ")
        id = [elem for elem in title.split(" ") if len(elem) > 0][1]
        winning_nums_text, our_nums_text = nums.split(" | ")
        winning_nums = [
            int(num) for num in winning_nums_text.split(" ") if len(num) > 0
        ]
        our_nums = [int(num) for num in our_nums_text.split(" ") if len(num) > 0]
        card = Card(id, winning_nums, our_nums)
        cards.append(card)
    return cards


def solve_problem(scratchcards: str) -> int:
    cards = create_card_objects(scratchcards)
    total_points = count_total_points(cards)
    return total_points


with open("2023/04/input.txt") as input:
    scratchcards = input.readlines()

    print("Solution for part 1: {}".format(solve_problem(scratchcards)))
