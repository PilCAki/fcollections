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

### Navigating and Transforming Complex JSON Trees

```python
from chaincollections import chain, cdict

# Nested JSON from an API response or config file
api_response = {
    "metadata": {"version": "1.0", "status": "success"},
    "results": [
        {
            "id": "node1",
            "type": "folder",
            "children": [
                {"id": "node2", "type": "file", "permissions": ["read", "write"], "size": 1024},
                {"id": "node3", "type": "file", "permissions": ["read"], "size": 2048}
            ]
        },
        {
            "id": "node4",
            "type": "folder",
            "children": [
                {"id": "node5", "type": "folder", "children": [
                    {"id": "node6", "type": "file", "permissions": ["read", "write", "execute"], "size": 4096}
                ]},
                {"id": "node7", "type": "file", "permissions": ["read"], "size": 512}
            ]
        }
    ]
}

# Find all executable files at any nesting level, with modified paths
result = (chain(api_response["results"])
    .flatmap(lambda node: chain([node])  # Start with top-level node
        .concat(                         # Then recursively gather:
            chain(node.get("children", []))
            .flatmap(lambda child: 
                chain([child]).concat(  # The child itself
                    chain(child.get("children", []))  # And its nested children
                    .flatmap(lambda c: c.get("children", []))  # And their children
                )
            )
        )
    )
    .filter(lambda node: node["type"] == "file" and "execute" in node.get("permissions", []))
    .map(lambda node: {
        "path": f"/root/{node['id']}",
        "size_kb": node["size"] / 1024,
        "full_permissions": "".join(p[0] for p in node.get("permissions", []))
    })
    .sort_by(lambda node: node["size_kb"], reverse=True)
    .to_list()
)

# Result: [
#   {"path": "/root/node6", "size_kb": 4.0, "full_permissions": "rwe"}
# ]
```

### Graph Traversal and Pathfinding Made Simple

```python
from chaincollections import cdict, chain
from collections import deque

# Represent a graph as an adjacency list dictionary
graph = cdict({
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
})

# Find all paths between two nodes using BFS
def find_all_paths(start, end, max_depth=10):
    queue = deque([(start, [start])])
    all_paths = []
    
    while queue and len(all_paths) < 100:  # Limit to prevent infinite loops
        node, path = queue.popleft()
        
        # Get neighboring nodes not already in path
        for neighbor in graph.get(node, []):
            if neighbor == end:
                all_paths.append(path + [neighbor])
            elif neighbor not in path and len(path) < max_depth:
                queue.append((neighbor, path + [neighbor]))
    
    return chain(all_paths)

# Find and analyze all paths from A to G
paths = (find_all_paths('A', 'G', max_depth=5)
    .map(lambda path: "->".join(path))      # Format each path as a string
    .sort_by(len)                           # Sort by path length
    .enumerate(start=1)                     # Add index to each path
    .map(lambda x: f"Path {x[0]}: {x[1]}")  # Format with index
    .to_list()
)

# Result: [
#   "Path 1: A->C->F->G",
#   "Path 2: A->B->E->F->G"
# ]

# Analyze the graph structure
graph_stats = (chain(graph.items())
    .map(lambda x: (x[0], len(x[1])))       # Get node and number of connections
    .sort_by(lambda x: x[1], reverse=True)  # Sort by number of connections
    .take(3)                                # Take top 3 most connected nodes
    .map(lambda x: f"Node {x[0]} has {x[1]} connections")
    .to_list()
)

# Result: [
#   "Node F has 3 connections",
#   "Node B has 3 connections",
#   "Node A has 2 connections"
# ]
```

### Natural Language Processing Pipeline

