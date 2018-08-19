from math import floor
from time import time, localtime, strftime
import logging


class Timer:
    """Simple Timer class which prints elapsed time since its creation"""

    DEFAULT_TIME_FORMAT = "%H:%M:%S"

    def __init__(self, name, logger=None):
        self.name = name
        self.logger = self.__init_logger(logger)
        self.__start_time = None
        self.__end_time = None
        self.start()

    def start(self):
        self.__start_time = time()
        self.logger.info("Started {}".format(self.name))

    def stop(self):
        self.__end_time = time()
        self.__get_elapsed__()

    def __get_elapsed__(self):
        """function to return a correctly formatted string according to time units"""
        elapsed = (self.__end_time - self.__start_time)
        unit = "seconds"
        if elapsed >= 3600:
            unit = "minutes"
            hours = elapsed / 3600
            minutes = hours % 60
            hours = floor(hours)
            self.logger.info("{} took {} hours and {:.2f} {} to complete".format(self.name, hours, minutes, unit))
        elif elapsed >= 60:
            minutes = floor(elapsed / 60)
            seconds = elapsed % 60
            self.logger.info("{} took {} minutes and {:.2f} {} to complete".format(self.name, minutes, seconds, unit))
        else:
            self.logger.info("{} took {:.2f} {} to complete".format(self.name, elapsed, unit))

    def __init_logger(self, logger):
        if logger:
            return logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.hasHandlers():
            formatter = logging.Formatter('{asctime} - {message}', datefmt="%H:%M:%S", style="{")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    @staticmethod
    def get_default_timestamp():
        return "{} -".format(strftime(Timer.DEFAULT_TIME_FORMAT, localtime(time())))
