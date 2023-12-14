elf: list[int] = []
elves = []
for line in map(lambda x: x.strip(), open("1.txt", "r").readlines()):
    if elf and not line:
        elves.append(elf)
        elf = []
    else:
        elf.append(int(line))
if elf:
    elves.append(elf)

# part 1
print(max(sum(e) for e in elves))

# part 2
print(sum(sorted(sum(e) for e in elves)[-3:]))
