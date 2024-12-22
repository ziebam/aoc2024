from collections import defaultdict, deque

from performance_utils.performance_utils import measure_performance

with open("day22/in22.txt") as in22:
    data = [int(line) for line in in22.readlines()]


def part1(data):
    out = 0
    for secret in data:
        new_secret = secret
        for _ in range(2000):
            new_secret = ((new_secret * 64) ^ new_secret) % 16777216
            new_secret = ((new_secret // 32) ^ new_secret) % 16777216
            new_secret = ((new_secret * 2048) ^ new_secret) % 16777216
        out += new_secret

    return out


def part2(data):
    seqs_to_bananas = defaultdict(lambda: 0)
    for secret in data:
        new_secret = secret
        bananas = int(str(secret)[-1])
        sequence = deque()
        seen_sequences = set()
        for _ in range(2000):
            # The current sequence is long enough (4) and...
            if len(sequence) == 4:
                t_sequence = tuple(sequence)
                # ...and we haven't seen it yet while calculating this number.
                if t_sequence not in seen_sequences:
                    seqs_to_bananas[t_sequence] += bananas
                seen_sequences.add(t_sequence)

            # Calcualte the next number in the same way as in part 1.
            new_secret = ((new_secret * 64) ^ new_secret) % 16777216
            new_secret = ((new_secret // 32) ^ new_secret) % 16777216
            new_secret = ((new_secret * 2048) ^ new_secret) % 16777216

            # Recalculate the current sequence.
            new_bananas = int(str(new_secret)[-1])
            sequence.append(new_bananas - bananas)
            if len(sequence) > 4:
                sequence.popleft()
            bananas = new_bananas

    highest = 0
    for sequence, bananas in seqs_to_bananas.items():
        if bananas > highest:
            highest = bananas

    return highest


measure_performance("part 1", part1, data, warmup_runs=10, actual_runs=100)
measure_performance("part 2", part2, data, warmup_runs=1, actual_runs=10)
