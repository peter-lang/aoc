from collections import defaultdict

pairs: list[tuple[list[frozenset[str]], list[frozenset[str]]]] = [
    (list(map(frozenset, a.split())), list(map(frozenset, b.split())))
    for a, b in (
        line.split(" | ")
        for line in filter(
            None, map(lambda x: x.strip(), open("8.txt", "r").readlines())
        )
    )
]


def create_decoder(nums: list[frozenset[str]]) -> dict[frozenset[str], int]:
    len2num: dict[int, list[frozenset[str]]] = defaultdict(list)
    for n in nums:
        len2num[len(n)].append(n)

    _1 = len2num[2][0]
    _7 = len2num[3][0]
    _4 = len2num[4][0]
    _8 = len2num[7][0]

    # len2num[5] contains _2, _3, _5
    _3 = next(e for e in len2num[5] if len(e - _1) == 3)
    _5 = next(e for e in len2num[5] if e != _3 and len(e - _4) == 2)
    _2 = next(e for e in len2num[5] if e not in (_3, _5))

    # len2num[6] contains _0, _6, _9
    _9 = _1 | _5
    _6 = next(e for e in len2num[6] if len(e - _7) == 4)
    _0 = next(e for e in len2num[6] if e != _9 and len(e - _7) == 3)

    result = {_0: 0, _1: 1, _2: 2, _3: 3, _4: 4, _5: 5, _6: 6, _7: 7, _8: 8, _9: 9}
    assert len(result) == 10
    return result


def decode(digits: list[frozenset[str]], decoder: dict[frozenset[str], int]) -> int:
    digit_str = "".join(str(decoder[d]) for d in digits)
    return int(digit_str)


# part 1
print(sum(sum(len(d) in {2, 4, 3, 7} for d in digits) for _, digits in pairs))


# part 2
print(sum(decode(digits, create_decoder(tbl)) for tbl, digits in pairs))
