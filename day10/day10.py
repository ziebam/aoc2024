from performance_utils.performance_utils import measure_performance

with open("day10/in10.txt") as in10:
    data = [[int(c) for c in row.strip()] for row in in10.readlines()]


def get_next_steps(grid, width, height, next, x, y):
    next_steps = []

    if x > 0 and grid[y][x - 1] == next:  # left
        next_steps.append((x - 1, y))

    if x < width - 1 and grid[y][x + 1] == next:  # right
        next_steps.append((x + 1, y))

    if y > 0 and grid[y - 1][x] == next:  # up
        next_steps.append((x, y - 1))

    if y < height - 1 and grid[y + 1][x] == next:  # down
        next_steps.append((x, y + 1))

    return next_steps


def get_reachable_peaks(grid, width, height, current, x, y, reachable_peaks=None):
    if reachable_peaks is None:
        reachable_peaks = set()

    next_steps = get_next_steps(grid, width, height, current + 1, x, y)

    if not next_steps:
        return []

    if current == 8:
        return next_steps

    for next_step in next_steps:
        reachable_peaks.update(
            get_reachable_peaks(
                grid,
                width,
                height,
                current + 1,
                next_step[0],
                next_step[1],
                reachable_peaks,
            )
        )

    return reachable_peaks


def get_unique_trails(grid, width, height, current, x, y, n=0):
    next_steps = get_next_steps(grid, width, height, current + 1, x, y)

    if not next_steps:
        return 0

    if current == 8:
        return len(next_steps)

    n = 0
    for next_step in next_steps:
        n += get_unique_trails(
            grid, width, height, current + 1, next_step[0], next_step[1], n
        )

    return n


def part1(data):
    width = len(data[0])
    height = len(data)

    out = 0
    for y, row in enumerate(data):
        for x, h in enumerate(row):
            if h == 0:
                out += len(get_reachable_peaks(data, width, height, 0, x, y))

    return out


def part2(data):
    width = len(data[0])
    height = len(data)

    out = 0
    for y, row in enumerate(data):
        for x, h in enumerate(row):
            if h == 0:
                out += get_unique_trails(data, width, height, 0, x, y)

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
