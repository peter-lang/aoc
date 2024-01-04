from itertools import permutations
import intcode

code = list(map(int, open("7.txt", "r").read().strip().split(",")))
comp = intcode.Computer(code)


def thrust(sequence):
    res = 0
    for n in sequence:
        res = comp.reset().run_to_output(n, res)
    return res


def thrust_feedback(sequence):
    res = 0
    res_e = 0
    states = [(s, intcode.Computer(code).reset()) for s in sequence]
    idx = 0
    while True:
        amp_init, amp_comp = states[idx % len(states)]
        if idx < len(states):
            res = amp_comp.run_to_output(amp_init, res)
        else:
            res = amp_comp.run_to_output(res)
        if res is None:
            return res_e
        if idx % len(states) == len(states) - 1:
            res_e = res
        idx += 1


# part 1
print(max(thrust(seq) for seq in permutations(list(range(5)))))

# part 2
print(max(thrust_feedback(seq) for seq in permutations(list(range(5, 10)))))
