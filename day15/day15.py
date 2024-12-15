from performance_utils.performance_utils import measure_performance

with open("day15/in15.txt") as in15:
    data = in15.read().strip()


DIRECTIONS = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}


def get_next_robot_pos_part1(grid, w, h, robot_pos, direction):
    x, y = robot_pos
    dx, dy = DIRECTIONS[direction]
    match direction:
        case "^" | "v":
            next_node = grid[y + dy][x]
            if next_node == "#":
                return (x, y)
            elif next_node == ".":
                grid[y][x] = "."
                grid[y + dy][x] = "@"
                return (x, y + dy)
            else:
                r = range(y - 1, -1, -1) if direction == "^" else range(y + 1, h)
                for yy in r:
                    if grid[yy][x] == "O":
                        continue
                    elif grid[yy][x] == "#":
                        return (x, y)
                    else:
                        grid[yy][x] = "O"
                        grid[y + dy][x] = "@"
                        grid[y][x] = "."
                        return (x, y + dy)
        case "<" | ">":
            next_node = grid[y][x + dx]
            if next_node == "#":
                return (x, y)
            elif next_node == ".":
                grid[y][x] = "."
                grid[y][x + dx] = "@"
                return (x + dx, y)
            else:
                r = range(x - 1, -1, -1) if direction == "<" else range(x + 1, w)
                for xx in r:
                    if grid[y][xx] == "O":
                        continue
                    elif grid[y][xx] == "#":
                        return (x, y)
                    else:
                        grid[y][xx] = "O"
                        grid[y][x + dx] = "@"
                        grid[y][x] = "."
                        return (x + dx, y)


def get_next_robot_pos_part2(grid, w, h, robot_pos, direction):
    x, y = robot_pos
    dx, dy = DIRECTIONS[direction]
    match direction:
        case "^" | "v":
            next_node = grid[y + dy][x]
            if next_node == "#":
                return (x, y)
            elif next_node == ".":
                grid[y][x] = "."
                grid[y + dy][x] = "@"
                return (x, y + dy)
            else:
                is_up = direction == "^"

                boxes_to_move = {}
                boxes_to_move[y + dy] = set()
                if next_node == "[":
                    boxes_to_move[y + dy].add((x, x + 1))
                else:
                    boxes_to_move[y + dy].add((x - 1, x))

                p = y + dy * 2
                condition = p >= 0 if is_up else p < h
                while condition:
                    boxes_to_move[p] = set()
                    for x1, x2 in boxes_to_move[p - dy]:
                        if grid[p][x1] == "#" or grid[p][x2] == "#":
                            return (x, y)

                        if grid[p][x1] == "[":
                            boxes_to_move[p].add((x1, x1 + 1))
                        elif grid[p][x2] == "[":
                            boxes_to_move[p].add((x2, x2 + 1))

                        if grid[p][x1] == "]":
                            boxes_to_move[p].add((x1 - 1, x1))
                        elif grid[p][x2] == "]":
                            boxes_to_move[p].add((x2 - 1, x2))
                    if len(boxes_to_move[p]):
                        p += dy
                    else:
                        for yy in range(p, y, 1 if is_up else -1):
                            for x1, x2 in boxes_to_move[yy]:
                                grid[yy + dy][x1] = "["
                                grid[yy + dy][x2] = "]"
                                grid[yy][x1] = "."
                                grid[yy][x2] = "."
                        grid[y + dy][x] = "@"
                        grid[y][x] = "."
                        return (x, y + dy)
        case "<" | ">":
            is_left = direction == "<"

            next_node = grid[y][x + dx]
            if next_node == "#":
                return (x, y)
            elif next_node == ".":
                grid[y][x] = "."
                grid[y][x + dx] = "@"
                return (x + dx, y)
            else:
                boxes_to_move = set()
                boxes_to_move.add((x + dx, y))
                p = x + dx * 3
                condition = p > 0 if is_left else p < w
                while condition:
                    if grid[y][p] == "#":
                        return (x, y)
                    elif grid[y][p] == ".":
                        for xx, yy in boxes_to_move:
                            if is_left:
                                grid[yy][xx - 2] = "["
                                grid[yy][xx - 1] = "]"
                            else:
                                grid[yy][xx + 1] = "["
                                grid[yy][xx + 2] = "]"
                        grid[y][x] = "."
                        grid[y][x + dx] = "@"
                        return (x + dx, y)
                    else:
                        boxes_to_move.add((p, y))
                        p += dx * 2


def part1(data):
    grid, moves = data.split("\n\n")
    grid = [[node for node in row] for row in grid.split("\n")]
    w = len(grid[0])
    h = len(grid)

    robot_pos = None
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node == "@":
                robot_pos = (x, y)
                break
        if robot_pos is not None:
            break

    for move in moves:
        if move == "\n":
            continue

        robot_pos = get_next_robot_pos_part1(grid, w, h, robot_pos, move)

    out = 0
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node == "O":
                out += 100 * y + x

    return out


def part2(data):
    grid, moves = data.split("\n\n")
    grid = grid.split("\n")
    robot_pos = None

    resized_grid = [[] for _ in range(len(grid))]
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node in "#.":
                resized_grid[y].append(node)
                resized_grid[y].append(node)
            elif node == "O":
                resized_grid[y].append("[")
                resized_grid[y].append("]")
            else:
                robot_pos = (x * 2, y)
                resized_grid[y].append("@")
                resized_grid[y].append(".")

    w = len(resized_grid[0])
    h = len(resized_grid)

    for move in moves:
        if move == "\n":
            continue

        robot_pos = get_next_robot_pos_part2(resized_grid, w, h, robot_pos, move)

    out = 0
    for y, row in enumerate(resized_grid):
        for x, node in enumerate(row):
            if node == "[":
                out += 100 * y + x

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
