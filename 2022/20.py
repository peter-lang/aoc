numbers = [
    int(line)
    for line in filter(None, map(lambda x: x.strip(), open("20.txt", "r").readlines()))
]


def move(perm: list[int], idx: int, step: int):
    if step > 0:
        n = (idx + step) % (len(perm) - 1)
    elif step < 0:
        n = (idx + step) % (len(perm) - 1)
        if n == 0:
            n = len(perm) - 1
    else:
        n = idx

    if n == idx:
        return
    if n > idx:
        tmp = perm[idx]
        perm[idx:n] = perm[(idx + 1) : (n + 1)]
        perm[n] = tmp
    else:
        tmp = perm[idx]
        perm[(n + 1) : (idx + 1)] = perm[n:idx]
        perm[n] = tmp


def mix(nums: list[int], cnt=1) -> list[int]:
    perm = list(range(len(nums)))
    for _ in range(cnt):
        for p_init, n in enumerate(nums):
            move(perm, perm.index(p_init), n)
    return perm


def apply(nums: list[int], perm: list[int]):
    return list(nums[p] for p in perm)


def groove_coords(nums: list[int]):
    i = nums.index(0)
    return sum(nums[(i + c) % len(nums)] for c in [1000, 2000, 3000])


# part 1
print(groove_coords(apply(numbers, mix(numbers))))

# part 2
decrypted = [811589153 * n for n in numbers]
print(groove_coords(apply(decrypted, mix(decrypted, 10))))
