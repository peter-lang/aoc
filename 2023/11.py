lines: list[str] = list(
    filter(None, map(lambda x: x.strip(), open("11.txt", "r").readlines()))
)

MAX_ROW = len(lines)
MAX_COL = len(lines[0])


def galaxy_coords(empty_space_factor):
    empty_rows = set()
    for row in range(MAX_ROW):
        if not any(lines[row][col] == "#" for col in range(MAX_COL)):
            empty_rows.add(row)

    empty_cols = set()
    for col in range(MAX_COL):
        if not any(lines[row][col] == "#" for row in range(MAX_ROW)):
            empty_cols.add(col)

    galaxies = []
    row_offset = 0
    for row in range(MAX_ROW):
        col_offset = 0
        if row in empty_rows:
            row_offset += empty_space_factor - 1
            continue
        for col in range(MAX_COL):
            if col in empty_cols:
                col_offset += empty_space_factor - 1
            elif lines[row][col] == "#":
                galaxies.append((row + row_offset, col + col_offset))

    return galaxies


def distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def pairs(array):
    for a in range(len(array)):
        for b in range(a):
            yield array[a], array[b]


# part 1
print(sum(distance(a, b) for a, b in pairs(galaxy_coords(2))))

# part 2
print(sum(distance(a, b) for a, b in pairs(galaxy_coords(1000000))))
