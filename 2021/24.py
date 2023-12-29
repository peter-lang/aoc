import pulp as pl

lines = list(filter(None, map(lambda x: x.strip(), open("24.txt", "r").readlines())))
group_len = len(lines) // 14
assert len(lines) % 14 == 0 and group_len == 18
assert all(
    all(lines[offset + i * group_len] == lines[offset] for i in range(1, 14))
    for offset in range(group_len)
    if offset not in (4, 5, 15)
), "all lines are the same except a few"
assert all(
    all(lines[offset + i * group_len][:6] == lines[offset][:6] for i in range(1, 14))
    for offset in (4, 5, 15)
), "varying lines only differ in RHS param"


# reverse engineered inner function:
# def func(w, z, d1, d2, d3):
#     if (z % 26 + d2) == w:
#         return int(z / d1)
#     else:
#         z = int(z / d1)
#         z = z * 26 + w + d3
#         return z

# d1 in {1, 26}; d3 >= 0
# result can be treated as a base26 number, which is a concatenation of elements in [0-25]
# when "(z % 26 + d2) == w", then no additional tail is concatenated
# otherwise, (w+d3) is concatenated to the end
# when d1 == 26, the tail is removed
# otherwise (d1 == 1), the tail remains

inner_func_params = [
    (
        int(lines[4 + i * group_len][6:]),
        int(lines[5 + i * group_len][6:]),
        int(lines[15 + i * group_len][6:]),
    )
    for i in range(14)
]

assert sum(ifp[0] == 26 for ifp in inner_func_params) == 7
# there are 7 cases, a tail is removed
assert sum(ifp[1] >= 10 for ifp in inner_func_params) == 7
# there are 7 cases, when additional tail is concatenated, because "(z % 26 + d2) == w" cannot be true
# we can only make the result 0 at the end, if we make sure that "(z % 26 + d2) == w" is true whenever possible


def solve(sense: int):
    model = pl.LpProblem(sense=sense)
    w = {
        i: pl.LpVariable(f"w{i}", lowBound=1, upBound=9, cat=pl.LpInteger)
        for i in range(14)
    }
    stack = []
    for idx, (d1, d2, d3) in enumerate(inner_func_params):
        if d2 >= 10:
            if d1 == 26:
                stack.pop()
            stack.append(w[idx] + d3)
        else:
            model += stack[-1] + d2 == w[idx]
            if d1 == 26:
                stack.pop()

    model += pl.lpSum(w[i] * 10 ** (14 - 1 - i) for i in range(14))
    model.solve(pl.PULP_CBC_CMD(msg=0))
    return int(model.objective.value())


# part 1
print(solve(pl.LpMaximize))

# part 2
print(solve(pl.LpMinimize))
