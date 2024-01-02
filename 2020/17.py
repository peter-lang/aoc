from itertools import product
import numpy as np

lines = filter(None, map(lambda x: x.strip(), open("17.txt", "r").readlines()))
BOARD_2D = np.array([[ch == "#" for ch in line] for line in lines], dtype=np.uint8)


def all_except(S: np.array, idx: int, val):
    return tuple(slice(0, S.shape[i]) if i != idx else val for i in range(len(S.shape)))


def invert(coords):
    return tuple(-c for c in coords)


def slice_offset(shape, i):
    if i == 0:
        return slice(0, shape)
    elif i > 0:
        return slice(i, shape)
    else:
        return slice(0, shape + i)


def slice_offsets(shapes: tuple, coords):
    return tuple(slice_offset(shape, c) for shape, c in zip(shapes, coords))


def update(S: np.array):
    padding = tuple(
        (int(np.any(S[all_except(S, i, 0)] > 0)), int(np.any(S[all_except(S, i, -1)])))
        for i in range(len(S.shape))
    )
    S = np.pad(S, padding)
    N = np.zeros_like(S)

    for offsets in product(range(-1, 2), repeat=len(S.shape)):
        if all(c == 0 for c in offsets):
            # this is the origin
            continue
        N[slice_offsets(N.shape, offsets)] += S[slice_offsets(S.shape, invert(offsets))]

    birth = (N == 3) & (S == 0)
    survive = ((N == 2) | (N == 3)) & (S == 1)
    S[...] = 0
    S[birth | survive] = 1
    return S


def update_times(state, n):
    for _ in range(n):
        state = update(state)
    return state


# part 1
print(update_times(np.expand_dims(BOARD_2D, axis=0), 6).sum())

# part 2
print(update_times(np.expand_dims(BOARD_2D, axis=(0, 1)), 6).sum())
