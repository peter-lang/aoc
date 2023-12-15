import pulp as pl
import numpy as np
import re
import sys

lines = list(filter(None, map(lambda x: x.strip(), open("16.txt", "r").readlines())))

pattern = re.compile(
    r"Valve (\S+) has flow rate=(\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)"
)

nodes = [
    (name, int(flow), neighbours.split(", "))
    for name, flow, neighbours in (pattern.match(line).groups() for line in lines)
]
nodes = sorted(nodes)
name2idx = {name: idx for idx, (name, _, _) in enumerate(nodes)}


def floyd_warshall():
    adjacency = np.full((len(nodes), len(nodes)), sys.maxsize // 2, dtype=int)
    for idx in range(len(nodes)):
        adjacency[idx, idx] = 0
        for n_idx in map(lambda x: name2idx[x], nodes[idx][2]):
            adjacency[idx, n_idx] = 1

    for k in range(len(nodes)):
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                updated_dist = adjacency[i, k] + adjacency[k, j]
                if adjacency[i, j] > updated_dist:
                    adjacency[i, j] = updated_dist

    return adjacency


DISTANCES = floyd_warshall()
assert nodes[name2idx["AA"]][1] == 0
FLOW_RATES = [flow for _, flow, _ in nodes if flow > 0]
poi = [name2idx["AA"]] + [idx for idx, (name, flow, _) in enumerate(nodes) if flow > 0]
DISTANCES = DISTANCES[poi, :][:, poi]


def part_1(distances, flow_rates, max_t):
    model = pl.LpProblem(sense=pl.LpMaximize)

    valves = [[] for _ in flow_rates]
    for idx, valve in enumerate(valves):
        init_dist = distances[0, idx + 1]
        for t in range(max_t):
            v = pl.LpVariable(f"v-{idx}-{t}", lowBound=0, upBound=1, cat=pl.LpInteger)
            valve.append(v)
            if t < init_dist:
                v.setInitialValue(0)
                v.fixValue()

    # a valve can be opened once
    for idx in range(len(flow_rates)):
        model += pl.lpSum(valves[idx][t] for t in range(max_t)) <= 1

    # if v1 opened at t1, v2 opened at t2, abs(t1 - t2) > dist
    for v1 in range(len(flow_rates)):
        for v2 in range(v1):
            dist = distances[v1 + 1, v2 + 1]
            for t1 in range(max_t - dist):
                model += (
                    pl.lpSum(
                        valves[v1][t1 + dt] + valves[v2][t1 + dt]
                        for dt in range(dist + 1)
                    )
                    <= 1
                )

    model += pl.lpSum(
        valves[idx][t] * flow * (max_t - t - 1)
        for idx, flow in enumerate(flow_rates)
        for t in range(max_t)
    )

    model.solve(pl.PULP_CBC_CMD(msg=0))
    return int(model.objective.value())


print(part_1(DISTANCES, FLOW_RATES, 30))


def part_2(distances, flow_rates, max_t, actors):
    model = pl.LpProblem(sense=pl.LpMaximize)

    valves = [[[] for v in flow_rates] for a in range(actors)]
    for a in range(actors):
        for idx, valve in enumerate(valves[a]):
            init_dist = distances[0, idx + 1]
            for t in range(max_t):
                v = pl.LpVariable(
                    f"v-{a}-{idx}-{t}", lowBound=0, upBound=1, cat=pl.LpInteger
                )
                valve.append(v)
                if t < init_dist:
                    v.setInitialValue(0)
                    v.fixValue()

    # a valve can be opened once
    for idx in range(len(flow_rates)):
        model += (
            pl.lpSum(valves[a][idx][t] for a in range(actors) for t in range(max_t))
            <= 1
        )

    # if v1 opened at t1, v2 opened at t2, abs(t1 - t2) > dist
    for a in range(actors):
        for v1 in range(len(flow_rates)):
            for v2 in range(v1):
                dist = distances[v1 + 1, v2 + 1]
                for t1 in range(max_t - dist):
                    model += (
                        pl.lpSum(
                            valves[a][v1][t1 + dt] + valves[a][v2][t1 + dt]
                            for dt in range(dist + 1)
                        )
                        <= 1
                    )

    model += pl.lpSum(
        valves[a][idx][t] * flow * (max_t - t - 1)
        for idx, flow in enumerate(flow_rates)
        for t in range(max_t)
        for a in range(actors)
    )

    model.solve(pl.PULP_CBC_CMD(msg=0))
    return int(model.objective.value())


print(part_2(DISTANCES, FLOW_RATES, 26, 2))
