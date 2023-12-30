NUMS = [0, 3, 1, 6, 7, 5]


def spoken_number(nums, idx):
    mem = {v: [idx] for idx, v in enumerate(nums)}

    turn = len(nums)
    prev = nums[-1]
    while turn < idx:
        if prev not in mem or len(mem[prev]) == 1:
            n = 0
        else:
            history = mem[prev]
            n = history[1] - history[0]
        if n not in mem:
            mem[n] = [turn]
        else:
            mem[n] = (mem[n] + [turn])[-2:]
        prev = n
        turn += 1
    return prev


# part 1
print(spoken_number(NUMS, 2020))

# part 2
print(spoken_number(NUMS, 30000000))
