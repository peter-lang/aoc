lines = filter(None, map(lambda x: x.strip(), open("25.txt", "r").readlines()))

decode = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

encode = ["0", "1", "2", "=", "-"]


def snafu2dec(s: str) -> int:
    return sum(decode[ch] * 5**idx for idx, ch in enumerate(reversed(s)))


def dec2snafu(d: int) -> str:
    result = []
    while d > 0:
        v = d % 5
        result.append(encode[v])
        d //= 5
        if v > 2:
            d += 1
    return "".join(reversed(result))


print(dec2snafu(sum(snafu2dec(line) for line in lines)))
