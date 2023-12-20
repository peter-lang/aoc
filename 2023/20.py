from collections import deque
from functools import partial, reduce
import math


ADR = int | None
STATE = list[bool] | bool | None


def parse_name(n: str):
    if n.startswith("&"):
        return "conjunction", n[1:]
    elif n.startswith("%"):
        return "flipflop", n[1:]
    else:
        return "broadcaster", n


lines = list(
    (parse_name(name), tuple(connections.split(", ")))
    for name, connections in map(
        lambda x: x.split(" -> "),
        filter(None, map(lambda x: x.strip(), open("20.txt", "r").readlines())),
    )
)

# broadcaster comes first
lines = sorted(lines)


def broadcast(
    sgn: bool, state: None, src: ADR, outs: list[ADR]
) -> tuple[bool, STATE, list[ADR]]:
    return sgn, state, outs


def flipflop(
    sgn: bool, state: bool, src: ADR, outs: list[ADR]
) -> tuple[bool, STATE, list[ADR]]:
    if sgn:
        return sgn, state, []
    else:
        state = not state
        return state, state, outs


def conjunction(
    sgn: bool, state: list[bool], src: int, outs: list[ADR], src2idx: dict[int, int]
) -> tuple[bool, STATE, list[ADR]]:
    state[src2idx[src]] = sgn
    return not all(state), state, outs


MODULES = []
name2idx: dict[str, int] = dict()
idx2type: dict[int, str] = dict()

conj2srcs: dict[str, list[int]] = dict()
for module_idx, ((module_type, name), _) in enumerate(lines):
    name2idx[name] = module_idx
    idx2type[module_idx] = module_type
    if module_type == "conjunction":
        conj2srcs[name] = []

rx_req = []
for module_idx, ((module_type, name), connections) in enumerate(lines):
    if "rx" in connections:
        rx_req.append(name)
        assert module_type == "conjunction", "rx parent is expected to be conjunction"
    for c in connections:
        if c in conj2srcs:
            conj2srcs[c].append(module_idx)

assert len(rx_req) <= 1
rx_req = [] if len(rx_req) == 0 else conj2srcs[rx_req[0]]


for (module_type, name), connections in lines:
    resolved_connections = list(name2idx.get(c, None) for c in connections)
    if module_type == "broadcaster":
        MODULES.append(partial(broadcast, outs=resolved_connections))
    elif module_type == "flipflop":
        MODULES.append(partial(flipflop, outs=resolved_connections))
    elif module_type == "conjunction":
        sources = conj2srcs[name]
        source_to_idx = {src: idx for idx, src in enumerate(sources)}
        MODULES.append(
            partial(conjunction, outs=resolved_connections, src2idx=source_to_idx)
        )


def initial_state() -> list[STATE]:
    result = []
    for (mod_type, name), _ in lines:
        if mod_type == "broadcaster":
            result.append(None)
        elif mod_type == "flipflop":
            result.append(False)
        elif mod_type == "conjunction":
            result.append([False] * len(conj2srcs[name]))
    return result


def process(modules, states: list[STATE], watching: list[int] | None):
    queue = deque([(False, None, 0)])

    if watching is not None:
        watch = [False] * len(watching)
        src2watch = {w: idx for idx, w in enumerate(watching)}
    else:
        watch = None
        src2watch = None

    sgn_hi = 0
    sgn_lo = 0
    while queue:
        sgn, src, dst = queue.popleft()
        if watching is not None and sgn and src in src2watch:
            watch[src2watch[src]] = True
        if sgn:
            sgn_hi += 1
        else:
            sgn_lo += 1

        if dst is None:
            continue

        sgn, states[dst], outs = modules[dst](sgn, states[dst], src)
        for out in outs:
            queue.append((sgn, dst, out))
    return sgn_hi, sgn_lo, watch


# part 1
states = initial_state()
total_hi, total_lo = 0, 0
for _ in range(1000):
    res = process(MODULES, states, None)
    total_hi += res[0]
    total_lo += res[1]
print(total_lo * total_hi)

# part 2
high_at_press = [[] for _ in rx_req]
states = initial_state()
total_presses = 0
while not all(len(mod) >= 3 for mod in high_at_press):
    _, _, rx_watch = process(MODULES, states, rx_req)
    total_presses += 1
    for req_idx, req_done in enumerate(rx_watch):
        if req_done:
            high_at_press[req_idx].append(total_presses)

assert all(
    all(d == hi[0] for d in (b - a for a, b in zip(hi[:-1], hi[1:])))
    for hi in high_at_press
)
mods = [hi[0] for hi in high_at_press]
print(reduce(lambda x, y: x * y // math.gcd(x, y), mods, 1))
