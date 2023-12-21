import numpy as np

lines = list(filter(None, map(lambda x: x.strip(), open("21.txt", "r").readlines())))
BOARD = np.array(
    list(list(False if ch == "#" else True for ch in line) for line in lines)
)

assert BOARD.shape[0] == BOARD.shape[1], "Board is square"
SIZE = BOARD.shape[0]
MID = (SIZE - 1) // 2
START = next((r, c) for r in range(SIZE) for c in range(SIZE) if lines[r][c] == "S")
assert SIZE % 2 == 1, "Board is odd-sized"
assert START == (MID, MID), "Start is mid-point"
assert np.all(BOARD[0, :]) and np.all(BOARD[SIZE - 1, :]), "Bottom & top edges are free"
assert np.all(BOARD[:, 0]) and np.all(BOARD[:, SIZE - 1]), "Left & right edges are free"
assert np.all(BOARD[MID, :]) and np.all(BOARD[:, MID]), "Mid-lanes are free"


def neighbours(e):
    if e[0] > 0:
        yield e[0] - 1, e[1]
    if e[0] < SIZE - 1:
        yield e[0] + 1, e[1]
    if e[1] > 0:
        yield e[0], e[1] - 1
    if e[1] < SIZE - 1:
        yield e[0], e[1] + 1


def next_edges(edge, prev_edge):
    next_edge = set(
        n for e in edge for n in neighbours(e) if BOARD[n] and n not in prev_edge
    )
    return next_edge, edge


def reachable_paths_detail(start: tuple[int, int], max_steps: int | None = None):
    if max_steps is not None and max_steps < 0:
        return 0, 0, 0
    edge = {start}
    prev_edge = {}
    total = len(edge)
    alt = len(prev_edge)
    steps = 0
    while (max_steps is None or steps < max_steps) and edge:
        total, alt = alt, total
        edge, prev_edge = next_edges(edge, prev_edge)
        total += len(edge)
        steps += 1
    return total, alt, steps


def reachable_paths(start: tuple[int, int], max_steps: int):
    total, alt, steps = reachable_paths_detail(start, max_steps)
    if (max_steps - steps) % 2 == 0:
        return total
    return alt


# part 1
print(reachable_paths((MID, MID), 64))

# part 2
cov_res, cov_alt, min_steps = reachable_paths_detail((MID, MID))
if min_steps % 2 == 1:
    even_cover, odd_cover = cov_alt, cov_res
else:
    even_cover, odd_cover = cov_res, cov_alt

steps_remaining = 26501365

# first tile is exception, handle separately
total_cover = even_cover if steps_remaining % 2 == 0 else odd_cover
steps_remaining -= SIZE

last_complete = (steps_remaining - min_steps) // SIZE + 1
if last_complete % 2 == 0:
    odd_layers = (last_complete // 2) ** 2
    even_layers = (last_complete // 2) * (1 + (last_complete // 2))
else:
    odd_layers = ((last_complete + 1) // 2) ** 2
    even_layers = (last_complete + 1) * (last_complete - 1) // 4
assert odd_layers + even_layers == last_complete * (last_complete + 1) // 2

# nth layer has n*4 tiles
# 1st layer has even covers, 2nd layer has odd covers
# add alternating complete layers
total_cover += (even_layers * odd_cover + odd_layers * even_cover) * 4

# deal with the rest incomplete layers
steps_remaining = steps_remaining - last_complete * SIZE
layer = last_complete + 1

while steps_remaining > -2 * MID:
    # north, south, east, west
    straight_steps = steps_remaining + MID
    total_cover += reachable_paths((MID, 0 * MID), straight_steps)
    total_cover += reachable_paths((MID, 2 * MID), straight_steps)
    total_cover += reachable_paths((0 * MID, MID), straight_steps)
    total_cover += reachable_paths((2 * MID, MID), straight_steps)

    # diagonals
    diag_steps = steps_remaining + 2 * MID
    total_cover += (layer - 1) * reachable_paths((0 * MID, 0 * MID), diag_steps)
    total_cover += (layer - 1) * reachable_paths((0 * MID, 2 * MID), diag_steps)
    total_cover += (layer - 1) * reachable_paths((2 * MID, 0 * MID), diag_steps)
    total_cover += (layer - 1) * reachable_paths((2 * MID, 2 * MID), diag_steps)

    steps_remaining -= SIZE
    layer += 1
print(total_cover)
