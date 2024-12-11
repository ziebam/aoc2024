from performance_utils.performance_utils import measure_performance

with open("day11/in11.txt") as in11:
    data = in11.read().strip()


def both_parts(data, is_part_one):
    counts = {}
    for num in data.split():
        num = int(num)
        counts[num] = counts.get(num, 0) + 1

    n = 25 if is_part_one else 75
    for _ in range(n):
        next_counts = {}
        for key, value in counts.items():
            if key == 0:
                next_counts[1] = next_counts.get(1, 0) + value
            elif len(str(key)) % 2 == 1:
                n = key * 2024
                next_counts[n] = next_counts.get(n, 0) + value
            else:
                s = str(key)
                s1 = int(s[: len(s) // 2])
                s2 = int(s[len(s) // 2 :])
                next_counts[s1] = next_counts.get(s1, 0) + value
                next_counts[s2] = next_counts.get(s2, 0) + value
        counts = next_counts

    out = 0
    for value in counts.values():
        out += value

    return out


measure_performance("part 1", both_parts, data, True)
measure_performance(
    "part 2", both_parts, data, False, warmup_runs=100, actual_runs=1000
)
