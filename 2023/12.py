from functools import cache

lines: list[str] = list(
    filter(None, map(lambda x: x.strip(), open("12.txt", "r").readlines()))
)

tasks = [
    (springs, tuple(map(int, symbols.split(","))))
    for springs, symbols in (line.split(" ") for line in lines)
]


@cache
def fits_group_fixed(group: str, symbols: tuple[int]) -> tuple[int, bool]:
    if len(symbols) == 0:
        if "#" in group:
            return 0, True
        else:
            return 1, True

    if len(group) < sum(symbols) + len(symbols) - 1:
        return 0, False

    char_cnt = symbols[0]
    if len(symbols) == 1:
        if len(group) < char_cnt:
            filled = 0, False
        else:
            filled = fits_group_fixed(group[char_cnt:], symbols[1:])
    else:
        if len(group) < char_cnt + 1:
            filled = 0, False
        elif group[char_cnt] == "?":
            filled = fits_group_fixed(group[(char_cnt + 1) :], symbols[1:])
        else:
            filled = 0, False

    if group[0] == "#":
        return filled
    else:
        unfilled = fits_group_fixed(group[1:], symbols)
        return filled[0] + unfilled[0], filled[1] or unfilled[1]


@cache
def fits_group(group: str, symbols: tuple[int]) -> list[tuple[int, int]]:
    results = []
    for parsed_sym_len in range(len(symbols) + 1):
        result, prefix_fit = fits_group_fixed(group, symbols[:parsed_sym_len])
        if not prefix_fit:
            return results
        else:
            results.append((parsed_sym_len, result))
    return results


@cache
def fits_groups(groups: tuple[str], symbols: tuple[int]) -> int:
    if len(groups) == 0:
        if len(symbols) == 0:
            return 1
        else:
            return 0

    if len(groups) == 1:
        result, _ = fits_group_fixed(groups[0], symbols)
        return result

    group = groups[0]
    results = 0
    for parsed_sym_len, result in fits_group(group, symbols):
        results += result * fits_groups(groups[1:], symbols[parsed_sym_len:])
    return results


def fits(line: str, symbols: tuple[int]) -> int:
    return fits_groups(tuple(filter(None, line.split("."))), symbols)


# part 1
print(sum(fits(springs, symbols) for springs, symbols in tasks))

# part 2
print(sum(fits("?".join([springs] * 5), symbols * 5) for springs, symbols in tasks))
