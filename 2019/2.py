code = list(map(int, open("2.txt", "r").read().strip().split(",")))


def int_code(arr):
    idx = 0
    while idx + 3 < len(arr) and arr[idx] in (1, 2):
        a, b, res = arr[idx + 1], arr[idx + 2], arr[idx + 3]
        if arr[idx] == 1:
            arr[res] = arr[a] + arr[b]
        else:
            arr[res] = arr[a] * arr[b]
        idx += 4
    return arr


def execute(arr, a, b):
    prog = list(arr)
    prog[1] = a
    prog[2] = b
    prog = int_code(prog)
    return prog[0]


# part 1
print(execute(code, 12, 2))

# part 2
print(
    next(
        100 * noun + verb
        for noun in range(100)
        for verb in range(100)
        if execute(code, noun, verb) == 19690720
    )
)
