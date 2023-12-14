from collections import Counter


lines = list(filter(None, map(lambda x: x.strip(), open("7.txt", "r").readlines())))


def hand_type(counts):
    if counts[0] == 1:  # high card
        return 0
    elif counts[0] == 2 and counts[1] == 1:  # 1-pair
        return 1
    elif counts[0] == 2 and counts[1] == 2:  # 2-pair
        return 2
    elif counts[0] == 3 and counts[1] == 1:  # 3 of a kind
        return 3
    elif counts[0] == 3 and counts[1] == 2:  # full house
        return 4
    elif counts[0] == 4:  # 4 of a kind
        return 5
    elif counts[0] == 5:  # 5 of a kind
        return 6
    else:
        assert False


# part 1
value_to_card_1 = list(map(lambda x: str(x), range(2, 10))) + ["T", "J", "Q", "K", "A"]
card_to_value_1 = {c: v for v, c in enumerate(value_to_card_1)}


def parse_hand_1(hand):
    cards = tuple(card_to_value_1[c] for c in hand)
    counter = Counter(cards)
    counts = sorted(counter.values(), reverse=True)
    return hand_type(counts), cards


hands_1 = list(
    (parse_hand_1(hand), int(bid)) for hand, bid in map(lambda x: x.split(), lines)
)

print(sum((r + 1) * bid for r, (hand, bid) in enumerate(sorted(hands_1))))

# part 2
value_to_card_2 = (
    ["J"] + list(map(lambda x: str(x), range(2, 10))) + ["T", "Q", "K", "A"]
)
card_to_value_2 = {c: v for v, c in enumerate(value_to_card_2)}


def parse_hand_2(hand):
    cards = tuple(card_to_value_2[c] for c in hand)
    counter = Counter(cards)
    jokers = counter[0]
    counts = sorted([cnt for c, cnt in counter.items() if c != 0], reverse=True)
    if jokers == 5:
        counts = [5]
    else:
        counts[0] += jokers
    return hand_type(counts), cards


hands_2 = list(
    (parse_hand_2(hand), int(bid)) for hand, bid in map(lambda x: x.split(), lines)
)

print(sum((r + 1) * bid for r, (hand, bid) in enumerate(sorted(hands_2))))
