# Contributing to fcollections

Thank you for your interest in contributing to fcollections! This document provides guidelines and instructions for contributing to this project.

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

- Python 2.7 (the project currently uses Python 2 syntax)
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```
   git clone https://github.com/your-username/fcollections.git
   cd fcollections
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
   python tests/fcollections_tests.py
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

- Follow the existing code style in the project
- Use 4 spaces for indentation (not tabs)
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Keep functions focused and modular

### Testing

- Add tests for new features
- Ensure all tests pass before submitting a pull request
- Tests should be placed in the `tests` directory
- Use the existing testing framework

## Community and Communication

- For questions or discussions, open an issue on GitHub
- For direct communication, contact the project maintainer: Phillip Adkins (philchiladki@yahoo.com)

---

Thank you for contributing to fcollections! Your efforts help make this project better for everyone.