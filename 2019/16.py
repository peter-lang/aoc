import numpy as np
import math

nums = list(map(int, open("16.txt", "r").read().strip()))


def phase(n, times):
    def create_mx(size):
        result = np.zeros(shape=(size, size), dtype=int)
        pattern = np.array([0, 1, 0, -1], dtype=int)
        for i in range(size):
            p = pattern.repeat(i + 1)
            p[:-1] = p[1:]
            p[-1] = 0
            result[i, :] = np.tile(p, math.ceil(size / p.shape[0]))[:size]
        return result

    v = np.array(n, dtype=int)
    mx = create_mx(v.shape[0])
    for _ in range(times):
        v = np.abs(mx @ v) % 10
    return v


# part 1
print("".join(str(d) for d in phase(nums, 100)[:8]))

# part 2
# For 6.5 million numbers this approach won't work, but if we check the matrix
# we can see that a digit's value only depends on the same and later digits.
# Because we are only interested in digits after a large offset,
# this means we can ignore all digits before the offset.
# The offset is larger than half the number of digits, which means, we need to simply
# add up all the digits till the end for all digits.
# We can reuse previous computation if we do it reverse, as the last digit would be itself
# and all the previous ones are itself plus the next one.
offset = int("".join(str(d) for d in nums[:7]))
total_length = len(nums) * 10000
assert offset > total_length // 2

tail = [nums[i % len(nums)] for i in range(offset, total_length)]
for _ in range(100):
    for idx in range(len(tail) - 2, -1, -1):
        tail[idx] = (tail[idx] + tail[idx + 1]) % 10
print("".join(str(d) for d in tail[:8]))
