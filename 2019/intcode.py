from collections import deque


class WaitForInput(Exception):
    pass


class Stopped(Exception):
    pass


class Computer:
    def __init__(self, code):
        self.code = code
        self.memory = None
        self.inputs = None
        self.outputs = None
        self.non_block_value = None
        self.ip = None
        self.rel_base = None

    def reset(self, inputs=None, non_block_value=None):
        self.memory = list(self.code)
        self.inputs = deque([] if inputs is None else inputs)
        self.outputs = deque([])
        self.non_block_value = non_block_value
        self.ip = 0
        self.rel_base = 0
        return self

    def p_val(self, idx):
        mode = (self.memory[self.ip] // (10 ** (idx + 1))) % 10
        p = self.memory[self.ip + idx]
        if mode == 0:
            return self.read(p)
        elif mode == 1:
            return p
        elif mode == 2:
            return self.read(self.rel_base + p)

    def p_adr(self, idx):
        mode = (self.memory[self.ip] // (10 ** (idx + 1))) % 10
        p = self.memory[self.ip + idx]
        if mode == 0:
            return p
        elif mode == 2:
            return self.rel_base + p

    def write(self, adr, val):
        if adr >= len(self.memory):
            self.memory.extend([0] * (adr + 1 - len(self.memory)))
        self.memory[adr] = val

    def read(self, adr):
        if adr < len(self.memory):
            return self.memory[adr]
        return 0

    def run_once(self):
        op_code = self.memory[self.ip] % 100
        if op_code == 1:
            self.write(self.p_adr(3), self.p_val(1) + self.p_val(2))
            self.ip += 4
        elif op_code == 2:
            self.write(self.p_adr(3), self.p_val(1) * self.p_val(2))
            self.ip += 4
        elif op_code == 3:
            if len(self.inputs) == 0:
                if self.non_block_value is None:
                    raise WaitForInput
                else:
                    input_val = self.non_block_value
            else:
                input_val = self.inputs.popleft()
            self.write(self.p_adr(1), input_val)
            self.ip += 2
        elif op_code == 4:
            out = self.p_val(1)
            self.ip += 2
            return out
        elif op_code == 5:
            if self.p_val(1) != 0:
                self.ip = self.p_val(2)
            else:
                self.ip += 3
        elif op_code == 6:
            if self.p_val(1) == 0:
                self.ip = self.p_val(2)
            else:
                self.ip += 3
        elif op_code == 7:
            self.write(self.p_adr(3), int(self.p_val(1) < self.p_val(2)))
            self.ip += 4
        elif op_code == 8:
            self.write(self.p_adr(3), int(self.p_val(1) == self.p_val(2)))
            self.ip += 4
        elif op_code == 9:
            self.rel_base += self.p_val(1)
            self.ip += 2
        else:
            raise Stopped
        return None

    def run_to_output(self, *args, wait_at_most=None) -> int | None:
        if args:
            self.inputs.extend(args)

        try:
            cycle = 0
            while (out := self.run_once()) is None and (
                wait_at_most is None or cycle < wait_at_most
            ):
                cycle += 1
            return out
        except Stopped:
            return None

    def run_to_outputs(self, count, *args, wait_at_most=None) -> list[int]:
        if args:
            self.inputs.extend(args)
        while (out := self.run_to_output(wait_at_most=wait_at_most)) is not None:
            self.outputs.append(out)
            if len(self.outputs) >= count:
                return [self.outputs.popleft() for _ in range(count)]
        return None

    def run_to_completion(self, *args, wait_at_most=None) -> list[int]:
        if args:
            self.inputs.extend(args)
        outputs = []
        while (out := self.run_to_output(wait_at_most=wait_at_most)) is not None:
            outputs.append(out)
        return outputs
