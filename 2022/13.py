from itertools import islice, zip_longest
from functools import cmp_to_key
from bisect import bisect

lines = list(filter(None, map(lambda x: x.strip(), open("13.txt", "r").readlines())))


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def compare(a, b):
    if b is None:
        return 1
    if a is None:
        return -1
    if isinstance(a, int) and isinstance(b, int):
        return a - b
    elif isinstance(a, list) and isinstance(b, list):
        for _a, _b in zip_longest(a, b):
            if (res := compare(_a, _b)) != 0:
                return res
        return 0
    elif isinstance(a, list):
        return compare(a, [b])
    else:
        return compare([a], b)


# part 1
print(
    sum(
        idx + 1
        for idx, (a, b) in enumerate(batched(lines, 2))
        if compare(eval(a), eval(b)) < 0
    )
)

# part 2
packets = [eval(line) for line in lines] + [[[2]], [[6]]]
key = cmp_to_key(compare)
packets.sort(key=key)
start_idx = bisect(packets, key([[2]]), key=key)
end_idx = bisect(packets, key([[6]]), key=key)
print(start_idx * end_idx)
