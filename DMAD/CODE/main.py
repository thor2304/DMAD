import random
import logging.config

from DMAD.Logging.logging_config import config_dict

logging.config.dictConfig(config_dict)

log = logging.getLogger(__name__)


def permutation_generator(n: int) -> list:
    output = [x for x in range(n)]
    random.shuffle(output)

    return output


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


def task4():
    p = permutation_generator(10)
    # p = [2, 3, 1, 4, 5]
    log.info(p)
    count = count_cycles(p)
    log.info(count)


if __name__ == '__main__':
    task4()
