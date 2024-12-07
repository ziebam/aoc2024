# TODO: Go from behind to prune many bad branches early on. The current solution is very
# inefficient.

from performance_utils.performance_utils import measure_performance

with open("day07/in07.txt") as in07:
    data = in07.readlines()


def should_add_to_out(nums, target, is_part_two=False):
    subtotals = [nums[0]]
    for num in nums[1:]:
        new_subtotals = []
        for subtotal in subtotals:
            if subtotal > target:
                continue
            new_subtotals.append(subtotal + num)
            new_subtotals.append(subtotal * num)
            if is_part_two:
                new_subtotals.append(int(str(subtotal) + str(num)))

            subtotals = new_subtotals

    if any([subtotal == target for subtotal in subtotals]):
        return True

    return False


def part1(data):
    out = 0
    for row in data:
        target, nums = row.split(":")
        target = int(target)
        nums = [int(num) for num in nums.split()]

        if should_add_to_out(nums, target):
            out += target

    return out


def part2(data):
    out = 0
    for row in data:
        target, nums = row.split(":")
        target = int(target)
        nums = [int(num) for num in nums.split()]

        if should_add_to_out(nums, target, is_part_two=True):
            out += target

    return out


measure_performance("part 1", part1, data, warmup_runs=100, actual_runs=1000)
measure_performance("part 2", part2, data, warmup_runs=10, actual_runs=100)
