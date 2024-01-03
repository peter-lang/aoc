lines = list(filter(None, map(lambda x: x.strip(), open("24.txt", "r").readlines())))


def move(n, d):
    if d.startswith("nw"):
        return (n[0] - 1, n[1] - 1), d[2:]
    if d.startswith("ne"):
        return (n[0] - 1, n[1] + 1), d[2:]
    if d.startswith("e"):
        return (n[0], n[1] + 2), d[1:]
    if d.startswith("se"):
        return (n[0] + 1, n[1] + 1), d[2:]
    if d.startswith("sw"):
        return (n[0] + 1, n[1] - 1), d[2:]
    if d.startswith("w"):
        return (n[0], n[1] - 2), d[1:]
    assert False


def execute(txt):
    n = (0, 0)
    while txt:
        n, txt = move(n, txt)
    return n


def flip_txts(txts):
    flipped = set()
    for txt in txts:
        final = execute(txt)
        if final in flipped:
            flipped.remove(final)
        else:
            flipped.add(final)
    return flipped


def neighbours(n):
    yield n[0] - 1, n[1] - 1  # nw
    yield n[0] - 1, n[1] + 1  # ne
    yield n[0], n[1] + 2  # e
    yield n[0] + 1, n[1] + 1  # se
    yield n[0] + 1, n[1] - 1  # sw
    yield n[0], n[1] - 2  # w


def flip_day(flipped):
    result = set()
    for f in flipped:
        if 1 <= sum(n in flipped for n in neighbours(f)) <= 2:
            result.add(f)
        for n in neighbours(f):
            if n not in flipped and sum(nn in flipped for nn in neighbours(n)) == 2:
                result.add(n)
    return result


def flip_day_times(flipped, times):
    for _ in range(times):
        flipped = flip_day(flipped)
    return flipped


blacks = flip_txts(lines)

# part 1
print(len(blacks))

# part 2
print(len(flip_day_times(blacks, 100)))
