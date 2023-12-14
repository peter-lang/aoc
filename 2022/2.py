rounds = [
    tuple(line.split())
    for line in filter(None, map(lambda x: x.strip(), open("2.txt", "r").readlines()))
]


def score(move, outcome):
    # outcome: {0: draw, 1: win, 2: loose}
    base = move + 1
    if outcome == 1:
        return base + 6
    if outcome == 0:
        return base + 3
    return base


# part 1
def match_1(a, b):
    move_a = ord(a) - ord("A")
    move_b = ord(b) - ord("X")
    outcome = (move_b - move_a) % 3
    # outcome: {0: draw, 1: win, 2: loose}
    return score(move_b, outcome)


print(sum(match_1(a, b) for a, b in rounds))


# part 2
def match_2(a, b):
    move_a = ord(a) - ord("A")
    outcome = (ord(b) - ord("X") - 1) % 3
    # outcome: {0: draw, 1: win, 2: loose}
    move_b = (outcome + move_a) % 3
    return score(move_b, outcome)


print(sum(match_2(a, b) for a, b in rounds))
