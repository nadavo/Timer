from time import sleep
from Timer import Timer


def test_Timer():
    test = Timer("Timer Testing")
    sleep(5)
    test.stop()


if __name__ == "__main__":
    test_Timer()
