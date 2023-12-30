import numpy as np

lines = list(filter(None, map(lambda x: x.strip(), open("11.txt", "r").readlines())))

SEAT = np.array([[ch != "." for ch in line] for line in lines])
OCCUPIED = np.array([[int(ch == "#") for ch in line] for line in lines], dtype=np.uint8)


def immediate_neighbours_padded(seat, occupied):
    neighbours = np.zeros_like(occupied)
    neighbours[1:-1, 1:-1] = (
        occupied[2:, 2:]
        + occupied[2:, 1:-1]
        + occupied[2:, :-2]
        + occupied[1:-1, 2:]
        + occupied[1:-1, :-2]
        + occupied[:-2, 2:]
        + occupied[:-2, 1:-1]
        + occupied[:-2, :-2]
    )
    return neighbours


def first_neighbours(seat, occupied):
    n_n = np.zeros_like(occupied)
    for r in range(1, occupied.shape[0]):
        n_n[r, :] = np.where(seat[r - 1, :], occupied[r - 1, :], n_n[r - 1, :])

    n_s = np.zeros_like(occupied)
    for r in range(occupied.shape[0] - 2, -1, -1):
        n_s[r, :] = np.where(seat[r + 1, :], occupied[r + 1, :], n_s[r + 1, :])

    n_w = np.zeros_like(occupied)
    for c in range(1, occupied.shape[1]):
        n_w[:, c] = np.where(seat[:, c - 1], occupied[:, c - 1], n_w[:, c - 1])

    n_e = np.zeros_like(occupied)
    for c in range(occupied.shape[1] - 2, -1, -1):
        n_e[:, c] = np.where(seat[:, c + 1], occupied[:, c + 1], n_e[:, c + 1])

    n_nw = np.zeros_like(occupied)
    for r in range(1, occupied.shape[0]):
        for c in range(1, occupied.shape[1]):
            n_nw[r, c] = (
                occupied[r - 1, c - 1] if seat[r - 1, c - 1] else n_nw[r - 1, c - 1]
            )

    n_ne = np.zeros_like(occupied)
    for r in range(1, occupied.shape[0]):
        for c in range(occupied.shape[1] - 2, -1, -1):
            n_ne[r, c] = (
                occupied[r - 1, c + 1] if seat[r - 1, c + 1] else n_ne[r - 1, c + 1]
            )

    n_sw = np.zeros_like(occupied)
    for r in range(occupied.shape[0] - 2, -1, -1):
        for c in range(1, occupied.shape[1]):
            n_sw[r, c] = (
                occupied[r + 1, c - 1] if seat[r + 1, c - 1] else n_sw[r + 1, c - 1]
            )

    n_se = np.zeros_like(occupied)
    for r in range(occupied.shape[0] - 2, -1, -1):
        for c in range(occupied.shape[1] - 2, -1, -1):
            n_se[r, c] = (
                occupied[r + 1, c + 1] if seat[r + 1, c + 1] else n_se[r + 1, c + 1]
            )

    return n_n + n_s + n_e + n_w + n_nw + n_ne + n_sw + n_se


def next_state(seat, occupied, neighbours_func, remains_limit):
    neighbours = neighbours_func(seat, occupied)
    result = np.zeros_like(occupied)
    birth = (occupied == 0) & (neighbours == 0)
    remains = (occupied == 1) & (neighbours < remains_limit)
    result[seat & (birth | remains)] = 1
    return result


def change_until_stable(seat, occupied, neighbours_func, remains_limit):
    while True:
        tmp = next_state(seat, occupied, neighbours_func, remains_limit)
        if np.all(tmp == occupied):
            return tmp
        else:
            occupied = tmp


# part 1
print(
    change_until_stable(
        np.pad(SEAT, ((1, 1), (1, 1)), constant_values=False),
        np.pad(OCCUPIED, ((1, 1), (1, 1)), constant_values=0),
        immediate_neighbours_padded,
        4,
    ).sum()
)

# part 2
print(change_until_stable(SEAT, OCCUPIED, first_neighbours, 5).sum())
