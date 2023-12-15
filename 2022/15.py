import re

coord_pattern = re.compile(
    "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def parse_coord(line):
    m = coord_pattern.match(line)
    return (int(m.group(2)), int(m.group(1))), (int(m.group(4)), int(m.group(3)))


COORD = tuple[int, int]
LINE = tuple[COORD, COORD]
lines: list[LINE] = [
    parse_coord(line)
    for line in filter(None, map(lambda x: x.strip(), open("15.txt", "r").readlines()))
]


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def minus(totals, bs):
    for b in bs:
        rem = []
        for t in totals:
            if not overlaps(b, t):
                rem.append(t)
            elif b[0] <= t[0] and b[1] < t[1]:
                rem.append((b[1] + 1, t[1]))
            elif b[1] >= t[1] and b[0] > t[0]:
                rem.append((t[0], b[0] - 1))
            elif t[0] < b[0] and b[1] < t[1]:
                rem.append((t[0], b[0] - 1))
                rem.append((b[1] + 1, t[1]))
        totals = rem
    return totals


def covered(row, col_int=None):
    intervals = []
    for src, beacon in lines:
        d = dist(src, beacon)
        d_v = abs(src[0] - row)
        d_h = d - d_v
        if d_h >= 0:
            if col_int is None:
                intervals.append((src[1] - d_h, src[1] + d_h))
            else:
                i = (max(src[1] - d_h, col_int[0]), min(src[1] + d_h, col_int[1]))
                if i[1] > i[0]:
                    if i == col_int:
                        return [i]
                    intervals.append(i)
    intervals.sort()

    prev = None
    disjoint_intervals = []
    for i in intervals:
        if prev is None:
            prev = i
        elif overlaps(i, prev):
            prev = (min(i[0], prev[0]), max(i[1], prev[1]))
        else:
            disjoint_intervals.append(prev)
            prev = None
    if prev is not None:
        disjoint_intervals.append(prev)

    return disjoint_intervals


def non_set_covers(row, intervals):
    occupied = set()
    for _, beacon in lines:
        if beacon[0] == row and any(a <= beacon[1] <= b for a, b in intervals):
            occupied.add(beacon[1])
    total = 0
    for a, b in intervals:
        total += b - a + 1
    return total - len(occupied)


# part 1
r = 2000000
print(non_set_covers(r, covered(r)))


# part 2
def find_non_covered(row_int, col_int):
    for row in range(row_int[0], row_int[1] + 1):
        covers = covered(row, col_int)
        if len(covers) > 1 or covers[0] != col_int:
            rem = minus([col_int], covers)
            assert len(rem) == 1 and rem[0][0] == rem[0][1]
            return row, rem[0][0]


r, c = find_non_covered((0, 4000000), (0, 4000000))
print(c * 4000000 + r)
