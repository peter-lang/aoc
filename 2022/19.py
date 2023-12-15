import pulp as pl
from functools import reduce
import operator
import re


ore_pattern = re.compile(r"Each ore robot costs (\d+) ore.")
clay_pattern = re.compile(r"Each clay robot costs (\d+) ore.")
obsidian_pattern = re.compile(r"Each obsidian robot costs (\d+) ore and (\d+) clay.")
geode_pattern = re.compile(r"Each geode robot costs (\d+) ore and (\d+) obsidian.")


def parse_prices(desc):
    ore_m = ore_pattern.search(desc)
    clay_m = clay_pattern.search(desc)
    obsidian_m = obsidian_pattern.search(desc)
    geode_m = geode_pattern.search(desc)
    return [
        [int(ore_m.group(1)), 0, 0, 0],
        [int(clay_m.group(1)), 0, 0, 0],
        [int(obsidian_m.group(1)), int(obsidian_m.group(2)), 0, 0],
        [int(geode_m.group(1)), 0, int(geode_m.group(2)), 0],
    ]


blueprints = [
    parse_prices(line)
    for line in filter(None, map(lambda x: x.strip(), open("19.txt", "r").readlines()))
]


def solve_problem(prices, max_time):
    max_res = len(prices)

    model = pl.LpProblem(sense=pl.LpMaximize)
    build = dict()
    for r in range(max_res):
        for t in range(max_time):
            build[r, t] = pl.LpVariable(
                f"B-{r}-{t}", lowBound=0, upBound=1, cat=pl.LpInteger
            )

    produce = dict()
    for r in range(max_res):
        produce[r, 0] = 1 if r == 0 else 0
        for t in range(1, max_time):
            produce[r, t] = produce[r, t - 1] + build[r, t - 1]

    stock = dict()
    for r in range(max_res):
        for t in range(max_time):
            prev_stock = stock[r, t - 1] if t > 0 else 0
            expanse = pl.lpSum(build[r_i, t] * prices[r_i][r] for r_i in range(max_res))
            model += expanse <= prev_stock
            stock[r, t] = prev_stock - expanse + produce[r, t]

    for t in range(max_time):
        model += pl.lpSum(build[r, t] for r in range(max_res)) <= 1

    model += stock[max_res - 1, max_time - 1]
    model.solve(pl.PULP_CBC_CMD(msg=0))
    return int(model.objective.value())


# part 1
print(
    sum(
        (idx + 1) * solve_problem(blueprint, 24)
        for idx, blueprint in enumerate(blueprints)
    )
)

# part 2
print(
    reduce(
        operator.mul,
        (solve_problem(blueprint, 32) for idx, blueprint in enumerate(blueprints[:3])),
        1,
    )
)
