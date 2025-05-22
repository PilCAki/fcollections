# fcollections

A Python library that provides enhanced collection classes with method chaining capabilities. fcollections wraps functionality from cytoolz and itertools as methods of collection classes, enabling a fluent functional programming style.

## Installation

```bash
pip install fcollections
```

## Development

### Setup

Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Code Linting and Formatting

This project uses:
- **flake8** for code linting
- **black** for code formatting (Python 3.7+ only)
- **isort** for sorting imports

#### Running the Tools

Using the Makefile:

```bash
# Run linting checks
make lint

# Format code (black & isort)
make format

# Check formatting without making changes
make check
```

Or run the tools directly:

```bash
# Linting
flake8 fcollections tests

# Sorting imports
isort fcollections tests

# Formatting (Python 3.7+ only)
black fcollections tests
```

#### Pre-commit Hook

A pre-commit hook is provided to automatically run these checks before each commit.
To install it:

```bash
# From the repository root
cp .github/hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please follow the code style guidelines before submitting pull requests.