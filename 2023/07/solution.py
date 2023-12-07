from typing import List


class Hand:
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.number = self.get_number(cards)
        self.rank = None

    @property
    def winnings(self):
        return self.bid * self.rank

    # Hand number is a representation of the hand as an integer, ranging from 0 (11111) to 61313131313 (AAAAA),
    # where the first digit is the hand type and subsequent pairs of digits represent individual cards.
    # Hand number can be used to sort a list of hands by rank because higher hand number means higher rank.
    def get_number(self, cards: str) -> int:
        card_list = list(cards)
        type_digit = self.get_type(card_list)
        strength_digits = self.get_hand_strength(card_list)
        return int(str(type_digit) + strength_digits)

    def get_type(self, card_list: List[str]) -> int:
        unique_cards = list(set(card_list))
        if len(unique_cards) == 1:
            return 6  # Five of a kind
        if len(unique_cards) == 2:
            first_card_count = card_list.count(unique_cards[0])
            if first_card_count == 4 or first_card_count == 1:
                return 5  # Four of a kind
            else:
                return 4  # Full house
        if len(unique_cards) == 3:
            for card in unique_cards:
                if card_list.count(card) == 3:
                    return 3  # Three of a kind
            return 2  # Two pair
        if len(unique_cards) == 4:
            return 1  # One pair
        return 0  # High card
    
    def get_hand_strength(self, card_list: List[str]) -> str:
        strength_digits = ""
        for card in card_list:
            strength_digits += self.get_card_strength(card)
        return strength_digits
            
    def get_card_strength(self, card: str) -> str:
        match card:
            case "A":
                return "12"
            case "K":
                return "11"
            case "Q":
                return "10"
            case "J":
                return "09"
            case "T":
                return "08"
            case _:
                return "0" + str(int(card) - 2)


def parse_hands(hand_text: str) -> List[Hand]:
    hands = []
    for line in hand_text:
        cards, bid = line.strip().split(" ")
        hands.append(Hand(cards, int(bid)))
    return hands


def solve_problem(hand_text: str) -> int:
    hands = parse_hands(hand_text)
    hands.sort(key = lambda c: c.number)

    total_winnings = 0
    for i in range(len(hands)):
        hand = hands[i]
        hand.rank = i + 1
        total_winnings += hand.winnings
    return total_winnings

with open("2023/07/input.txt") as input:
    race_stats = input.readlines()
    print("Solution for part 1: {}".format(solve_problem(race_stats)))
