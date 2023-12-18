numbers = list(
    map(int, filter(None, map(lambda x: x.strip(), open("1.txt", "r").readlines())))
)

# part 1
print(sum(a < b for a, b in zip(numbers[:-1], numbers[1:])))

# part 2
print(sum(a < b for a, b in zip(numbers[:-3], numbers[3:])))
