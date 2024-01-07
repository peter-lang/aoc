import numpy as np
import re
import intcode

CODE = list(map(int, open("17.txt", "r").read().strip().split(",")))
DIRS = {"L": 0, "U": 1, "R": 2, "D": 3}

comp = intcode.Computer(CODE).reset()
board = [[]]
current = (-1, -1), -1
while (out := comp.run_to_output()) is not None:
    ch_out = chr(out)
    if ch_out == "\n":
        if board[-1]:
            board.append([])
    else:
        board[-1].append(ch_out != ".")
        current_coord = (len(board) - 1, len(board[-1]) - 1)
        if ch_out == "^":
            current = current_coord, DIRS["U"]
        elif ch_out == ">":
            current = current_coord, DIRS["R"]
        elif ch_out == "<":
            current = current_coord, DIRS["L"]
        elif ch_out == "v":
            current = current_coord, DIRS["D"]
board = np.array(board if board[-1] else board[:-1], dtype=int)


def intersections():
    board_p = np.pad(board, ((1, 1), (1, 1)))
    neigh_p = np.copy(board_p)
    neigh_p[1:-1, 1:-1] += (
        board_p[:-2, 1:-1] + board_p[2:, 1:-1] + board_p[1:-1, :-2] + board_p[1:-1, 2:]
    )
    neigh_p = neigh_p[1:-1, 1:-1]
    return tuple(tuple(r) for r in np.argwhere(neigh_p == 5))


# part 1
print(sum(r * c for r, c in intersections()))


def turn_right(d):
    return (d + 1) % 4


def turn_left(d):
    return (d - 1) % 4


def left_or_right(d):
    return d % 2 == 0


def next_rc(coord: tuple[int, int], d: int) -> tuple[int, int]:
    if left_or_right(d):
        diff = d - 1
        return coord[0], coord[1] + diff
    else:
        diff = d - 2
        return coord[0] + diff, coord[1]


def is_path(coord: tuple[int, int]):
    return (
        0 <= coord[0] < board.shape[0]
        and 0 <= coord[1] < board.shape[1]
        and bool(board[coord])
    )


def find_path(rc: tuple[int, int], d: int):
    visited = {rc}
    path = []

    def next_turn():
        if is_path(next_rc(rc, turn_left(d))):
            return "L", turn_left(d)
        elif is_path(next_rc(rc, turn_right(d))):
            return "R", turn_right(d)
        return None

    while (turn_res := next_turn()) is not None:
        turn, d = turn_res
        path.append(turn)
        length = 0
        n_rc = next_rc(rc, d)
        while is_path(n_rc):
            rc = n_rc
            visited.add(rc)
            length += 1
            n_rc = next_rc(rc, d)
        path.append(str(length))
    assert len(visited) == board.sum()
    return "".join(path)


path_comp_pat = re.compile(r"([LR])(\d+)")


def path_components(path):
    return path_comp_pat.findall(path)


def compress(sections: list[str], max_depth=3):
    if max_depth == 0:
        return not sections, []
    components = path_components(sections[0])
    for prefix_len in range(len(components), 0, -1):
        prefix = "".join((f"{a}{b}" for a, b in components[:prefix_len]))
        total_chrs = len(prefix) + 2 * prefix_len - 1
        if total_chrs > 20:
            continue
        remaining_sections = [
            rem for sec in sections for rem in sec.split(prefix) if rem
        ]
        success, sub_words = compress(remaining_sections, max_depth - 1)
        if success:
            return True, [prefix] + sub_words
    return False, []


def solve():
    path = find_path(*current)
    comp_res, words = compress([path])
    assert comp_res
    for ch, word in zip(["A", "B", "C"], words):
        path = path.replace(word, ch)

    comp_inputs = [",".join(list(path))]
    for word in words:
        comp_inputs.append(",".join((f"{a},{b}" for a, b in path_components(word))))
    comp_inputs = "\n".join(comp_inputs) + "\n"
    comp_inputs = list(map(ord, comp_inputs))
    return comp_inputs


# part 2
comp = intcode.Computer([2] + CODE[1:]).reset(inputs=solve() + [ord("n"), ord("\n")])
last_out = None
while (out := comp.run_to_output()) is not None:
    last_out = out
print(last_out)
