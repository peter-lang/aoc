from typing import NamedTuple, Generator
from bisect import bisect

FILE = NamedTuple(
    "FILE",
    [
        ("parent", "FILE"),
        ("children", list["FILE"] | None),
        ("name", str),
        ("size", int),
    ],
)
root: FILE = FILE(None, [], "/", 0)
cwd = root
for line in map(lambda x: x.strip(), open("7.txt", "r").readlines()):
    parts = line.split()
    if parts[0] == "$":
        if parts[1] == "cd":
            if parts[2] == "/":
                cwd = root
            elif parts[2] == "..":
                cwd = cwd.parent
            else:
                cwd = next(ch for ch in cwd.children if ch.name == parts[2])
    elif parts[0] == "dir":
        cwd.children.append(FILE(cwd, [], parts[1], 0))
    else:
        cwd.children.append(FILE(cwd, None, parts[1], int(parts[0])))


def traverse_dirs(r: FILE) -> Generator[tuple[int, str], None, int]:
    if r.children is None:
        return r.size
    else:
        total = 0
        for ch in r.children:
            total += yield from traverse_dirs(ch)
        yield total, r.name
        return total


dirs = sorted(traverse_dirs(root))


# part 1
idx = bisect(dirs, (100000,))
print(sum(size for size, name in dirs[:idx]))

# part 2
UNUSED = 70000000 - dirs[-1][0]
DELETE = 30000000 - UNUSED
idx = bisect(dirs, (DELETE,))
print(dirs[idx][0])
