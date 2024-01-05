import intcode

COMP = intcode.Computer(list(map(int, open("11.txt", "r").read().strip().split(","))))


DIRS = {"L": 0, "U": 1, "R": 2, "D": 3}


def turn_right(d):
    return (d + 1) % 4


def turn_left(d):
    return (d - 1) % 4


def left_or_right(d):
    return d % 2 == 0


def up_or_down(d):
    return d % 2 == 1


def next_rc(coord: tuple[int, int], d: int) -> tuple[int, int]:
    if left_or_right(d):
        diff = d - 1
        return coord[0], coord[1] + diff
    else:
        diff = d - 2
        return coord[0] + diff, coord[1]


def do_paint(comp, paint=None):
    if paint is None:
        paint = dict()
    rc, d = (0, 0), DIRS["U"]
    while (res := comp.run_to_outputs(2, paint.get(rc, 0))) is not None:
        col, right = res
        assert col in (0, 1) and right in (0, 1)
        paint[rc] = col
        if right == 1:
            d = turn_right(d)
        else:
            d = turn_left(d)
        rc = next_rc(rc, d)
    return paint


# part 1
print(len(do_paint(COMP.reset())))


# part 2
def print_img(pixels):
    whites = {k for k, v in pixels.items() if v == 1}
    min_row, max_row = min(r for r, c in whites), max(r for r, c in whites)
    min_col, max_col = min(c for r, c in whites), max(c for r, c in whites)

    def dec(rc):
        return "#" if rc in whites else " "

    for row in range(min_row, max_row + 1):
        print("".join(dec((row, col)) for col in range(min_col, max_col + 1)))


print_img(do_paint(COMP.reset(), {(0, 0): 1}))
