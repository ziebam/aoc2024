from performance_utils.performance_utils import measure_performance

with open("day02/in02.txt") as in02:
    data = in02.readlines()


def is_safe(levels):
    increasing = int(levels[1]) - int(levels[0]) > 0

    idx = 0
    for level in levels[:-1]:
        difference = int(levels[idx + 1]) - int(level)
        if increasing and (difference <= 0 or difference > 3):
            return 0
        elif not increasing and (difference >= 0 or difference < -3):
            return 0

        idx += 1

    return 1


def part1(data):
    out = 0
    for report in data:
        out += is_safe(report.split())

    return out


def part2(data):
    out = 0
    for report in data:
        levels = report.split()

        if is_safe(levels):
            out += 1
        else:
            for idx in range(len(levels)):
                if is_safe(levels[:idx] + levels[idx + 1 :]):
                    out += 1
                    break

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
