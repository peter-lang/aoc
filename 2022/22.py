import numpy as np
from typing import NamedTuple

LINES = [l.rstrip("\n") for l in open("22.txt", "r").readlines()]
COORD = tuple[int, int]


def flat_join_arrs(arrs, el):
    yield from arrs[0]
    for a in arrs[1:]:
        yield el
        yield from a


PATH = list(
    flat_join_arrs(
        list(
            flat_join_arrs([[int(d)] for d in seg.split("L")], "L")
            for seg in LINES[-1].split("R")
        ),
        "R",
    )
)


SIDE_LEN = 50

DIFFS = {
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0),
}

TURN = {
    "R": {"R": "D", "L": "U"},
    "D": {"R": "L", "L": "R"},
    "L": {"R": "U", "L": "D"},
    "U": {"R": "R", "L": "L"},
}

D_SCORE = {
    "R": 0,
    "D": 1,
    "L": 2,
    "U": 3,
}


def add(a: COORD, b: COORD) -> COORD:
    return a[0] + b[0], a[1] + b[1]


def sub(a: COORD, b: COORD) -> COORD:
    return a[0] - b[0], a[1] - b[1]


Face = NamedTuple(
    "Face",
    [
        ("row", int),
        ("col", int),
        ("board", np.array),
        ("identify", dict[str, tuple["Face", str]]),
    ],
)


def parse(board, r, c) -> Face:
    decode = {".": 0, "#": 1}
    return Face(
        row=r,
        col=c,
        board=np.array(
            [
                [
                    decode[board[r * SIDE_LEN + h][c * SIDE_LEN + w]]
                    for w in range(SIDE_LEN)
                ]
                for h in range(SIDE_LEN)
            ]
        ),
        identify=dict(),
    )


def transform(c: COORD, side_from: str, side_to: str) -> tuple[COORD, str]:
    if side_from == "U":
        if side_to == "D":
            return (SIDE_LEN, c[1]), "U"
        elif side_to == "U":
            return (-1, SIDE_LEN - 1 - c[1]), "D"
        elif side_to == "R":
            return (SIDE_LEN - 1 - c[1], SIDE_LEN), "L"
        elif side_to == "L":
            return (c[1], -1), "R"
    elif side_from == "L":
        if side_to == "R":
            return (c[0], SIDE_LEN), "L"
        elif side_to == "L":
            return (SIDE_LEN - 1 - c[0], -1), "R"
        elif side_to == "U":
            return (-1, c[0]), "D"
        elif side_to == "D":
            return (SIDE_LEN, SIDE_LEN - 1 - c[0]), "U"
    elif side_from == "D":
        if side_to == "U":
            return (-1, c[1]), "D"
        elif side_to == "D":
            return (SIDE_LEN, SIDE_LEN - 1 - c[1]), "U"
        elif side_to == "L":
            return (SIDE_LEN - 1 - c[1], -1), "R"
        elif side_to == "R":
            return (c[1], SIDE_LEN), "L"
    elif side_from == "R":
        if side_to == "L":
            return (c[0], -1), "R"
        elif side_to == "R":
            return (SIDE_LEN - 1 - c[0], SIDE_LEN), "L"
        elif side_to == "U":
            return (-1, SIDE_LEN - 1 - c[0]), "D"
        elif side_to == "D":
            return (SIDE_LEN, c[0]), "U"
    assert False


def walk(face: Face, coord: COORD, d: str, step: int):
    while step > 0:
        coord = add(coord, DIFFS[d])
        step -= 1

        if (
            coord[0] == -1
            or coord[0] == SIDE_LEN
            or coord[1] == -1
            or coord[1] == SIDE_LEN
        ):
            other, side_to = face.identify[d]
            coord = sub(coord, DIFFS[d])
            step += 1

            c_in, d_in = transform(coord, d, side_to)
            f_out, c_out, d_out = walk(other, c_in, d_in, step)
            if c_out == c_in:
                # blockade at other side
                return face, coord, d
            else:
                return f_out, c_out, d_out

        if face.board[coord] == 1:
            coord = sub(coord, DIFFS[d])
            return face, coord, d

    return face, coord, d


