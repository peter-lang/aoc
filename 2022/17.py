COORD = tuple[int, int]
POINTS = tuple[COORD, ...]
SHAPE = tuple[POINTS, int, int]

SHAPES: list[SHAPE] = [
    (((0, 0), (0, 1), (0, 2), (0, 3)), 1, 4),
    (((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)), 3, 3),
    (((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)), 3, 3),
    (((0, 0), (1, 0), (2, 0), (3, 0)), 4, 1),
    (((0, 0), (0, 1), (1, 0), (1, 1)), 2, 2),
]

JETS = open("17.txt", "r").read()


def c_add(a: COORD, b: COORD) -> COORD:
    return a[0] + b[0], a[1] + b[1]


def c_subtr(a: COORD, b: COORD) -> COORD:
    return a[0] - b[0], a[1] - b[1]


def p_add(points: POINTS, c: COORD) -> POINTS:
    return tuple(c_add(p, c) for p in points)


def p_subtr(points: POINTS, c: COORD) -> POINTS:
    return tuple(c_subtr(p, c) for p in points)


def fall_object(
    objects: set[COORD], shape: SHAPE, pos: COORD, jet_idx: int
) -> tuple[POINTS, COORD, int]:
    obj, _, w = shape
    while True:
        jet = JETS[jet_idx]
        jet_idx = (jet_idx + 1) % len(JETS)
        # jet_move if can
        jet_move = (0, 1) if jet == ">" else (0, -1)
        pos = c_add(pos, jet_move)
        if pos[1] == -1 or pos[1] + w == 8:
            pos = c_subtr(pos, jet_move)
        else:
            obj = p_add(obj, jet_move)
            if any(o in objects for o in obj):
                obj = p_subtr(obj, jet_move)
                pos = c_subtr(pos, jet_move)
        # falling
        fall = (-1, 0)
        pos = c_add(pos, fall)
        if pos[0] == -1:
            pos = c_subtr(pos, fall)
            return obj, pos, jet_idx
        obj = p_add(obj, fall)
        if any(o in objects for o in obj):
            obj = p_subtr(obj, fall)
            pos = c_subtr(pos, fall)
            return obj, pos, jet_idx


def rounds(cnt):
    height = 0
    shape_idx = 0
    jet_idx = 0
    objects: set[COORD] = set()

    period_dict = dict()
    sim_height = 0

    i = 0
    while i < cnt:
        obj, h, w = SHAPES[shape_idx]
        shape_idx = (shape_idx + 1) % len(SHAPES)

        pos = (height + 3, 2)
        obj = p_add(obj, pos)
        obj, pos_finish, jet_idx = fall_object(objects, (obj, h, w), pos, jet_idx)

        pos_diff = c_subtr(pos, pos_finish)
        pos = pos_finish

        height = max(height, pos[0] + h)

        state = (shape_idx, jet_idx, pos_diff)
        if state in period_dict:
            prev_i, prev_height = period_dict[state]
            mod = i - prev_i
            cycles = (cnt - i) // mod
            if cycles > 0:
                sim_height += cycles * (height - prev_height)
                i += cycles * mod
        else:
            period_dict[state] = (i, height)

        objects.update(obj)
        i += 1

    return height + sim_height


# part 1
print(rounds(2022))

# part 2
print(rounds(1000000000000))
