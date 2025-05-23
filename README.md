# fcollections


[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/fcollections.svg)](https://pypi.org/project/fcollections/)
![Tests](https://github.com/PilCAki/fcollections/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/PilCAki/fcollections/branch/master/graph/badge.svg)](https://codecov.io/gh/PilCAki/fcollections)

> **Elegant method chaining for Python collections**
>
> `data.filter(...).map(...).reduce(...)`

## Showcase: The Power of Method Chaining

```python
from fcollections import frange, flist
import numpy as np

# Data processing pipeline - all in one fluid expression
result = (frange(100)
    .filter(lambda x: x % 3 == 0)                  # Keep multiples of 3
    .map(lambda x: x ** 2)                         # Square each value
    .partition(5)                                  # Group into chunks of 5
    .map(lambda chunk: chunk.reduce(lambda a, b: a + b))  # Sum each chunk
    .filter(lambda x: x > 1000)                    # Filter sums > 1000
    .pipe(np.array, np.mean))                      # Convert to numpy array and calculate mean

# Text processing with chaining
sentences = flist(["hello world", "python is great", "functional programming rocks"])
word_lengths = (sentences
    .map(lambda s: s.split())                      # Split into words
    .flatten()                                     # Flatten list of lists
    .map(len)                                      # Get length of each word
    .groupby(lambda x: "short" if x <= 5 else "long")  # Group by length
    .valmap(len))                                  # Count words in each group

# Working with structured data
data = flist([
    {"name": "Alice", "age": 25, "score": 95},
    {"name": "Bob", "age": 20, "score": 85},
    {"name": "Charlie", "age": 30, "score": 90},
    {"name": "David", "age": 20, "score": 70},
    {"name": "Eve", "age": 25, "score": 92}
])

stats_by_age = (data
    .groupby(lambda x: x["age"])                   # Group by age
    .valmap(lambda people: flist(people)
        .map(lambda p: p["score"])                 # Extract scores 
        .pipe(lambda scores: {                     # Calculate statistics
            "count": len(scores),
            "avg": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores)
        })
    ))
```

## Why fcollections?

### Side-by-Side Comparison with Standard Python

**Complex Data Transformation:**

With standard Python:
```python
# Complex data processing with standard Python
data = list(range(100))
filtered = list(filter(lambda x: x % 3 == 0, data))
squared = list(map(lambda x: x ** 2, filtered))
chunks = [squared[i:i+5] for i in range(0, len(squared), 5)]
chunk_sums = [sum(chunk) for chunk in chunks]
large_sums = list(filter(lambda x: x > 1000, chunk_sums))
result = sum(large_sums) / len(large_sums) if large_sums else 0
```

With fcollections:
```python
# The same operation with fcollections
result = (frange(100)
    .filter(lambda x: x % 3 == 0)
    .map(lambda x: x ** 2)
    .partition(5)
    .map(lambda chunk: chunk.reduce(lambda a, b: a + b))
    .filter(lambda x: x > 1000)
    .pipe(lambda x: sum(x) / len(x) if x else 0))
```

**Data Analysis:**

With standard Python:
```python
# Grouping and analysis with standard Python
data = [
    {"name": "Alice", "age": 25, "score": 95},
    {"name": "Bob", "age": 20, "score": 85},
    {"name": "Charlie", "age": 30, "score": 90},
    {"name": "David", "age": 20, "score": 70},
    {"name": "Eve", "age": 25, "score": 92}
]

# Group by age
age_groups = {}
for person in data:
    age = person["age"]
    if age not in age_groups:
        age_groups[age] = []
    age_groups[age].append(person)

# Calculate statistics for each age group
stats = {}
for age, people in age_groups.items():
    scores = [person["score"] for person in people]
    stats[age] = {
        "count": len(scores),
        "avg": sum(scores) / len(scores),
        "min": min(scores),
        "max": max(scores)
    }
```

With fcollections:
```python
# The same operation with fcollections
stats = (flist(data)
    .groupby(lambda x: x["age"])
    .valmap(lambda people: flist(people)
        .map(lambda p: p["score"])
        .pipe(lambda scores: {
            "count": len(scores),
            "avg": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores)
        })
    ))
```

### Benefits of Method Chaining

1. **Readability** - Code reads like a sequence of operations, top to bottom
2. **Maintainability** - Easy to modify, add, or remove steps in the data pipeline
3. **Type Preservation** - Operations return appropriate collection types automatically
4. **Expressiveness** - Complex operations expressed clearly without temporary variables
5. **Composition** - Build sophisticated data pipelines by combining simple operations
6. **Conciseness** - Eliminate intermediate variables and boilerplate code
7. **Immutability** - Method chaining promotes immutable data transformations
8. **Discoverability** - IDE auto-completion makes it easy to discover available operations

## Overview

fcollections provides collections with functional programming operations and method chaining for Python.

- `flist` - A list that returns `flist` for operations when it makes sense
- `fgenerator` - A generator that returns `fgenerator` for operations when it makes sense
- `fdict` - A dictionary with additional functional operations
- `fset` - A set with chainable methods and functional operations

A Python library that provides enhanced collection classes with method chaining capabilities. fcollections wraps functionality from cytoolz and itertools as methods of collection classes, enabling a fluent functional programming style.

## Features

- Method chaining for cleaner, more readable code
- Functional programming paradigm with Python collections
- Type preservation (methods return the same collection type when possible)
- Seamless integration with cytoolz and itertools functionality
- Four main collection types: flist, fgenerator, fdict, and fset
- Easy conversions between collection types

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

## Dependencies

- cytoolz
- Python 2.x (uses itertools.imap and xrange)

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

The power of fcollections is in its method chaining capability:

```python
from fcollections import frange

# Without method chaining
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
filtered = filter(lambda x: x % 2 == 0, data)
mapped = map(lambda x: x * 2, filtered)
result = list(mapped)  # [0, 4, 8, 12, 16]

# With fcollections' method chaining
result = (frange(10)
          .filter(lambda x: x % 2 == 0)
          .map(lambda x: x * 2))
# result is an flist containing [0, 4, 8, 12, 16]
```

## Core Collection Types

### flist

An enhanced list that inherits from Python's list and provides additional functional methods with chaining capability.

```python
from fcollections import flist

numbers = flist([1, 2, 3, 4, 5])

# Basic operations
doubled = numbers.map(lambda x: x * 2)  # flist([2, 4, 6, 8, 10])
evens = numbers.filter(lambda x: x % 2 == 0)  # flist([2, 4])
total = numbers.reduce(lambda a, b: a + b)  # 15

# Sorting
sorted_list = numbers.sort()  # Returns a new sorted flist
sorted_by_custom = numbers.sort_by(lambda x: -x)  # Sort by custom key

# Convert to generator
gen = numbers.to_generator()  # Convert to fgenerator

# New conversion methods
s = numbers.to_set()  # Convert to fset
t = numbers.to_tuple()  # Convert to tuple
```

### fgenerator

A lazy generator-like object that provides functional methods with chaining capability while maintaining lazy evaluation.

```python
from fcollections import fgenerator, fxrange

# Create a generator from 0 to 999
gen = fxrange(1000)

# Take only what you need (lazy evaluation)
first_five = gen.take(5)  # fgenerator with first 5 elements
last_five = gen.tail(5)   # fgenerator with last 5 elements

# Convert to list when needed
as_list = gen.to_list()  # Converts to flist
```

### fdict

An enhanced dictionary with functional operations that return fdict or appropriate collection types.

```python
from fcollections import fdict

data = fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})

# Key/value operations
keys = data.keys()  # flist(['a', 'b', 'c', 'd'])
values = data.values()  # flist([1, 2, 3, 4])
items = data.items()  # flist([('a', 1), ('b', 2), ('c', 3), ('d', 4)])

# Transformations
upper_keys = data.keymap(lambda k: k.upper())  # fdict({'A': 1, 'B': 2, ...})
doubled_values = data.valmap(lambda v: v * 2)  # fdict({'a': 2, 'b': 4, ...})

# Filtering
evens = data.valfilter(lambda v: v % 2 == 0)  # fdict({'b': 2, 'd': 4})

# New conversion methods
pairs = data.to_pairs()  # Convert to list of pairs: flist([('a', 1), ('b', 2), ...])
new_dict = fdict.from_pairs([('x', 10), ('y', 20)])  # Create from pairs
```

### fset

A set with functional methods and chaining capability.

```python
from fcollections import fset, frange

# Create sets
s1 = fset([1, 2, 3, 4, 5])
s2 = fset([4, 5, 6, 7, 8])

# Set operations
union = s1.union(s2)  # fset({1, 2, 3, 4, 5, 6, 7, 8})
intersection = s1.intersection(s2)  # fset({4, 5})
difference = s1.difference(s2)  # fset({1, 2, 3})

# Functional operations
doubled = s1.map(lambda x: x * 2)  # fset({2, 4, 6, 8, 10})
evens = s1.filter(lambda x: x % 2 == 0)  # fset({2, 4})

# Conversion methods
l = s1.to_list()  # Convert to flist
g = s1.to_generator()  # Convert to fgenerator
t = s1.to_tuple()  # Convert to tuple
```

## Advanced Features

### Partitioning and Grouping

```python
from fcollections import frange

nums = frange(10)

# Partitioning
chunks = nums.partition(3)  # flist([flist([0, 1, 2]), flist([3, 4, 5]), flist([6, 7, 8])])
all_chunks = nums.partition_all(3)  # Includes partial final chunk

# Grouping
is_even = lambda x: 'even' if x % 2 == 0 else 'odd'
grouped = nums.groupby(is_even)  # fdict({'even': flist([0, 2, 4, 6, 8]), 'odd': flist([1, 3, 5, 7, 9])})
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

### New Chainable Methods

```python
from fcollections import frange

nums = frange(10)

# find - Get first element matching a predicate
found = nums.find(lambda x: x > 5)  # 6
not_found = nums.find(lambda x: x > 20)  # None

# zip_with - Combine two sequences using a function
zipped = nums.zip_with(frange(10, 20), lambda a, b: a + b)  # [10, 12, 14, ...]

# chunk - Alias for partition with more intuitive name
chunks = nums.chunk(2)  # [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]

# flatten - Flatten one level of nesting
nested = flist([[1, 2], [3, 4], [5, 6]])
flattened = nested.flatten()  # [1, 2, 3, 4, 5, 6]

# any_match / all_match - Check if any/all elements satisfy predicate
has_evens = nums.any_match(lambda x: x % 2 == 0)  # True
all_positive = nums.all_match(lambda x: x >= 0)  # True

# enumerate - Add index to each element
with_indices = nums.enumerate(start=1)  # [(1, 0), (2, 1), (3, 2), ...]

# take_while / drop_while - Take/drop elements while predicate is true
taken = nums.take_while(lambda x: x < 5)  # [0, 1, 2, 3, 4]
dropped = nums.drop_while(lambda x: x < 5)  # [5, 6, 7, 8, 9]
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

## License

GNU General Public License v3.0

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/PilCAki/fcollections).
