code = list(map(int, open("5.txt", "r").read().strip().split(",")))


def int_code(arr, inputs):
    ip = 0
    output = None
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
            output = a
            ip += 2
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
    return output


# part 1
print(int_code(list(code), iter([1])))

# part 2
print(int_code(list(code), iter([5])))
