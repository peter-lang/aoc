import numpy as np
from functools import reduce
import operator

board = np.array(
    [
        list(map(int, line))
        for line in filter(
            None, map(lambda x: x.strip(), open("9.txt", "r").readlines())
        )
    ],
    dtype=np.int8,
)
MAX_ROW = board.shape[0]
MAX_COL = board.shape[1]


pad_board = np.pad(board, [[1, 1], [1, 1]], constant_values=10)
dec_from_north = (pad_board[1:-1, 1:-1] - pad_board[:-2, 1:-1]) < 0
dec_from_south = (pad_board[1:-1, 1:-1] - pad_board[2:, 1:-1]) < 0
dec_from_west = (pad_board[1:-1, 1:-1] - pad_board[1:-1, :-2]) < 0
dec_from_east = (pad_board[1:-1, 1:-1] - pad_board[1:-1, 2:]) < 0
low_points = np.argwhere(
    dec_from_north & dec_from_south & dec_from_west & dec_from_east
)

print(sum(board[tuple(lp)] + 1 for lp in low_points))


def neighbours(n):
    if n[0] > 0:
        yield n[0] - 1, n[1]
    if n[0] < MAX_ROW - 1:
        yield n[0] + 1, n[1]
    if n[1] > 0:
        yield n[0], n[1] - 1
    if n[1] < MAX_COL - 1:
        yield n[0], n[1] + 1


def basin_size(point):
    open_set = {point}
    visited = set()

    while open_set:
        n = open_set.pop()
        n_v = board[n]
        visited.add(n)
        for ch in neighbours(n):
            ch_v = board[ch]
            if ch_v == 9 or ch_v <= n_v:
                continue
            if ch in visited:
                continue
            open_set.add(ch)

    return len(visited)


basin_sizes = sorted([basin_size(tuple(lp)) for lp in low_points])
print(reduce(operator.mul, basin_sizes[-3:]))
