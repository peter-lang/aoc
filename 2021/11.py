import numpy as np

BOARD = np.array(
    [
        list(map(int, line))
        for line in filter(
            None, map(lambda x: x.strip(), open("11.txt", "r").readlines())
        )
    ],
    dtype=np.int8,
)

ones = np.ones_like(BOARD)
zeros = np.zeros_like(BOARD)


def iterate(p_board):
    p_board[1:-1, 1:-1] += ones
    flashed = np.zeros_like(BOARD, dtype=bool)
    while True:
        flashes = (p_board[1:-1, 1:-1] >= 10) & ~flashed
        if not np.any(flashes):
            break

        flashed |= flashes
        # add flashes
        p_board[:-2, :-2] += flashes
        p_board[:-2, 1:-1] += flashes
        p_board[:-2, 2:] += flashes
        p_board[1:-1, :-2] += flashes
        p_board[1:-1, 2:] += flashes
        p_board[2:, :-2] += flashes
        p_board[2:, 1:-1] += flashes
        p_board[2:, 2:] += flashes

    np.putmask(p_board[1:-1, 1:-1], flashed, zeros)
    return np.sum(flashed)


board_size = BOARD.shape[0] * BOARD.shape[1]

# part 1
board = np.pad(np.copy(BOARD), ((1, 1), (1, 1)))
print(sum(iterate(board) for _ in range(100)))

# part 2
board = np.pad(np.copy(BOARD), ((1, 1), (1, 1)))
idx = 1
while iterate(board) < board_size:
    idx += 1

print(idx)
