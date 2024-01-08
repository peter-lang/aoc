import sympy as sp
import re
import z3

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


# part 1
print(collisions_2d_inside(hailstones, 200000000000000, 400000000000000))


# part 2
def solve(trajectories):
    # for first 3 lines, this gives 9 equations and 9 variables:
    # ap + r * av == u + r * v
    # bp + s * bv == u + s * v
    # cp + t * cv == u + t * v
    solver = z3.SolverFor("QF_LIA")

    p = z3.IntVector("p", 3)
    v = z3.IntVector("v", 3)
    ts = z3.IntVector("t", len(trajectories))

    for t_i, (hs_p, hs_v) in zip(ts, trajectories):
        solver.add(t_i > 0)
        for i in range(3):
            solver.add(hs_p[i] + t_i * hs_v[i] == p[i] + t_i * v[i])

    assert solver.check() == z3.sat
    mod = solver.model()
    p_val = [mod[p[i]].as_long() for i in range(3)]
    v_val = [mod[v[i]].as_long() for i in range(3)]
    return p_val, v_val


res_p, _ = solve(hailstones[:3])

print(int(sum(res_p)))
