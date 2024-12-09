from performance_utils.performance_utils import measure_performance

with open("day09/in09.txt") as in09:
    data = in09.read().strip()


def part1(data):
    sectors = [int(sector) for sector in data]

    # This would be needed in case the input wasn't always of an odd length.
    # back_pointer = len(sectors) - 1 if len(sectors) % 2 == 1 else len(sectors) - 2
    back_pointer = len(sectors) - 1
    i = out = 0
    for idx, sector in enumerate(sectors):
        if idx % 2 == 0:
            for _ in range(sectors[idx]):
                out += (idx // 2) * i
                i += 1
        else:
            for _ in range(sector):
                out += (back_pointer // 2) * i
                i += 1

                sectors[back_pointer] -= 1
                if sectors[back_pointer] == 0:
                    back_pointer -= 2

        if idx >= back_pointer:
            break

    return out


def part2(data):
    sectors = [int(sector) for sector in data]
    n = len(sectors)

    placed = set()
    i = out = 0
    for idx, sector in enumerate(sectors):
        if idx % 2 == 0 and (id := idx // 2) not in placed:
            for _ in range(sector):
                out += id * i
                i += 1
            placed.add(id)
        else:
            for j in range(n - 1, idx, -2):
                if sectors[j] <= sector and (id := j // 2) not in placed:
                    for _ in range(sectors[j]):
                        out += id * i
                        i += 1
                    placed.add(id)

                    sector -= sectors[j]
                    if not sector:
                        break
            for _ in range(sector):
                i += 1

        if len(placed) == (n // 2) + 1:
            break

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data, warmup_runs=10, actual_runs=100)
