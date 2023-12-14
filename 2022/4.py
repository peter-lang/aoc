intervals = list(
    (tuple(map(int, a.split("-"))), tuple(map(int, b.split("-"))))
    for a, b in (
        line.split(",")
        for line in filter(
            None, map(lambda x: x.strip(), open("4.txt", "r").readlines())
        )
    )
)


def contains(a, b):
    return a[0] <= b[0] and b[1] <= a[1] or b[0] <= a[0] and a[1] <= b[1]


def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


# part 1
print(sum(contains(a, b) for a, b in intervals))

# part 2
print(sum(overlaps(a, b) for a, b in intervals))
