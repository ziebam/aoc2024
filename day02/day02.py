from performance_utils.performance_utils import measure_performance

with open("day02/in02.txt") as in02:
    data = in02.readlines()


def is_safe(report):
    increasing = int(report[1]) - int(report[0]) > 0

    idx = 0
    for level in report[:-1]:
        subdifference = int(report[idx + 1]) - int(level)
        if increasing and (subdifference <= 0 or subdifference > 3):
            return 0
        elif not increasing and (subdifference >= 0 or subdifference < -3):
            return 0

        idx += 1

    return 1


def part1(data):
    out = 0
    for report in data:
        report = report.split()
        out += is_safe(report)

    return out


def part2(data):
    out = 0
    for report in data:
        report = report.split()
        safe = is_safe(report)

        if safe:
            out += 1
        else:
            for idx in range(len(report)):
                if is_safe(report[:idx] + report[idx + 1 :]):
                    out += 1
                    break

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
