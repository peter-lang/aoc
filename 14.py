from typing import Iterator

ROW = tuple[int, ...]
BOARD = tuple[ROW, ...]

lines: Iterator[str] = filter(
    None, map(lambda x: x.strip(), open("14.txt", "r").readlines())
)


def rotate_left(b: BOARD) -> BOARD:
    rows = len(b)
    cols = len(b[0])
    return tuple(tuple(b[r][c] for r in range(rows)) for c in range(cols - 1, -1, -1))


def rotate_right(b: BOARD) -> BOARD:
    rows = len(b)
    cols = len(b[0])
    return tuple(tuple(b[r][c] for r in range(rows - 1, -1, -1)) for c in range(cols))


board: BOARD = tuple(
    tuple(1 if ch == "O" else -1 if ch == "#" else 0 for ch in line) for line in lines
)
# rotate left: top->down, left->right processing is easier
board = rotate_left(board)


def left_tilt_row(row: ROW) -> ROW:
    res = [0] * len(row)
    tar = 0
    for i, v in enumerate(row):
        if v == 1:
            res[tar] = 1
            tar += 1
        elif v == -1:
            res[i] = -1
            tar = i + 1
    return tuple(res)


def left_tilt(b: BOARD) -> BOARD:
    return tuple(map(left_tilt_row, b))


def left_weight(b: BOARD) -> int:
    cols = len(b[0])
    return sum(sum(cols - col for col, i in enumerate(row) if i == 1) for row in b)


def cycle(b: BOARD) -> BOARD:
    for _ in range(4):
        b = left_tilt(b)
        b = rotate_right(b)

    return b


def cycles(b: BOARD, times: int) -> BOARD:
    state2idx = dict()
    idx2state = list()
    cycle_start = -1
    for i in range(times):
        if (idx := state2idx.get(b, None)) is not None:
            cycle_start = idx
            break
        else:
            state2idx[b] = i
            idx2state.append(b)
            b = cycle(b)
    cycle_len = len(idx2state) - cycle_start
    cycle_offset = (times - cycle_start) % cycle_len
    return idx2state[cycle_start + cycle_offset]


# part 1
print(left_weight(left_tilt(board)))

# part 2
print(left_weight(cycles(board, 1000000000)))
