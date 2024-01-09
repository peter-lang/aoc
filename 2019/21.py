import intcode
import random

CODE = list(map(int, open("21.txt", "r").read().strip().split(",")))

comp = intcode.Computer(CODE)


def run_code(instructions):
    inputs = []
    for inst in instructions:
        inputs.extend(map(ord, inst))
        inputs.append(ord("\n"))
    comp.reset(inputs)
    last_out = None
    while (out := comp.run_to_output()) is not None:
        last_out = out
    return last_out


# part 1
print(run_code(["NOT C J", "NOT A T", "OR T J", "AND D J", "WALK"]))

# part 2
print(
    run_code(
        [
            "OR H T",
            "NOT C T",
            "OR T J",
            "NOT B J",
            "AND D J",
            "OR T J",
            "AND E T",
            "AND H J",
            # BEFORE: result of random search
            # AFTER: reasonable assumptions
            "NOT A T",
            "OR T J",
            "AND D J",
            "RUN",
        ]
    )
)


# I have no idea why part 2 works. I saw jumps are not consistent when running,
# my guess was if it ran before jumps, it jumped longer. I've implemented a
# state-machine, but that did not work. At that point, I had enough.


def random_search():
    def generate_seq(max_len):
        length = random.randint(1, max_len)
        for _ in range(length):
            op = random.choice(["NOT", "OR", "AND"])
            ro = random.choice(["B", "C", "D", "E", "F", "G", "H", "T"])
            wr = random.choice(["T", "J"])
            yield f"{op} {ro} {wr}"

    def run():
        seq = list(generate_seq(10)) + ["NOT A T", "OR T J", "AND D J", "RUN"]
        return run_code(seq), seq

    while (res := run())[0] < 255:
        pass
    return res
