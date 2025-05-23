# fcollections

fcollections is a Python library that enhances standard collection classes with method chaining capabilities. By wrapping functionality from cytoolz and itertools as methods of collection classes, fcollections enables a fluent functional programming style in Python.

## Features

- **Method Chaining**: Write cleaner, more readable code by chaining operations
- **Enhanced Collections**: Use improved versions of standard collections (flist, fgenerator, fdict)
- **Functional Utilities**: Access common functional programming patterns directly from collection objects
- **Seamless Integration**: Works with cytoolz and itertools functionality
- **Performance**: Maintain lazy evaluation when appropriate for better performance

## Installation

```bash
pip install fcollections
```

## Quick Start

```python
from fcollections import flist, frange

# Create a collection
numbers = frange(10)

# Chain methods for clean, readable transformations
result = (numbers
    .map(lambda x: x * 3)
    .filter(lambda x: x % 2 == 0)
    .take(3)
    .to_list())

print(result)  # [0, 6, 12]
```

## Collection Types

### flist

An enhanced list with functional operations and method chaining:

```python
from fcollections import flist

data = flist([1, 2, 3, 4, 5])
result = data.map(lambda x: x * 2).filter(lambda x: x > 5)
print(result)  # flist([6, 8, 10])
```

### fgenerator

A generator wrapper that preserves lazy evaluation while adding functional methods:

```python
from fcollections import fgenerator

gen = fgenerator(x for x in range(1000))
# Operations happen lazily - nothing is computed yet
pipeline = gen.map(lambda x: x * 2).filter(lambda x: x % 10 == 0)
# Only compute the first 5 values
print(pipeline.take(5).to_list())  # flist([0, 20, 40, 60, 80])
```

### fdict

A dictionary with enhanced functionality:

```python
from fcollections import fdict

data = fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
# Filter values
evens = data.valfilter(lambda v: v % 2 == 0)
print(evens)  # fdict({'b': 2, 'd': 4})
```

## Common Operations

### Transformation

```python
from fcollections import flist

# Map transformation
doubled = flist([1, 2, 3]).map(lambda x: x * 2)  # flist([2, 4, 6])

# Filter elements
evens = flist(range(10)).filter(lambda x: x % 2 == 0)  # flist([0, 2, 4, 6, 8])

# Reduce to a single value
total = flist([1, 2, 3, 4]).reduce(lambda a, b: a + b)  # 10
```

### Grouping and Partitioning

```python
from fcollections import frange

data = frange(10)

# Partition into chunks of specific size
chunks = data.partition(3).to_list()  # [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Group by a key function
grouped = data.groupby(lambda x: 'even' if x % 2 == 0 else 'odd')
# {'even': [0, 2, 4, 6, 8], 'odd': [1, 3, 5, 7, 9]}
```

### Advanced Operations

```python
from fcollections import frange

# Sliding window
windows = frange(5).sliding_window(2).to_list()  # [[0, 1], [1, 2], [2, 3], [3, 4]]

# Top K elements
top3 = frange(10).top_k(3)  # [9, 8, 7]

# Unique elements
unique = flist([1, 1, 2, 2, 3]).unique()  # [1, 2, 3]
```

## Feedback and Suggestions

We value your input and would love to hear about your experience using fcollections. Your feedback directly influences the development roadmap and helps make the library more useful for everyone.

### Ways to Contribute Feedback

- **Feature Requests**: Open an issue with the label `enhancement` to suggest new functionality
- **Bug Reports**: Submit issues with the label `bug` when you encounter problems
- **General Feedback**: Use the label `feedback` for general thoughts and suggestions
- **Help Wanted**: Look for issues labeled `help wanted` if you'd like to contribute

### Submitting Feedback

1. Visit the [GitHub Issues page](https://github.com/PilCAki/fcollections/issues)
2. Click "New Issue"
3. Select the appropriate template or start from scratch
4. Apply relevant labels
5. Provide as much detail as possible about your suggestion or the problem you're experiencing

Your feedback helps us prioritize development efforts and identify areas that need improvement.

## Contributing

Contributions to fcollections are welcome! Here's how you can contribute:

1. **Code Contributions**: Fork the repository, make your changes, and submit a pull request
2. **Documentation**: Help improve this README or add more examples
3. **Testing**: Add tests to improve coverage or identify edge cases
4. **Ideas**: Share your thoughts on how fcollections could be improved (see Feedback section)

For more details, please see our [Contributing Guidelines](https://github.com/PilCAki/fcollections).

## License

fcollections is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contact

- GitHub: [PilCAki/fcollections](https://github.com/PilCAki/fcollections)
- Author: Phillip Adkins