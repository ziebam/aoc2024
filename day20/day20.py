# TODO: Some memoization for part 2?

from performance_utils.performance_utils import measure_performance

with open("day20/in20.txt") as in20:
    data = [line.strip() for line in in20.readlines()]


DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))


def part1(data):
    start = end = None
    path_tiles = set()
    shortcuts = set()
    for y, row in enumerate(data[1:-1], start=1):
        for x, tile in enumerate(row[1:-1], start=1):
            match tile:
                case ".":
                    path_tiles.add((x, y))
                case "#":
                    if data[y][x - 1] != "#" and data[y][x + 1] != "#":
                        shortcuts.add(((x - 1, y), (x + 1, y)))
                    elif data[y - 1][x] != "#" and data[y + 1][x] != "#":
                        shortcuts.add(((x, y - 1), (x, y + 1)))
                case "S":
                    start = (x, y)
                case "E":
                    end = (x, y)

    path = {start: 0}
    current = start
    n = 1
    while path_tiles:
        x, y = current
        for dx, dy in DIRECTIONS:
            if (next := (x + dx, y + dy)) in path_tiles:
                path[next] = n
                path_tiles.remove(next)
                current = next
                n += 1
                break
    path[end] = n

    out = 0
    for p_from, p_to in shortcuts:
        if abs(path[p_from] - path[p_to]) - 2 >= 100:
            out += 1

    return out


def part2(data):
    start = end = None
    path_tiles = set()
    for y, row in enumerate(data[1:-1], start=1):
        for x, tile in enumerate(row[1:-1], start=1):
            match tile:
                case ".":
                    path_tiles.add((x, y))
                case "S":
                    start = (x, y)
                case "E":
                    end = (x, y)

    path = {0: start}
    current = start
    n = 1
    while path_tiles:
        x, y = current
        for dx, dy in DIRECTIONS:
            if (next := (x + dx, y + dy)) in path_tiles:
                path[n] = next
                path_tiles.remove(next)
                current = next
                n += 1
                break
    path[n] = end
    l = len(path)

    out = 0
    for step, tile in path.items():
        if step == l - 100:
            break

        for i in range(step + 101, l):
            x1, y1 = tile
            x2, y2 = path[i]
            d = abs(x1 - x2) + abs(y1 - y2)
            if d <= 20 and i - step - d >= 100:
                out += 1

    return out


measure_performance("part 1", part1, data)
print(
    f"Part 2 answer: \033[92m{part2(data)}\x1b[0m. Too slow for performance measurement.\n"
)
