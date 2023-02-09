import time
import timeit
from multiprocessing import Process, current_process
from multiprocessing import Array as mp_array

import math
# import numpy as np
import random
import logging.config
from typing import Callable, Tuple
from math import log10

from DMAD.Logging.logging_config import config_dict

logging.config.dictConfig(config_dict)

log = logging.getLogger(__name__)


def _brute_force(max_val: int, func: Callable[[int], float], startvalue: int, stepsize: int) -> tuple[int, int]:
    n = startvalue
    time = func(n)
    prev_n = 1
    while time < max_val:
        prev_n = n
        n += stepsize
        time = func(n)

    return n - 1, prev_n


def accelerated_search(max_val: int, func: Callable[[int], float]) -> int:
    n = 1
    time = func(n)
    prev_n = 1
    while time < max_val:
        prev_n = n
        n += n
        time = func(n)

    step_size = (n - prev_n) // 10
    while step_size > 1000:
        n, prev_n = _brute_force(max_val, func, prev_n, step_size)
        step_size = (n - prev_n) // 100

    return _brute_force(max_val, func, prev_n, 1)[0]


def fac(n: int) -> int:
    return n * fac(n - 1) if n > 2 else 2


def task1():
    # Create an output table of how large n can be for the function to still complete in less than x time
    # Assume that one unit of work takes 1 ns to complete
    # print(type(brute_force))

    times = {
        "one second": 10 ** 9,
        "one minute": 60 * 10 ** 9,
        "one hour": 60 * 60 * 10 ** 9,
        "one day": 24 * 60 * 60 * 10 ** 9,
        "one month": 30 * 24 * 60 * 60 * 10 ** 9,
        "one year": 365 * 24 * 60 * 60 * 10 ** 9,
        "one century": 1000 * 365 * 24 * 60 * 60 * 10 ** 9,

    }

    non_brute_functions = {
        "fac": fac,
        "2**n": (lambda x: 2 ** x),
        "n**3": (lambda x: x ** 3),
        "n**2": (lambda x: x ** 2),
        "n * log n": (lambda x: x * log10(x)),
        "n": (lambda x: x),
        "sqrt": math.sqrt,
        # "log": log10,
    }

    for key, val in non_brute_functions.items():
        print(key)
        for time, ns in times.items():
            print(f"{time}: {accelerated_search(ns, val)}")

    print(f"log")
    for time, ns in times.items():
        print(f"{time}: 10**{ns} - 1")


def count_cycles(input_list: list[int]) -> int:
    cycles = [0 for _ in input_list]
    number_of_cycles = 0

    for i, n in enumerate(input_list):
        # put the number in the cycle array
        # increment the number of cycles if the thing is already in cycles
        log.debug(f"n: {n}, i {i}")
        if cycles[i] == 1:
            log.debug("skipping")
            continue

        while cycles[n] != 1:
            cycles[n] = 1
            n = input_list[n]
            log.debug(f"while looping: n: {n}, ")

        log.debug("increment")
        number_of_cycles += 1

    return number_of_cycles


def permutation_generator(n: int) -> list:
    output = [x for x in range(n)]
    random.shuffle(output)

    return output


def task4():
    p = permutation_generator(10)
    p = [2, 6, 0, 3, 1, 4, 5]
    log.info(p)
    count = count_cycles(p)
    log.info(count)


def taskb_2():
    size = 16
    runs = 10_000_000

    num_processes = 8

    def run_counts(my_size: int, my_runs: int, output: mp_array):
        process_name = current_process().name
        print(process_name)

        for _ in range(my_runs):
            calculated_count = count_cycles(permutation_generator(my_size))
            output[calculated_count] += 1

    processes = []
    results = []

    for _ in range(num_processes):
        r = mp_array('i', size + 1)
        p = Process(target=run_counts, args=(size, runs // num_processes, r))
        processes.append(p)
        results.append(r)
        p.start()

    for process in processes:
        process.join()

    counts = [0 for _ in range(size + 1)]

    for count in results:
        for i, x in enumerate(count):
            counts[i] += x

    for i, x in enumerate(counts):
        print(f"{i}: {x} - {round((x / runs) * 100)}%")


if __name__ == '__main__':
    # task4()
    # task1()
    start = time.perf_counter_ns()
    taskb_2()
    end = time.perf_counter_ns()
    print(f"Elapsed time: {(end - start) // 10**9} s")

