import copy
import time
from typing import List


class Card:
    def __init__(self, id: int, winning_nums: List[int], our_nums: List[int]):
        self.id = id
        self.winning_nums = winning_nums
        self.our_nums = our_nums
        
        
def get_card_copy(target_id: int, cards: List[Card]) -> Card:
    for other_card in cards:
        if other_card.id == target_id:
            return copy.copy(other_card)
    return None


def count_points(card: Card, use_instructions: bool, all_cards: List[Card]) -> (int, List[Card]):
    if use_instructions:
        match_count = 0
        if card is None or card.our_nums is None:
            return (0, [])
        for num in card.our_nums:
            if num in card.winning_nums:
                match_count += 1
        new_cards = []
        for i in range(1, match_count + 1):
            new_card = get_card_copy(card.id + i, all_cards)
            if new_card is not None:
                new_cards.append(new_card)
        return (0, new_cards)
    else:
        points = 0
        for num in card.our_nums:
            if num in card.winning_nums:
                points = points * 2 if points > 0 else 1
        return (points, [])


def count_total_points(cards: List[Card], use_instructions: bool) -> int:
    total_points = 0
    i = 0
    while True:
        if i >= len(cards):
            break
        card = cards[i]
        new_points, new_cards = count_points(card, use_instructions, cards)
        total_points += new_points
        cards += new_cards
        i += 1
    return len(cards) if use_instructions else total_points


def create_card_objects(scratchcards: str) -> List[Card]:
    cards = []
    for card in scratchcards:
        text = card.strip()
        title, nums = text.split(": ")
        id = int([elem for elem in title.split(" ") if len(elem) > 0][1])
        winning_nums_text, our_nums_text = nums.split(" | ")
        winning_nums = [
            int(num) for num in winning_nums_text.split(" ") if len(num) > 0
        ]
        our_nums = [int(num) for num in our_nums_text.split(" ") if len(num) > 0]
        card = Card(id, winning_nums, our_nums)
        cards.append(card)
    return cards


def solve_problem(scratchcards: str, use_instructions: bool = False) -> int:
    start_time = time.time()
    print("Parsing cards...")
    cards = create_card_objects(scratchcards)
    print("Parsed the cards in {:.4f} seconds".format(time.time() - start_time))
    print("Solving the problem...")
    total_points = count_total_points(cards, use_instructions)
    print("Solved the problem in {:.4f} seconds".format(time.time() - start_time))
    return total_points


with open("2023/04/input.txt") as input:
    scratchcards = input.readlines()

    print("PART 1")
    print("Solution for part 1: {}\n".format(solve_problem(scratchcards)))
    print("PART 2")
    print("Solution for part 2: {}".format(solve_problem(scratchcards, True)))
