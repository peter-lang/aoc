import math
from functools import reduce
import operator

lines = list(filter(None, map(lambda x: x.strip(), open("13.txt", "r").readlines())))

# part 1
ts = int(lines[0])
periods = list(map(lambda x: None if x == "x" else int(x), lines[1].split(",")))
known_periods = list(filter(None, periods))
wait_time, next_bus_id = min(
    (period - (ts % period), period) for period in known_periods
)
print(wait_time * next_bus_id)

# part 2
assert all(
    math.gcd(p1, p2) == 1
    for idx, p1 in enumerate(known_periods)
    for p2 in known_periods[:idx]
), "all periods are co-prime"
N = reduce(operator.mul, known_periods)

mod_sys = [(t, p) for t, p in enumerate(periods) if p is not None]

# Chinese remainder theorem
result = 0
for t, p in mod_sys:
    y = N // p
    z = pow(y, -1, p)
    result += (p - t) * z * y
print(result % N)
