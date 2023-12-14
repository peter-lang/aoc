from itertools import islice

lines = list(filter(None, map(lambda x: x.strip(), open("3.txt", "r").readlines())))


def prio(ch):
    if "a" <= ch <= "z":
        return ord(ch) - ord("a") + 1
    return ord(ch) - ord("A") + 27


def common(*args):
    return set.intersection(*map(set, args))


def split_in_half(line):
    midpoint = len(line) // 2
    return line[:midpoint], line[midpoint:]


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


# part 1
print(sum(prio(ch) for line in lines for ch in common(*split_in_half(line))))

# part 2
print(sum(prio(ch) for batch in batched(lines, 3) for ch in common(*batch)))
