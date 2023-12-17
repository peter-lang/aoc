import heapdict
import math
from typing import Iterator

COORD = tuple[int, int]
COORD_DIR = tuple[int, int, int]

board = [
    [int(ch) for ch in line]
    for line in (map(lambda x: x.strip(), open("17.txt", "r").readlines()))
]

MAX_ROW = len(board)
MAX_COL = len(board[0])

DIRS = {"L": 0, "U": 1, "R": 2, "D": 3}

start_node = (0, 0)
end_node = (MAX_ROW - 1, MAX_COL - 1)


def turn_right(d: int) -> int:
    return (d + 1) % 4


def turn_left(d: int) -> int:
    return (d - 1) % 4


def left_or_right(d: int) -> bool:
    return d % 2 == 0


def next_rc(row: int, col: int, d: int, step: int) -> COORD:
    if left_or_right(d):
        diff = d - 1
        return row, col + diff * step
    else:
        diff = d - 2
        return row + diff * step, col


def is_valid(row: int, col: int) -> bool:
    return 0 <= row < MAX_ROW and 0 <= col < MAX_COL


def neighbours(n: COORD_DIR, steps_min: int, steps_max: int) -> Iterator[COORD_DIR]:
    for d in (turn_left(n[2]), turn_right(n[2])):
        for s in range(steps_min, steps_max + 1):
            r, c = next_rc(n[0], n[1], d, s)
            if is_valid(r, c):
                yield r, c, d


def points_to(a: int, b: int) -> range:
    if a < b:
        return range(a + 1, b + 1)
    else:
        return range(a - 1, b - 1, -1)


def dist(a: COORD_DIR, b: COORD_DIR) -> int:
    total = 0
    if a[0] == b[0]:
        for i in points_to(a[1], b[1]):
            total += board[a[0]][i]
    else:
        for i in points_to(a[0], b[0]):
            total += board[i][a[1]]
    return total


def heuristic(n: COORD_DIR) -> int:
    return abs(n[0] - end_node[0]) + abs(n[1] - end_node[1])


def a_star(starts, ends, min_step, max_step):
    open_set = heapdict.heapdict()
    g_score = dict()
    for start in starts:
        open_set[start] = heuristic(start)
        g_score[start] = 0

    while open_set:
        current, _ = open_set.popitem()
        if current in ends:
            return g_score[current]

        for child in neighbours(current, min_step, max_step):
            tentative_g_score = g_score[current] + dist(current, child)
            if tentative_g_score < g_score.get(child, math.inf):
                g_score[child] = tentative_g_score
                open_set[child] = tentative_g_score + heuristic(child)
    return None


# part 1
print(
    a_star(
        set([start_node + (DIRS[_d],) for _d in ["R", "D"]]),
        set([end_node + (DIRS[_d],) for _d in DIRS]),
        1,
        3,
    )
)

# part 2
print(
    a_star(
        set([start_node + (DIRS[_d],) for _d in ["R", "D"]]),
        set([end_node + (DIRS[_d],) for _d in DIRS]),
        4,
        10,
    )
)
