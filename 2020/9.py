def all_pairs(nums):
    for idx, a in enumerate(nums):
        for b in nums[:idx]:
            yield a, b


NUMS = list(
    map(int, filter(None, map(lambda x: x.strip(), open("9.txt", "r").readlines())))
)


def first_invalid(nums, preamble_len):
    for idx in range(preamble_len, len(nums)):
        if nums[idx] not in set(
            a + b for a, b in all_pairs(nums[(idx - preamble_len) : idx])
        ):
            return nums[idx]


def find_interval_sum_equals(nums, expected):
    a, b = 0, 2
    acc = sum(nums[a:b])
    while b < len(nums):
        if acc < expected:
            acc += nums[b]
            b += 1
        elif acc > expected:
            if b == a + 2:
                acc += nums[b]
                b += 1
            acc -= nums[a]
            a += 1
        else:
            return a, b
    return None


# part 1
invalid = first_invalid(NUMS, 25)
print(invalid)

# part 2
s, e = find_interval_sum_equals(NUMS, invalid)
print(min(NUMS[s:e]) + max(NUMS[s:e]))
