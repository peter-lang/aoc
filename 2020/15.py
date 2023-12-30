NUMS = [0, 3, 1, 6, 7, 5]


def spoken_number(nums, idx):
    # we don't need the last value, as it would be read as first prev value during for-loop
    mem = {v: idx for idx, v in enumerate(nums[:-1])}

    prev = nums[-1]
    for turn in range(len(nums), idx):
        if prev not in mem:
            n = 0
        else:
            # we know that prev was last said at (turn-1), mem[prev] stores the second to last turn
            n = turn - 1 - mem[prev]
        # update mem[prev] to its last turn, AFTER it has been read
        # so during next read (after it has been spoken), it will contain second to last turn
        mem[prev] = turn - 1
        prev = n
    return prev


# part 1
print(spoken_number(NUMS, 2020))

# part 2
print(spoken_number(NUMS, 30000000))
