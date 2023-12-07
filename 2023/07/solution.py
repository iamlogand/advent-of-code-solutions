from typing import List


class Hand:
    def __init__(self, cards: str, bid: int, joker_rule: bool):
        self.cards = cards
        self.bid = bid
        if joker_rule is False or "J" not in cards:
            self.number = self.get_number(cards)
            self.substituted_cards = None
        else:
            self.number, self.substituted_cards = self.get_highest_number(cards)
        self.rank = None

        # For debugging

    @property
    def winnings(self):
        return self.bid * self.rank

    # Hand number is a representation of the hand as an integer, ranging from 0 (11111) to 61313131313 (AAAAA),
    # where the first digit is the hand type and subsequent pairs of digits represent individual cards.
    # Hand number can be used to sort a list of hands by rank because higher hand number means higher rank.
    def get_number(self, cards: str, cards_with_jack_subs: str | None = None) -> int:
        card_list = list(cards)
        type_digit = self.get_type(cards_with_jack_subs or cards)
        strength_digits = self.get_hand_strength(
            card_list, cards_with_jack_subs is not None
        )
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

    def get_hand_strength(self, card_list: List[str], jack_rule: bool) -> str:
        strength_digits = ""
        for card in card_list:
            strength_digits += self.get_card_strength(card, jack_rule)
        return strength_digits

    def get_card_strength(self, card: str, jack_rule: bool) -> str:
        match card:
            case "A":
                return "13"
            case "K":
                return "12"
            case "Q":
                return "11"
            case "J":
                return "00" if jack_rule else "10"
            case "T":
                return "09"
            case _:
                return "0" + str(int(card) - 1)

    def get_highest_number(self, cards: str) -> int:
        jack_positions = []
        for i in range(len(cards)):
            card = cards[i]
            if card == "J":
                jack_positions.append(i)
        unique_cards = list(set(list(cards)))
        unique_cards.remove("J")
        highest_number = 0
        highest_substituted_cards = None
        if len(jack_positions) == 5:
            return (self.get_number("JJJJJ", "AAAAA"), "AAAAA")
        for sub in unique_cards:
            substituted_cards = cards.replace("J", sub)
            number = self.get_number(cards, substituted_cards)
            if number > highest_number:
                highest_number = number
                highest_substituted_cards = substituted_cards
        return (highest_number, highest_substituted_cards)


def parse_hands(hand_text: str, joker_rule: bool) -> List[Hand]:
    hands = []
    for line in hand_text:
        cards, bid = line.strip().split(" ")
        hands.append(Hand(cards, int(bid), joker_rule))
    return hands


def solve_problem(hand_text: str, joker_rule: bool = False) -> int:
    hands = parse_hands(hand_text, joker_rule)
    hands.sort(key=lambda c: c.number)

    total_winnings = 0
    for i in range(len(hands)):
        hand = hands[i]
        hand.rank = i + 1
        total_winnings += hand.winnings
    return total_winnings


with open("2023/07/input.txt") as input:
    hand_text = input.readlines()
    print("Solution for part 1: {}".format(solve_problem(hand_text)))
    print("Solution for part 2: {}".format(solve_problem(hand_text, True)))
