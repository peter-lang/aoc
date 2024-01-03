def move(order, times):
    # convert to zero indexed
    right_neighbour = [-1] * len(order)
    for a, b in zip(order[:-1], order[1:]):
        right_neighbour[a - 1] = b - 1
    right_neighbour[order[-1] - 1] = order[0] - 1
    current = order[0] - 1
    assert all(n >= 0 for n in right_neighbour)

    for _ in range(times):
        # first three next to current (x, y, z)
        x = right_neighbour[current]
        y = right_neighbour[x]
        z = right_neighbour[y]

        # select destination
        dst = (current - 1) % len(right_neighbour)
        while dst in (x, y, z):
            dst = (dst - 1) % len(right_neighbour)

        # after the first
        next_cup = right_neighbour[z]
        right_neighbour[current] = next_cup

        dst_next = right_neighbour[dst]
        right_neighbour[dst] = x
        right_neighbour[z] = dst_next
        current = next_cup
    return right_neighbour


def after(cups, val, length):
    res = []
    for i in range(length):
        next_val = cups[val]
        res.append(next_val)
        val = next_val
    return res


CUPS = [3, 8, 9, 1, 2, 5, 4, 6, 7]

# part 1
print("".join(str(d + 1) for d in after(move(CUPS, 100), 0, len(CUPS) - 1)))

# part 2
r0, r1 = (
    d + 1
    for d in after(move(CUPS + list(range(len(CUPS) + 1, 1000001)), 10000000), 0, 2)
)
print(r0 * r1)
