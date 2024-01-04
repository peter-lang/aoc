import intcode

comp = intcode.Computer(list(map(int, open("9.txt", "r").read().strip().split(","))))

# part 1
print(comp.reset().run_to_output(1))

# part 2
print(comp.reset().run_to_output(2))
