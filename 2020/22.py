from collections import deque
from functools import cache

p1_cards, p2_cards = [], []
current = p1_cards
for line in filter(None, map(lambda x: x.strip(), open("22.txt", "r").readlines())):
    if line == "Player 1:":
        current = p1_cards
        continue
    if line == "Player 2:":
        current = p2_cards
        continue
    current.append(int(line))
p1_cards, p2_cards = tuple(p1_cards), tuple(p2_cards)


def crab_combat(p1, p2):
    p1, p2 = deque(p1), deque(p2)
    while p1 and p2:
        p1_c, p2_c = p1.popleft(), p2.popleft()
        if p1_c > p2_c:
            p1.append(p1_c)
            p1.append(p2_c)
        else:
            p2.append(p2_c)
            p2.append(p1_c)
    return bool(p1), p1, p2


# part 1
_, p1_res, p2_res = crab_combat(p1_cards, p2_cards)
print(sum((idx + 1) * val for idx, val in enumerate(reversed(p1_res or p2_res))))


@cache
def recursive_combat(p1, p2):
    visited = set()
    p1, p2 = deque(p1), deque(p2)
    while p1 and p2:
        state = (tuple(p1), tuple(p2))
        if state in visited:
            return True, p1, p2
        else:
            visited.add(state)
        p1_c, p2_c = p1.popleft(), p2.popleft()
        if p1_c <= len(p1) and p2_c <= len(p2):
            sub_res, sub_p1, sub_p2 = recursive_combat(
                tuple(p1)[:p1_c], tuple(p2)[:p2_c]
            )
            if sub_res:
                p1.append(p1_c)
                p1.append(p2_c)
            else:
                p2.append(p2_c)
                p2.append(p1_c)
        else:
            if p1_c > p2_c:
                p1.append(p1_c)
                p1.append(p2_c)
            else:
                p2.append(p2_c)
                p2.append(p1_c)

    return bool(p1), p1, p2


# part 2
_, p1_res, p2_res = recursive_combat(p1_cards, p2_cards)
print(sum((idx + 1) * val for idx, val in enumerate(reversed(p1_res or p2_res))))
