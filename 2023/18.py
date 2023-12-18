COORD = tuple[int, int]
RECT = tuple[COORD, COORD]

COL2DIR = {"0": "R", "1": "D", "2": "L", "3": "U"}
DIRS = {"L": 0, "U": 1, "R": 2, "D": 3}

lines = list(filter(None, map(lambda x: x.strip(), open("18.txt", "r").readlines())))
plan1 = [
    (d_str, int(step_str)) for d_str, step_str, _ in map(lambda x: x.split(), lines)
]
plan2 = [
    (COL2DIR[col[-2]], int(col[2:-2], 16))
    for _, _, col in map(lambda x: x.split(), lines)
]


def cross_product(a: COORD, b: COORD, c: COORD) -> int:
    #    LEFT   (1, 3)      RIGHT   (1, 3)
    #   POSITIVE   ^       NEGATIVE    |
    #              |                   v
    # (2, 1) -> (2, 3)    (2, 1) <- (2, 3)
    return (b[1] - a[1]) * (b[0] - c[0]) - (a[0] - b[0]) * (c[1] - b[1])


def sign(a: int):
    if a == 0:
        return 0
    if a < 0:
        return -1
    return 1


def left_or_right(d: int) -> bool:
    return d % 2 == 0


def next_rc(row: int, col: int, d: int, step: int) -> COORD:
    if left_or_right(d):
        diff = d - 1
        return row, col + diff * step
    else:
        diff = d - 2
        return row + diff * step, col


def do_step(c: COORD, d_str: str, step: int) -> COORD:
    return next_rc(c[0], c[1], DIRS[d_str], step)


def to_points(plan: list[tuple[str, int]]) -> tuple[list[COORD], int]:
    start = (0, 0)
    result = [start]
    result.append(do_step(result[-1], *plan[0]))
    result.append(do_step(result[-1], *plan[1]))
    total_rot = 0
    for p in plan[2:]:
        current = do_step(result[-1], *p)
        rot = sign(cross_product(result[-2], result[-1], current))
        assert rot != 0
        total_rot += rot
        result.append(current)
    assert result[-1] == start
    signed_total_rot = sign(total_rot)
    assert signed_total_rot != 0
    return result[:-1], signed_total_rot


def signed_cross_product_at(idx: int, points: list[COORD]) -> int:
    cp = cross_product(*(points[(idx + i) % len(points)] for i in range(3)))
    return sign(cp)


def identify_rectangle(q: list[COORD]) -> tuple[RECT, int]:
    if q[1][1] == q[2][1]:
        if q[1][1] > q[0][1]:
            # 1--0
            # |
            # 2----3
            right = q[1][1]
            left = max(q[0][1], q[3][1])
        else:
            #   0--1
            #      |
            # 3----2
            left = q[1][1]
            right = min(q[0][1], q[3][1])
        top = min(q[1][0], q[2][0])
        bottom = max(q[1][0], q[2][0])
        clip_area = (bottom - top + 1) * (right - left)
    else:
        if q[1][0] > q[0][0]:
            #    3
            # 0  |
            # |  |
            # 1--2
            top = max(q[0][0], q[3][0])
            bottom = q[1][0]
        else:
            # 1--2
            # |  |
            # 0  |
            #    3
            top = q[1][0]
            bottom = min(q[0][0], q[3][0])
        left = min(q[1][1], q[2][1])
        right = max(q[1][1], q[2][1])
        clip_area = (right - left + 1) * (bottom - top)
    return ((top, left), (bottom, right)), clip_area


def any_points_in_rect(points, idx_start, idx_end_exclusive, rect: RECT) -> bool:
    while idx_start != idx_end_exclusive:
        p = points[idx_start]
        if rect[0][0] <= p[0] <= rect[1][0] and rect[0][1] <= p[1] <= rect[1][1]:
            return True
        idx_start = (idx_start + 1) % len(points)
    return False


def replace_idx(
    points: list[COORD], idx_start: int, idx_end: int, points_to_add: list[COORD]
) -> list[COORD]:
    if idx_end < idx_start:
        return points[(idx_end + 1) : idx_start] + points_to_add
    else:
        return points[:idx_start] + points_to_add + points[(idx_end + 1) :]


def clip_ear(points: list[COORD], rot_sign: int) -> tuple[list[COORD], int]:
    if len(points) == 4:
        top = min(p[0] for p in points)
        bottom = max(p[0] for p in points)
        left = min(p[1] for p in points)
        right = max(p[1] for p in points)
        assert set(points) == {
            (top, left),
            (top, right),
            (bottom, left),
            (bottom, right),
        }
        return [], (bottom - top + 1) * (right - left + 1)
    idx = 0
    while True:
        while (
            signed_cross_product_at(idx, points) != rot_sign
            or signed_cross_product_at(idx + 1, points) != rot_sign
        ):
            idx += 1
        q = [points[(idx + i) % len(points)] for i in range(4)]
        rect, clip_area = identify_rectangle(q)

        # check if other points are in ear, search another ear if there are
        if any_points_in_rect(points, (idx + 4) % len(points), idx % len(points), rect):
            idx += 1
            continue

        # remove points
        rect_points = {
            rect[0],
            rect[1],
            (rect[0][0], rect[1][1]),
            (rect[1][0], rect[0][1]),
        }
        quad_points = set(q)
        if rect_points == quad_points:
            return (
                replace_idx(points, idx % len(points), (idx + 3) % len(points), []),
                clip_area,
            )
        else:
            additional_point = rect_points - quad_points
            assert len(additional_point) == 1
            additional_point = additional_point.pop()
            remaining_point = quad_points - rect_points
            assert len(remaining_point) == 1
            remaining_point = remaining_point.pop()
            rem_idx = q.index(remaining_point)
            assert rem_idx == 0 or rem_idx == 3
            if rem_idx == 0:
                pts_to_add = [remaining_point, additional_point]
            else:
                pts_to_add = [additional_point, remaining_point]

            clipped_points = replace_idx(
                points, idx % len(points), (idx + 3) % len(points), pts_to_add
            )
            return clipped_points, clip_area


def quad_tessellate(points: list[COORD], total_rot_sign: int) -> int:
    total_area = 0
    while len(points) > 0:
        points, clip_area = clip_ear(points, total_rot_sign)
        total_area += clip_area
    return total_area


# part 1
print(quad_tessellate(*to_points(plan1)))

# part 2
print(quad_tessellate(*to_points(plan2)))
