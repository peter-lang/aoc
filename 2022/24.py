import heapdict
import math

lines = list(filter(None, map(lambda x: x.strip(), open("24.txt", "r").readlines())))

MAX_ROW = len(lines) - 2
MAX_COL = len(lines[0]) - 2

PERIOD = MAX_ROW * MAX_COL // math.gcd(MAX_ROW, MAX_COL)
h_tornadoes = [set() for _ in range(MAX_COL)]
v_tornadoes = [set() for _ in range(MAX_ROW)]

for r in range(MAX_ROW):
    for c in range(MAX_COL):
        ch = lines[r + 1][c + 1]
        if ch == ">":
            for i in range(MAX_COL):
                h_tornadoes[i].add((r, (c + i) % MAX_COL))
        elif ch == "<":
            for i in range(MAX_COL):
                h_tornadoes[i].add((r, (c - i) % MAX_COL))
        elif ch == "^":
            for i in range(MAX_ROW):
                v_tornadoes[i].add(((r - i) % MAX_ROW, c))
        elif ch == "v":
            for i in range(MAX_ROW):
                v_tornadoes[i].add(((r + i) % MAX_ROW, c))


def neighbours(n):
    if n == (-1, 0):
        yield 0, 0
        yield n
    elif n == (MAX_ROW, MAX_COL - 1):
        yield MAX_ROW - 1, MAX_COL - 1
        yield n
    else:
        if n == (0, 0):
            yield -1, 0
        if n == (MAX_ROW - 1, MAX_COL - 1):
            yield MAX_ROW, MAX_COL - 1
        if n[0] > 0:
            yield n[0] - 1, n[1]
        if n[0] < MAX_ROW - 1:
            yield n[0] + 1, n[1]
        if n[1] > 0:
            yield n[0], n[1] - 1
        if n[1] < MAX_COL - 1:
            yield n[0], n[1] + 1
        yield n


def heuristic(n, end_node):
    return abs(n[0] - end_node[0]) + abs(n[1] - end_node[1])


def a_star(start, end, t_0=0):
    open_set = heapdict.heapdict()
    open_set[(start, t_0 % PERIOD)] = heuristic(start, end)

    g_score = dict()
    g_score[(start, t_0 % PERIOD)] = 0

    while open_set:
        (current, t), _ = open_set.popitem()
        if current == end:
            return g_score[(current, t)]

        for child in neighbours(current):
            if child in v_tornadoes[t % MAX_ROW] or child in h_tornadoes[t % MAX_COL]:
                continue
            tentative_g_score = g_score[(current, t)] + 1
            key = (child, (t + 1) % PERIOD)
            if tentative_g_score < g_score.get(key, math.inf):
                g_score[key] = tentative_g_score
                open_set[key] = tentative_g_score + heuristic(child, end)
    return None


# part 1
s2e_time = a_star((-1, 0), (MAX_ROW, MAX_COL - 1))
print(s2e_time - 1)

# part 2
e2s_time = a_star((MAX_ROW, MAX_COL - 1), (-1, 0), s2e_time) + s2e_time
s2e_time_2 = a_star((-1, 0), (MAX_ROW, MAX_COL - 1), e2s_time) + e2s_time
print(s2e_time_2 - 1)
