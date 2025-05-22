# Contributing to fcollections

Thank you for considering contributing to fcollections!

## Code Style Guidelines

This project follows these code style practices:

1. **PEP 8**: We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code, with some modifications as defined in our configuration files.

2. **Line Length**: We use a maximum line length of 100 characters.

3. **Imports**: Imports should be sorted using isort with the Black profile.

4. **Code Formatting**: Code should be formatted using Black (for Python 3.7+).

## Development Workflow

1. Set up your development environment:
   ```bash
   pip install -e ".[dev]"
   ```

2. Before committing changes:
   ```bash
   # Run the linter
   make lint
   
   # Format your code
   make format
   ```

3. Write tests for new functionality.

4. Submit a pull request with your changes.

## Running Tests

Tests can be run with:

```bash
python tests/fcollections_tests.py
```