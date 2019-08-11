# Timer
## Simple Yet Convenient Timer For Python 3

### Installation
```
pip install git+https://github.com/nadavo/Timer.git
```

### Usage

##### Timer object:
```
timer_test = Timer("Timer Testing")
sleep(5)
timer_test.stop()
```
Will produce the following output:
```
<timestamp> - Started Timer Testing
<timestamp> - Timer Testing took 5.00 seconds to complete
```
##### @timer function decorator:
```
@timer
def test_timer_decorator():
    sleep(5)
```
Calling the function will produce the following output:
```
<timestamp> - Started test_timer_decorator
<timestamp> - test_timer_decorator took 5.00 seconds to complete
```
