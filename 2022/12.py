import heapdict
import math

lines = list(map(lambda x: x.strip(), open("12.txt", "r").readlines()))

MAX_ROW = len(lines)
MAX_COL = len(lines[0])

start_node = next(
    (r, c) for r, line in enumerate(lines) for c, ch in enumerate(line) if ch == "S"
)
end_node = next(
    (r, c) for r, line in enumerate(lines) for c, ch in enumerate(line) if ch == "E"
)

board = [
    [ord(ch) - ord("a") for ch in line.replace("S", "a").replace("E", "z")]
    for line in lines
]


def neighbours(n):
    if n[0] > 0:
        yield n[0] - 1, n[1]
    if n[0] < MAX_ROW - 1:
        yield n[0] + 1, n[1]
    if n[1] > 0:
        yield n[0], n[1] - 1
    if n[1] < MAX_COL - 1:
        yield n[0], n[1] + 1


def valid(a, b):
    # b <= a+1
    return board[b[0]][b[1]] <= board[a[0]][a[1]] + 1


def heuristic(n):
    return board[n[0]][n[1]]


def a_star(start, ends):
    open_set = heapdict.heapdict()
    open_set[start] = heuristic(start)

    g_score = dict()
    g_score[start] = 0

    come_from = dict()

    def path(n):
        res = [n]
        while n in come_from:
            n = come_from[n]
            res.append(n)
        return res

    while open_set:
        current, _ = open_set.popitem()
        if current in ends:
            return path(current)

        for child in filter(lambda x: valid(x, current), neighbours(current)):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(child, math.inf):
                come_from[child] = current
                g_score[child] = tentative_g_score
                open_set[child] = tentative_g_score + heuristic(child)
    return None


# part 1
print(len(a_star(end_node, {start_node})) - 1)

# part 2
low_nodes = {
    (r, c) for r, line in enumerate(lines) for c, ch in enumerate(line) if ch == "a"
}
print(len(a_star(end_node, {start_node} | low_nodes)) - 1)
