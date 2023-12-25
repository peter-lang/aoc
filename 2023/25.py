import numpy as np
from collections import deque

EDGE_LIST = {
    a: b.split(" ")
    for a, b in map(
        lambda x: x.split(": "),
        filter(None, map(lambda x: x.strip(), open("25.txt", "r").readlines())),
    )
}

ID2VERTEX = list(
    set(EDGE_LIST.keys())
    | set(ch for children in EDGE_LIST.values() for ch in children)
)
VERTEX2ID = {v: idx for idx, v in enumerate(ID2VERTEX)}


def edmonds_karp(s, t, expected_max_flow):
    adj_mx = np.zeros(shape=(len(ID2VERTEX), len(ID2VERTEX)), dtype=bool)
    for parent, children in EDGE_LIST.items():
        p_idx = VERTEX2ID[parent]
        for ch in children:
            ch_idx = VERTEX2ID[ch]
            adj_mx[p_idx, ch_idx] = True
            adj_mx[ch_idx, p_idx] = True

    def bfs(start):
        visited = [False] * len(ID2VERTEX)
        parent_of = [-1] * len(ID2VERTEX)

        queue = deque([start])
        visited[start] = True

        while queue:
            u = queue.popleft()
            for idx, v in enumerate(adj_mx[u]):
                if not visited[idx] and v:
                    queue.append(idx)
                    visited[idx] = True
                    parent_of[idx] = u

        return visited, parent_of

    max_flow = 0
    while True:
        vis, par = bfs(s)
        if not vis[t]:
            break
        max_flow += 1

        v = t
        while v != s:
            u = par[v]
            adj_mx[u, v] = False
            adj_mx[v, u] = True
            v = par[v]

    if max_flow == expected_max_flow:
        vis_s, _ = bfs(s)
        comp1_size = sum(vis_s)
        return comp1_size, len(ID2VERTEX) - comp1_size
    else:
        return None


for t in range(1, len(ID2VERTEX)):
    res = edmonds_karp(0, t, 3)
    if res is not None:
        print(res[0] * res[1])
        break
