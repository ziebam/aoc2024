# TODO: Avoid hardcoding the values.

from collections import defaultdict
from math import inf

from performance_utils.performance_utils import measure_performance

with open("day21/in21.txt") as in21:
    data = [line.strip() for line in in21.readlines()]

NUMERIC_KEYPAD = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

DIRECTIONAL_KEYPAD = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}


def get_numeric_paths(current, target):
    x1, y1 = NUMERIC_KEYPAD[current]
    x2, y2 = NUMERIC_KEYPAD[target]

    horizontal = "<" if x2 < x1 else ">"
    vertical = "^" if y2 < y1 else "v"

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    paths = [vertical * dy + horizontal * dx, horizontal * dx + vertical * dy]
    valid_paths = []
    for path in paths:
        new_x, new_y = x1, y1
        for move in path:
            match move:
                case "<":
                    new_x -= 1
                case ">":
                    new_x += 1
                case "^":
                    new_y -= 1
                case "v":
                    new_y += 1

            if (0, 3) == (new_x, new_y):
                break
        else:
            valid_paths.append(path + "A")

    return valid_paths


# Some hardcoded best choices I've found empirically while bashing my head against this puzzle.
BEST_PATHS = {("v", "A"): "^>A", ("^", "<"): "v<A", ("^", ">"): "v>A"}


def get_best_directional_path(current, target):
    if current == target:
        return "A"

    if (current, target) in BEST_PATHS:
        return BEST_PATHS[(current, target)]

    x1, y1 = DIRECTIONAL_KEYPAD[current]
    x2, y2 = DIRECTIONAL_KEYPAD[target]

    horizontal = "<" if x2 < x1 else ">"
    vertical = "^" if y2 < y1 else "v"

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    d = dx + dy

    if d == 2 or d == 4:
        return horizontal * (d // 2) + vertical * (d // 2) + "A"
    else:
        paths = [vertical * dy + horizontal * dx, horizontal * dx + vertical * dy]
        for path in paths:
            new_x, new_y = x1, y1
            for move in path:
                match move:
                    case "<":
                        new_x -= 1
                    case ">":
                        new_x += 1
                    case "^":
                        new_y -= 1
                    case "v":
                        new_y += 1

                # Gap in the directional keypad, cannot go there.
                if (new_x, new_y) == (0, 0):
                    break
            else:
                return path + "A"


def both_parts(data, is_part_one):
    n_directional_keypads = 2 if is_part_one else 25

    out = 0
    for code in data:
        complexity = 0
        current = "A"
        for num in code:
            paths = get_numeric_paths(current, num)

            scomplexity = inf
            for path in paths:
                subcomplexity = 0
                steps_to_counts = defaultdict(lambda: 0)
                curr = "A"
                for step in path:
                    steps_to_counts[(curr, step)] += 1
                    curr = step

                for _ in range(n_directional_keypads):
                    new_steps_to_counts = defaultdict(lambda: 0)
                    for step, count in steps_to_counts.items():
                        if step == ("A", "A"):
                            new_steps_to_counts[step] += count
                            continue

                        source, target = step
                        path = get_best_directional_path(source, target)

                        curr = "A"
                        for s in path:
                            new_steps_to_counts[(curr, s)] += count
                            curr = s
                    steps_to_counts = new_steps_to_counts

                for count in steps_to_counts.values():
                    subcomplexity += count

                if subcomplexity < scomplexity:
                    scomplexity = subcomplexity

            current = num
            complexity += scomplexity

        out += complexity * int(code[:-1])

    return out


measure_performance("part 1", both_parts, data, True)
measure_performance("part 2", both_parts, data, False)
