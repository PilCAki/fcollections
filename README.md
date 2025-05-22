# fcollections

A functional collections library for Python with method chaining support.

## Overview

fcollections provides functional collection types with method chaining support, making functional programming in Python more natural and readable.

## Features

- Chain methods together for cleaner, more readable code
- Functional replacements for standard Python collections
- Compatible with both Python 2 and 3
- Integration with cytoolz, numpy, and pandas
- Support for lazy evaluation with generators

## Collection Types

- `flist` - Enhanced list with chainable methods
- `fdict` - Enhanced dictionary with chainable methods
- `fgenerator` - Generator wrapper with chainable methods
- `fset` - Enhanced set with chainable methods

## Example Usage

```python
from fcollections import flist, frange

# Chain operations together
result = (frange(100)
          .filter(lambda x: x % 2 == 0)  # Keep even numbers
          .map(lambda x: x * 3)          # Multiply by 3
          .take(10)                      # Take first 10 items
          .reduce(lambda a, b: a + b))   # Sum them up

# Process nested data
nested = flist([[1, 2], [3, 4], [5, 6]])
flattened = nested.flatten()  # [1, 2, 3, 4, 5, 6]

# Work with sets
s1 = fset([1, 2, 3, 4])
s2 = fset([3, 4, 5, 6])
result = s1.union(s2).filter(lambda x: x > 3)  # fset([4, 5, 6])

# Enhanced dictionary operations
d1 = fdict({'a': 1, 'b': 2})
d2 = fdict({'b': 20, 'c': 30})
merged = d1.merge_with(lambda x, y: x + y, d2)  # {'a': 1, 'b': 22, 'c': 30}
```

## Integration with NumPy and Pandas

```python
from fcollections import from_numpy, to_numpy, from_pandas, to_pandas
import numpy as np
import pandas as pd

# Convert NumPy array to flist and back
arr = np.array([1, 2, 3, 4])
fl = from_numpy(arr)
processed = fl.map(lambda x: x * 2)
arr2 = to_numpy(processed)

# Convert Pandas DataFrame to fdict and back
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
fd = from_pandas(df)
processed_df = to_pandas(fd.valmap(lambda col: col.map(lambda x: x * 2)))
```

## Installation

```
pip install fcollections
```

## License

See LICENSE file for details.