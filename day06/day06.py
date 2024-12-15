from performance_utils.performance_utils import measure_performance

with open("day06/in06.txt") as in06:
    data = [row.strip() for row in in06.readlines()]

DIRECTION_TO_NEXT = {(0, -1): (1, 0), (1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1)}


def get_guard_starting_state(data):
    for y, row in enumerate(data):
        for x, pos in enumerate(row):
            match pos:
                case "^":
                    return x, y, (0, -1)
                case ">":
                    return x, y, (1, 0)
                case "v":
                    return x, y, (0, 1)
                case "<":
                    return x, y, (-1, 0)


def get_visited(data, gx, gy, direction, include_init=True):
    width = len(data[0])
    height = len(data)

    visited = set()
    if include_init:
        visited.add((gx, gy))

    while True:
        new_gx = gx + direction[0]
        new_gy = gy + direction[1]

        if new_gx < 0 or new_gx > width - 1 or new_gy < 0 or new_gy > height - 1:
            break

        if data[new_gy][new_gx] == "#":
            direction = DIRECTION_TO_NEXT[direction]
        else:
            gx, gy = new_gx, new_gy
            visited.add((new_gx, new_gy))

    return visited


def part1(data):
    gx, gy, direction = get_guard_starting_state(data)
    visited = get_visited(data, gx, gy, direction)

    return len(visited)


def part2(data):
    width = len(data[0])
    height = len(data)

    init_gx, init_gy, init_direction = get_guard_starting_state(data)

    # Only need to check the positions that are visited in part 1 as the others are unreachable
    # prior to putting in an obstruction.
    positions_to_check = get_visited(
        data, init_gx, init_gy, init_direction, include_init=False
    )

    grid = [[node for node in row] for row in data]

    out = 0
    for position in positions_to_check:
        x, y = position
        grid[y][x] = "#"

        gx, gy, direction = init_gx, init_gy, init_direction

        hit = set()
        while True:
            new_gx = gx + direction[0]
            new_gy = gy + direction[1]

            if new_gx < 0 or new_gx > width - 1 or new_gy < 0 or new_gy > height - 1:
                break

            if grid[new_gy][new_gx] == "#":
                if (new_gx, new_gy, direction) in hit:
                    out += 1
                    break

                hit.add((new_gx, new_gy, direction))
                direction = DIRECTION_TO_NEXT[direction]
            else:
                gx, gy = new_gx, new_gy

        grid[y][x] = "."

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data, warmup_runs=5, actual_runs=15)
