# fcollections

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/fcollections.svg)](https://pypi.org/project/fcollections/)
[![Build Status](https://img.shields.io/github/workflow/status/PilCAki/fcollections/Python%20package/master)](https://github.com/PilCAki/fcollections/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-not%20available-lightgrey)](https://github.com/PilCAki/fcollections)

Collections with method chaining.

## Installation

```bash
pip install fcollections
```

## Usage

```python
from fcollections import flist, frange

# Example usage
a = frange(10)
print(a.map(lambda x: x*2))
```

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.