__version__ = "0.1.0"

import time
import logging
import os
import random
from functools import wraps
from multiprocessing.pool import Pool
from dataclasses import dataclass

import click
import logzero
from logzero import logger

from .impl import search


def capture_exceptions(func):
    @wraps(func)
    def __wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)

    return __wrap


# This will be hard to make dynamic - in the case of multiprocessing, we need to ensure that the new process is setup
# to log to the log file, as was done for the parent process. As we can't leverage any sort of nested function tricky
# to dynamically define our map function, this a quick hack because I don't want to handle it. We'd probably have to
# de-structure the nested functions, and pass all of the inputs as once, so something like:
#
#  def dispatch_with_logger(func, log_file, *args):
#      logzero.logfile(...)
#      func(*args)
#
#  pool.starmap(dispatch_with_logger, [(search, ctx.log_file, n, lower_bound, upper_bound) for n in number])
#
# So that child process will setup the logfile, fully dynamically. We should probably abstract that out as to not
# require it's use every. Maybe something like a Spawner that can contain data required for spawning logging child
# process:
#
#  @dataclass
#  class Spawner:
#      log_file: str
#      pool: Pool = Pool()
#
#      def starmap(function, iterables):
#          self.pool.starmap(dispatch_with_logger, [(function, self.log_file) + sub_iter for sub_iter in iterables])
#
LOG_FILE: str = "./logs/sample_tool.log"


def setup_logging(n, lower_bound, upper_bound):
    logzero.logfile(LOG_FILE, loglevel=logging.INFO)
    search(n, lower_bound, upper_bound)


@click.group()
@click.option("--log-file", "-l", help="A log file to write to", default=LOG_FILE)
def cli(log_file: str):
    if not os.path.exists(os.path.dirname(log_file)):
        logger.debug("%s does not exist -- creating.", os.path.dirname(log_file))
        os.makedirs(os.path.dirname(log_file))
    logzero.logfile(log_file, maxBytes=256 * 1e6, backupCount=3, loglevel=logging.INFO)
    logger.debug("Logging to %s", log_file)


@cli.command(name="work")
@click.argument("number", nargs=-1, type=int)
@click.option(
    "--upper-bound", "-u", help="The upper bound of randomness", default=10000
)
@click.option("--lower-bound", "-l", help="The upper bound of randomness", default=0)
@click.option(
    "--parallel/--no-parallel",
    help="Whether or not to search in parallel",
    default=False,
)
@capture_exceptions
def work(number, lower_bound, upper_bound, parallel):
    """Given a random number, look randomly until it's found."""
    logger.info("Length of input: %d", len(number))
    if parallel:
        logger.info("Running in parallel")
        pool = Pool()

        pool.starmap(setup_logging, [(n, lower_bound, upper_bound) for n in number])
        pool.close()
    else:
        for n in number:
            search(n, lower_bound, upper_bound)
