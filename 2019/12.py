from functools import reduce
from math import gcd


def parse_pos(line):
    parts = line[1:-1].split(", ")
    return tuple(int(part[2:]) for part in parts)


lines = filter(None, map(lambda x: x.strip(), open("12.txt", "r").readlines()))
positions = tuple(map(parse_pos, lines))

pos_axis = tuple(tuple(p[i] for p in positions) for i in range(3))
vel_axis = tuple((0,) * len(positions) for i in range(3))
state_axis = tuple(zip(pos_axis, vel_axis))


def sign(v):
    if v < 0:
        return -1
    if v > 0:
        return 1
    return 0


def update_1d(pos, vel):
    vel = tuple(v + sum(sign(j - p) for j in pos) for p, v in zip(pos, vel))
    pos = tuple(p + v for p, v in zip(pos, vel))
    return pos, vel


def sim_1d(pos, vel, t_max):
    for _ in range(t_max):
        pos, vel = update_1d(pos, vel)
    return pos, vel


def period_1d(pos, vel):
    memo = {(pos, vel): 0}
    t = 0
    while True:
        pos, vel = update_1d(pos, vel)
        t += 1
        if (prev_t := memo.get((pos, vel), None)) is not None:
            period = t - prev_t
            return prev_t, period


def energy(state):
    pot = [0] * len(positions)
    kin = [0] * len(positions)
    for p, v in state:
        for i, pi in enumerate(p):
            pot[i] += abs(pi)
        for i, vi in enumerate(v):
            kin[i] += abs(vi)
    return sum(p * k for p, k in zip(pot, kin))


# part 1
final_state_axis = tuple(sim_1d(p, v, 1000) for p, v in state_axis)
print(energy(final_state_axis))

# part 2
periods = tuple(period_1d(p, v) for p, v in state_axis)
assert all(p[0] == 0 for p in periods)
periods = tuple(p[1] for p in periods)
print(reduce(lambda a, b: a * b // gcd(a, b), periods))
