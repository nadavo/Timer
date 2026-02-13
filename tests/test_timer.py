import pytest
from time import sleep
from syct import Timer, timer
import logging

# It's better to have a small tolerance for timing tests
# as the execution time can vary slightly.
TOLERANCE = 0.1  # 10% tolerance

def test_timer_class():
    """Tests the Timer class basic functionality."""
    sleep_time = 1
    t = Timer("test_timer_class")
    sleep(sleep_time)
    t.stop()
    assert t.elapsed is not None
    assert sleep_time <= t.elapsed <= sleep_time + TOLERANCE

def test_timer_context_manager():
    """Tests the Timer class as a context manager."""
    sleep_time = 1
    with Timer("test_timer_context_manager") as t:
        sleep(sleep_time)
    assert t.elapsed is not None
    assert sleep_time <= t.elapsed <= sleep_time + TOLERANCE

def test_timer_decorator_no_args():
    """Tests the timer decorator without arguments."""
    sleep_time = 1
    @timer
    def decorated_function():
        sleep(sleep_time)
        return "done"

    result = decorated_function()
    assert result == "done"
    # We can't directly access the timer object here,
    # but we can check the log output.

def test_timer_decorator_with_args(caplog):
    """Tests the timer decorator with arguments."""
    sleep_time = 1
    timer_name = "test_decorator_with_args"

    @timer(name=timer_name, log_level=logging.WARNING)
    def decorated_function():
        sleep(sleep_time)
        return "done"

    with caplog.at_level(logging.WARNING):
        result = decorated_function()

    assert result == "done"
    assert timer_name in caplog.text
    assert "took" in caplog.text
    assert "WARNING" in caplog.text

def test_format_ms(caplog):
    """Tests the millisecond formatting of the log message."""
    sleep_time = 0.01  # 10 ms
    with caplog.at_level(logging.INFO):
        with Timer("test_format_ms") as t:
            sleep(sleep_time)

    assert "ms" in caplog.text
    assert t.elapsed is not None
    assert sleep_time <= t.elapsed <= sleep_time + TOLERANCE

def test_format_seconds(caplog):
    """Tests the seconds formatting of the log message."""
    sleep_time = 1
    with caplog.at_level(logging.INFO):
        with Timer("test_format_seconds") as t:
            sleep(sleep_time)

    assert "seconds" in caplog.text
    assert t.elapsed is not None
    assert sleep_time <= t.elapsed <= sleep_time + TOLERANCE

def test_format_minutes(caplog):
    """Tests the minutes formatting of the log message."""
    # We don't want to wait for 60 seconds, so we can cheat by setting the elapsed time manually.
    with caplog.at_level(logging.INFO):
        t = Timer("test_format_minutes")
        t.elapsed = 70  # 1 minute 10 seconds
        t.logger.log(msg=t._format_elapsed_msg(), level=t.log_level)

    assert "minutes" in caplog.text
    assert "1 minutes and 10.00 seconds" in caplog.text

def test_format_hours(caplog):
    """Tests the hours formatting of the log message."""
    with caplog.at_level(logging.INFO):
        t = Timer("test_format_hours")
        t.elapsed = 3670  # 1 hour 1 minute 10 seconds
        t.logger.log(msg=t._format_elapsed_msg(), level=t.log_level)

    assert "hours" in caplog.text
    assert "1 hours and 1.17 minutes" in caplog.text

def test_custom_logger(caplog):
    """Tests using a custom logger."""
    custom_logger = logging.getLogger("custom_test_logger")
    custom_logger.setLevel(logging.DEBUG)

    with caplog.at_level(logging.DEBUG, logger="custom_test_logger"):
        with Timer("test_custom_logger", logger=custom_logger, log_level=logging.DEBUG):
            sleep(0.01)

    assert "test_custom_logger" in caplog.text
    assert "DEBUG" in caplog.text


def test_init_logger_no_logger_provided():
    """Tests that a new logger is created when none is provided."""
    logger = Timer.init_logger(name="new_logger", level=logging.DEBUG)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "new_logger"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    # Clean up handlers to avoid affecting other tests
    logger.handlers = []

def test_init_logger_with_existing_logger():
    """Tests that an existing logger is returned unmodified."""
    existing_logger = logging.getLogger("existing_logger")
    existing_logger.setLevel(logging.WARNING)
    returned_logger = Timer.init_logger(logger=existing_logger)
    assert returned_logger is existing_logger
    assert returned_logger.level == logging.WARNING

def test_init_logger_does_not_add_handler_if_one_exists():
    """Tests that a handler is not added if the logger already has one."""
    logger = logging.getLogger("handler_test_logger")
    logger.addHandler(logging.NullHandler())
    assert len(logger.handlers) == 1
    Timer.init_logger(logger=logger)
    assert len(logger.handlers) == 1
    # Clean up handlers
    logger.handlers = []
