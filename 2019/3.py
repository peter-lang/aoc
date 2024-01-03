a, b = filter(None, map(lambda x: x.strip(), open("3.txt", "r").readlines()))


def path(_path):
    result = dict()
    s = (0, 0)
    total = 0
    for el in _path:
        length = int(el[1:])
        if el[0] == "R":
            for i in range(length):
                result[(s[0], s[1] + i)] = total + i
            s = (s[0], s[1] + length)
            total += length
        elif el[0] == "L":
            for i in range(length):
                result[(s[0], s[1] - i)] = total + i
            s = (s[0], s[1] - length)
            total += length
        elif el[0] == "U":
            for i in range(length):
                result[(s[0] - i, s[1])] = total + i
            s = (s[0] - length, s[1])
            total += length
        elif el[0] == "D":
            for i in range(length):
                result[(s[0] + i, s[1])] = total + i
            s = (s[0] + length, s[1])
            total += length
    del result[(0, 0)]
    return result


def dist(pt):
    return abs(pt[0]) + abs(pt[1])


a = path(a.split(","))
b = path(b.split(","))

# part 1
print(min(dist(p) for p in set(a.keys()) & set(b.keys())))

# part 2
print(min(a[p] + b[p] for p in set(a.keys()) & set(b.keys())))
