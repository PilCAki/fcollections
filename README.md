# chaincollections


[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/chaincollections.svg)](https://pypi.org/project/chaincollections/)
![Tests](https://github.com/PilCAki/chaincollections/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/PilCAki/chaincollections/branch/master/graph/badge.svg)](https://codecov.io/gh/PilCAki/chaincollections)

Collections with method chaining for Python.

## Why chaincollections?

Transform your Python data processing with elegant, readable method chains:

```python
# Vanilla Python - verbose and hard to follow
data = list(range(100))
filtered = list(filter(lambda x: x % 2 == 0 and x % 3 == 0, data))
mapped = list(map(lambda x: {"value": x, "square": x**2}, filtered))
sorted_data = sorted(mapped, key=lambda x: x["square"], reverse=True)
result = sorted_data[:5]

# chaincollections - elegant and expressive
from chaincollections import crange

result = (crange(100)
    .filter(lambda x: x % 2 == 0 and x % 3 == 0)
    .map(lambda x: {"value": x, "square": x**2})
    .sort_by(lambda x: x["square"], reverse=True)
    .take(5))
```

### Powerful Data Transformations in One Fluid Chain

```python
from chaincollections import crange, cdict, chain

# Process sales data with complex transformations in a single readable chain
result = (chain([
        {"product": "Apple", "category": "Fruit", "price": 0.5, "sales": 100},
        {"product": "Orange", "category": "Fruit", "price": 0.7, "sales": 80},
        {"product": "Carrot", "category": "Vegetable", "price": 0.3, "sales": 120},
        {"product": "Cucumber", "category": "Vegetable", "price": 0.6, "sales": 60},
        {"product": "Banana", "category": "Fruit", "price": 0.4, "sales": 110}
    ])
    .groupby(lambda x: x["category"])                   # Group by category
    .valmap(lambda items: chain(items)                  # For each category:
        .map(lambda x: {**x, "revenue": x["price"] * x["sales"]})  # Calculate revenue
        .sort_by(lambda x: x["revenue"], reverse=True)  # Sort by revenue
        .map(lambda x: f"{x['product']}: ${x['revenue']:.2f}")     # Format output
        .to_list())                                     # Convert to list
)

# Result: {
#   'Fruit': ['Apple: $50.00', 'Banana: $44.00', 'Orange: $56.00'],
#   'Vegetable': ['Carrot: $36.00', 'Cucumber: $36.00']
# }
```

### Real-world Data Analysis Made Simple

```python
from chaincollections import chain
import datetime

# Analyze log data with complex transformations in a clear, readable flow
logs = [
    {"timestamp": "2023-06-01 08:30:22", "level": "INFO", "service": "auth", "message": "User login successful"},
    {"timestamp": "2023-06-01 08:31:15", "level": "ERROR", "service": "db", "message": "Connection timeout"},
    {"timestamp": "2023-06-01 08:32:45", "level": "INFO", "service": "api", "message": "Request processed"},
    {"timestamp": "2023-06-01 08:33:30", "level": "ERROR", "service": "auth", "message": "Invalid credentials"},
    {"timestamp": "2023-06-01 08:34:10", "level": "WARN", "service": "api", "message": "Slow response time"},
    {"timestamp": "2023-06-01 08:35:22", "level": "ERROR", "service": "db", "message": "Query failed"}
]

# Parse, filter, group, and format log data in one expressive chain
result = (chain(logs)
    .map(lambda log: {
        **log, 
        "datetime": datetime.datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
    })
    .filter(lambda log: log["level"] in ["ERROR", "WARN"])
    .groupby(lambda log: log["service"])
    .valmap(lambda logs: chain(logs)
        .map(lambda log: f"{log['level']} at {log['datetime'].strftime('%H:%M:%S')}: {log['message']}")
        .to_list()
    )
)

# Result: {
#   'db': ['ERROR at 08:31:15: Connection timeout', 'ERROR at 08:35:22: Query failed'],
#   'auth': ['ERROR at 08:33:30: Invalid credentials'],
#   'api': ['WARN at 08:34:10: Slow response time']
# }
```

### Key Benefits

- **Improved Readability**: Write data processing pipelines that read from left to right
- **Reduced Boilerplate**: Eliminate temporary variables and repetitive function calls
- **Type Preservation**: Methods return the same collection type when appropriate
- **Function Composition**: Pipe data through multiple processing steps with ease
- **Seamless Integration**: Works with your existing Python codebase

## Overview

chaincollections provides collections with functional programming operations and method chaining for Python.

- `clist` - A list that returns `clist` for operations when it makes sense
- `cgenerator` - A generator that returns `cgenerator` for operations when it makes sense
- `cdict` - A dictionary with additional functional operations
- `cset` - A set with chainable methods and functional operations

A Python library that provides enhanced collection classes with method chaining capabilities. chaincollections wraps functionality from cytoolz and itertools as methods of collection classes, enabling a fluent functional programming style.

## Features

- Method chaining for cleaner, more readable code
- Functional programming paradigm with Python collections
- Type preservation (methods return the same collection type when possible)
- Seamless integration with cytoolz and itertools functionality
- Four main collection types with both new and legacy naming
- Easy conversions between collection types
- Full backwards compatibility with existing code

## Installation

```bash
pip install chaincollections
```

## Usage

### Chaincollections API

```python
from chaincollections import clist, crange, cdict, cgenerator, chain

# Create a list
a = crange(10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Method chaining
result = (
    a.filter(lambda x: x % 2 == 0)  # Keep even numbers
     .map(lambda x: x * 3)           # Multiply by 3
     .reduce(lambda a, b: a + b)     # Sum them up
)
print(result)  # 72

# Working with dictionaries
d = cdict({'a': 1, 'b': 2, 'c': 3})
result = d.valmap(lambda x: x * 10)
print(result)  # {'a': 10, 'b': 20, 'c': 30}

# Using the chain function for automatic conversion
result = chain([1, 2, 3, 4]).map(lambda x: x * 2)  # Automatically converts to clist
print(result)  # [2, 4, 6, 8]

# Automatic dict conversion
result = chain({'a': 1, 'b': 2}).valmap(lambda x: x * 10)
print(result)  # {'a': 10, 'b': 20}
```

## Migration Guide

If you were previously using the old API (fcollections), here's how to migrate to the new chaincollections API:

### Import Changes

Old:
```python
from fcollections import flist, fgenerator, fdict, fset, frange, fxrange
```

New:
```python
from chaincollections import clist, cgenerator, cdict, cset, crange, cxrange, chain
```

### Type Renaming

| Old Type      | New Type     |
|---------------|--------------|
| `flist`       | `clist`      |
| `fgenerator`  | `cgenerator` |
| `fdict`       | `cdict`      |
| `fset`        | `cset`       |
| `frange()`    | `crange()`   |
| `fxrange()`   | `cxrange()`  |

### New Chain Function

The new API introduces a `chain()` function that automatically detects the input type and returns the appropriate chainable collection:

```python
from chaincollections import chain

# Automatically converts to appropriate type
list_data = chain([1, 2, 3, 4, 5])  # clist
dict_data = chain({'a': 1, 'b': 2})  # cdict
set_data = chain({1, 2, 3})         # cset
gen_data = chain(range(5))          # cgenerator
```

This is the recommended way to create chainable collections as it's more concise and handles type detection automatically.

## Testing

To run the tests:

```bash
pip install pytest pytest-cov
pytest --cov=chaincollections tests/
```

## Dependencies

- cytoolz
- Python 3.6+ (as specified in setup.py)

## Basic Usage

### Creating Collections

```python
from chaincollections import clist, cgenerator, cdict, crange, cxrange, chain, cset

# Creating from existing collections
my_list = clist([1, 2, 3, 4, 5])
my_generator = cgenerator(x for x in range(10))
my_dict = cdict({'a': 1, 'b': 2, 'c': 3})
my_set = cset({1, 2, 3, 4, 5})

# Using utility functions
nums = crange(10)  # clist containing [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
nums_gen = cxrange(10)  # cgenerator containing values 0-9

# Using the chain function for automatic type detection
auto_list = chain([1, 2, 3, 4, 5])  # clist
auto_dict = chain({'a': 1, 'b': 2})  # cdict
auto_set = chain({1, 2, 3})         # cset
auto_gen = chain(range(5))          # cgenerator
```

### Method Chaining

The power of chaincollections is in its method chaining capability:

```python
from chaincollections import crange

# Without method chaining
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
filtered = filter(lambda x: x % 2 == 0, data)
mapped = map(lambda x: x * 2, filtered)
result = list(mapped)  # [0, 4, 8, 12, 16]

# With chaincollections' method chaining
result = (crange(10)
          .filter(lambda x: x % 2 == 0)
          .map(lambda x: x * 2))
# result is a clist containing [0, 4, 8, 12, 16]
```

## Core Collection Types

### clist

An enhanced list that inherits from Python's list and provides additional functional methods with chaining capability.

```python
from chaincollections import clist

numbers = clist([1, 2, 3, 4, 5])

# Basic operations
doubled = numbers.map(lambda x: x * 2)  # clist([2, 4, 6, 8, 10])
evens = numbers.filter(lambda x: x % 2 == 0)  # clist([2, 4])
total = numbers.reduce(lambda a, b: a + b)  # 15

# Sorting
sorted_list = numbers.sort()  # Returns a new sorted clist
sorted_by_custom = numbers.sort_by(lambda x: -x)  # Sort by custom key

# Convert to generator
gen = numbers.to_generator()  # Convert to cgenerator

# New conversion methods
s = numbers.to_set()  # Convert to cset
t = numbers.to_tuple()  # Convert to tuple
```

### cgenerator

A lazy generator-like object that provides functional methods with chaining capability while maintaining lazy evaluation.

```python
from chaincollections import cgenerator, cxrange

# Create a generator from 0 to 999
gen = cxrange(1000)

# Take only what you need (lazy evaluation)
first_five = gen.take(5)  # cgenerator with first 5 elements
last_five = gen.tail(5)   # cgenerator with last 5 elements

# Convert to list when needed
as_list = gen.to_list()  # Converts to clist
```

### cdict

An enhanced dictionary with functional operations that return cdict or appropriate collection types.

```python
from chaincollections import cdict

data = cdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})

# Key/value operations
keys = data.keys()  # clist(['a', 'b', 'c', 'd'])
values = data.values()  # clist([1, 2, 3, 4])
items = data.items()  # clist([('a', 1), ('b', 2), ('c', 3), ('d', 4)])

# Transformations
upper_keys = data.keymap(lambda k: k.upper())  # cdict({'A': 1, 'B': 2, ...})
doubled_values = data.valmap(lambda v: v * 2)  # cdict({'a': 2, 'b': 4, ...})

# Filtering
evens = data.valfilter(lambda v: v % 2 == 0)  # cdict({'b': 2, 'd': 4})

# New conversion methods
pairs = data.to_pairs()  # Convert to list of pairs: clist([('a', 1), ('b', 2), ...])
new_dict = cdict.from_pairs([('x', 10), ('y', 20)])  # Create from pairs
```

### cset

A set with functional methods and chaining capability.

```python
from chaincollections import cset, crange

# Create sets
s1 = cset([1, 2, 3, 4, 5])
s2 = cset([4, 5, 6, 7, 8])

# Set operations
union = s1.union(s2)  # cset({1, 2, 3, 4, 5, 6, 7, 8})
intersection = s1.intersection(s2)  # cset({4, 5})
difference = s1.difference(s2)  # cset({1, 2, 3})

# Functional operations
doubled = s1.map(lambda x: x * 2)  # cset({2, 4, 6, 8, 10})
evens = s1.filter(lambda x: x % 2 == 0)  # cset({2, 4})

# Conversion methods
l = s1.to_list()  # Convert to clist
g = s1.to_generator()  # Convert to cgenerator
t = s1.to_tuple()  # Convert to tuple
```

## Advanced Features

### Partitioning and Grouping

```python
from chaincollections import crange

nums = crange(10)

# Partitioning
chunks = nums.partition(3)  # clist([clist([0, 1, 2]), clist([3, 4, 5]), clist([6, 7, 8])])
all_chunks = nums.partition_all(3)  # Includes partial final chunk

# Grouping
is_even = lambda x: 'even' if x % 2 == 0 else 'odd'
grouped = nums.groupby(is_even)  # cdict({'even': clist([0, 2, 4, 6, 8]), 'odd': clist([1, 3, 5, 7, 9])})
```

### Sliding Window and Other Operations

```python
from chaincollections import crange

nums = crange(10)

# Sliding window
windows = nums.sliding_window(3).to_list()  # clist([clist([0, 1, 2]), clist([1, 2, 3]), ...])

# Other operations
unique_values = clist([1, 2, 2, 3, 3, 3]).unique()  # clist([1, 2, 3])
top_values = nums.top_k(3)  # clist([9, 8, 7])
```

### New Chainable Methods

```python
from chaincollections import crange

nums = crange(10)

# find - Get first element matching a predicate
found = nums.find(lambda x: x > 5)  # 6
not_found = nums.find(lambda x: x > 20)  # None

# zip_with - Combine two sequences using a function
zipped = nums.zip_with(crange(10, 20), lambda a, b: a + b)  # [10, 12, 14, ...]

# chunk - Alias for partition with more intuitive name
chunks = nums.chunk(2)  # [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]

# flatten - Flatten one level of nesting
nested = clist([[1, 2], [3, 4], [5, 6]])
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
from chaincollections import crange

# Complex processing with method chaining
result = (crange(100)
    .partition(10)  # Split into chunks of 10
    .map(lambda l: clist(l * 3))  # Repeat each chunk 3 times
    .reduce(lambda a, b: clist(a + b))  # Combine all chunks
    .reduce(lambda a, b: a + b))  # Sum all values
```

### Pipe Operations

```python
from chaincollections import crange
import numpy as np

data = crange(10)

# Pipe data through a sequence of functions
std_dev = data.pipe(lambda x: x * 3, np.asarray, np.std)

# Apply multiple functions to each element
adjusted = data.pipe_map(lambda x: x - 4, lambda x: x + 4, lambda x: x * 2)
```

## License

GNU General Public License v3.0

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests on the [GitHub repository](https://github.com/PilCAki/chaincollections).
