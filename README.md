# fcollections

A Python library that provides enhanced collection classes with method chaining capabilities. fcollections wraps functionality from cytoolz and itertools as methods of collection classes, enabling a fluent functional programming style.

## Features

- Method chaining for cleaner, more readable code
- Enhanced collection types (flist, fgenerator, fdict)
- Functional programming utilities built into collection objects
- Integration with cytoolz and itertools
- Sliding window operations, partitioning, and grouping

## Installation

```bash
pip install fcollections
```

## Dependencies

- Python 2.7 or Python 3.x
- cytoolz

## Basic Usage

### Creating Collections

```python
from fcollections import flist, fgenerator, fdict, frange, fxrange

# Creating from existing collections
my_list = flist([1, 2, 3, 4, 5])
my_generator = fgenerator(x for x in range(10))
my_dict = fdict({'a': 1, 'b': 2, 'c': 3})

# Using utility functions
nums = frange(10)  # flist containing [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
nums_gen = fxrange(10)  # fgenerator containing values 0-9
```

### Method Chaining

```python
from fcollections import frange

# Chain methods together for cleaner code
result = frange(10).map(lambda x: x * 2).filter(lambda x: x > 5).to_list()
# Result: [6, 8, 10, 12, 14, 16, 18]
```

## Core Collection Types

### flist

An enhanced list with method chaining for common operations.

```python
from fcollections import flist

data = flist([1, 2, 3, 4, 5])
result = data.map(lambda x: x * 2).filter(lambda x: x > 5).to_list()
```

### fgenerator

A generator wrapper with method chaining that maintains lazy evaluation.

```python
from fcollections import fgenerator

gen = fgenerator(x for x in range(10))
result = gen.map(lambda x: x * 2).filter(lambda x: x > 5).take(3).to_list()
# Result: [6, 8, 10]
```

### fdict

An enhanced dictionary with functional operations.

```python
from fcollections import fdict

data = fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
evens = data.valfilter(lambda v: v % 2 == 0)  # fdict({'b': 2, 'd': 4})
```

## Advanced Features

### Partitioning and Grouping

```python
from fcollections import frange

nums = frange(10)

# Partitioning
chunks = nums.partition(3).to_list()  # flist([flist([0, 1, 2]), flist([3, 4, 5]), flist([6, 7, 8])])

# Grouping by a function
by_parity = nums.groupby(lambda x: 'even' if x % 2 == 0 else 'odd')
# Result: {'even': [0, 2, 4, 6, 8], 'odd': [1, 3, 5, 7, 9]}
```

### Sliding Window and Other Operations

```python
from fcollections import frange

nums = frange(10)

# Sliding window
windows = nums.sliding_window(3).to_list()  # flist([flist([0, 1, 2]), flist([1, 2, 3]), ...])

# Other operations
unique_values = flist([1, 2, 2, 3, 3, 3]).unique()  # flist([1, 2, 3])
top_values = nums.top_k(3)  # flist([9, 8, 7])
```

### Complex Method Chaining

```python
from fcollections import frange

# Complex processing with method chaining
result = (frange(100)
    .partition(10)  # Split into chunks of 10
    .map(lambda l: flist(l * 3))  # Repeat each chunk 3 times
    .reduce(lambda a, b: flist(a + b))  # Combine all chunks
    .reduce(lambda a, b: a + b))  # Sum all values
```

### Pipe Operations

```python
from fcollections import frange
import numpy as np

data = frange(10)

# Pipe data through a sequence of functions
std_dev = data.pipe(lambda x: x * 3, np.asarray, np.std)

# Apply multiple functions to each element
adjusted = data.pipe_map(lambda x: x - 4, lambda x: x + 4, lambda x: x * 2)
```

## Feedback and Suggestions

We value your input! If you have ideas for new features, improvements, or encounter any issues, please share them with us:

- **Feature Requests**: Open an issue with the label `enhancement` to suggest new functionality
- **Bug Reports**: Submit issues with the label `bug` to report problems
- **General Feedback**: Use the label `feedback` for general thoughts and suggestions
- **Help Wanted**: Look for issues labeled `help wanted` if you'd like to contribute to specific areas

Your feedback directly influences the development roadmap and helps make fcollections more useful for everyone.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. **Code Contributions**: Fork the repository and submit pull requests for new features or bug fixes
2. **Documentation**: Help improve or expand the documentation
3. **Testing**: Add tests or identify testing gaps
4. **Feedback**: Share your experience using fcollections (see [Feedback and Suggestions](#feedback-and-suggestions))

Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/PilCAki/fcollections).