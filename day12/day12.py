# TODO: Better approach for part 2.

from performance_utils.performance_utils import measure_performance

with open("day12/in12.txt") as in12:
    data = [row.strip() for row in in12.readlines()]


width = len(data[0])
height = len(data)


# `region` is populated as a side effect. The returned value is said region's perimeter.
def flood_fill(grid, plant, x, y, region):
    if (x, y) in region:
        return 0

    if grid[y][x] != plant:
        return 1

    region.add((x, y))

    perimeter = 0

    perimeter += flood_fill(grid, plant, x + 1, y, region) if x < width - 1 else 1
    perimeter += flood_fill(grid, plant, x, y + 1, region) if y < height - 1 else 1
    perimeter += flood_fill(grid, plant, x - 1, y, region) if x > 0 else 1
    perimeter += flood_fill(grid, plant, x, y - 1, region) if y > 0 else 1

    return perimeter


def get_fences(grid, plant, region):
    fences = set()
    min_x = min_y = max_x = max_y = 0

    for x, y in region:
        if x == width - 1 or grid[y][x + 1] != plant:
            fences.add((x + 1, y, "e"))
            if x + 1 > max_x:
                max_x = x + 1

        if y == height - 1 or grid[y + 1][x] != plant:
            fences.add((x, y + 1, "s"))
            if y + 1 > max_y:
                max_y = y + 1

        if x == 0 or grid[y][(x - 1)] != plant:
            fences.add((x - 1, y, "w"))
            if x - 1 < min_x:
                min_x = x - 1

        if y == 0 or grid[y - 1][x] != plant:
            fences.add((x, y - 1, "n"))
            if y - 1 < min_y:
                min_y = y - 1

    return fences, min_x, min_y, max_x, max_y


def part1(data):
    checked = set()

    out = 0
    for y, row in enumerate(data):
        for x, plant in enumerate(row):
            if (x, y) in checked:
                continue

            region = set()
            perimeter = flood_fill(data, plant, x, y, region)
            checked.update(region)
            area = len(region)

            out += area * perimeter

    return out


def part2(data):
    checked = set()

    out = 0
    for y, row in enumerate(data):
        for x, plant in enumerate(row):
            if (x, y) in checked:
                continue

            region = set()
            flood_fill(data, plant, x, y, region)
            checked.update(region)
            area = len(region)

            fences, min_x, min_y, max_x, max_y = get_fences(data, plant, region)

            unique_fences = 0

            n_flag = False
            s_flag = False
            for yy in range(min_y, max_y + 1):
                for xx in range(min_x, max_x + 1):
                    if (xx, yy, "n") in fences:
                        if not n_flag:
                            unique_fences += 1
                        n_flag = True
                    else:
                        n_flag = False

                    if (xx, yy, "s") in fences:
                        if not s_flag:
                            unique_fences += 1
                        s_flag = True
                    else:
                        s_flag = False

            w_flag = False
            e_flag = False
            for xx in range(min_x, max_x + 1):
                for yy in range(min_y, max_y + 1):
                    if (xx, yy, "w") in fences:
                        if not w_flag:
                            unique_fences += 1
                        w_flag = True
                    else:
                        w_flag = False

                    if (xx, yy, "e") in fences:
                        if not e_flag:
                            unique_fences += 1
                        e_flag = True
                    else:
                        e_flag = False

            out += area * unique_fences

    return out


# Probably off by a few microseconds since `width` and `height` are globals for convenience,
# and therefore not calculated into the runtime, but I think it's negligible.
measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data, warmup_runs=100, actual_runs=1000)
