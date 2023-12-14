import re

order_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
buffer: list[str] = []
starting_stacks: list[list[str]] = None
orders: list[tuple[int, int, int]] = []
for line in open("5.txt", "r").readlines():
    if line and not line.isspace():
        if starting_stacks is None:
            buffer.append(line)
        else:
            m = order_pattern.match(line)
            orders.append((int(m.group(1)), int(m.group(2)) - 1, int(m.group(3)) - 1))
    elif buffer:
        stack_names = list(map(int, buffer[-1].split()))
        starting_stacks = [[] for _ in stack_names]
        for b in reversed(buffer[:-1]):
            for i in range(len(stack_names)):
                idx = 1 + i * 4
                ch = b[idx] if idx < len(b) else " "
                if ch.isalpha():
                    starting_stacks[i].append(ch)


def execute_moves(
    stacks: list[list[str]], moves: list[tuple[int, int, int]], reverse: bool
):
    for cnt, from_idx, to_idx in moves:
        top = stacks[from_idx][-cnt:]
        if reverse:
            top = reversed(top)
        stacks[to_idx] += top
        stacks[from_idx] = stacks[from_idx][:-cnt]


# part 1
part_1 = list(list(s) for s in starting_stacks)
execute_moves(part_1, orders, True)
print("".join(p[-1] for p in part_1))

# part 2
part_2 = list(list(s) for s in starting_stacks)
execute_moves(part_2, orders, False)
print("".join(p[-1] for p in part_2))
