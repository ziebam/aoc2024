import timeit


def measure_performance(
    name, func, *args, unit="milliseconds", warmup_runs=1000, actual_runs=10000
):
    warmup_start = timeit.default_timer()

    for _ in range(warmup_runs):
        func(*args)
    warmup_end = timeit.default_timer()
    print(
        f"Finished {warmup_runs} warmup runs for {name} in ~{(warmup_end - warmup_start):.2f} seconds."
    )

    starts = []
    ends = []
    for _ in range(actual_runs):
        starts.append(timeit.default_timer())
        answer = func(*args)
        ends.append(timeit.default_timer())

    m = {"milliseconds": 1000, "microseconds": 1000000, "nanoseconds": 1000000000}
    print(
        f"{name.capitalize()} answer: \033[92m{answer}\x1b[0m. Ran {actual_runs} times in ~{(sum(ends) / len(starts) - sum(starts) / len(starts)) * m[unit]:.2f} {unit} on average.\n"
    )
