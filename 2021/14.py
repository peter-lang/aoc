from functools import cache

lines = list(filter(None, map(lambda x: x.strip(), open("14.txt", "r").readlines())))

template = lines[0]
rules = {a: b for a, b in (line.split(" -> ") for line in lines[1:])}


def add(*args: dict) -> dict:
    return {
        k: sum(a.get(k, 0) for a in args)
        for k in set.union(*(set(a.keys()) for a in args))
    }


@cache
def steps(seg, time) -> dict[str, int]:
    if (r := rules.get(seg, None)) is not None:
        a = seg[0] + r
        b = r + seg[1]
        if time == 1:
            return {r: 1}
        else:
            return add(steps(a, time - 1), steps(b, time - 1), {r: 1})
    else:
        if time == 1:
            return dict()
        else:
            return steps(seg, time - 1)


def steps_str(s, time):
    base = add(*({ch: 1} for ch in s))
    cnts = add(base, *(steps(s[p : (p + 2)], time) for p in range(len(s) - 1)))
    return cnts


def score(cnts: dict[str, int]) -> int:
    vals = sorted(cnts.values())
    return vals[-1] - vals[0]


# part 1
print(score(steps_str(template, 10)))

# part 2
print(score(steps_str(template, 40)))
