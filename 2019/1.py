numbers = list(
    map(int, filter(None, map(lambda x: x.strip(), open("1.txt", "r").readlines())))
)

# part 1
print(sum(n // 3 - 2 for n in numbers))


def fuel_req(n):
    total = 0
    req = n // 3 - 2
    while req > 0:
        total += req
        req = req // 3 - 2
    return total


# part 2
print(sum(fuel_req(n) for n in numbers))
