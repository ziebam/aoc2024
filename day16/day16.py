# TODO: Could probably avoid exploding nodes.

from performance_utils.performance_utils import measure_performance

from math import inf

with open("day16/in16.txt") as in16:
    data = [row.strip() for row in in16.readlines()]


WIDTH = len(data[0])
HEIGHT = len(data)

# For constructing the search space.
# When we come from the top, we are facing south, etc.
NODES_TO_EXPLODE = {(0, -1): "s", (0, 1): "n", (-1, 0): "e", (1, 0): "w"}

# For neighbor checking.
NEIGHBORS = {(0, -1): "n", (0, 1): "s", (-1, 0): "w", (1, 0): "e"}

# We always start in the bottom left corner, facing east.
SOURCE = (1, HEIGHT - 2, "e")

# The target is always in the top right corner, can be reached either facing east or north.
TARGETS = ((WIDTH - 2, 1, "e"), (WIDTH - 2, 1, "n"))


# Returns a set of (x, y) tiles that are visited at least once in each best path.
def get_unique_tiles(distances, prev, source, target, unique_tiles=None):
    if unique_tiles is None:
        unique_tiles = set()

    if not prev[source]:
        return

    unique_tiles.add((source[0], source[1]))
    for next_step in prev[source]:
        if (
            distances[next_step] == distances[source] - 1001
            or distances[next_step] == distances[source] - 1
        ):
            unique_tiles.add((next_step[0], next_step[1]))
            get_unique_tiles(distances, prev, next_step, target, unique_tiles)

    return unique_tiles


def dijkstra(grid):
    distances = {}
    prev = {}

    nodes = set()
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            # Skip unreachable nodes (walls).
            if tile == "#":
                continue

            # The starting node is only ever visited while facing east.
            if tile == "S":
                distances[SOURCE] = 0
                prev[SOURCE] = set()
                nodes.add(SOURCE)
            # Otherwise, explode each node into K nodes, where K is the amount of its neighbors.
            # This is needed to incorporate turning into the weight calculation later on.
            else:
                for (dx, dy), dir in NODES_TO_EXPLODE.items():
                    if data[y + dy][x + dx] != "#":
                        distances[(x, y, dir)] = inf
                        prev[(x, y, dir)] = set()
                        nodes.add((x, y, dir))

    # For performance, keep track of the nodes whose destinations we need to check to
    # avoid iterating over the whole `distances` dictionary every time.
    nodes_to_check = set([SOURCE])
    while len(nodes) != 0:
        min_distance = inf
        next_node = None
        for node in nodes_to_check:
            if node in nodes and distances[node] <= min_distance:
                min_distance = distances[node]
                next_node = node
        nodes.remove(next_node)
        nodes_to_check.remove(next_node)

        if next_node in TARGETS:
            return distances, prev

        x, y, dir = next_node

        neighbors = set()
        for (dx, dy), neighbor_dir in NEIGHBORS.items():
            xx = x + dx
            yy = y + dy

            if (xx, yy, dir) in nodes:
                neighbors.add((xx, yy, dir))
            elif (xx, yy, neighbor_dir) in nodes:
                neighbors.add((xx, yy, neighbor_dir))

        for neighbor in neighbors:
            alt = distances[next_node]
            if neighbor[2] == dir:
                alt += 1
            else:
                alt += 1001

            if alt <= distances[neighbor]:
                prev[neighbor].add(next_node)
                distances[neighbor] = alt
                nodes_to_check.add(neighbor)


def part1(data):
    distances, _ = dijkstra(data)

    min_distance = inf
    for target in TARGETS:
        if distances[target] < min_distance:
            min_distance = distances[target]

    return min_distance


def part2(data):
    distances, prev = dijkstra(data)

    min_distance = inf
    for target in TARGETS:
        if distances[target] < min_distance:
            min_distance = distances[target]
            source = target
    target = SOURCE

    # We do DFS backwards backwards, so source and target swap places above.
    return len(get_unique_tiles(distances, prev, source, target))


measure_performance("part 1", part1, data, warmup_runs=100, actual_runs=1000)
measure_performance("part 2", part2, data, warmup_runs=100, actual_runs=1000)
