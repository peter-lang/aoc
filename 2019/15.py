from collections import deque
import math
import heapdict
import intcode

CODE = list(map(int, open("15.txt", "r").read().strip().split(",")))
COMP = intcode.Computer(CODE).reset()


def neighbour(pt):
    yield pt[0] - 1, pt[1]
    yield pt[0] + 1, pt[1]
    yield pt[0], pt[1] - 1
    yield pt[0], pt[1] + 1


BOARD = {(0, 0): 1}
UNKNOWN = {p for p in neighbour((0, 0))}


def bfs(src, targets, board):
    visited = set()
    nodes = deque([(src, [src])])
    while nodes:
        node, path_to = nodes.popleft()

        visited.add(node)
        for child in neighbour(node):
            if child in targets:
                return path_to + [child]
            if child in visited or board.get(child, 0) == 0:
                continue
            nodes.append((child, path_to + [child]))
    return None


def bfs_fill(src, board):
    visited = set()
    nodes = deque([(src, 0)])
    dist = math.inf
    while nodes:
        node, dist = nodes.popleft()
        visited.add(node)
        for child in neighbour(node):
            if child in visited or board[child] == 0:
                continue
            nodes.append((child, dist + 1))
    return dist


def a_star(start, end, board):
    def heuristic(n):
        return abs(n[0] - end[0]) + abs(n[1] - end[1])

    open_set = heapdict.heapdict()
    open_set[start] = heuristic(start)

    g_score = dict()
    g_score[start] = 0

    while open_set:
        node, dist = open_set.popitem()
        if node == end:
            return dist

        for child in neighbour(node):
            if board[child] == 0:
                continue
            tentative_g_score = g_score[node] + 1
            if tentative_g_score < g_score.get(child, math.inf):
                g_score[child] = tentative_g_score
                open_set[child] = tentative_g_score + heuristic(child)
    return None


def try_move_path(path):
    out = None
    for a, b in zip(path[:-1], path[1:]):
        if b[0] == a[0]:
            if b[1] > a[1]:
                d = 3  # west
            else:
                d = 4  # east
        elif b[0] > a[0]:
            d = 2  # south
        else:
            d = 1  # north

        out = COMP.run_to_output(d)
        if out == 0:
            return a, b, out
    return path[-1], path[-1], out


current = (0, 0)
target = None

while UNKNOWN:
    exploration_path = bfs(current, UNKNOWN, BOARD)
    current, loc, res = try_move_path(exploration_path)

    BOARD[loc] = res
    UNKNOWN.remove(loc)
    if res != 0:
        for loc_n in neighbour(loc):
            if loc_n not in BOARD:
                UNKNOWN.add(loc_n)

    if BOARD[current] == 2:
        target = current


# part 1
print(a_star((0, 0), target, BOARD))

# part 2
print(bfs_fill(target, BOARD))
