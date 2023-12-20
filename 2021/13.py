POINTS = set()
FOLDS = []
for line in filter(None, map(lambda x: x.strip(), open("13.txt", "r").readlines())):
    if line.startswith("fold along "):
        a, b = line[len("fold along ") :].split("=")
        FOLDS.append((a, int(b)))
    else:
        POINTS.add(tuple(map(int, line.split(","))))


def do_fold(points, fold):
    res = set()
    if fold[0] == "x":
        for p in points:
            if p[0] > fold[1]:
                res.add((fold[1] - (p[0] - fold[1]), p[1]))
            else:
                res.add(p)
    else:
        for p in points:
            if p[1] > fold[1]:
                res.add((p[0], fold[1] - (p[1] - fold[1])))
            else:
                res.add(p)
    return res


def pretty_print(points):
    xmax = max(p[0] for p in points)
    ymax = max(p[1] for p in points)
    for y in range(ymax + 1):
        print("".join("#" if (x, y) in points else " " for x in range(xmax + 1)))


# part 1
print(len(do_fold(POINTS, FOLDS[0])))

# part 2
pts = POINTS
for f in FOLDS:
    pts = do_fold(pts, f)
pretty_print(pts)
