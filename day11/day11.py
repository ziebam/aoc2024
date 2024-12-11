# TODO: Part 2. It's probably something to do with individual digits as every number eventually
# converges to one or more of them (Collatz conjecture at home), and they have repeatable results
# after each iteration.

with open("day11/in11.txt") as in11:
    data = in11.read().strip()


def part1(data):
    nums = [int(num) for num in data.split()]

    for _ in range(25):
        new = []
        for num in nums:
            if num == 0:
                new.append(1)
            elif len(str(num)) % 2 == 1:
                new.append(num * 2024)
            else:
                snum = str(num)
                new.append(int(snum[: len(snum) // 2]))
                new.append(int(snum[len(snum) // 2 :]))

        nums = new

    return len(nums)


print(part1(data))
