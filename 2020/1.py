import operator
from functools import reduce

numbers = list(
    map(int, filter(None, map(lambda x: x.strip(), open("1.txt", "r").readlines())))
)


def all_pairs(nums):
    for idx, a in enumerate(nums):
        for b in nums[:idx]:
            yield a, b


def all_triples(nums):
    for a_idx, a in enumerate(nums):
        for b_idx, b in enumerate(nums[:a_idx]):
            for c in nums[:b_idx]:
                yield a, b, c


def prod(it):
    return reduce(operator.mul, it)


# part 1
print(prod(next(p for p in all_pairs(numbers) if sum(p) == 2020)))

# part 2
print(prod(next(tr for tr in all_triples(numbers) if sum(tr) == 2020)))
