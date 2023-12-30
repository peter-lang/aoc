INSTRUCTIONS = list(
    map(
        lambda x: (x[:3], int(x[4:])),
        filter(None, map(lambda x: x.strip(), open("8.txt", "r").readlines())),
    )
)


def run(code):
    visited = set()
    ip = 0
    acc = 0
    while ip < len(code) and ip not in visited:
        visited.add(ip)
        if code[ip][0] == "jmp":
            ip += code[ip][1]
        else:
            if code[ip][0] == "acc":
                acc += code[ip][1]
            ip += 1
    return acc, ip == len(code)


def try_change_until_success():
    for idx in range(len(INSTRUCTIONS) - 1, -1, -1):
        ins, cnt = INSTRUCTIONS[idx]
        if ins not in ("jmp", "nop"):
            continue
        mod_ins = "jmp" if ins == "nop" else "nop"
        modified = INSTRUCTIONS[:idx] + [(mod_ins, cnt)] + INSTRUCTIONS[(idx + 1) :]
        result, success = run(modified)
        if success:
            return result


# part 1
print(run(INSTRUCTIONS)[0])

# part 2
print(try_change_until_success())
