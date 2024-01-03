min_range = 240298
max_range = 784956


def to_digits(num):
    return list(map(int, str(num)))


def criteria_1(pwd):
    return all(a <= b for a, b in zip(pwd[:-1], pwd[1:])) and any(
        a == b for a, b in zip(pwd[:-1], pwd[1:])
    )


def criteria_2(pwd):
    return all(a <= b for a, b in zip(pwd[:-1], pwd[1:])) and (
        pwd[0] == pwd[1]
        and pwd[1] != pwd[2]
        or pwd[-1] == pwd[-2]
        and pwd[-2] != pwd[-3]
        or any(
            b == c and a != b and c != d
            for a, b, c, d in zip(pwd[:-3], pwd[1:-2], pwd[2:-1], pwd[3:])
        )
    )


# part 1
print(sum(criteria_1(to_digits(num)) for num in range(min_range, max_range + 1)))

# part 2
print(sum(criteria_2(to_digits(num)) for num in range(min_range, max_range + 1)))
