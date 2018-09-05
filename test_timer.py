from time import sleep
from Timer import Timer, timer


def test_Timer():
    test = Timer("Timer Testing")
    sleep(5)
    test.stop()


@timer
def test_timer_decorator():
    sleep(5)


@timer(name="Timer Decorator Testing")
def test_timer_decorator_args():
    sleep(5)


if __name__ == "__main__":
    test_Timer()
    test_timer_decorator()
    test_timer_decorator_args()

