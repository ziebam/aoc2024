# Advent of Code 2024

This repository contains my solutions for [Advent of Code 2024](https://adventofcode.com/2024).

The solution require Python 3.10+ (due to the usage of
[pattern matching](https://peps.python.org/pep-0634/)). Other than that there are no dependencies.

To run the given solution, use `python dayXX/dayXX.py` from the root of the repository, where `XX`
is the day number padded with a leading zero for days 1-9.

Benchmarking code does warmup runs as I sometimes tested the performance using PyPy, whose JIT can
benefit from those.
