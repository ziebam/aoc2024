from collections import defaultdict

from performance_utils.performance_utils import measure_performance

with open("day23/in23.txt") as in23:
    data = in23.read().strip()


def part1(data):
    computers_to_connections = defaultdict(list)
    for second_computer in data.split("\n"):
        one, two = second_computer.split("-")
        computers_to_connections[one].append(two)
        computers_to_connections[two].append(one)

    seen = []
    out = 0
    for computer, connections in computers_to_connections.items():
        if not computer.startswith("t"):
            continue

        for idx, second_computer in enumerate(connections):
            for third_computer in connections[idx + 1 :]:
                third_connections = computers_to_connections[third_computer]
                if (
                    computer in third_connections
                    and second_computer in third_connections
                ):
                    new_set = set([computer, second_computer, third_computer])
                    for s in seen:
                        if len(new_set - s) == 0:
                            break
                    else:
                        seen.append(new_set)
                        out += 1

    return out


def part2(data):
    computers_to_connections = defaultdict(list)
    for next_computer in data.split("\n"):
        one, two = next_computer.split("-")
        computers_to_connections[one].append(two)
        computers_to_connections[two].append(one)

    sets = []
    for computer, connections in computers_to_connections.items():
        new_set = set()
        new_set.add(computer)
        new_set.add(connections[0])
        for next_computer in connections[1:]:
            next_connections = computers_to_connections[next_computer]
            for comp in new_set:
                if comp not in next_connections:
                    break
            else:
                new_set.add(next_computer)
        sets.append(new_set)

    return ",".join(sorted(list(max(sets, key=len))))


measure_performance("part 1", part1, data, warmup_runs=100, actual_runs=1000)
measure_performance("part 2", part2, data, warmup_runs=100, actual_runs=1000)
