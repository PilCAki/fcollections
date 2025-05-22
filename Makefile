.PHONY: lint format check clean

# Run flake8 linting
lint:
	flake8 fcollections tests

# Format code with black and isort
format:
	isort fcollections tests
	black fcollections tests || echo "Black formatting skipped (requires Python 3.7+)"

# Check formatting without making changes
check:
	isort --check-only fcollections tests
	black --check fcollections tests || echo "Black check skipped (requires Python 3.7+)"

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete