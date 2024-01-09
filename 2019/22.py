from functools import reduce, partial
from typing import NamedTuple

ModOp = NamedTuple("ModOp", [("a", int), ("b", int), ("m", int)])

INSTRUCTIONS = list(map(lambda x: x.rstrip(), open("22.txt", "r").readlines()))


def chain(inner: ModOp, outer: ModOp):
    assert inner.m == outer.m
    # (inner.a * x + inner.b) * outer.a + outer.b
    return ModOp(
        inner.a * outer.a % inner.m, inner.b * outer.a + outer.b % inner.m, inner.m
    )


def inverse(op: ModOp) -> ModOp:
    # y = (a*x + b) % m
    # pow(a, -1, m) * y - pow(a, -1, m)*b = x
    inv_a = pow(op.a, -1, op.m)
    return ModOp(inv_a, -op.b * inv_a % op.m, op.m)


def apply(op: ModOp, x: int):
    return (op.a * x + op.b) % op.m


def parse_inst(inst, deck_size) -> ModOp:
    if inst.startswith("cut "):
        val = int(inst[4:])
        return ModOp(1, -val, deck_size)
    elif inst.startswith("deal with increment "):
        val = int(inst[20:])
        return ModOp(val, 0, deck_size)
    elif inst == "deal into new stack":
        return ModOp(-1, -1, deck_size)
    else:
        assert False


shuffle = reduce(chain, map(partial(parse_inst, deck_size=10007), INSTRUCTIONS))

# part 1
print(apply(shuffle, 2019))


def apply_multi(op: ModOp, x: int, times: int):
    if times == 0:
        return x
    if times % 2 == 1:
        return apply_multi(op, apply(op, x), times - 1)
    squared = chain(op, op)
    return apply_multi(squared, x, times // 2)


rev_shuffle = reduce(
    chain,
    map(
        inverse,
        map(partial(parse_inst, deck_size=119315717514047), reversed(INSTRUCTIONS)),
    ),
)

# part 2
print(apply_multi(rev_shuffle, 2020, 101741582076661))
