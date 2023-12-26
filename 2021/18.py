from dataclasses import dataclass
from typing import Optional
from functools import reduce


@dataclass
class SnailFishNumber:
    parent: Optional["SnailFishNumber"] = None
    a: "SnailFishItem" = 0
    b: "SnailFishItem" = 0

    @property
    def is_leaf(self):
        return isinstance(self.a, int) and isinstance(self.b, int)


SnailFishItem = SnailFishNumber | int


def parse(s: str) -> SnailFishItem:
    def parse_rec(elem, par) -> SnailFishItem:
        if isinstance(elem, int):
            return elem
        elif isinstance(elem, list):
            assert len(elem) == 2
            num = SnailFishNumber(parent=par)
            num.a = parse_rec(elem[0], num)
            num.b = parse_rec(elem[1], num)
            return num

    raw = eval(s)
    return parse_rec(raw, None)


sf_numbers = list(
    map(parse, filter(None, map(lambda x: x.strip(), open("18.txt", "r").readlines())))
)


def add(a: SnailFishItem, b: SnailFishItem) -> SnailFishNumber:
    res = SnailFishNumber(a=a, b=b)
    a.parent = res
    b.parent = res
    return res


def to_str(sfi: SnailFishItem):
    if isinstance(sfi, int):
        return str(sfi)
    else:
        return f"[{to_str(sfi.a)},{to_str(sfi.b)}]"


def find_first_value_to_left(
    sfi: SnailFishNumber,
) -> Optional[tuple[SnailFishNumber, bool]]:
    curr, prev = sfi.parent, sfi

    while curr is not None and curr.a is prev:
        prev, curr = curr, curr.parent

    if curr is None:
        return None

    if isinstance(curr.a, int):
        return curr, True

    curr = curr.a
    while isinstance(curr.b, SnailFishNumber):
        curr = curr.b
    return curr, False


def find_first_value_to_right(
    sfi: SnailFishNumber,
) -> Optional[tuple[SnailFishNumber, bool]]:
    curr, prev = sfi.parent, sfi

    while curr is not None and curr.b is prev:
        prev, curr = curr, curr.parent

    if curr is None:
        return None

    if isinstance(curr.b, int):
        return curr, False

    curr = curr.b
    while isinstance(curr.a, SnailFishNumber):
        curr = curr.a
    return curr, True


def do_explodes(sfi: SnailFishItem, depth=0):
    if isinstance(sfi, int):
        return False
    elif depth >= 4 and sfi.is_leaf:
        if (res := find_first_value_to_left(sfi)) is not None:
            v, side = res
            if side:
                v.a += sfi.a
            else:
                v.b += sfi.a
        if (res := find_first_value_to_right(sfi)) is not None:
            v, side = res
            if side:
                v.a += sfi.b
            else:
                v.b += sfi.b
        curr = sfi.parent
        if curr.a is sfi:
            curr.a = 0
        else:
            curr.b = 0
        return True
    else:
        return do_explodes(sfi.a, depth + 1) or do_explodes(sfi.b, depth + 1)


def do_splits(sfi: SnailFishItem, depth=0):
    if isinstance(sfi, int):
        return False
    else:
        if isinstance(sfi.a, SnailFishNumber):
            if do_splits(sfi.a, depth + 1):
                return True
        elif sfi.a >= 10:
            sfi.a = SnailFishNumber(parent=sfi, a=sfi.a // 2, b=(sfi.a + 1) // 2)
            return True
        if isinstance(sfi.b, SnailFishNumber):
            if do_splits(sfi.b, depth + 1):
                return True
        elif sfi.b >= 10:
            sfi.b = SnailFishNumber(parent=sfi, a=sfi.b // 2, b=(sfi.b + 1) // 2)
            return True
        return False


def add_reduce(a: SnailFishItem, b: SnailFishItem):
    res = add(a, b)
    while do_explodes(res) or do_splits(res):
        pass
    return res


def magnitude(el: SnailFishItem):
    if isinstance(el, int):
        return el
    else:
        return 3 * magnitude(el.a) + 2 * magnitude(el.b)


def copy(el: SnailFishItem, parent: Optional[SnailFishNumber] = None):
    if isinstance(el, int):
        return el
    else:
        res = SnailFishNumber(parent=parent)
        res.a = copy(el.a, res)
        res.b = copy(el.b, res)
        return res


# part 1
print(magnitude(reduce(add_reduce, [copy(n) for n in sf_numbers])))


# part 2
def all_pairs(elems: list) -> tuple:
    for a_idx, a in enumerate(elems):
        for b_idx, b in enumerate(elems):
            if a_idx != b_idx:
                yield copy(a), copy(b)


print(max(magnitude(add_reduce(a, b)) for a, b in all_pairs(sf_numbers)))
