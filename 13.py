import numpy as np

patterns: list[np.array] = []
rows = []
for line in map(lambda x: x.strip(), open("13.txt", "r").readlines()):
    if rows and not line:
        patterns.append(np.array(rows))
        rows = []
    else:
        rows.append([1 if ch == "#" else 0 for ch in line])
if rows:
    patterns.append(np.array(rows))


def find_reflection(pattern: np.array, errors: int):
    vertical = np.flip(pattern, axis=1)
    for i in range(2, pattern.shape[1] + 1, 2):
        if np.sum(pattern[:, :i] != vertical[:, -i:]) == errors:
            return i // 2, True
        if (
            i != pattern.shape[1]
            and np.sum(pattern[:, -i:] != vertical[:, :i]) == errors
        ):
            return pattern.shape[1] - i // 2, True

    horizontal = np.flip(pattern, axis=0)
    for i in range(2, pattern.shape[0] + 1, 2):
        if np.sum(pattern[:i, :] != horizontal[-i:, :]) == errors:
            return i // 2, False
        if (
            i != pattern.shape[0]
            and np.sum(pattern[-i:, :] != horizontal[:i, :]) == errors
        ):
            return pattern.shape[0] - i // 2, False


# print 1
print(
    sum(
        idx if vertical else idx * 100
        for idx, vertical in (find_reflection(p, 0) for p in patterns)
    )
)

# print 2
print(
    sum(
        idx if vertical else idx * 100
        for idx, vertical in (find_reflection(p, 2) for p in patterns)
    )
)
