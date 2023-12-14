import numpy as np

COORD = tuple[int, ...]
LINE = tuple[COORD, ...]

lines: list[LINE] = [
    tuple(
        map(
            lambda x: tuple(reversed(tuple(map(int, x.split(","))))), line.split(" -> ")
        )
    )
    for line in filter(None, map(lambda x: x.strip(), open("14.txt", "r").readlines()))
]


def create_board(lines, with_floor):
    row_vals = [coord[0] for line in lines for coord in line] + [0]
    col_vals = [coord[1] for line in lines for coord in line] + [500]

    min_row = min(row_vals)
    max_row = max(row_vals)
    min_col = min(col_vals)
    max_col = max(col_vals)

    if with_floor:
        floor_row = max_row + 2
        floor_min_col = 500 - floor_row
        floor_max_col = 500 + floor_row
        lines.append(((floor_row, floor_min_col), (floor_row, floor_max_col)))
        max_row = max(max_row, floor_row)
        min_col = min(min_col, floor_min_col)
        max_col = max(max_col, floor_max_col)

    res = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)
    for line in lines:
        for a, b in zip(line[:-1], line[1:]):
            if a[0] == b[0]:
                for c in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                    res[a[0] - min_row, c - min_col] = -1
            else:
                for r in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                    res[r - min_row, a[1] - min_col] = -1
    return res, (min_row, min_col)


def drop_sand(board, offset):
    sand = (0 - offset[0], 500 - offset[1])
    if board[sand] == 1:
        return False
    # down
    while True:
        tmp = (sand[0] + 1, sand[1])
        if tmp[0] == board.shape[0]:
            return False
        if board[tmp] == 0:
            sand = tmp
            continue
        tmp = (sand[0] + 1, sand[1] - 1)
        if tmp[1] == -1:
            return False
        if board[tmp] == 0:
            sand = tmp
            continue
        tmp = (sand[0] + 1, sand[1] + 1)
        if tmp[1] == board.shape[1]:
            return False
        if board[tmp] == 0:
            sand = tmp
            continue
        break
    board[sand] = 1
    return True


# part 1
b, o = create_board(list(lines), False)
total = 0
while drop_sand(b, o):
    total += 1
print(total)

# part 2
b, o = create_board(list(lines), True)
total = 0
while drop_sand(b, o):
    total += 1
print(total)
