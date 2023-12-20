import heapdict
import math
import numpy as np

risks = np.array(
    list(
        list(map(int, line))
        for line in filter(
            None, map(lambda x: x.strip(), open("15.txt", "r").readlines())
        )
    )
)


def neighbours(n, risk_map):
    if n[0] > 0:
        yield n[0] - 1, n[1]
    if n[0] < risk_map.shape[0] - 1:
        yield n[0] + 1, n[1]
    if n[1] > 0:
        yield n[0], n[1] - 1
    if n[1] < risk_map.shape[1] - 1:
        yield n[0], n[1] + 1


def heuristic(n, end_node):
    return abs(n[0] - end_node[0]) + abs(n[1] - end_node[1])


def a_star(risk_map):
    start = (0, 0)
    end = (risk_map.shape[0] - 1, risk_map.shape[1] - 1)

    open_set = heapdict.heapdict()
    open_set[start] = heuristic(start, end)

    g_score = dict()
    g_score[start] = 0

    while open_set:
        current, _ = open_set.popitem()
        if current == end:
            return g_score[current]

        for child in neighbours(current, risk_map):
            tentative_g_score = g_score[current] + risk_map[child]
            if tentative_g_score < g_score.get(child, math.inf):
                g_score[child] = tentative_g_score
                open_set[child] = tentative_g_score + heuristic(child, end)
    return None


# part 1
print(a_star(risks))

# part 2
extended = np.tile(risks, (5, 5))
ones = np.ones_like(risks)
rows = risks.shape[0]
cols = risks.shape[1]
for r in range(5):
    for c in range(5):
        extended[r * rows : (r + 1) * rows, c * cols : (c + 1) * cols] += (r + c) * ones
extended = (extended - 1) % 9 + 1

print(a_star(extended))
