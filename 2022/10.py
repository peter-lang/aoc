cycles = []
val = 1
for line in map(lambda x: x.strip(), open("10.txt", "r").readlines()):
    if line == "noop":
        cycles.append(val)
    else:
        cycles.append(val)
        cycles.append(val)
        val += int(line.split()[1])

# part 1
print(sum(idx * cycles[idx - 1] for idx in [20, 60, 100, 140, 180, 220]))

# part 2
for r in range(6):
    line = "".join(
        "#" if v <= pos <= v + 2 else " "
        for pos, v in ((idx + 1, cycles[r * 40 + idx]) for idx in range(40))
    )
    print(line)
