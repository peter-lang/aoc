import numpy as np

decode = {"#": 1, ".": 0}

BOARD = np.array(
    [
        [decode[ch] for ch in line]
        for line in filter(
            None, map(lambda x: x.strip(), open("23.txt", "r").readlines())
        )
    ],
    dtype=bool,
)


def execute_round(board: np.array, offset: int):
    padding = (
        (1 if np.any(board[0, :] == 1) else 0, 1 if np.any(board[-1, :] == 1) else 0),
        (1 if np.any(board[:, 0] == 1) else 0, 1 if np.any(board[:, -1] == 1) else 0),
    )
    if padding != ((0, 0), (0, 0)):
        board = np.pad(board, padding)

    r_max = board.shape[0]
    c_max = board.shape[1]

    no_east = np.zeros_like(board)
    no_east[1:-1, 1:-1] = ~(board[:-2, 2:] | board[1:-1, 2:] | board[2:, 2:])
    no_west = np.zeros_like(board)
    no_west[1:-1, 1:-1] = ~(board[:-2, :-2] | board[1:-1, :-2] | board[2:, :-2])
    no_north = np.zeros_like(board)
    no_north[1:-1, 1:-1] = ~(board[:-2, :-2] | board[:-2, 1:-1] | board[:-2, 2:])
    no_south = np.zeros_like(board)
    no_south[1:-1, 1:-1] = ~(board[2:, :-2] | board[2:, 1:-1] | board[2:, 2:])

    no_move = board & no_south & no_west & no_east & no_north
    rest = board & ~no_move
    move_checks = [
        (no_north, (-1, 0)),
        (no_south, (1, 0)),
        (no_west, (0, -1)),
        (no_east, (0, 1)),
    ]

    might_move = []
    for idx in range(4):
        no_neighbour, (r_d, c_d) = move_checks[(idx + offset) % 4]
        move = np.zeros_like(board)
        movable = rest & no_neighbour

        # move forward
        r_start = 1 + r_d
        r_end = r_max - 1 + r_d
        c_start = 1 + c_d
        c_end = c_max - 1 + c_d
        move[r_start:r_end, c_start:c_end] = movable[1:-1, 1:-1]

        might_move.append((move, (r_d, c_d)))
        rest &= ~no_neighbour

    result = no_move | rest

    any_move = False

    for idx in range(4):
        move, (r_d, c_d) = might_move[idx]
        others = np.any(
            [o for o_idx, (o, _) in enumerate(might_move) if o_idx != idx], axis=0
        )
        move_no_collision = move & ~others
        any_move |= np.any(move_no_collision)
        result |= move_no_collision

        collision = move & others

        # move backward
        r_start = 1 - r_d
        r_end = r_max - 1 - r_d
        c_start = 1 - c_d
        c_end = c_max - 1 - c_d
        result[1:-1, 1:-1] |= collision[r_start:r_end, c_start:c_end]

    return result, any_move


# part 1
b = np.copy(BOARD)
for i in range(10):
    b, _ = execute_round(b, i)
edges = np.where(b)
min_rect = (edges[0].max() - edges[0].min() + 1) * (edges[1].max() - edges[1].min() + 1)
print(min_rect - np.sum(BOARD))

# part 2
i = 0
b_prev = np.copy(BOARD)
while True:
    b, moved = execute_round(b_prev, i)
    if not moved:
        break
    i += 1
    b_prev = b
print(i + 1)
