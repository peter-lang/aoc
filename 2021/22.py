from itertools import product
from functools import reduce
import operator


def parse(line):
    prefix, coords = line.split(" ")
    x, y, z = (p.split("=")[1] for p in coords.split(","))
    return prefix == "on", (
        tuple(map(int, x.split(".."))),
        tuple(map(int, y.split(".."))),
        tuple(map(int, z.split(".."))),
    )


CUBOIDS = list(
    map(parse, filter(None, map(lambda x: x.strip(), open("22.txt", "r").readlines())))
)


def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


FILTERED = [
    (sign, coords)
    for sign, coords in CUBOIDS
    if all(overlaps(coord, (-50, 50)) for coord in coords)
]


def sum_cubes_each(signed_cuboids):
    result = set()
    for sign, cuboid in signed_cuboids:
        cubes = set(product(*(range(cuboid[i][0], cuboid[i][1] + 1) for i in range(3))))
        if sign:
            result |= cubes
        else:
            result -= cubes
    return len(result)


def intersect(a, b):
    if not all(overlaps(a[i], b[i]) for i in range(3)):
        return None
    return tuple((max(a[i][0], b[i][0]), min(a[i][1], b[i][1])) for i in range(3))


def minus_intersect(a, b):
    def coord_split(ai, bi):
        if ai[0] < bi[0]:
            yield 0, (ai[0], bi[0] - 1)
        yield 1, (bi[0], bi[1])
        if bi[1] < ai[1]:
            yield 2, (bi[1] + 1, ai[1])

    for (x_idx, x), (y_idx, y), (z_idx, z) in product(
        *(list(coord_split(a[i], b[i])) for i in range(3))
    ):
        if x_idx == 1 and y_idx == 1 and z_idx == 1:
            continue
        yield x, y, z


def minus(a, b):
    intersection = intersect(a, b)
    if intersection is None:
        yield a
    else:
        yield from minus_intersect(a, intersection)


def sum_cubes(signed_cuboids):
    cuboids = []
    for sign, cuboid in signed_cuboids:
        cuboids = [c for existing in cuboids for c in minus(existing, cuboid)]
        if sign:
            cuboids.append(cuboid)

    return sum(
        reduce(operator.mul, (c[i][1] - c[i][0] + 1 for i in range(3))) for c in cuboids
    )


# part 1
# print(sum_cubes_each(FILTERED))
print(sum_cubes(FILTERED))

# part 2
print(sum_cubes(CUBOIDS))
