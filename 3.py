from functools import reduce
import numpy as np

lines: list[str] = list(filter(None, map(lambda x: x.strip(), open("3.txt", "r").readlines())))

symbols: list[tuple[int, int]] = []
stars: list[tuple[int, int]] = []
numbers: list[list[tuple[int, int]]] = []
num_values: list[int] = []


def to_val(num_idx: list[tuple[int, int]], chars: str) -> int:
    return reduce(lambda acc, el: 10 * acc + int(chars[el[1]]), num_idx, 0)


num_arr = []
for row, line in enumerate(lines):
    for col, ch in enumerate(line):
        if ch.isdigit():
            num_arr.append((row, col))
        else:
            if num_arr:
                numbers.append(num_arr)
                num_values.append(to_val(num_arr, line))
                num_arr = []
            if ch != '.':
                if ch == '*':
                    stars.append((row, col))
                symbols.append((row, col))
    if num_arr:
        numbers.append(num_arr)
        num_values.append(to_val(num_arr, line))
        num_arr = []

# pad numbers to same length
max_nums_len = max(len(nums) for nums in numbers)
numbers = [nums + [(-1, -1)] * (max_nums_len - len(nums)) for nums in numbers]

#########
# NUMPY #
#########

numbers_np = np.expand_dims(np.array(numbers, dtype=np.int16), axis=0)
symbols_np = np.expand_dims(np.array(symbols, dtype=np.int16), axis=(1, 2))
stars_np = np.expand_dims(np.array(stars, dtype=np.int16), axis=(1, 2))

# part 1
dists_p1 = np.abs(numbers_np - symbols_np).max(axis=3).min(axis=(0, 2))
parts = np.squeeze(np.argwhere(dists_p1 == 1))
print(sum(num_values[idx] for idx in parts))

# part 2
dists_from_stars = np.abs(numbers_np - stars_np).max(axis=3).min(axis=2)
dists_from_stars_1 = np.expand_dims(dists_from_stars, axis=1)
dists_from_stars_2 = np.expand_dims(dists_from_stars, axis=2)
max_dists = np.maximum(dists_from_stars_1, dists_from_stars_2).min(axis=0)

# remove duplicates and self-pairs
max_dists[np.tril_indices_from(max_dists)] = 0

gear_pairs = np.argwhere(max_dists == 1)

print(sum(num_values[a] * num_values[b] for a, b in gear_pairs))

###############
# TORCH - MPS #
###############
#
# import torch
#
# numbers_t = torch.reshape(torch.tensor(numbers, device="mps", dtype=torch.int16), shape=(1, len(numbers), max_nums_len, 2))
# symbols_t = torch.reshape(torch.tensor(symbols, device="mps", dtype=torch.int16), shape=(len(symbols), 1, 1, 2))
# stars_t = torch.reshape(torch.tensor(stars, device="mps", dtype=torch.int16), shape=(len(stars), 1, 1, 2))
#
# # part 1
# dists_p1 = torch.min(torch.min(torch.max(torch.abs(numbers_t - symbols_t), dim=3).values, dim=2).values, dim=0).values
# parts = torch.squeeze(torch.argwhere(dists_p1 == torch.ones_like(dists_p1, device="mps", dtype=torch.int16))).cpu().numpy()
#
# print(sum(num_values[idx] for idx in parts))
#
# # part 2
# dists_from_stars = torch.min(torch.max(torch.abs(numbers_t - symbols_t), dim=3).values, dim=2).values
# dists_from_stars_1 = torch.reshape(dists_from_stars, shape=(len(symbols), 1, len(numbers)))
# dists_from_stars_2 = torch.reshape(dists_from_stars, shape=(len(symbols), len(numbers), 1))
# max_dists = torch.min(torch.maximum(dists_from_stars_1, dists_from_stars_2), dim=0).values
#
# # remove duplicates and self-pairs
# max_dists = torch.triu(max_dists, diagonal=1)
#
# gear_pairs = torch.argwhere(max_dists == torch.ones_like(max_dists, device="mps", dtype=torch.int16)).cpu().numpy()
# print(sum(num_values[a] * num_values[b] for a, b in gear_pairs))
