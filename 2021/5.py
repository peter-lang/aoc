import numpy as np

pairs = [
    (tuple(map(int, a.split(","))), tuple(map(int, b.split(","))))
    for a, b in (
        line.split(" -> ")
        for line in filter(
            None, map(lambda x: x.strip(), open("5.txt", "r").readlines())
        )
    )
]

MIN = tuple(min(p[e][i] for e in range(2) for p in pairs) for i in range(2))
MAX = tuple(max(p[e][i] for e in range(2) for p in pairs) for i in range(2))


horizontal = list(filter(lambda p: p[0][0] == p[1][0], pairs))
vertical = list(filter(lambda p: p[0][1] == p[1][1], pairs))
diagonal = list(
    filter(lambda p: abs(p[0][0] - p[1][0]) == abs(p[0][1] - p[1][1]), pairs)
)


def overlaps(lines):
    board = np.zeros(tuple(MAX[i] - MIN[i] + 1 for i in range(2)), dtype=np.uint8)
    for (ar, ac), (br, bc) in lines:
        rdiff = ar - br
        cdiff = ac - bc
        if rdiff == 0:
            for c in range(min(ac, bc), max(ac, bc) + 1):
                board[ar - MIN[0], c - MIN[1]] += 1
        elif cdiff == 0:
            for r in range(min(ar, br), max(ar, br) + 1):
                board[r - MIN[0], ac - MIN[1]] += 1
        elif rdiff == cdiff:
            r = min(ar, br)
            c = min(ac, bc)
            for d in range(abs(rdiff) + 1):
                board[r + d - MIN[0], c + d - MIN[1]] += 1
        elif rdiff == -cdiff:
            r = min(ar, br)
            c = max(ac, bc)
            for d in range(abs(rdiff) + 1):
                board[r + d - MIN[0], c - d - MIN[1]] += 1
    return np.sum(board >= 2)


# part 1
print(overlaps(horizontal + vertical))

# part 2
print(overlaps(horizontal + vertical + diagonal))
