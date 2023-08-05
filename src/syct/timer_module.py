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
        self.name = name
        self.log_level = log_level
        self.logger = self.init_logger(logger, log_level, name)
        self._start_time = self._start()
        self._end_time = None

    def __enter__(self):
        return self

    def __exit__(self, var_type, value, traceback):
        self.stop()

    def _start(self) -> float:
        self.logger.log(msg=f"Started Timer for {self.name}", level=self.log_level)
        return default_timer()

    def _format_elapsed_msg(self) -> str:
        """
        Internal function which correctly formats a log message according to elapsed time units
        """
        elapsed = self._end_time - self._start_time
        unit = "seconds"
        if elapsed >= 3600.0:
            unit = "minutes"
            hours = elapsed / 3600.0
            minutes = hours % 60.0
            hours = floor(hours)
            log_message = (
                f"{self.name} took {hours} hours and {minutes:.2f} {unit} to complete"
            )
        elif elapsed >= 60.0:
            minutes = floor(elapsed / 60.0)
            seconds = elapsed % 60.0
            log_message = f"{self.name} took {minutes} minutes and {seconds:.2f} {unit} to complete"
        elif elapsed < 0.1:
            unit = "ms"
            log_message = f"{self.name} took {elapsed * 1000.:.2f} {unit} to complete"
        else:
            log_message = f"{self.name} took {elapsed:.2f} {unit} to complete"
        return log_message

    def stop(self) -> None:
        self._end_time = default_timer()
        self.logger.log(msg=self._format_elapsed_msg(), level=self.log_level)

    @staticmethod
    def init_logger(
        logger: Optional[logging.Logger] = None,
        level: int = logging.INFO,
        name: str = __name__,
    ) -> logging.Logger:
        if logger is None:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            if not logger.hasHandlers():
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
