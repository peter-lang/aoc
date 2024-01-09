import intcode
from itertools import cycle

CODE = list(map(int, open("23.txt", "r").read().strip().split(",")))


def simulate_until_255():
    comps = [
        intcode.Computer(CODE).reset(inputs=[addr], non_block_value=-1)
        for addr in range(50)
    ]
    for comp in cycle(comps):
        res = comp.run_to_outputs(3, wait_at_most=50)
        if res is None:
            continue
        addr, x, y = res
        if addr == 255:
            return y
        comps[addr].inputs.extend([x, y])


# part 1
print(simulate_until_255())


def simulate_nat():
    comps = [
        intcode.Computer(CODE).reset(inputs=[addr], non_block_value=-1)
        for addr in range(50)
    ]
    nat_packets = None
    prev_nat_delivery = None
    while True:
        packet_sent = False
        for comp in comps:
            res = comp.run_to_outputs(3, wait_at_most=50)
            if res is None:
                continue
            packet_sent = True
            addr, x, y = res
            if addr == 255:
                nat_packets = (x, y)
            else:
                comps[addr].inputs.extend([x, y])
        if (
            not packet_sent
            and all(len(c.inputs) == 0 for c in comps)
            and nat_packets is not None
        ):
            comps[0].inputs.extend(nat_packets)
            if prev_nat_delivery is not None and prev_nat_delivery[1] == nat_packets[1]:
                return nat_packets[1]
            prev_nat_delivery = nat_packets
            nat_packets = None


# part 2
print(simulate_nat())
