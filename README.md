# Simple Yet Convenient Timer for Python 3

### Installation
```
pip install syct
```

### Common Usage

#### Wrap a function with the `@timer` function decorator:
```
from syct import timer

@timer
def test_timer_decorator():
    sleep(5)
```
Calling the function will produce the following output:
```
<timestamp> - Started test_timer_decorator
<timestamp> - test_timer_decorator took 5.00 seconds to complete
```

#### Wrap a block of code using `with Timer`:
```
from syct import Timer

with Timer("with Timer block"):
    sleep(1)
    sleep(1)
    sleep(1)
    sleep(1)
    sleep(1)
```
Will produce the following output:
```
<timestamp> - Started with Timer block
<timestamp> - with Timer block took 5.00 seconds to complete
```

#### Create a custom `Timer` object in your code:
```
from syct import Timer

timer_test = Timer("Timer Testing")
sleep(5)
timer_test.stop()
```
Will produce the following output:
```
<timestamp> - Started Timer Testing
<timestamp> - Timer Testing took 5.00 seconds to complete
```