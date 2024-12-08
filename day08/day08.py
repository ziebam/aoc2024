# TODO: Simple math could probably make this code more readable.

from performance_utils.performance_utils import measure_performance

with open("day08/in08.txt") as in08:
    data = [row.strip() for row in in08.readlines()]


def is_in_bounds(point, width, height):
    x, y = point

    if x < 0 or x > width - 1 or y < 0 or y > height - 1:
        return False

    return True


def part1(data):
    width = len(data[0])
    height = len(data)

    antennas = dict()
    antinodes = set()
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == ".":
                continue

            if cell in antennas:
                for antenna in antennas[cell]:
                    x1, x2, y1, y2 = antenna[0], x, antenna[1], y
                    dx, dy = x2 - x1, y2 - y1

                    antinode1 = (x1 - dx, y1 - dy)
                    antinode2 = (x2 + dx, y2 + dy)

                    if is_in_bounds(antinode1, width, height):
                        antinodes.add(antinode1)

                    if is_in_bounds(antinode2, width, height):
                        antinodes.add(antinode2)

                antennas[cell].append((x, y))
            else:
                antennas[cell] = [(x, y)]

    return len(antinodes)


def part2(data):
    width = len(data[0])
    height = len(data)

    antennas = dict()
    antinodes = set()
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == ".":
                continue

            if cell in antennas:
                # If an antenna of a given type is already in the dictionary, that means the one
                # we're checking now is at least the second one, so they both need to count as
                # antinodes.
                antinodes.add((x, y))

                for antenna in antennas[cell]:
                    antinodes.add(antenna)

                    x1, x2, y1, y2 = antenna[0], x, antenna[1], y
                    dx, dy = x2 - x1, y2 - y1

                    # Traverse in one direction.
                    antinode1 = (x1 - dx, y1 - dy)
                    while is_in_bounds(antinode1, width, height):
                        antinodes.add(antinode1)
                        antinode1 = (
                            antinode1[0] - dx,
                            antinode1[1] - dy,
                        )

                    # Traverse in the other direction.
                    antinode2 = (x2 + dx, y2 + dy)
                    while is_in_bounds(antinode2, width, height):
                        antinodes.add(antinode2)
                        antinode2 = (
                            antinode2[0] + dx,
                            antinode2[1] + dy,
                        )

                antennas[cell].append((x, y))
            else:
                antennas[cell] = [(x, y)]

    return len(antinodes)


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
