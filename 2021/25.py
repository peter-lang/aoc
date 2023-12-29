right = set()
down = set()

lines = list(filter(None, map(lambda x: x.strip(), open("25.txt", "r").readlines())))
for r, line in enumerate(lines):
    for c, ch in enumerate(line):
        if ch == ">":
            right.add((r, c))
        elif ch == "v":
            down.add((r, c))
MAX_ROW = len(lines)
MAX_COL = len(lines[0])

step = 0
moved = True
while moved:
    step += 1
    moved = False
    tmp = set()
    for n in right:
        ch = (n[0], (n[1] + 1) % MAX_COL)
        if ch in right or ch in down:
            tmp.add(n)
        else:
            tmp.add(ch)
            moved = True
    right = tmp
    tmp = set()
    for n in down:
        ch = ((n[0] + 1) % MAX_ROW, n[1])
        if ch in right or ch in down:
            tmp.add(n)
        else:
            tmp.add(ch)
            moved = True
    down = tmp

print(step)
