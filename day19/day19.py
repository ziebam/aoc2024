from collections import defaultdict

from performance_utils.performance_utils import measure_performance


with open("day19/in19.txt") as in19:
    data = in19.read().strip()


def count_possibilities(pattern, available_towels, cached_patterns):
    if not pattern:
        return 1

    if pattern in cached_patterns:
        return cached_patterns[pattern]

    cached_patterns[pattern] = 0

    for towel in available_towels[pattern[0]]:
        l = len(towel)
        if pattern[:l] == towel:
            cached_patterns[pattern] += count_possibilities(
                pattern[l:], available_towels, cached_patterns
            )

    return cached_patterns[pattern]


def part1(data):
    towels, patterns = data.split("\n\n")

    available_towels = defaultdict(list)
    for towel in towels.split(", "):
        available_towels[towel[0]].append(towel)

    out = 0
    cached_patterns = defaultdict(lambda: 0)
    for pattern in patterns.split("\n"):
        if count_possibilities(pattern, available_towels, cached_patterns):
            out += 1

    return out


def part2(data):
    towels, patterns = data.split("\n\n")

    available_towels = defaultdict(list)
    for towel in towels.split(", "):
        available_towels[towel[0]].append(towel)

    out = 0
    cached_patterns = defaultdict(lambda: 0)
    for pattern in patterns.split("\n"):
        out += count_possibilities(pattern, available_towels, cached_patterns)

    return out


measure_performance("part 1", part1, data, warmup_runs=100, actual_runs=1000)
measure_performance("part 2", part2, data, warmup_runs=100, actual_runs=1000)
