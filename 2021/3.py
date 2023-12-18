from collections import Counter

lines = list(filter(None, map(lambda x: x.strip(), open("3.txt", "r").readlines())))

BIT_LEN = len(lines[0])


def most_common_value_at(idx: int, values: list[str]) -> str:
    common = Counter(v[idx] for v in values).most_common(2)
    return "1" if common[0][1] == common[1][1] else common[0][0]


def least_common_value_at(idx: int, values: list[str]) -> str:
    common = Counter(v[idx] for v in values).most_common(2)
    return "0" if common[0][1] == common[1][1] else common[1][0]


# part 1
gamma_rate = int("".join(most_common_value_at(i, lines) for i in range(BIT_LEN)), 2)
epsilon_rate = (1 << BIT_LEN) - 1 - gamma_rate
print(gamma_rate * epsilon_rate)


def filter_until_found(values: list[str], filter_by):
    for i in range(BIT_LEN):
        v = filter_by(i, values)
        values = list(filter(lambda c: c[i] == v, values))
        if len(values) == 1:
            return int(values[0], 2)


oxy_rate = filter_until_found(lines, most_common_value_at)
co2_rate = filter_until_found(lines, least_common_value_at)

# part 2
print(oxy_rate * co2_rate)
