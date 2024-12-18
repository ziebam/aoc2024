from collections import defaultdict
from math import inf

from performance_utils.performance_utils import measure_performance

with open("day18/in18.txt") as in18:
    data = [location.strip() for location in in18.readlines()]


WIDTH = HEIGHT = 71
START = (0, 0)
GOAL = (WIDTH - 1, HEIGHT - 1)

OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def manhattan_distance(a, b):
    x1, y1 = a
    x2, y2 = b

    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbors(node, corrupted_locations):
    x, y = node

    neighbors = []
    for dx, dy in OFFSETS:
        nx = x + dx
        ny = y + dy

        if (nx, ny) not in corrupted_locations and 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            neighbors.append((nx, ny))

    return neighbors


def get_path(prev, current):
    path = set()
    while current in prev:
        current = prev[current]
        path.add(current)
    return path


def a_star(start, goal, corrupted_locations):
    open = set([start])

    prev = {}

    # Distances.
    d = defaultdict(lambda: inf)
    d[start] = 0

    # Distances + heuristic.
    dph = defaultdict(lambda: inf)
    dph[start] = manhattan_distance(start, goal)

    while len(open) > 0:
        min_distance = inf
        for node in open:
            if node not in corrupted_locations and dph[node] < min_distance:
                min_distance = dph[node]
                current = node

        if current == goal:
            return get_path(prev, current)

        open.remove(current)

        for neighbor in get_neighbors(current, corrupted_locations):
            maybe_d = d[current] + 1
            if maybe_d < d[neighbor]:
                prev[neighbor] = current
                d[neighbor] = maybe_d
                dph[neighbor] = maybe_d + manhattan_distance(neighbor, goal)
                if neighbor not in open:
                    open.add(neighbor)


def part1(data):
    corrupted_locations = set()
    for i in range(1024):
        x, y = (int(n) for n in data[i].split(","))
        corrupted_locations.add((x, y))

    return len(a_star(START, GOAL, corrupted_locations))


def part2(data):
    start = (0, 0)
    goal = (WIDTH - 1, HEIGHT - 1)

    corrupted_locations = set()
    for i in range(1024):
        x, y = (int(n) for n in data[i].split(","))
        corrupted_locations.add((x, y))

    path = a_star(start, goal, corrupted_locations)
    i = 1024
    while True:
        x, y = (int(n) for n in data[i].split(","))
        corrupted_locations.add((x, y))

        if (x, y) in path:
            path = a_star(start, goal, corrupted_locations)
            if path is None:
                return f"{x},{y}"

        i += 1


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data, warmup_runs=100, actual_runs=1000)
