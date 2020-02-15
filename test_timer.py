from time import sleep
from Timer import Timer, timer


def test_Timer():
    test = Timer("Timer Testing")
    sleep(2)
    test.stop()


@timer
def test_timer_decorator():
    sleep(2)


@timer(name="Timer Decorator Args Testing")
def test_timer_decorator_args():
    sleep(2)


def test_Timer_ms():
    test = Timer("Timer Testing (ms)")
    sleep(0.0007)
    test.stop()


if __name__ == "__main__":
    test_Timer()
    test_timer_decorator()
    test_timer_decorator_args()
    test_Timer_ms()

