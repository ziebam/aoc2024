from performance_utils.performance_utils import measure_performance

with open("day24/in24.txt") as in24:
    data = in24.read().strip()


def part1(data):
    init_state, gates = data.split("\n\n")

    state = dict()
    for entry in init_state.split("\n"):
        wire, value = entry.split(":")
        state[wire] = int(value.strip())

    operations = set()
    for gate in gates.split("\n"):
        left, output = gate.split(" -> ")
        in1, operand, in2 = left.split(" ")
        operations.add((in1, operand, in2, output))

    while len(operations):
        to_subtract = set()
        for operation in operations:
            in1, operand, in2, output = operation
            if in1 in state and in2 in state:
                match operand:
                    case "AND":
                        state[output] = state[in1] & state[in2]
                    case "OR":
                        state[output] = state[in1] | state[in2]
                    case "XOR":
                        state[output] = state[in1] ^ state[in2]

                to_subtract.add(operation)
        operations -= to_subtract

    out = 0
    for wire, value in state.items():
        if not wire.startswith("z"):
            continue

        out += value * 2 ** int(wire[1:])

    return out


measure_performance("part 1", part1, data)
