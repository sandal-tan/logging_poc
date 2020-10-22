import random

from logzero import logger


def search(number, lower_bound, upper_bound):
    """Given a random number, look randomly until it's found.

    Args:
        number: The number to search for
        bound: The upper bound of randomness

    """
    logger.info("Start looking for %d", number)
    if not lower_bound <= number <= upper_bound:
        raise RuntimeError(f"Given number must be in [{lower_bound}, {upper_bound}]")
    while True:
        guess = random.randint(lower_bound, upper_bound)
        if guess == number:
            logger.info("Found %d!", number)
            break
        if number % guess == 0:
            logger.warning("Found perfect divisor of %d: %d", number, guess)
