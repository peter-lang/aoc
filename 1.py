words = {
    w: idx + 1
    for idx, w in enumerate(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    )
}


def digit_at(s: str, pos: int, use_words: bool):
    if s[pos].isdigit():
        return int(s[pos])
    if use_words:
        for w, val in words.items():
            if s[pos:].startswith(w):
                return val
    return None


def calibration_value(s: str, use_words: bool):
    first = next(
        d for d in (digit_at(s, p, use_words) for p in range(len(s))) if d is not None
    )
    last = next(
        d
        for d in (digit_at(s, p, use_words) for p in range(len(s) - 1, -1, -1))
        if d is not None
    )
    return first * 10 + last


lines = list(filter(None, map(lambda x: x.strip(), open("1.txt", "r").readlines())))
# part 1
print(sum(calibration_value(line, use_words=False) for line in lines))
# part 2
print(sum(calibration_value(line, use_words=True) for line in lines))
