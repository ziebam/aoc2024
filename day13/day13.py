from performance_utils.performance_utils import measure_performance

with open("day13/in13.txt") as in13:
    data = in13.read().strip()


def both_parts(data, is_part_one):
    out = 0
    for machine in data.split("\n\n"):
        button_a, button_b, prize = machine.split("\n")

        button_a = button_a.split("+")
        ax = int(button_a[1].split(",")[0])
        ay = int(button_a[2])

        button_b = button_b.split("+")
        bx = int(button_b[1].split(",")[0])
        by = int(button_b[2])

        prize = prize.split("=")
        prize_x = int(prize[1].split(",")[0]) + (
            0 if is_part_one else 10_000_000_000_000
        )
        prize_y = int(prize[2]) + (0 if is_part_one else 10_000_000_000_000)

        denominator = ax * by - ay * bx

        x = abs((bx * prize_y - by * prize_x) / denominator)
        if int(x) != x:
            continue

        y = abs((prize_x * ay - prize_y * ax) / denominator)
        if int(y) != y:
            continue

        out += int(x) * 3 + int(y)

    return out


measure_performance("part 1", both_parts, data, True)
measure_performance("part 2", both_parts, data, False)
