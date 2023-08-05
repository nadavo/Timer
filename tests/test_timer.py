from time import sleep
from src.syct import Timer, timer
import logging


def test_Timer_object():
    test = Timer("Timer Testing")
    sleep(2)
    test.stop()


@timer
def test_timer_fn_decorator():
    sleep(2)


@timer(name="Timer fn Decorator Args Testing", log_level=logging.DEBUG)
def test_timer_fn_decorator_args():
    sleep(2)


def test_Timer_ms():
    test = Timer("Timer Testing (ms)")
    sleep(0.002)
    test.stop()


def test_Timer_with():
    with Timer("with Timer block Testing"):
        sleep(1)
        sleep(1)


def run_all_tests():
    test_Timer_object()
    test_timer_fn_decorator()
    test_timer_fn_decorator_args()
    test_Timer_ms()
    test_Timer_with()


if __name__ == "__main__":
    run_all_tests()
