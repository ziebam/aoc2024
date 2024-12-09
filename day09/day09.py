# TODO: Improve this. The approach seems incorrect given how slow it is, and part 2 is a mess.

from performance_utils.performance_utils import measure_performance

with open("day09/in09.txt") as in09:
    data = in09.read().strip()


def part1(data):
    n_sectors = len(data)

    pointer = n_sectors - 1 if n_sectors % 2 == 1 else n_sectors - 2
    disk = []
    sizes = [int(sector) for sector in data]
    for idx, sector in enumerate(data):
        if idx % 2 == 0:
            for _ in range(sizes[idx]):
                disk.append(idx // 2)
        else:
            count = sizes[pointer]
            for _ in range(int(sector)):
                disk.append(pointer // 2)
                count -= 1
                sizes[pointer] -= 1
                if count == 0:
                    pointer -= 2
                    if idx >= pointer:
                        break
                    count = sizes[pointer]

        if idx >= pointer:
            break

    out = 0
    for idx, block in enumerate(disk):
        out += idx * block

    return out


def part2(data):
    disk = []
    for idx, sector in enumerate(data):
        if idx % 2 == 0:
            for _ in range(int(sector)):
                disk.append(idx // 2)
        else:
            for _ in range(int(sector)):
                disk.append(".")

    orig_file_sizes = [int(size) for size in data[::2]]
    file_sizes = orig_file_sizes[::]
    empty_sizes = [int(size) for size in data[1::2]]
    pointer = file_sizes[0]
    for idx, empty_size in enumerate(empty_sizes):
        # TODO: Don't reverse the list every iteration.
        for jdx, file_size in enumerate(file_sizes[::-1]):
            if len(file_sizes) - 1 - jdx <= idx:
                pointer += empty_size
                break

            if empty_size == 0:
                break

            if 0 < file_size <= empty_size:
                try:
                    # TODO: Find the first occurence and replace based on the block size.
                    while file_to_move_idx := disk.index(len(file_sizes) - 1 - jdx):
                        disk[file_to_move_idx] = "."
                except ValueError:
                    pass

                for _ in range(file_size):
                    disk[pointer] = len(file_sizes) - 1 - jdx
                    pointer += 1
                    empty_size -= 1
                file_sizes[len(file_sizes) - 1 - jdx] = 0

        pointer += orig_file_sizes[idx + 1]

    out = 0
    for idx, block in enumerate(disk):
        if block == ".":
            continue
        out += idx * block

    return out


measure_performance("part 1", part1, data)
print(
    f"Part 2 answer: \033[92m{part2(data)}\x1b[0m. Too slow for performance measurement.\n"
)
