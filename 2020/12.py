import numpy as np

lines = filter(None, map(lambda x: x.strip(), open("12.txt", "r").readlines()))
instructions = list(map(lambda x: (x[0], int(x[1:])), lines))

left, right, up, down = (
    np.array([-1, 0]),
    np.array([1, 0]),
    np.array([0, 1]),
    np.array([0, -1]),
)

rotation = [
    np.array([[1, 0], [0, 1]]),
    np.array([[0, 1], [-1, 0]]),
    np.array([[-1, 0], [0, -1]]),
    np.array([[0, -1], [1, 0]]),
]


def move_1(state: tuple[np.array, int], inst: tuple[str, int]) -> tuple[np.array, int]:
    action, value = inst
    if action == "F":
        if state[1] == 0:  # 0 => left
            return state[0] + left * value, state[1]
        elif state[1] == 1:  # 1 => up
            return state[0] + up * value, state[1]
        elif state[1] == 2:  # 2 => right
            return state[0] + right * value, state[1]
        else:  # state[1] == 3  # 3 => down
            return state[0] + down * value, state[1]
    elif action == "R":
        return state[0], (state[1] + value // 90) % 4
    elif action == "L":
        return state[0], (state[1] - value // 90) % 4
    elif action == "N":
        return state[0] + up * value, state[1]
    elif action == "S":
        return state[0] + down * value, state[1]
    elif action == "E":
        return state[0] + right * value, state[1]
    elif action == "W":
        return state[0] + left * value, state[1]


def move_2(
    state: np.array, waypoint: np.array, inst: tuple[str, int]
) -> tuple[np.array, np.array]:
    action, value = inst
    if action == "F":
        return state + value * waypoint, waypoint
    elif action == "R":
        return state, rotation[(value // 90) % 4] @ waypoint
    elif action == "L":
        return state, rotation[(-value // 90) % 4] @ waypoint
    elif action == "N":
        return state, waypoint + up * value
    elif action == "S":
        return state, waypoint + down * value
    elif action == "E":
        return state, waypoint + right * value
    elif action == "W":
        return state, waypoint + left * value


# part 1
pos = (np.array([0, 0]), 2)
for instruction in instructions:
    pos = move_1(pos, instruction)
print(np.abs(pos[0]).sum())

# part 2
pos = np.array([0, 0])
wp = 10 * right + 1 * up
for instruction in instructions:
    pos, wp = move_2(pos, wp, instruction)
print(np.abs(pos).sum())
