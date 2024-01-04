import intcode

comp = intcode.Computer(list(map(int, open("5.txt", "r").read().strip().split(","))))


# part 1
print(comp.reset().run_to_completion(1)[-1])

# part 2
print(comp.reset().run_to_completion(5)[-1])
