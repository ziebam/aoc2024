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


def get_paths(current, target, keypad, gap, depth=0):
    x1, y1 = keypad[current]
    x2, y2 = keypad[target]

    horizontal = "<" if x2 < x1 else ">"
    vertical = "^" if y2 < y1 else "v"

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    d = dx + dy

    valid_paths = []
    paths = [horizontal * dx + vertical * dy, vertical * dy + horizontal * dx]
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

            if gap == (new_x, new_y):
                break
        else:
            valid_path = "".join(path + "A")
            if valid_path not in valid_paths:
                valid_paths.append(valid_path)

    if depth == 2:
        return valid_paths
    else:
        current = "A"
        next_step = []
        for s in valid_paths:
            new_sequences = [""]
            for d in s:
                new_new_sequences = []
                for s in new_sequences:
                    for path in get_paths(
                        current, d, DIRECTIONAL_KEYPAD, (0, 0), depth + 1
                    ):
                        new_new_sequences.append(s + path)
                new_sequences = new_new_sequences[::]
                current = d
            next_step += new_sequences

        return [min(next_step, key=len)]


def part1(data):
    out = 0

    current = "A"
    for code in data:
        complexity = 0
        for num in code:
            paths = get_paths(current, num, NUMERIC_KEYPAD, (0, 3))
            complexity += len(min(paths, key=len))
            current = num
        out += complexity * int(code[:-1])

    return out


measure_performance("part 1", part1, data)
