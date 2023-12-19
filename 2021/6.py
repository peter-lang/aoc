from collections import Counter

cnt = Counter(map(int, open("6.txt", "r").read().strip().split(",")))
INITIAL_STATE = tuple(cnt[i] for i in range(9))


def evolve(state, steps):
    for _ in range(steps):
        state = tuple(
            v + state[0] if idx == 6 else v for idx, v in enumerate(state[1:])
        ) + (state[0],)
    return state


# part 1
print(sum(evolve(INITIAL_STATE, 80)))

# part 2
print(sum(evolve(INITIAL_STATE, 256)))
