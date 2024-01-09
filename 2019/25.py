import intcode

CODE = list(map(int, open("25.txt", "r").read().strip().split(",")))

comp = intcode.Computer(CODE).reset()

while True:
    try:
        while (out := comp.run_to_output()) is not None:
            print(chr(out), end="")
    except intcode.WaitForInput:
        res = input()
        comp.inputs.extend(map(ord, res.strip() + "\n"))

# MAP:
#
# (dark matter) - ( ) --------- ( ) ------- ( ) - (START)
#                  |             |           |
#           ( ) - ( )   ( ) - (astronaut)   ( )                    (END)
#                             (ice cream)    |                       |
#                                |          ( )                   (CHECK)
#                                |           |                       |
#                                |          ( )     ( )              |
#                                |                   |               |
#                               ( ) --------- (easter egg) - (weather machine)
#
# Items needed:
# - astronaut ice cream
# - easter egg
# - dark matter
# - weather machine
