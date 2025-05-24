# Contributing to chaincollections

Thank you for your interest in contributing to chaincollections! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Issues](#reporting-issues)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Guidelines](#development-guidelines)
  - [Code Style](#code-style)
  - [Testing](#testing)
- [Community and Communication](#community-and-communication)

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

### Prerequisites

- Python 3.6+ (as specified in setup.py)
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/chaincollections.git
   cd chaincollections
   ```
3. Install for development:
   ```
   pip install -e .
   ```

## How to Contribute

### Reporting Issues

Before submitting an issue, please:

- Check the existing issues to avoid duplicates
- Use the issue template if available
- Provide a clear and descriptive title
- Include steps to reproduce the issue
- Include expected and actual behavior
- Include Python version and operating system information

### Submitting Pull Requests

1. Create a new branch from `master`:
   ```
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run the tests to ensure they pass:
   ```
   python -m pytest tests/
   ```
4. Commit your changes with a clear commit message:
   ```
   git commit -m "Add feature: description of your changes"
   ```
5. Push to your fork:
   ```
   git push origin feature/your-feature-name
   ```
6. Open a pull request against the `master` branch of the original repository

## Development Guidelines

### Code Style

- Code should be formatted with [Black](https://black.readthedocs.io/)
- Imports should be sorted with [isort](https://pycqa.github.io/isort/)
- Code should pass [flake8](https://flake8.pycqa.org/) linting
- Maximum line length is 100 characters
- Use 4 spaces for indentation (not tabs)
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Keep functions focused and modular

To format your code before submitting:
```bash
# Install formatting tools
pip install black isort flake8

# Option 1: Use the formatting script
./scripts/format_code.sh

# Option 2: Run tools individually
black .
isort .
flake8 .
```

### Testing

- Add tests for new features
- Ensure all tests pass before submitting a pull request
- Tests should be placed in the `tests` directory
- Use the existing testing framework

## Community and Communication

- For questions or discussions, open an issue on GitHub
- For direct communication, contact the project maintainer: Phillip Adkins (philchiladki@yahoo.com)

---

Thank you for contributing to chaincollections! Your efforts help make this project better for everyone.