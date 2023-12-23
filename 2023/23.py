from typing import Iterator
import math
import pulp as pl

board = list(filter(None, map(lambda x: x.strip(), open("23.txt", "r").readlines())))

MAX_ROW = len(board)
MAX_COL = len(board[0])
START = (0, 1)
END = (MAX_ROW - 1, MAX_COL - 2)

NODE = tuple[int, int]


def neighbours(n) -> Iterator[NODE]:
    if n[0] > 0:
        yield n[0] - 1, n[1]
    if n[0] < MAX_ROW - 1:
        yield n[0] + 1, n[1]
    if n[1] > 0:
        yield n[0], n[1] - 1
    if n[1] < MAX_COL - 1:
        yield n[0], n[1] + 1


def slope_valid(p: NODE, ch: NODE) -> bool:
    if board[p[0]][p[1]] == "<":
        return ch == (p[0], p[1] - 1)
    elif board[p[0]][p[1]] == ">":
        return ch == (p[0], p[1] + 1)
    elif board[p[0]][p[1]] == "v":
        return ch == (p[0] + 1, p[1])
    elif board[p[0]][p[1]] == "^":
        return ch == (p[0] - 1, p[1])
    else:
        return True


def valid_children(p: NODE, check_slope: bool, prev: NODE | None) -> list[NODE]:
    result = []
    for ch in neighbours(p):
        if (
            board[ch[0]][ch[1]] != "#"
            and (not check_slope or slope_valid(p, ch))
            and (prev is None or ch != prev)
        ):
            result.append(ch)
    return result


def next_nodes(p: NODE, check_slope: bool) -> list[tuple[NODE, int]]:
    result = []
    path_starts = valid_children(p, check_slope, None)
    for path_start in path_starts:
        children = None
        curr, prev, weight = path_start, p, 1
        while (
            curr not in (START, END)
            and len((children := valid_children(curr, check_slope, prev))) == 1
        ):
            curr, prev, weight = children[0], curr, weight + 1
        if curr in (START, END) or children:
            result.append((curr, weight))
    return result


def create_reduced_graph(check_slope: bool) -> dict[NODE, list[tuple[NODE, int]]]:
    open_set = {START}
    result = dict()
    while open_set:
        node = open_set.pop()
        children = next_nodes(node, check_slope)
        result[node] = children
        open_set.update((ch for ch, _ in children if ch not in result))
    return result


def longest_path_from(
    node: NODE, visited: set[NODE], graph: dict[NODE, list[tuple[NODE, int]]]
) -> int:
    if node == END:
        return 0
    return max(
        (
            longest_path_from(child, visited | {node}, graph) + weight
            for child, weight in graph[node]
            if child not in visited
        ),
        default=-math.inf,
    )


def longest_path_ip(graph: dict[NODE, list[tuple[NODE, int]]]) -> int:
    model = pl.LpProblem(sense=pl.LpMaximize)
    edge2weight: dict[tuple[NODE, NODE], int] = dict()

    # deg_in, deg_out ensures that nodes are visited at most once
    # ordering ensures that edges make a single continuous path
    node_deg_out = dict()
    node_deg_in = dict()
    node_order = dict()
    for node in graph:
        node_deg_out[node] = pl.LpVariable(
            f"in({node[0]},{node[1]})", lowBound=0, upBound=1, cat=pl.LpInteger
        )
        node_deg_in[node] = pl.LpVariable(
            f"out({node[0]},{node[1]})", lowBound=0, upBound=1, cat=pl.LpInteger
        )
        node_order[node] = pl.LpVariable(
            f"order({node[0]},{node[1]})",
            lowBound=0,
            upBound=len(graph) - 1,
            cat=pl.LpInteger,
        )

    # fix start-end nodes
    node_order[START].setInitialValue(0)
    node_order[START].fixValue()
    node_deg_out[START].setInitialValue(1)
    node_deg_out[START].fixValue()
    node_deg_in[START].setInitialValue(0)
    node_deg_in[START].fixValue()

    node_deg_out[END].setInitialValue(0)
    node_deg_out[END].fixValue()
    node_deg_in[END].setInitialValue(1)
    node_deg_in[END].fixValue()

    # add edges
    edges = dict()
    edges_by_start = dict()
    edges_by_end = dict()
    for start, children in graph.items():
        edges_by_start[start] = []
        for end, weight in children:
            edge = (start, end)
            edges_by_start[start].append(edge)
            if end in edges_by_end:
                edges_by_end[end].append(edge)
            else:
                edges_by_end[end] = [edge]
            edges[edge] = edge_var = pl.LpVariable(
                f"({start[0]},{start[1]})-({end[0]},{end[1]})",
                lowBound=0,
                upBound=1,
                cat=pl.LpInteger,
            )

            edge2weight[edge] = weight

            # if there is an edge, the order needs to increase by 1
            # if there is no edge, the last part makes sure this is always true, independent of order
            order_end = node_order[end]
            order_start = node_order[start]
            model += order_end <= order_start + 1 - len(graph) * (edge_var - 1)
            model += order_end >= order_start + 1 + len(graph) * (edge_var - 1)

    # inner nodes must have the same in/out degree
    for node in graph:
        if node not in (START, END):
            model += node_deg_out[node] == node_deg_in[node]

    # deg_out = number of edges starting from node
    for start, start_edges in edges_by_start.items():
        model += node_deg_out[start] == pl.lpSum(edges[e] for e in start_edges)
    # deg_in = number of edges ending at node
    for end, end_edges in edges_by_end.items():
        model += node_deg_in[end] == pl.lpSum(edges[e] for e in end_edges)

    model += pl.lpSum(edges[e] * edge2weight[e] for e in edges)
    model.solve(pl.PULP_CBC_CMD(msg=0))
    return int(model.objective.value())


# part 1
print(longest_path_ip(create_reduced_graph(True)))
# print(longest_path_from(START, set(), create_reduced_graph(True)))

# part 2
print(longest_path_ip(create_reduced_graph(False)))
# print(longest_path_from(START, set(), create_reduced_graph(False)))
