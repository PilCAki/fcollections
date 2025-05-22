# fcollections

![Tests](https://github.com/PilCAki/fcollections/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/PilCAki/fcollections/branch/master/graph/badge.svg)](https://codecov.io/gh/PilCAki/fcollections)

Collections with method chaining for Python.

## Overview

fcollections provides collections with functional programming operations and method chaining for Python.

- `flist` - A list that returns `flist` for operations when it makes sense
- `fgenerator` - A generator that returns `fgenerator` for operations when it makes sense
- `fdict` - A dictionary with additional functional operations

## Installation

```bash
pip install fcollections
```

## Usage

```python
from fcollections import flist, frange, fdict, fgenerator

# Create a list
a = frange(10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Method chaining
result = (
    a.filter(lambda x: x % 2 == 0)  # Keep even numbers
     .map(lambda x: x * 3)           # Multiply by 3
     .reduce(lambda a, b: a + b)     # Sum them up
)
print(result)  # 72

# Working with dictionaries
d = fdict({'a': 1, 'b': 2, 'c': 3})
result = d.valmap(lambda x: x * 10)
print(result)  # {'a': 10, 'b': 20, 'c': 30}
```

## Testing

To run the tests:

```bash
pip install pytest pytest-cov
pytest --cov=fcollections tests/
```

## License

GNU General Public License v3.0