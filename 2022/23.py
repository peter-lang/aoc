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


def round(b: np.array, offset: int):
    padding = (
        (1 if np.any(b[0, :] == 1) else 0, 1 if np.any(b[-1, :] == 1) else 0),
        (1 if np.any(b[:, 0] == 1) else 0, 1 if np.any(b[:, -1] == 1) else 0),
    )
    if padding != ((0, 0), (0, 0)):
        b = np.pad(b, padding)
    no_east = np.zeros_like(b)
    no_east[1:-1, 1:-1] = ~(b[:-2, 2:] | b[1:-1, 2:] | b[2:, 2:])
    no_west = np.zeros_like(b)
    no_west[1:-1, 1:-1] = ~(b[:-2, :-2] | b[1:-1, :-2] | b[2:, :-2])
    no_north = np.zeros_like(b)
    no_north[1:-1, 1:-1] = ~(b[:-2, :-2] | b[:-2, 1:-1] | b[:-2, 2:])
    no_south = np.zeros_like(b)
    no_south[1:-1, 1:-1] = ~(b[2:, :-2] | b[2:, 1:-1] | b[2:, 2:])

    no_move = b & no_south & no_west & no_east & no_north
    rest = b & ~no_move
    move_checks = [
        (no_north, (-1, 0)),
        (no_south, (1, 0)),
        (no_west, (0, -1)),
        (no_east, (0, 1)),
    ]

    move = []
    for idx in range(4):
        no_neighbour, (r_d, c_d) = move_checks[(idx + offset) % 4]
        m = np.zeros_like(b)
        can_move = rest & no_neighbour
        m[
            (1 + r_d) : (m.shape[0] - 1 + r_d), (1 + c_d) : (m.shape[1] - 1 + c_d)
        ] = can_move[1:-1, 1:-1]
        move.append((m, (-r_d, -c_d)))
        rest &= ~no_neighbour

    result = no_move | rest

    any_move = False

    for idx in range(4):
        m, (r_d, c_d) = move[idx]
        others = np.any(
            [o for o_idx, (o, _) in enumerate(move) if o_idx != idx], axis=0
        )
        move_without_collision = m & ~others
        if np.any(move_without_collision):
            any_move = True
        result |= move_without_collision
        collision = m & others
        rollback = collision[
            (1 + r_d) : (collision.shape[0] - 1 + r_d),
            (1 + c_d) : (collision.shape[1] - 1 + c_d),
        ]
        result[1:-1, 1:-1] |= rollback

    return result, any_move


# part 1
b = np.copy(BOARD)
for i in range(10):
    b, _ = round(b, i)
edges = np.where(b)
min_rect = (edges[0].max() - edges[0].min() + 1) * (edges[1].max() - edges[1].min() + 1)
print(min_rect - np.sum(BOARD))


# part 2
i = 0
b_prev = np.copy(BOARD)
while True:
    b, moved = round(b_prev, i)
    if not moved:
        break
    i += 1
    b_prev = b
print(i + 1)
