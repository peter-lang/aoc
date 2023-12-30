from functools import reduce


def split_lines_by_empty(lines):
    result = []
    for line in lines:
        if line:
            result.append(line)
        elif result:
            yield result
            result = []
    if result:
        yield result


groups = list(
    split_lines_by_empty(map(lambda x: x.strip(), open("6.txt", "r").readlines()))
)

# part 1
print(sum(len(reduce(set.union, map(set, group))) for group in groups))

# part 2
print(sum(len(reduce(set.intersection, map(set, group))) for group in groups))
