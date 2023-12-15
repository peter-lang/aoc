from typing import Iterator

POINT = tuple[int, ...]

CUBES: set[POINT] = set(
    tuple(map(int, l.split(",")))
    for l in filter(None, map(lambda x: x.strip(), open("18.txt", "r").readlines()))
)

MIN: POINT = tuple(min(c[i] for c in CUBES) for i in range(3))
MAX: POINT = tuple(max(c[i] for c in CUBES) for i in range(3))


def neighbours(c: POINT) -> Iterator[POINT]:
    for idx in range(3):
        yield tuple(c_i - 1 if idx == i else c_i for i, c_i in enumerate(c))
        yield tuple(c_i + 1 if idx == i else c_i for i, c_i in enumerate(c))


def count_surface(cubes: set[POINT]) -> int:
    total = len(cubes) * 6
    for c in cubes:
        touching = sum(n in cubes for n in neighbours(c))
        total -= touching
    return total


# part 1
print(count_surface(CUBES))


def is_edge(c: POINT) -> bool:
    return any(c[idx] <= MIN[idx] or c[idx] >= MAX[idx] for idx in range(3))


def floodfill(
    cubes: set[POINT], interior: set[POINT], exterior: set[POINT], open_set: set[POINT]
):
    is_exterior = None
    checked = set()
    while open_set:
        n = open_set.pop()
        checked.add(n)
        if is_edge(n) or n in exterior:
            assert is_exterior is not False
            is_exterior = True
        elif n in interior:
            assert is_exterior is not True
            is_exterior = False
        if not is_edge(n):
            for ch in neighbours(n):
                if ch not in cubes and ch not in checked:
                    open_set.add(ch)

    if is_exterior is True:
        exterior.update(checked)
    else:
        interior.update(checked)


# part 2
INTERIOR = set()
EXTERIOR = set()
for cube in CUBES:
    for child in neighbours(cube):
        if child not in CUBES and child not in INTERIOR and child not in EXTERIOR:
            floodfill(CUBES, INTERIOR, EXTERIOR, {child})

print(count_surface(CUBES | INTERIOR))
