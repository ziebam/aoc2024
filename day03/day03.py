import re

from performance_utils.performance_utils import measure_performance

with open("day03/in03.txt") as in03:
    data = in03.read()


def part1(data):
    out = 0

    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
    for match in matches:
        out += int(match[0]) * int(match[1])

    return out


def part2(data):
    out = 0

    matches = re.findall(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))", data)

    enabled = True
    for match in matches:
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif enabled:
            out += int(match[1]) * int(match[2])

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
