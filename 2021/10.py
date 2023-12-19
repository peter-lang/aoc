lines = list(filter(None, map(lambda x: x.strip(), open("10.txt", "r").readlines())))


def validating(s):
    cnt = [0, 0, 0, 0]
    stacks = [[], [], [], []]
    decoder = {
        "(": (0, False),
        ")": (0, True),
        "[": (1, False),
        "]": (1, True),
        "{": (2, False),
        "}": (2, True),
        "<": (3, False),
        ">": (3, True),
    }
    for idx, ch in enumerate(s):
        stack_idx, closing = decoder[ch]
        stack = stacks[stack_idx]
        if closing:
            if len(stack) == 0:
                return idx
            prev = stack.pop()
            if prev != tuple(cnt):
                return idx
            cnt[stack_idx] -= 1
            if any(c < 0 for c in cnt):
                return idx
        else:
            cnt[stack_idx] += 1
            stack.append(tuple(cnt))
    return cnt, stacks


def invalid_score(s):
    score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    res = validating(s)
    if isinstance(res, int):
        return score[s[res]]
    return 0


def find_stack_with_count(stacks, cnt):
    for idx, st in enumerate(stacks):
        if st and st[-1] == cnt:
            return idx


def autocomplete_score(s):
    res = validating(s)
    if isinstance(res, int):
        return 0
    cnt, stacks = res
    score = 0
    while tuple(cnt) != (0, 0, 0, 0):
        stack_idx = find_stack_with_count(stacks, tuple(cnt))
        stacks[stack_idx].pop()
        cnt[stack_idx] -= 1
        score = 5 * score + stack_idx + 1
    return score


# part 1
print(sum(invalid_score(line) for line in lines))

# part 2
scores = sorted(filter(None, (autocomplete_score(line) for line in lines)))
print(scores[(len(scores) - 1) // 2])
