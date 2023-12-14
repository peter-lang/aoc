lines = list(filter(None, map(lambda x: x.strip(), open("10.txt", "r").readlines())))

MAX_ROW = len(lines)
MAX_COL = len(lines[0])


def valid_coord(c):
    return 0 <= c[0] < MAX_ROW and 0 <= c[1] < MAX_COL


connects: list[list[list[tuple[int, int]]]] = [
    [[] for _ in range(MAX_COL)] for _ in range(MAX_ROW)
]
starting_point = (-1, -1)
for row, line in enumerate(lines):
    for col, ch in enumerate(line):
        if ch == "|":
            connects[row][col] = list(
                filter(valid_coord, [(row - 1, col), (row + 1, col)])
            )
        elif ch == "-":
            connects[row][col] = list(
                filter(valid_coord, [(row, col - 1), (row, col + 1)])
            )
        elif ch == "7":
            connects[row][col] = list(
                filter(valid_coord, [(row + 1, col), (row, col - 1)])
            )
        elif ch == "J":
            connects[row][col] = list(
                filter(valid_coord, [(row - 1, col), (row, col - 1)])
            )
        elif ch == "L":
            connects[row][col] = list(
                filter(valid_coord, [(row - 1, col), (row, col + 1)])
            )
        elif ch == "F":
            connects[row][col] = list(
                filter(valid_coord, [(row + 1, col), (row, col + 1)])
            )
        elif ch == "S":
            starting_point = (row, col)


def find_next(prev: tuple[int, int], curr: tuple[int, int]) -> tuple[int, int] | None:
    nexts = connects[curr[0]][curr[1]]
    if len(nexts) != 2:
        return None
    try:
        return nexts[1 - nexts.index(prev)]
    except ValueError:
        return None


def possible_nodes(s):
    return [
        list(filter(valid_coord, [(s[0] - 1, s[1]), (s[0] + 1, s[1])])),
        list(filter(valid_coord, [(s[0], s[1] - 1), (s[0], s[1] + 1)])),
        list(filter(valid_coord, [(s[0] + 1, s[1]), (s[0], s[1] - 1)])),
        list(filter(valid_coord, [(s[0] - 1, s[1]), (s[0], s[1] - 1)])),
        list(filter(valid_coord, [(s[0] - 1, s[1]), (s[0], s[1] + 1)])),
        list(filter(valid_coord, [(s[0] + 1, s[1]), (s[0], s[1] + 1)])),
    ]


def find_loop_with(
    s: tuple[int, int], substitute: list[tuple[int, int]]
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]] | None:
    loop = [s]
    if len(substitute) != 2:
        return None
    p, n = s, substitute[0]
    while n != s:
        loop.append(n)
        p, n = n, find_next(p, n)
        if n is None:
            return None
    if p != substitute[1]:
        return None
    return loop, substitute


def find_loop(
    s: tuple[int, int]
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    return max(
        filter(None, (find_loop_with(s, sub) for sub in possible_nodes(s))),
        key=lambda x: len(x[0]),
        default=([], []),
    )


found_loop, sub = find_loop(starting_point)

# fix connections
connects[starting_point[0]][starting_point[1]] = sub

# part 1
print(len(found_loop) // 2)


# part 2
def is_vertical(r, c):
    # crossing while left bottom -> right bottom
    return any(n[0] == r + 1 for n in connects[r][c])


def interior_counts(loop):
    cnt = 0
    loop_set = set(loop)
    for r in range(MAX_ROW):
        prev = 0
        for c in range(MAX_COL):
            if (r, c) in loop_set:
                if is_vertical(r, c):
                    prev += 1
            elif prev % 2 == 1:
                cnt += 1
    return cnt


print(interior_counts(found_loop))
