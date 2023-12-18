from functools import reduce


def decode(a, b):
    if a == "forward":
        return int(b), 0
    elif a == "down":
        return 0, int(b)
    elif a == "up":
        return 0, -int(b)


lines = list(
    map(
        lambda x: decode(*x.split()),
        filter(None, map(lambda x: x.strip(), open("2.txt", "r").readlines())),
    )
)

# part 1
pos = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), lines, (0, 0))
print(pos[0] * pos[1])

# part 2
pos = reduce(
    lambda acc, el: (acc[0] + el[0], acc[1] + el[0] * acc[2], acc[2] + el[1]),
    lines,
    (0, 0, 0),
)
print(pos[0] * pos[1])
