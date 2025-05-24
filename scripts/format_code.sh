#!/bin/bash
# Simple script to run linting and formatting tools

echo "Running isort to sort imports..."
isort .

echo "Running black to format code..."
black .

echo "Running flake8 to check for issues..."
flake8 . --count --statistics

echo "All done! Check the output above for any remaining issues."