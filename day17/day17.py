from performance_utils.performance_utils import measure_performance

with open("day17/in17.txt") as in17:
    data = in17.read().strip()


class Computer:
    def __init__(self, A, B, C, program, p):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.p = p
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
        return self.opcodes[self.program[self.p]]()

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

    def adv(self):
        self.A = self.A // 2 ** self.combo_operand(self.program[self.p + 1])
        self.p += 2
        return self.p

    def bxl(self):
        self.B = self.B ^ self.program[self.p + 1]
        self.p += 2
        return self.p

    def bst(self):
        self.B = self.combo_operand(self.program[self.p + 1]) % 8
        self.p += 2
        return self.p

    def jnz(self):
        if self.A == 0:
            self.p += 2
            return self.p

        self.p = self.program[self.p + 1]
        return self.p

    def bxc(self):
        self.B = self.B ^ self.C
        self.p += 2
        return self.p

    def out(self):
        self.output.append(str(self.combo_operand(self.program[self.p + 1]) % 8))
        self.p += 2
        return self.p

    def bdv(self):
        self.B = self.A // 2 ** self.combo_operand(self.program[self.p + 1])
        self.p += 2
        return self.p

    def cdv(self):
        self.C = self.A // 2 ** self.combo_operand(self.program[self.p + 1])
        self.p += 2
        return self.p


def part1(data):
    registers, program = data.split("\n\n")
    A, B, C = (int(line.split(":")[1]) for line in registers.split("\n"))
    program = [int(opcode) for opcode in program.split(":")[1].split(",")]

    p = 0
    computer = Computer(A, B, C, program, p)
    while p < len(program):
        p = computer.process_next_opcode()

    return ",".join(computer.output)


measure_performance("part 1", part1, data, unit="microseconds")
