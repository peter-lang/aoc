from collections import Counter
from functools import cache

lines = filter(None, map(lambda x: x.strip(), open("10.txt", "r").readlines()))
nums = sorted(list(map(int, lines)))
nums = [0] + nums + [nums[-1] + 3]


@cache
def all_paths_from(idx):
    if idx == len(nums) - 1:
        return 1
    n = idx + 1
    total = 0
    while n < len(nums) and (nums[n] - nums[idx]) <= 3:
        total += all_paths_from(n)
        n += 1
    return total


cnt = Counter(b - a for a, b in zip(nums[:-1], nums[1:]))
print(cnt[1] * cnt[3])

print(all_paths_from(0))
