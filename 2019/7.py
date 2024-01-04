from itertools import permutations

code = list(map(int, open("7.txt", "r").read().strip().split(",")))


def int_code(arr, inputs, ip=0):
    while True:
        op = arr[ip]
        if op % 100 == 1:
            a, b, res = arr[ip + 1], arr[ip + 2], arr[ip + 3]
            a = a if (op // 100 % 10 == 1) else arr[a]
            b = b if (op // 1000 % 10 == 1) else arr[b]
            arr[res] = a + b
            ip += 4
        elif op % 100 == 2:
            a, b, res = arr[ip + 1], arr[ip + 2], arr[ip + 3]
            a = a if (op // 100 % 10 == 1) else arr[a]
            b = b if (op // 1000 % 10 == 1) else arr[b]
            arr[res] = a * b
            ip += 4
        elif op % 100 == 3:
            a = arr[ip + 1]
            arr[a] = next(inputs)
            ip += 2
        elif op % 100 == 4:
            a = arr[ip + 1]
            a = a if (op // 100 % 10 == 1) else arr[a]
            ip += 2
            return a, ip
        elif op % 100 == 5:
            a, b = arr[ip + 1], arr[ip + 2]
            a = a if (op // 100 % 10 == 1) else arr[a]
            b = b if (op // 1000 % 10 == 1) else arr[b]
            if a != 0:
                ip = b
            else:
                ip += 3
        elif op % 100 == 6:
            a, b = arr[ip + 1], arr[ip + 2]
            a = a if (op // 100 % 10 == 1) else arr[a]
            b = b if (op // 1000 % 10 == 1) else arr[b]
            if a == 0:
                ip = b
            else:
                ip += 3
        elif op % 100 == 7:
            a, b, res = arr[ip + 1], arr[ip + 2], arr[ip + 3]
            a = a if (op // 100 % 10 == 1) else arr[a]
            b = b if (op // 1000 % 10 == 1) else arr[b]
            arr[res] = 1 if a < b else 0
            ip += 4
        elif op % 100 == 8:
            a, b, res = arr[ip + 1], arr[ip + 2], arr[ip + 3]
            a = a if (op // 100 % 10 == 1) else arr[a]
            b = b if (op // 1000 % 10 == 1) else arr[b]
            arr[res] = 1 if a == b else 0
            ip += 4
        else:
            break
    return None


def thrust(sequence):
    res = 0
    for n in sequence:
        res, _ = int_code(list(code), iter([n, res]))
    return res


def thrust_feedback(sequence):
    res = 0
    res_e = 0
    states = [[s, list(code), 0] for s in sequence]
    idx = 0
    while True:
        state = states[idx % len(states)]
        if idx >= len(states):
            out = int_code(state[1], iter([res]), state[2])
        else:
            out = int_code(state[1], iter([state[0], res]), state[2])
        if out is None:
            return res_e
        res, ip = out
        if idx % len(states) == len(states) - 1:
            res_e = res
        state[2] = ip
        idx += 1


# part 1
print(max(thrust(seq) for seq in permutations(list(range(5)))))

# part 2
print(max(thrust_feedback(seq) for seq in permutations(list(range(5, 10)))))
