# NOTE: The code for part 2 is heavily annotated as the solution for part 2 took me pretty much the
# whole day to arrive at, and it's so neat that I'd like to be able to get back to it in the future,
# and understand it at a glance.

from performance_utils.performance_utils import measure_performance

with open("day17/in17.txt") as in17:
    data = in17.read().strip()


class Computer:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program

        self.p = 0
        self.output = []
        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def __repr__(self):
        return f"Register A: {self.A}, register B: {self.B}, register C: {self.C}.\nOutput: {','.join(self.output)}"

    def process_next_opcode(self):
        self.opcodes[self.program[self.p]]()

    def execute_program(self):
        while self.p < len(self.program):
            self.process_next_opcode()

        return self.output

    def combo_operand(self, n):
        match n:
            case 0 | 1 | 2 | 3:
                return n
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                return None  # RESERVED

    def handle_combo_operand(self):
        return self.combo_operand(self.program[self.p + 1])

    def adv(self):
        self.A = self.A // 2 ** self.handle_combo_operand()
        self.p += 2

    def bxl(self):
        self.B = self.B ^ self.program[self.p + 1]
        self.p += 2

    def bst(self):
        self.B = self.handle_combo_operand() % 8
        self.p += 2

    def jnz(self):
        if self.A == 0:
            self.p += 2
            return

        self.p = self.program[self.p + 1]

    def bxc(self):
        self.B = self.B ^ self.C
        self.p += 2

    def out(self):
        self.output.append(str(self.handle_combo_operand() % 8))
        self.p += 2

    def bdv(self):
        self.B = self.A // 2 ** self.handle_combo_operand()
        self.p += 2

    def cdv(self):
        self.C = self.A // 2 ** self.handle_combo_operand()
        self.p += 2


def find_A_that_produces_output(output, depth, A, B, C, program):
    # When we're `len(output)` deep, that means we've found our A. Going further would produce
    # longer output.
    if depth == len(output):
        return A

    # A certain instruction in the program does A = A' // 8. A' is the previous value in the
    # register A, and it's the only time that said register changed. This equation can be rewritten
    # as A' = A * 8 + r, where r is a number between 0 and 7, the remainder of division by 8.
    for r in range(8):
        A_prim = A * 8 + r
        computer = Computer(A_prim, B, C, program)

        # On depth 0, we expect a valid A' for further iteration to produce output that matches
        # `depth + 1` last items from the full output.
        if computer.execute_program() == output[-depth - 1 :]:
            # If the below returns `Nonew`, we need to keep looking at a certain depth. For example,
            # for my input, depth = 0 and i = 0 produces valid output initially, but after a certain
            # amount of steps, there are no A_prims that continue producing valid output. In that
            # case, we need to roll back and keep looking at an earlier depth.
            if next_A := find_A_that_produces_output(
                output, depth + 1, A_prim, B, C, program
            ):
                return next_A
    # If we've exhausted the options for `r`, this branch is no longer valid. We return `None` to
    # properly roll back using the above checks.
    else:
        return None


def part1(data):
    registers, program = data.split("\n\n")
    A, B, C = (int(line.split(":")[1]) for line in registers.split("\n"))
    program = [int(opcode) for opcode in program.split(":")[1].split(",")]

    computer = Computer(A, B, C, program)

    return ",".join(computer.execute_program())


def part2(data):
    registers, program = data.split("\n\n")
    _, B, C = (int(line.split(":")[1]) for line in registers.split("\n"))
    output = [opcode.strip() for opcode in program.split(":")[1].split(",")]
    program = [int(opcode) for opcode in output]

    # We start with A = 0 as every program ends with a `jnz` instruction, so exhausting the A
    # register is the only way to halt.
    return find_A_that_produces_output(output, 0, 0, B, C, program)


measure_performance("part 1", part1, data, unit="microseconds")
measure_performance("part 2", part2, data)
