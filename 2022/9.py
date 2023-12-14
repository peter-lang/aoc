moves = [
    (d, int(cnt))
    for d, cnt in (
        line.split()
        for line in filter(
            None, map(lambda x: x.strip(), open("9.txt", "r").readlines())
        )
    )
]


def move(r, d):
    if d == "L":
        r[0] = (r[0][0], r[0][1] - 1)
    elif d == "R":
        r[0] = (r[0][0], r[0][1] + 1)
    elif d == "U":
        r[0] = (r[0][0] - 1, r[0][1])
    elif d == "D":
        r[0] = (r[0][0] + 1, r[0][1])

    for i in range(1, len(r)):
        row_diff = r[i - 1][0] - r[i][0]
        col_diff = r[i - 1][1] - r[i][1]
        if abs(row_diff) == 2:
            if col_diff > 0:
                r[i] = (r[i][0] + row_diff // 2, r[i][1] + 1)
            elif col_diff < 0:
                r[i] = (r[i][0] + row_diff // 2, r[i][1] - 1)
            else:
                r[i] = (r[i][0] + row_diff // 2, r[i][1])
        elif abs(col_diff) == 2:
            if row_diff > 0:
                r[i] = (r[i][0] + 1, r[i][1] + col_diff // 2)
            elif row_diff < 0:
                r[i] = (r[i][0] - 1, r[i][1] + col_diff // 2)
            else:
                r[i] = (r[i][0], r[i][1] + col_diff // 2)


# part 1
rope = [(0, 0)] * 2
tail_coords = set()
for m, cnt in moves:
    for _ in range(cnt):
        move(rope, m)
        tail_coords.add(rope[-1])
print(len(tail_coords))

# part 2
rope = [(0, 0)] * 10
tail_coords = set()
for m, cnt in moves:
    for _ in range(cnt):
        move(rope, m)
        tail_coords.add(rope[-1])
print(len(tail_coords))
