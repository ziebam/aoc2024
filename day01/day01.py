from performance_utils.performance_utils import measure_performance

with open("day01/in01.txt") as in01:
    data = in01.readlines()


def part1(data):
    left_list = []
    right_list = []

    for line in data:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

    left_list.sort()
    right_list.sort()

    out = 0
    for x, y in zip(left_list, right_list):
        out += abs(x - y)

    return out


def part2(data):
    ids = []
    multipliers = dict()

    for line in data:
        left, right = line.split()
        # Doing this manually is faster than list/tuple comprehensions or `map`.
        left = int(left)
        right = int(right)

        ids.append(left)
        multipliers[right] = multipliers.setdefault(right, 0) + 1

    out = 0
    for id in ids:
        out += id * multipliers.get(id, 0)

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
