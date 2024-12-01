from performance_utils.performance_utils import measure_performance

with open("day01/in01.txt") as in01:
    data = in01.readlines()


def part1(data):
    l1 = []
    l2 = []

    for line in data:
        entries = line.split()
        l1.append(int(entries[0]))
        l2.append(int(entries[1]))

    l1.sort()
    l2.sort()

    out = 0
    for x, y in zip(l1, l2):
        out += abs(x - y)

    return out


def part2(data):
    l1 = []
    l2 = []

    for line in data:
        entries = line.split()
        l1.append(int(entries[0]))
        l2.append(int(entries[1]))

    out = 0
    for entry in l1:
        multiplier = 0
        for m in l2:
            if m == entry:
                multiplier += 1
        out += entry * multiplier

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
