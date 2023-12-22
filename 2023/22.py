from collections import defaultdict

bricks = [
    (idx, tuple(map(int, a.split(","))), tuple(map(int, b.split(","))))
    for idx, (a, b) in enumerate(
        map(
            lambda x: x.split("~"),
            filter(None, map(lambda x: x.strip(), open("22.txt", "r").readlines())),
        )
    )
]


# Original idx,(x0,y0,z0),(x1,y1,z1) => min(z) min(x) min(y) len(z) len(x) len(y) idx
def transform(idx, a, b):
    return (
        min(a[2], b[2]),
        min(a[0], b[0]),
        min(a[1], b[1]),
        abs(a[2] - b[2]) + 1,
        abs(a[0] - b[0]) + 1,
        abs(a[1] - b[1]) + 1,
        idx,
    )


def a_supports_b(a: tuple[int, int, int, int], b: tuple[int, int, int, int]):
    for x in range(b[2]):
        for y in range(b[3]):
            if a[0] <= b[0] + x < a[0] + a[2] and a[1] <= b[1] + y < a[1] + a[3]:
                return True
    return False


def brick_is_supported_by(
    supports: list[tuple[int, int, int, int, int]], sfc: tuple[int, int, int, int]
) -> list[int]:
    return [sp[4] for sp in supports if a_supports_b(sp[:4], sfc)]


transformed = sorted([transform(idx, a, b) for idx, a, b in bricks])
level2supports = defaultdict(list)
brick_supported_by = dict()

for min_z, min_x, min_y, len_z, len_x, len_y, idx in transformed:
    surface = (min_x, min_y, len_x, len_y)
    while True:
        if min_z == 1:
            level2supports[min_z + len_z].append(surface + (idx,))
            brick_supported_by[idx] = frozenset()
            break
        if supported_by := brick_is_supported_by(level2supports[min_z], surface):
            level2supports[min_z + len_z].append(surface + (idx,))
            brick_supported_by[idx] = frozenset(supported_by)
            break
        min_z -= 1

brick_gives_support_to = {idx: frozenset() for idx in brick_supported_by.keys()}
for idx, supported_by in brick_supported_by.items():
    for sup in supported_by:
        brick_gives_support_to[sup] |= {idx}


def find_falling(removed: frozenset, effected: frozenset) -> frozenset:
    return frozenset(e for e in effected if not (brick_supported_by[e] - removed))


def would_fall_if_removed(
    removed: frozenset, effected: frozenset
) -> tuple[frozenset, frozenset]:
    while falling := find_falling(removed, effected):
        removed |= falling
        effected -= falling
        for f in falling:
            effected |= brick_gives_support_to[f]
    return removed, effected


removable = 0
collapse_count = 0
for idx, supports in brick_gives_support_to.items():
    would_fall, _ = would_fall_if_removed(frozenset({idx}), supports)
    if len(would_fall) == 1:
        removable += 1
    else:
        collapse_count += len(would_fall) - 1

# part 1
print(removable)

# part 2
print(collapse_count)