def walk_path(path: list[int | str], face: Face, coord: COORD, d: str):
    for p in path:
        if isinstance(p, str):
            d = TURN[d][p]
        else:
            face, coord, d = walk(face, coord, d, p)
    return face, coord, d


faces = [
    parse(LINES[:-2], 0, 1),  # 0
    parse(LINES[:-2], 0, 2),  # 1
    parse(LINES[:-2], 1, 1),  # 2
    parse(LINES[:-2], 2, 0),  # 3
    parse(LINES[:-2], 2, 1),  # 4
    parse(LINES[:-2], 3, 0),  # 5
]

# part 1
faces[0].identify["U"] = (faces[4], "D")
faces[0].identify["L"] = (faces[1], "R")
faces[0].identify["R"] = (faces[1], "L")
faces[0].identify["D"] = (faces[2], "U")

faces[1].identify["U"] = (faces[1], "D")
faces[1].identify["L"] = (faces[0], "R")
faces[1].identify["R"] = (faces[0], "L")
faces[1].identify["D"] = (faces[1], "U")

faces[2].identify["U"] = (faces[0], "D")
faces[2].identify["L"] = (faces[2], "R")
faces[2].identify["R"] = (faces[2], "L")
faces[2].identify["D"] = (faces[4], "U")

faces[3].identify["U"] = (faces[5], "D")
faces[3].identify["L"] = (faces[4], "R")
faces[3].identify["R"] = (faces[4], "L")
faces[3].identify["D"] = (faces[5], "U")

faces[4].identify["U"] = (faces[2], "D")
faces[4].identify["L"] = (faces[3], "R")
faces[4].identify["R"] = (faces[3], "L")
faces[4].identify["D"] = (faces[0], "U")

faces[5].identify["U"] = (faces[3], "D")
faces[5].identify["L"] = (faces[5], "R")
faces[5].identify["R"] = (faces[5], "L")
faces[5].identify["D"] = (faces[3], "U")


f_stop, coord_stop, d_stop = walk_path(PATH, faces[0], (0, 0), "R")
password = (
    1000 * (f_stop.row * SIDE_LEN + coord_stop[0] + 1)
    + 4 * (f_stop.col * SIDE_LEN + coord_stop[1] + 1)
    + D_SCORE[d_stop]
)
print(password)


# part 2
faces[0].identify["U"] = (faces[5], "L")
faces[0].identify["L"] = (faces[3], "L")
faces[0].identify["R"] = (faces[1], "L")
faces[0].identify["D"] = (faces[2], "U")

faces[1].identify["U"] = (faces[5], "D")
faces[1].identify["L"] = (faces[0], "R")
faces[1].identify["R"] = (faces[4], "R")
faces[1].identify["D"] = (faces[2], "R")

faces[2].identify["U"] = (faces[0], "D")
faces[2].identify["L"] = (faces[3], "U")
faces[2].identify["R"] = (faces[1], "D")
faces[2].identify["D"] = (faces[4], "U")

faces[3].identify["U"] = (faces[2], "L")
faces[3].identify["L"] = (faces[0], "L")
faces[3].identify["R"] = (faces[4], "L")
faces[3].identify["D"] = (faces[5], "U")

faces[4].identify["U"] = (faces[2], "D")
faces[4].identify["L"] = (faces[3], "R")
faces[4].identify["R"] = (faces[1], "R")
faces[4].identify["D"] = (faces[5], "R")

faces[5].identify["U"] = (faces[3], "D")
faces[5].identify["L"] = (faces[0], "U")
faces[5].identify["R"] = (faces[4], "D")
faces[5].identify["D"] = (faces[1], "U")


f_stop, coord_stop, d_stop = walk_path(PATH, faces[0], (0, 0), "R")
password = (
    1000 * (f_stop.row * SIDE_LEN + coord_stop[0] + 1)
    + 4 * (f_stop.col * SIDE_LEN + coord_stop[1] + 1)
    + D_SCORE[d_stop]
)
print(password)
