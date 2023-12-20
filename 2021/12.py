from typing import Iterator

edges = [
    tuple(line.split("-"))
    for line in filter(None, map(lambda x: x.strip(), open("12.txt", "r").readlines()))
]

edge_list = {**{a: set() for a, _ in edges}, **{b: set() for _, b in edges}}
for a, b in edges:
    edge_list[a].add(b)
    edge_list[b].add(a)


def dfs(path: tuple, visited: set, can_visit_twice: bool) -> Iterator[tuple]:
    for n in edge_list[path[-1]]:
        if n == "end":
            yield path + (n,)
        elif n.isupper():
            yield from dfs(path + (n,), visited, can_visit_twice)
        elif n not in visited:
            yield from dfs(path + (n,), visited | {n}, can_visit_twice)
        elif n != "start" and can_visit_twice:
            yield from dfs(path + (n,), visited, False)


# part 1
print(len(list(dfs(("start",), {"start"}, False))))

# part 2
print(len(list(dfs(("start",), {"start"}, True))))