```python
from chaincollections import chain
import re

# Sample text from a document
text = """
Python is a high-level programming language known for its readability.
Created by Guido van Rossum in 1991, Python emphasizes code readability
with its notable use of whitespace. Python features a dynamic type system
and automatic memory management. Python supports multiple programming
paradigms, including procedural, object-oriented, and functional programming.
"""

# Build a comprehensive text analysis pipeline
result = (chain(text.lower().split("\n"))
    .filter(bool)                              # Remove empty lines
    .map(lambda line: re.sub(r'[^\w\s]', '', line))  # Remove punctuation
    .map(lambda line: line.split())            # Split into words
    .flatten()                                 # Flatten list of lists into a single list
    .filter(lambda word: len(word) > 3)        # Filter out short words
    .frequencies()                             # Count word frequencies
    .items()                                   # Get (word, count) pairs
    .filter(lambda x: x[1] > 1)                # Keep words that appear more than once
    .sort_by(lambda x: x[1], reverse=True)     # Sort by frequency
    .take(5)                                   # Take top 5 most frequent words
    .map(lambda x: {"word": x[0], "count": x[1], "length": len(x[0])})
    .sort_by(lambda x: (x["count"], x["length"]), reverse=True)  # Sort by count, then length
    .to_list()
)

# Result: [
#   {"word": "python", "count": 4, "length": 6},
#   {"word": "programming", "count": 3, "length": 11},
#   {"word": "readability", "count": 2, "length": 11},
#   {"word": "code", "count": 2, "length": 4},
#   {"word": "with", "count": 2, "length": 4}
# ]

# Identify word co-occurrences in the same line
co_occurrences = (chain(text.lower().split("\n"))
    .filter(bool)                              # Remove empty lines
    .map(lambda line: re.findall(r'\b\w+\b', line))  # Extract words
    .filter(lambda words: len(words) > 1)      # Only lines with multiple words
    .flatmap(lambda words: [                   # Generate all word pairs in each line
        (w1, w2) for i, w1 in enumerate(words) 
        for w2 in words[i+1:] 
        if len(w1) > 3 and len(w2) > 3        # Only consider words > 3 chars
    ])
    .frequencies()                             # Count pair frequencies
    .items()                                   # Get (pair, count) tuples
    .sort_by(lambda x: x[1], reverse=True)     # Sort by frequency
    .take(3)                                   # Take top 3 pairs
    .map(lambda x: f"'{x[0][0]}' co-occurs with '{x[0][1]}' {x[1]} times")
    .to_list()
)

# Result: [
#   "'python' co-occurs with 'programming' 3 times",
#   "'programming' co-occurs with 'language' 2 times",
#   "'code' co-occurs with 'readability' 2 times"
# ]
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

# Recursive chaining for nested structures
nested_data = {
    'users': [
        {'name': 'Alice', 'scores': [85, 90, 78]},
        {'name': 'Bob', 'scores': [92, 88, 76]}
    ]
}

# Without recursive=True, you'd need to chain each level manually
basic = chain(nested_data)
users = chain(basic['users'])
user = chain(users[0])
scores = chain(user['scores'])

# With recursive=True, nested structures are automatically chainable
recursive = chain(nested_data, recursive=True)
# Chain methods at any nesting level
high_scores = recursive['users'].map(
    lambda user: {'name': user['name'], 
                 'avg_score': user['scores'].filter(lambda s: s > 80).reduce(lambda a, b: a + b) / 
                              user['scores'].filter(lambda s: s > 80).count()}
)
print(high_scores)  # [{'name': 'Alice', 'avg_score': 87.5}, {'name': 'Bob', 'avg_score': 90.0}]
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

# Enable recursive chaining for nested structures
nested_data = chain({'a': {'b': [1, 2, 3]}}, recursive=True)
# Now you can chain methods at any level
filtered = nested_data['a']['b'].filter(lambda x: x > 1)  # [2, 3]
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

### Recursive Chaining

The `chain()` function supports recursive chaining via the `recursive=True` parameter, which automatically wraps nested dictionaries and lists as chainable objects when they are accessed:

```python
from chaincollections import chain

# Complex nested structure
data = {
    "products": [
        {"id": 1, "name": "Widget", "categories": ["tools", "home"]},
        {"id": 2, "name": "Gadget", "categories": ["electronics", "tools"]},
        {"id": 3, "name": "Doohickey", "categories": ["misc"]}
    ],
    "metadata": {
        "tags": ["inventory", "2023"],
        "version": 2.1
    }
}

# Enable recursive chaining
c = chain(data, recursive=True)

# Chain operations at any nesting level without manual wrapping
tool_products = c["products"].filter(
    lambda p: "tools" in p["categories"]
).map(
    lambda p: {"name": p["name"], "category_count": len(p["categories"])}
)

print(tool_products)
# [{"name": "Widget", "category_count": 2}, {"name": "Gadget", "category_count": 2}]
```

The recursive behavior is preserved when creating new collections via methods like `filter()`, `map()`, etc., allowing for cleaner code when working with complex nested data structures.

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
