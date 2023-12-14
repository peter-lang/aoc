from itertools import islice
from typing import NamedTuple, Callable
from math import gcd
from functools import reduce, partial
import operator

Monkey = NamedTuple(
    "Monkey",
    [
        ("op", Callable[[int], int]),
        ("div", int),
        ("t_idx", int),
        ("f_idx", int),
    ],
)


def lcm(a, b):
    return a * b // gcd(a, b)


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


monkey_items: list[list[int]] = []
monkeys: list[Monkey] = []
for desc in batched(
    filter(None, map(lambda x: x.strip(), open("11.txt", "r").readlines())), 6
):
    starting_items = list(map(int, desc[1][len("Starting items: ") :].split(", ")))
    operation = desc[2][len("Operation: new = old ") :]
    if operation[0] == "*":
        if operation[2:] == "old":
            op = lambda x: x * x
        else:
            op = partial(operator.mul, int(operation[2:]))
    else:
        if operation[2:] == "old":
            op = lambda x: x + x
        else:
            op = partial(operator.add, int(operation[2:]))
    div = int(desc[3][len("Test: divisible by ") :])
    t_idx = int(desc[4][len("If true: throw to monkey ") :])
    f_idx = int(desc[5][len("If false: throw to monkey ") :])
    monkeys.append(Monkey(op, div, t_idx, f_idx))
    monkey_items.append(starting_items)


def monkey_business(items, rounds, reducer):
    inspections = [0] * len(monkeys)
    for _ in range(rounds):
        for idx, monkey in enumerate(monkeys):
            for item in items[idx]:
                inspections[idx] += 1
                level = monkey.op(item)
                level = reducer(level)
                if level % monkey.div == 0:
                    items[monkey.t_idx].append(level)
                else:
                    items[monkey.f_idx].append(level)
            items[idx] = []

    inspections = sorted(inspections)
    return inspections[-1] * inspections[-2]


# part 1
starting_items = [list(i) for i in monkey_items]
print(monkey_business(starting_items, 20, lambda x: x // 3))

# part 2
starting_items = [list(i) for i in monkey_items]
common_div = reduce(lcm, (m.div for m in monkeys))
print(monkey_business(starting_items, 10000, lambda x: x % common_div))
