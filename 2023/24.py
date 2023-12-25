import sympy as sp
import re

hailstones = [
    (tuple(map(int, re.split(r"\s*,\s*", a))), tuple(map(int, re.split(r"\s*,\s*", b))))
    for a, b in map(
        lambda x: re.split(r"\s*@\s*", x),
        filter(None, map(lambda x: x.strip(), open("24.txt", "r").readlines())),
    )
]


def collision_2d(ap, av, bp, bv, axis):
    # solve for:
    # ap + at * av == bp + bt * bv
    mx = sp.Matrix(
        [
            [av[axis[0]], -bv[axis[0]], bp[axis[0]] - ap[axis[0]]],
            [av[axis[1]], -bv[axis[1]], bp[axis[1]] - ap[axis[1]]],
        ]
    )
    m_rref, m_pivots = mx.rref()
    if m_pivots != (0, 1):
        # parallel trajectories
        return None
    at = m_rref[0, 2]
    bt = m_rref[1, 2]
    return at, bt


def future_collision_2d_in_region(ap, av, bp, bv, pos_min, pos_max):
    coll = collision_2d(ap, av, bp, bv, axis=(0, 1))
    if coll is None:
        return False
    at, bt = coll
    if at < 0 or bt < 0:
        # collision in past
        return False
    pt = (ap[0] + at * av[0], ap[1] + at * av[1])
    return bool(pos_min <= pt[0] <= pos_max and pos_min <= pt[1] <= pos_max)


def collisions_2d_inside(trajectories, pos_min: int, pos_max: int):
    return sum(
        future_collision_2d_in_region(a[0], a[1], b[0], b[1], pos_min, pos_max)
        for idx, a in enumerate(trajectories)
        for b in trajectories[idx:]
    )


def all_2d_collisions(trajectories):
    for idx, a in enumerate(trajectories):
        collisions = []
        for b in trajectories[idx:]:
            coll = collision_2d(a[0], a[1], b[0], b[1], axis=(1, 2))
            if coll is not None:
                collisions.append((coll, b))
        if len(collisions) >= 2:
            pass


# part 1
print(collisions_2d_inside(hailstones, 200000000000000, 400000000000000))


# part 2
def print_equations(ap, av, bp, bv, cp, cv):
    # for first 3 lines, this gives 9 equations and 9 variables:
    # ap + r * av == u + r * v
    # bp + s * bv == u + s * v
    # cp + t * cv == u + t * v
    # rearranging:
    # (ap + r * av - bp - s * bv)/(r-s) == v
    # (ap + r * av - cp - t * cv)/(r-t) == v
    # rearranging:
    # (ap + r * av - bp - s * bv)*(r-t) == (ap + r * av - cp - t * cv)*(r-s)
    # solved this in wolframalpha: https://www.wolframalpha.com/input/?i=system+of+equations
    for i in range(3):
        print(
            f"({ap[i]}+r*({av[i]})-({bp[i]})-s*({bv[i]}))*(r-t) = ({ap[i]}+r*({av[i]})-({cp[i]})-t*({cv[i]}))*(r-s)"
        )


print_equations(*hailstones[0], *hailstones[1], *hailstones[2])

r = 711444906273
s = 943556327678
t = 69419109633


def find_vectors(ap, av, bp, bv, cp, cv, r, s, t):
    v = tuple((ap[i] + r * av[i] - bp[i] - s * bv[i]) / (r - s) for i in range(3))
    p = tuple(ap[i] + r * (av[i] - v[i]) for i in range(3))
    return p, v


res_p, res_v = find_vectors(*hailstones[0], *hailstones[1], *hailstones[2], r, s, t)
print(int(sum(res_p)))
