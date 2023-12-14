from functools import reduce

lines = filter(None, map(lambda x: x.strip(), open("2.txt", "r").readlines()))

multiset = dict[str, int]


def parse_cubes(s: str) -> list[multiset]:
    return [
        {
            color.strip(): int(cnt.strip())
            for cnt, color in (el.strip().split() for el in group.strip().split(","))
        }
        for group in s.strip().split(";")
    ]


games = [(idx + 1, parse_cubes(line.split(":")[1])) for idx, line in enumerate(lines)]


def union(*args: multiset) -> multiset:
    return {
        k: max(*(arg.get(k, 0) for arg in args))
        for k in set.union(*(set(arg.keys()) for arg in args))
    }


# part 1
requirement = {"red": 12, "green": 13, "blue": 14}
print(sum(g_id for g_id, cubes in games if union(requirement, *cubes) == requirement))

# part 2
print(sum(reduce(lambda a, b: a * b, union(*cubes).values(), 1) for _, cubes in games))
