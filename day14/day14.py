from performance_utils.performance_utils import measure_performance

with open("day14/in14.txt") as in14:
    data = in14.readlines()


def part1(data):
    width = 101
    x_middle = width // 2
    height = 103
    y_middle = height // 2

    i = ii = iii = iv = 0
    for robot in data:
        xy, dxdy = robot.split()
        x, y = xy.split(",")
        x = int(x.split("=")[1])
        y = int(y)
        dx, dy = dxdy.split(",")
        dx = int(dx.split("=")[1])
        dy = int(dy)

        x = (x + dx * 100) % width
        y = (y + dy * 100) % height

        if x < x_middle and y < y_middle:
            i += 1
        elif x > x_middle and y < y_middle:
            ii += 1
        elif x < x_middle and y > y_middle:
            iii += 1
        elif x > x_middle and y > y_middle:
            iv += 1

    return i * ii * iii * iv


def part2(data):
    width = 101
    height = 103

    robots = []
    for robot in data:
        xy, dxdy = robot.split()
        x, y = xy.split(",")
        x = int(x.split("=")[1])
        y = int(y)
        dx, dy = dxdy.split(",")
        dx = int(dx.split("=")[1])
        dy = int(dy)

        robots.append((x, y, dx, dy))

    i = 0
    while True:
        grid = [["." for _ in range(width)] for _ in range(height)]

        new_robots = []
        for x, y, dx, dy in robots:
            grid[y][x] = "X"
            new_robots.append(((x + dx) % width, (y + dy) % height, dx, dy))
        robots = new_robots

        christmas_tree_upper_border = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        for j in range(height - 30):
            for idx, c in enumerate(grid[j]):
                if (
                    c == "X"
                    and "".join(grid[j][idx : idx + len(christmas_tree_upper_border)])
                    == christmas_tree_upper_border
                ):
                    return i
        i += 1


measure_performance("part 1", part1, data)
print(
    f"Part 2 answer: \033[92m{part2(data)}\x1b[0m. Too slow for performance measurement.\n"
)
