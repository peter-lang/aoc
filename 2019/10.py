import math

lines = filter(None, map(lambda x: x.strip(), open("10.txt", "r").readlines()))

ASTEROIDS = set()
for row, line in enumerate(lines):
    for col, ch in enumerate(line):
        if ch == "#":
            ASTEROIDS.add((row, col))


def get_dir(src, dst):
    diff = dst[0] - src[0], dst[1] - src[1]
    if diff[0] == 0:
        diff = (0, 1 if diff[1] > 0 else -1)
    elif diff[1] == 0:
        diff = (1 if diff[0] > 0 else -1, 0)
    else:
        div = math.gcd(diff[0], diff[1])
        diff = diff[0] // div, diff[1] // div
    return diff


def find_first(asteroids, src, diff):
    src = (src[0] + diff[0], src[1] + diff[1])
    while src not in asteroids:
        src = (src[0] + diff[0], src[1] + diff[1])
    return src


def in_los(asteroids, src, dst):
    if src == dst:
        return False
    diff = get_dir(src, dst)
    return find_first(asteroids, src, diff) == dst


def all_dirs(asteroids, src):
    valid_dirs = set(get_dir(src, dst) for dst in asteroids if src != dst)
    valid_dirs = list((math.atan2(c, r), (r, c)) for r, c in valid_dirs)
    valid_dirs.sort(reverse=True)
    return [b for a, b in valid_dirs]


def find_nth_to_shoot(asteroids, src, idx):
    while asteroids:
        for diff in all_dirs(asteroids, src):
            idx -= 1
            dst = find_first(asteroids, src, diff)
            if idx == 0:
                return dst
            asteroids.remove(dst)


# part 1
max_in_los, loc = max(
    (sum(in_los(ASTEROIDS, a, b) for b in ASTEROIDS), a) for a in ASTEROIDS
)
print(max_in_los)

# part 2
row, col = find_nth_to_shoot(set(ASTEROIDS), loc, 200)
print(col * 100 + row)
