import re
from itertools import product

lines = list(filter(None, map(lambda x: x.strip(), open("14.txt", "r").readlines())))

mem_pattern = re.compile(r"mem\[(\d+)] = (\d+)")


def possible_values(bits, value):
    for bit_set_values in product([False, True], repeat=len(bits)):
        res = value
        for bit_idx, bit_set in zip(bits, bit_set_values):
            if bit_set:
                res |= 1 << bit_idx
            else:
                res &= ~(1 << bit_idx)
        yield res


# part 1
mem = dict()
for line in lines:
    if line.startswith("mask = "):
        mask_or = int(line[7:].replace("X", "0"), 2)
        mask_and = int(line[7:].replace("X", "1"), 2)
    else:
        m = mem_pattern.match(line)
        pos, val = int(m.group(1)), int(m.group(2))
        mem[pos] = (val | mask_or) & mask_and
print(sum(mem.values()))

# part 2
mem = dict()
for line in lines:
    if line.startswith("mask = "):
        mask_or = int(line[7:].replace("X", "0"), 2)
        floating_bits = [idx for idx, ch in enumerate(reversed(line[7:])) if ch == "X"]
    else:
        m = mem_pattern.match(line)
        pos, val = int(m.group(1)), int(m.group(2))
        for v in possible_values(floating_bits, pos):
            mem[v | mask_or] = val
print(sum(mem.values()))
