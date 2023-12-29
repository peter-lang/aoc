import math

dec_fb = {"F": "0", "B": "1"}
dec_lr = {"L": "0", "R": "1"}


def parse(space_txt: str):
    row = int("".join(dec_fb[ch] for ch in space_txt[:7]), 2)
    col = int("".join(dec_lr[ch] for ch in space_txt[7:]), 2)
    return row * 8 + col


min_val = math.inf
max_val = -math.inf
total = 0
for line in filter(None, map(lambda x: x.strip(), open("5.txt", "r").readlines())):
    seat = parse(line)
    total += seat
    if seat < min_val:
        min_val = seat
    if seat > max_val:
        max_val = seat

# part 1
print(max_val)

# part 2
expected_total = max_val * (max_val + 1) // 2 - min_val * (min_val - 1) // 2
print(expected_total - total)
