from math import floor
from typing import Optional
from time import localtime, strftime
from timeit import default_timer
import logging
import functools


class Timer:
    """
    Simple (Yet Convenient) Timer class which logs elapsed runtime for any arbitrary piece of code
    """

    DEFAULT_TIME_FORMAT = "%H:%M:%S"

    def __init__(
        self,
        name: str,
        log_level: int = logging.INFO,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initializes the Timer object.

        Args:
            name (str): The name of the timer.
            log_level (int, optional): The logging level. Defaults to logging.INFO.
            logger (Optional[logging.Logger], optional): A logger instance. Defaults to None.
        """
        self.name = name
        self.log_level = log_level
        self.logger = self.init_logger(logger, log_level, name)
        self._start_time = self._start()
        self._end_time = None
        self.elapsed = None

    def __enter__(self):
        """Starts the timer upon entering the context."""
        return self

    def __exit__(self, var_type, value, traceback):
        """Stops the timer upon exiting the context."""
        self.stop()

    def _start(self) -> float:
        """Starts the timer and logs the start time."""
        self.logger.log(msg=f"Started Timer for {self.name}", level=self.log_level)
        return default_timer()

    def _format_elapsed_msg(self) -> str:
        """
        Internal function which correctly formats a log message according to elapsed time units
        """
        unit = "seconds"
        if self.elapsed >= 3600.0:
            unit = "minutes"
            hours = floor(self.elapsed / 3600.0)
            minutes = (self.elapsed % 3600.0) / 60.0
            log_message = (
                f"{self.name} took {hours} hours and {minutes:.2f} {unit} to complete"
            )
        elif self.elapsed >= 60.0:
            minutes = floor(self.elapsed / 60.0)
            seconds = self.elapsed % 60.0
            log_message = f"{self.name} took {minutes} minutes and {seconds:.2f} {unit} to complete"
        elif self.elapsed < 0.1:
            unit = "ms"
            log_message = (
                f"{self.name} took {self.elapsed * 1000.:.2f} {unit} to complete"
            )
        else:
            log_message = f"{self.name} took {self.elapsed:.2f} {unit} to complete"
        return log_message

    def stop(self) -> None:
        """Stops the timer, calculates the elapsed time, and logs the result."""
        self._end_time = default_timer()
        self.elapsed = self._end_time - self._start_time
        self.logger.log(msg=self._format_elapsed_msg(), level=self.log_level)

    @staticmethod
    def init_logger(
        logger: Optional[logging.Logger] = None,
        level: int = logging.INFO,
        name: str = __name__,
    ) -> logging.Logger:
        """
        Initializes and returns a logger.

        If a logger is provided, it is returned as is. Otherwise, a new logger
        is created with a stream handler if it doesn't have any handlers.

        Args:
            logger (Optional[logging.Logger], optional): An existing logger. Defaults to None.
            level (int, optional): The logging level for a new logger. Defaults to logging.INFO.
            name (str, optional): The name for a new logger. Defaults to __name__.

        Returns:
            logging.Logger: The initialized logger.
        """
        if logger is None:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            if not logger.handlers:
                formatter = logging.Formatter(
                    "{levelname} - {asctime} - {message}",
                    datefmt=Timer.DEFAULT_TIME_FORMAT,
                    style="{",
                )
                handler = logging.StreamHandler()
                handler.setFormatter(formatter)
                logger.addHandler(handler)
        return logger

    @staticmethod
    def get_default_timestamp() -> str:
        """Returns a timestamp string in the default format."""
        return f"{strftime(Timer.DEFAULT_TIME_FORMAT, localtime(default_timer()))} -"


def timer(
    _args=None,
    *,
    name: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    log_level: Optional[int] = logging.INFO,
):
    """
    Timer decorator which utilizes a Timer object for timing a given function's runtime
    """

    def timer_decorator(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            if name is None:
                timer_name = func.__name__
            else:
                timer_name = name
            timer_wrapper = Timer(name=timer_name, logger=logger, log_level=log_level)
            func_ret_val = func(*args, **kwargs)
            timer_wrapper.stop()
            return func_ret_val

        return wrapper_timer

    if _args is None:
        return timer_decorator
    else:
        return timer_decorator(_args)
