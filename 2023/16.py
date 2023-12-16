import numpy as np
from collections import deque

mirrors = list(filter(None, map(lambda x: x.strip(), open("16.txt", "r").readlines())))

MAX_ROW = len(mirrors)
MAX_COL = len(mirrors[0])


DIRS = {"L": 0, "U": 1, "R": 2, "D": 3}


def turn_right(d):
    return (d + 1) % 4


def turn_left(d):
    return (d - 1) % 4


def left_or_right(d):
    return d % 2 == 0


def up_or_down(d):
    return d % 2 == 1


def next_rc(row: int, col: int, d: int) -> tuple[int, int]:
    if left_or_right(d):
        diff = d - 1
        return row, col + diff
    else:
        diff = d - 2
        return row + diff, col


def follow_beam(coord: tuple[int, int], d_str: str):
    beam = np.zeros((4, MAX_ROW, MAX_COL), dtype=bool)
    beams_to_follow = deque([(coord[0], coord[1], DIRS[d_str])])
    while beams_to_follow:
        row, col, d = beams_to_follow.popleft()
        while 0 <= row < MAX_ROW and 0 <= col < MAX_COL and not beam[d, row, col]:
            beam[d, row, col] = True

            m = mirrors[row][col]
            if m == "/":
                if left_or_right(d):
                    d = turn_left(d)
                else:
                    d = turn_right(d)
            elif m == "\\":
                if left_or_right(d):
                    d = turn_right(d)
                else:
                    d = turn_left(d)
            elif (m == "|" and left_or_right(d)) or (m == "-" and up_or_down(d)):
                d_alt = turn_right(d)
                beams_to_follow.append(next_rc(row, col, d_alt) + (d_alt,))
                d = turn_left(d)

            row, col = next_rc(row, col, d)
    return beam


def heat(coord: tuple[int, int], d_str: str) -> int:
    beam = follow_beam(coord, d_str)
    return np.sum(np.any(beam, axis=0))


# part 1
print(heat((0, 0), "R"))


# part 2
def all_starts():
    for i in range(MAX_ROW):
        yield (i, 0), "R"
    for i in range(MAX_ROW):
        yield (i, MAX_COL - 1), "L"
    for i in range(MAX_COL):
        yield (0, i), "D"
    for i in range(MAX_COL):
        yield (MAX_ROW - 1, i), "U"


print(max(heat(c, d) for c, d in all_starts()))
