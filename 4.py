lines: list[str] = list(
    filter(None, map(lambda x: x.strip(), open("4.txt", "r").readlines()))
)

cards = [
    (list(map(lambda x: int(x), lhs.split())), list(map(lambda x: int(x), rhs.split())))
    for lhs, rhs in (
        map(lambda x: x.strip(), l.split(":")[1].strip().split("|")) for l in lines
    )
]


def match_count(card: tuple[list[int], list[int]]) -> int:
    winning_numbers = set(card[0])
    return sum(n in winning_numbers for n in card[1])


# part 1
def score(card: tuple[list[int], list[int]]) -> int:
    match_cnt = match_count(card)
    if match_cnt == 0:
        return 0
    else:
        return 1 << (match_cnt - 1)


print(sum(score(card) for card in cards))


# part 2
def won_cards(pile: list[tuple[list[int], list[int]]]) -> int:
    copies = [0] * len(pile)
    for i in range(len(pile)):
        cnt = match_count(pile[i])
        for j in range(cnt):
            copies[i + j + 1] += 1 + copies[i]
    return len(pile) + sum(copies)


print(won_cards(cards))
